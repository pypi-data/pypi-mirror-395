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
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationCloudWatchLoggingOptionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "cloud_watch_logging_option": "cloudWatchLoggingOption",
    },
)
class CfnApplicationCloudWatchLoggingOptionMixinProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
        cloud_watch_logging_option: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationCloudWatchLoggingOptionPropsMixin.CloudWatchLoggingOptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationCloudWatchLoggingOptionPropsMixin.

        :param application_name: The name of the application.
        :param cloud_watch_logging_option: Provides a description of Amazon CloudWatch logging options, including the log stream Amazon Resource Name (ARN).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationcloudwatchloggingoption.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
            
            cfn_application_cloud_watch_logging_option_mixin_props = kinesisanalyticsv2_mixins.CfnApplicationCloudWatchLoggingOptionMixinProps(
                application_name="applicationName",
                cloud_watch_logging_option=kinesisanalyticsv2_mixins.CfnApplicationCloudWatchLoggingOptionPropsMixin.CloudWatchLoggingOptionProperty(
                    log_stream_arn="logStreamArn"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b452be3edc2cf79768f12326eeb61a0f09cc7602d5e4b66a916d2f83a501463f)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument cloud_watch_logging_option", value=cloud_watch_logging_option, expected_type=type_hints["cloud_watch_logging_option"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if cloud_watch_logging_option is not None:
            self._values["cloud_watch_logging_option"] = cloud_watch_logging_option

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationcloudwatchloggingoption.html#cfn-kinesisanalyticsv2-applicationcloudwatchloggingoption-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_watch_logging_option(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationCloudWatchLoggingOptionPropsMixin.CloudWatchLoggingOptionProperty"]]:
        '''Provides a description of Amazon CloudWatch logging options, including the log stream Amazon Resource Name (ARN).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationcloudwatchloggingoption.html#cfn-kinesisanalyticsv2-applicationcloudwatchloggingoption-cloudwatchloggingoption
        '''
        result = self._values.get("cloud_watch_logging_option")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationCloudWatchLoggingOptionPropsMixin.CloudWatchLoggingOptionProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationCloudWatchLoggingOptionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationCloudWatchLoggingOptionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationCloudWatchLoggingOptionPropsMixin",
):
    '''Adds an Amazon CloudWatch log stream to monitor application configuration errors.

    .. epigraph::

       Only one *ApplicationCloudWatchLoggingOption* resource can be attached per application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationcloudwatchloggingoption.html
    :cloudformationResource: AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
        
        cfn_application_cloud_watch_logging_option_props_mixin = kinesisanalyticsv2_mixins.CfnApplicationCloudWatchLoggingOptionPropsMixin(kinesisanalyticsv2_mixins.CfnApplicationCloudWatchLoggingOptionMixinProps(
            application_name="applicationName",
            cloud_watch_logging_option=kinesisanalyticsv2_mixins.CfnApplicationCloudWatchLoggingOptionPropsMixin.CloudWatchLoggingOptionProperty(
                log_stream_arn="logStreamArn"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApplicationCloudWatchLoggingOptionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26869c70c051c38a37b4c1b92a0d0dc31f42432b034edc2017e56a47dc85f0dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66a889b38540ec13f679ff743042ecc0660e8b0c7009108c1a95edbd5996a54f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1f8351d6b05c05ec9bb4d5e1e0f76022778293d342e651516a8cf4d5f7c5c6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationCloudWatchLoggingOptionMixinProps:
        return typing.cast(CfnApplicationCloudWatchLoggingOptionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationCloudWatchLoggingOptionPropsMixin.CloudWatchLoggingOptionProperty",
        jsii_struct_bases=[],
        name_mapping={"log_stream_arn": "logStreamArn"},
    )
    class CloudWatchLoggingOptionProperty:
        def __init__(
            self,
            *,
            log_stream_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides a description of Amazon CloudWatch logging options, including the log stream Amazon Resource Name (ARN).

            :param log_stream_arn: The ARN of the CloudWatch log to receive application messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationcloudwatchloggingoption-cloudwatchloggingoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                cloud_watch_logging_option_property = kinesisanalyticsv2_mixins.CfnApplicationCloudWatchLoggingOptionPropsMixin.CloudWatchLoggingOptionProperty(
                    log_stream_arn="logStreamArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__99a34de6c7bf66ee445a92951f8c595ef057bb84d32239fdf255e760270f0cf4)
                check_type(argname="argument log_stream_arn", value=log_stream_arn, expected_type=type_hints["log_stream_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_stream_arn is not None:
                self._values["log_stream_arn"] = log_stream_arn

        @builtins.property
        def log_stream_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the CloudWatch log to receive application messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationcloudwatchloggingoption-cloudwatchloggingoption.html#cfn-kinesisanalyticsv2-applicationcloudwatchloggingoption-cloudwatchloggingoption-logstreamarn
            '''
            result = self._values.get("log_stream_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLoggingOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_configuration": "applicationConfiguration",
        "application_description": "applicationDescription",
        "application_maintenance_configuration": "applicationMaintenanceConfiguration",
        "application_mode": "applicationMode",
        "application_name": "applicationName",
        "run_configuration": "runConfiguration",
        "runtime_environment": "runtimeEnvironment",
        "service_execution_role": "serviceExecutionRole",
        "tags": "tags",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        application_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ApplicationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        application_description: typing.Optional[builtins.str] = None,
        application_maintenance_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ApplicationMaintenanceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        application_mode: typing.Optional[builtins.str] = None,
        application_name: typing.Optional[builtins.str] = None,
        run_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.RunConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        runtime_environment: typing.Optional[builtins.str] = None,
        service_execution_role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param application_configuration: Use this parameter to configure the application.
        :param application_description: The description of the application. Default: - ""
        :param application_maintenance_configuration: Specifies the maintenance window parameters for a Kinesis Data Analytics application.
        :param application_mode: To create a Kinesis Data Analytics Studio notebook, you must set the mode to ``INTERACTIVE`` . However, for a Kinesis Data Analytics for Apache Flink application, the mode is optional.
        :param application_name: The name of the application.
        :param run_configuration: Describes the starting parameters for an Managed Service for Apache Flink application.
        :param runtime_environment: The runtime environment for the application.
        :param service_execution_role: Specifies the IAM role that the application uses to access external resources.
        :param tags: A list of one or more tags to assign to the application. A tag is a key-value pair that identifies an application. Note that the maximum number of application tags includes system tags. The maximum number of user-defined application tags is 50.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
            
            cfn_application_mixin_props = kinesisanalyticsv2_mixins.CfnApplicationMixinProps(
                application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationConfigurationProperty(
                    application_code_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationCodeConfigurationProperty(
                        code_content=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CodeContentProperty(
                            s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentLocationProperty(
                                bucket_arn="bucketArn",
                                file_key="fileKey",
                                object_version="objectVersion"
                            ),
                            text_content="textContent",
                            zip_file_content="zipFileContent"
                        ),
                        code_content_type="codeContentType"
                    ),
                    application_encryption_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationEncryptionConfigurationProperty(
                        key_id="keyId",
                        key_type="keyType"
                    ),
                    application_snapshot_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationSnapshotConfigurationProperty(
                        snapshots_enabled=False
                    ),
                    application_system_rollback_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationSystemRollbackConfigurationProperty(
                        rollback_enabled=False
                    ),
                    environment_properties=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.EnvironmentPropertiesProperty(
                        property_groups=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.PropertyGroupProperty(
                            property_group_id="propertyGroupId",
                            property_map={
                                "property_map_key": "propertyMap"
                            }
                        )]
                    ),
                    flink_application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.FlinkApplicationConfigurationProperty(
                        checkpoint_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CheckpointConfigurationProperty(
                            checkpointing_enabled=False,
                            checkpoint_interval=123,
                            configuration_type="configurationType",
                            min_pause_between_checkpoints=123
                        ),
                        monitoring_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MonitoringConfigurationProperty(
                            configuration_type="configurationType",
                            log_level="logLevel",
                            metrics_level="metricsLevel"
                        ),
                        parallelism_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ParallelismConfigurationProperty(
                            auto_scaling_enabled=False,
                            configuration_type="configurationType",
                            parallelism=123,
                            parallelism_per_kpu=123
                        )
                    ),
                    sql_application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.SqlApplicationConfigurationProperty(
                        inputs=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputProperty(
                            input_parallelism=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputParallelismProperty(
                                count=123
                            ),
                            input_processing_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputProcessingConfigurationProperty(
                                input_lambda_processor=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputLambdaProcessorProperty(
                                    resource_arn="resourceArn"
                                )
                            ),
                            input_schema=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputSchemaProperty(
                                record_columns=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RecordColumnProperty(
                                    mapping="mapping",
                                    name="name",
                                    sql_type="sqlType"
                                )],
                                record_encoding="recordEncoding",
                                record_format=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RecordFormatProperty(
                                    mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MappingParametersProperty(
                                        csv_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                                            record_column_delimiter="recordColumnDelimiter",
                                            record_row_delimiter="recordRowDelimiter"
                                        ),
                                        json_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                                            record_row_path="recordRowPath"
                                        )
                                    ),
                                    record_format_type="recordFormatType"
                                )
                            ),
                            kinesis_firehose_input=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.KinesisFirehoseInputProperty(
                                resource_arn="resourceArn"
                            ),
                            kinesis_streams_input=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.KinesisStreamsInputProperty(
                                resource_arn="resourceArn"
                            ),
                            name_prefix="namePrefix"
                        )]
                    ),
                    vpc_configurations=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.VpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )],
                    zeppelin_application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ZeppelinApplicationConfigurationProperty(
                        catalog_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CatalogConfigurationProperty(
                            glue_data_catalog_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.GlueDataCatalogConfigurationProperty(
                                database_arn="databaseArn"
                            )
                        ),
                        custom_artifacts_configuration=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CustomArtifactConfigurationProperty(
                            artifact_type="artifactType",
                            maven_reference=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MavenReferenceProperty(
                                artifact_id="artifactId",
                                group_id="groupId",
                                version="version"
                            ),
                            s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentLocationProperty(
                                bucket_arn="bucketArn",
                                file_key="fileKey",
                                object_version="objectVersion"
                            )
                        )],
                        deploy_as_application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.DeployAsApplicationConfigurationProperty(
                            s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentBaseLocationProperty(
                                base_path="basePath",
                                bucket_arn="bucketArn"
                            )
                        ),
                        monitoring_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ZeppelinMonitoringConfigurationProperty(
                            log_level="logLevel"
                        )
                    )
                ),
                application_description="applicationDescription",
                application_maintenance_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationMaintenanceConfigurationProperty(
                    application_maintenance_window_start_time="applicationMaintenanceWindowStartTime"
                ),
                application_mode="applicationMode",
                application_name="applicationName",
                run_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RunConfigurationProperty(
                    application_restore_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationRestoreConfigurationProperty(
                        application_restore_type="applicationRestoreType",
                        snapshot_name="snapshotName"
                    ),
                    flink_run_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.FlinkRunConfigurationProperty(
                        allow_non_restored_state=False
                    )
                ),
                runtime_environment="runtimeEnvironment",
                service_execution_role="serviceExecutionRole",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb090809c844b83eeb283df39e178df5a843e5f0a1feb6c082c66bab7dbf9962)
            check_type(argname="argument application_configuration", value=application_configuration, expected_type=type_hints["application_configuration"])
            check_type(argname="argument application_description", value=application_description, expected_type=type_hints["application_description"])
            check_type(argname="argument application_maintenance_configuration", value=application_maintenance_configuration, expected_type=type_hints["application_maintenance_configuration"])
            check_type(argname="argument application_mode", value=application_mode, expected_type=type_hints["application_mode"])
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument run_configuration", value=run_configuration, expected_type=type_hints["run_configuration"])
            check_type(argname="argument runtime_environment", value=runtime_environment, expected_type=type_hints["runtime_environment"])
            check_type(argname="argument service_execution_role", value=service_execution_role, expected_type=type_hints["service_execution_role"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_configuration is not None:
            self._values["application_configuration"] = application_configuration
        if application_description is not None:
            self._values["application_description"] = application_description
        if application_maintenance_configuration is not None:
            self._values["application_maintenance_configuration"] = application_maintenance_configuration
        if application_mode is not None:
            self._values["application_mode"] = application_mode
        if application_name is not None:
            self._values["application_name"] = application_name
        if run_configuration is not None:
            self._values["run_configuration"] = run_configuration
        if runtime_environment is not None:
            self._values["runtime_environment"] = runtime_environment
        if service_execution_role is not None:
            self._values["service_execution_role"] = service_execution_role
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationConfigurationProperty"]]:
        '''Use this parameter to configure the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-applicationconfiguration
        '''
        result = self._values.get("application_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationConfigurationProperty"]], result)

    @builtins.property
    def application_description(self) -> typing.Optional[builtins.str]:
        '''The description of the application.

        :default: - ""

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-applicationdescription
        '''
        result = self._values.get("application_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_maintenance_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationMaintenanceConfigurationProperty"]]:
        '''Specifies the maintenance window parameters for a Kinesis Data Analytics application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-applicationmaintenanceconfiguration
        '''
        result = self._values.get("application_maintenance_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationMaintenanceConfigurationProperty"]], result)

    @builtins.property
    def application_mode(self) -> typing.Optional[builtins.str]:
        '''To create a Kinesis Data Analytics Studio notebook, you must set the mode to ``INTERACTIVE`` .

        However, for a Kinesis Data Analytics for Apache Flink application, the mode is optional.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-applicationmode
        '''
        result = self._values.get("application_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.RunConfigurationProperty"]]:
        '''Describes the starting parameters for an Managed Service for Apache Flink application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-runconfiguration
        '''
        result = self._values.get("run_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.RunConfigurationProperty"]], result)

    @builtins.property
    def runtime_environment(self) -> typing.Optional[builtins.str]:
        '''The runtime environment for the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-runtimeenvironment
        '''
        result = self._values.get("runtime_environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_execution_role(self) -> typing.Optional[builtins.str]:
        '''Specifies the IAM role that the application uses to access external resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-serviceexecutionrole
        '''
        result = self._values.get("service_execution_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of one or more tags to assign to the application.

        A tag is a key-value pair that identifies an application. Note that the maximum number of application tags includes system tags. The maximum number of user-defined application tags is 50.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationOutputMixinProps",
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

        :param application_name: The name of the application.
        :param output: Describes a SQL-based Kinesis Data Analytics application's output configuration, in which you identify an in-application stream and a destination where you want the in-application stream data to be written. The destination can be a Kinesis data stream or a Kinesis Data Firehose delivery stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationoutput.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
            
            cfn_application_output_mixin_props = kinesisanalyticsv2_mixins.CfnApplicationOutputMixinProps(
                application_name="applicationName",
                output=kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.OutputProperty(
                    destination_schema=kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.DestinationSchemaProperty(
                        record_format_type="recordFormatType"
                    ),
                    kinesis_firehose_output=kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty(
                        resource_arn="resourceArn"
                    ),
                    kinesis_streams_output=kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty(
                        resource_arn="resourceArn"
                    ),
                    lambda_output=kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.LambdaOutputProperty(
                        resource_arn="resourceArn"
                    ),
                    name="name"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9499736b700cabc7a0640638ae22982d46448fe7b01a820616dfd567647e6616)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if output is not None:
            self._values["output"] = output

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationoutput.html#cfn-kinesisanalyticsv2-applicationoutput-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.OutputProperty"]]:
        '''Describes a SQL-based Kinesis Data Analytics application's output configuration, in which you identify an in-application stream and a destination where you want the in-application stream data to be written.

        The destination can be a Kinesis data stream or a Kinesis Data Firehose delivery stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationoutput.html#cfn-kinesisanalyticsv2-applicationoutput-output
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
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationOutputPropsMixin",
):
    '''Adds an external destination to your SQL-based Amazon Kinesis Data Analytics application.

    If you want Kinesis Data Analytics to deliver data from an in-application stream within your application to an external destination (such as an Kinesis data stream, a Kinesis Data Firehose delivery stream, or an Amazon Lambda function), you add the relevant configuration to your application using this operation. You can configure one or more outputs for your application. Each output configuration maps an in-application stream and an external destination.

    You can use one of the output configurations to deliver data from your in-application error stream to an external destination so that you can analyze the errors.

    Any configuration update, including adding a streaming source using this operation, results in a new version of the application. You can use the `DescribeApplication <https://docs.aws.amazon.com/managed-flink/latest/apiv2/API_DescribeApplication.html>`_ operation to find the current application version.
    .. epigraph::

       Creation of multiple outputs should be sequential (use of DependsOn) to avoid a problem with a stale application version ( *ConcurrentModificationException* ).

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationoutput.html
    :cloudformationResource: AWS::KinesisAnalyticsV2::ApplicationOutput
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
        
        cfn_application_output_props_mixin = kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin(kinesisanalyticsv2_mixins.CfnApplicationOutputMixinProps(
            application_name="applicationName",
            output=kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.OutputProperty(
                destination_schema=kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.DestinationSchemaProperty(
                    record_format_type="recordFormatType"
                ),
                kinesis_firehose_output=kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty(
                    resource_arn="resourceArn"
                ),
                kinesis_streams_output=kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty(
                    resource_arn="resourceArn"
                ),
                lambda_output=kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.LambdaOutputProperty(
                    resource_arn="resourceArn"
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
        '''Create a mixin to apply properties to ``AWS::KinesisAnalyticsV2::ApplicationOutput``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05b4cb94ed101faea0bbf8cc46cb18b994628d0535260878e8531d59622af706)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc8d0916b300b6e19c640c220a5c7064cd80794ac2d7e64c8e8daa7e6f6a7c4d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2e0a629eb0ed12d0fb4cf8259b03cd647cd84f3b10757e71c013e129d1571b)
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationOutputPropsMixin.DestinationSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"record_format_type": "recordFormatType"},
    )
    class DestinationSchemaProperty:
        def __init__(
            self,
            *,
            record_format_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the data format when records are written to the destination in a SQL-based Kinesis Data Analytics application.

            :param record_format_type: Specifies the format of the records on the output stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-destinationschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                destination_schema_property = kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.DestinationSchemaProperty(
                    record_format_type="recordFormatType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__deb95f57a5a1f98d56fae1ecd10409905e0ce52dcce1c1aef5326681abe007fb)
                check_type(argname="argument record_format_type", value=record_format_type, expected_type=type_hints["record_format_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if record_format_type is not None:
                self._values["record_format_type"] = record_format_type

        @builtins.property
        def record_format_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the format of the records on the output stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-destinationschema.html#cfn-kinesisanalyticsv2-applicationoutput-destinationschema-recordformattype
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn"},
    )
    class KinesisFirehoseOutputProperty:
        def __init__(
            self,
            *,
            resource_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''For a SQL-based Kinesis Data Analytics application, when configuring application output, identifies a Kinesis Data Firehose delivery stream as the destination.

            You provide the stream Amazon Resource Name (ARN) of the delivery stream.

            :param resource_arn: The ARN of the destination delivery stream to write to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-kinesisfirehoseoutput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                kinesis_firehose_output_property = kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty(
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__41929938915ebf2fe3b7de59a4f25536db126f3dcab0eb671bcf6fca39bd2415)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the destination delivery stream to write to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-kinesisfirehoseoutput.html#cfn-kinesisanalyticsv2-applicationoutput-kinesisfirehoseoutput-resourcearn
            '''
            result = self._values.get("resource_arn")
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn"},
    )
    class KinesisStreamsOutputProperty:
        def __init__(
            self,
            *,
            resource_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When you configure a SQL-based Kinesis Data Analytics application's output, identifies a Kinesis data stream as the destination.

            You provide the stream Amazon Resource Name (ARN).

            :param resource_arn: The ARN of the destination Kinesis data stream to write to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-kinesisstreamsoutput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                kinesis_streams_output_property = kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty(
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0c3cb8b8394f9b7ffb90efa920fe89cb779000d597c9eb48e0cc844079c81f1f)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the destination Kinesis data stream to write to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-kinesisstreamsoutput.html#cfn-kinesisanalyticsv2-applicationoutput-kinesisstreamsoutput-resourcearn
            '''
            result = self._values.get("resource_arn")
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationOutputPropsMixin.LambdaOutputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn"},
    )
    class LambdaOutputProperty:
        def __init__(
            self,
            *,
            resource_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When you configure a SQL-based Kinesis Data Analytics application's output, identifies an Amazon Lambda function as the destination.

            You provide the function Amazon Resource Name (ARN) of the Lambda function.

            :param resource_arn: The Amazon Resource Name (ARN) of the destination Lambda function to write to. .. epigraph:: To specify an earlier version of the Lambda function than the latest, include the Lambda function version in the Lambda function ARN. For more information about Lambda ARNs, see `Example ARNs: Amazon Lambda <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#arn-syntax-lambda>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-lambdaoutput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                lambda_output_property = kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.LambdaOutputProperty(
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c4209998ab24d66d43f4f0353adb1e455bcaf20162cc3e090bb5dbae351107e4)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the destination Lambda function to write to.

            .. epigraph::

               To specify an earlier version of the Lambda function than the latest, include the Lambda function version in the Lambda function ARN. For more information about Lambda ARNs, see `Example ARNs: Amazon Lambda <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#arn-syntax-lambda>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-lambdaoutput.html#cfn-kinesisanalyticsv2-applicationoutput-lambdaoutput-resourcearn
            '''
            result = self._values.get("resource_arn")
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationOutputPropsMixin.OutputProperty",
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
            '''Describes a SQL-based Kinesis Data Analytics application's output configuration, in which you identify an in-application stream and a destination where you want the in-application stream data to be written.

            The destination can be a Kinesis data stream or a Kinesis Data Firehose delivery stream.

            :param destination_schema: Describes the data format when records are written to the destination.
            :param kinesis_firehose_output: Identifies a Kinesis Data Firehose delivery stream as the destination.
            :param kinesis_streams_output: Identifies a Kinesis data stream as the destination.
            :param lambda_output: Identifies an Amazon Lambda function as the destination.
            :param name: The name of the in-application stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                output_property = kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.OutputProperty(
                    destination_schema=kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.DestinationSchemaProperty(
                        record_format_type="recordFormatType"
                    ),
                    kinesis_firehose_output=kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty(
                        resource_arn="resourceArn"
                    ),
                    kinesis_streams_output=kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty(
                        resource_arn="resourceArn"
                    ),
                    lambda_output=kinesisanalyticsv2_mixins.CfnApplicationOutputPropsMixin.LambdaOutputProperty(
                        resource_arn="resourceArn"
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bf21a8f69f385258a78658e04217a01202c91e919dc0837258654d2edab25e87)
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

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-destinationschema
            '''
            result = self._values.get("destination_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.DestinationSchemaProperty"]], result)

        @builtins.property
        def kinesis_firehose_output(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty"]]:
            '''Identifies a Kinesis Data Firehose delivery stream as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-kinesisfirehoseoutput
            '''
            result = self._values.get("kinesis_firehose_output")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty"]], result)

        @builtins.property
        def kinesis_streams_output(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty"]]:
            '''Identifies a Kinesis data stream as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-kinesisstreamsoutput
            '''
            result = self._values.get("kinesis_streams_output")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty"]], result)

        @builtins.property
        def lambda_output(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.LambdaOutputProperty"]]:
            '''Identifies an Amazon Lambda function as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-lambdaoutput
            '''
            result = self._values.get("lambda_output")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.LambdaOutputProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the in-application stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-name
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
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin",
):
    '''Creates an Amazon Kinesis Data Analytics application.

    For information about creating a Kinesis Data Analytics application, see `Creating an Application <https://docs.aws.amazon.com/managed-flink/latest/java/getting-started.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html
    :cloudformationResource: AWS::KinesisAnalyticsV2::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
        
        cfn_application_props_mixin = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin(kinesisanalyticsv2_mixins.CfnApplicationMixinProps(
            application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationConfigurationProperty(
                application_code_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationCodeConfigurationProperty(
                    code_content=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CodeContentProperty(
                        s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentLocationProperty(
                            bucket_arn="bucketArn",
                            file_key="fileKey",
                            object_version="objectVersion"
                        ),
                        text_content="textContent",
                        zip_file_content="zipFileContent"
                    ),
                    code_content_type="codeContentType"
                ),
                application_encryption_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationEncryptionConfigurationProperty(
                    key_id="keyId",
                    key_type="keyType"
                ),
                application_snapshot_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationSnapshotConfigurationProperty(
                    snapshots_enabled=False
                ),
                application_system_rollback_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationSystemRollbackConfigurationProperty(
                    rollback_enabled=False
                ),
                environment_properties=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.EnvironmentPropertiesProperty(
                    property_groups=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.PropertyGroupProperty(
                        property_group_id="propertyGroupId",
                        property_map={
                            "property_map_key": "propertyMap"
                        }
                    )]
                ),
                flink_application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.FlinkApplicationConfigurationProperty(
                    checkpoint_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CheckpointConfigurationProperty(
                        checkpointing_enabled=False,
                        checkpoint_interval=123,
                        configuration_type="configurationType",
                        min_pause_between_checkpoints=123
                    ),
                    monitoring_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MonitoringConfigurationProperty(
                        configuration_type="configurationType",
                        log_level="logLevel",
                        metrics_level="metricsLevel"
                    ),
                    parallelism_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ParallelismConfigurationProperty(
                        auto_scaling_enabled=False,
                        configuration_type="configurationType",
                        parallelism=123,
                        parallelism_per_kpu=123
                    )
                ),
                sql_application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.SqlApplicationConfigurationProperty(
                    inputs=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputProperty(
                        input_parallelism=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputParallelismProperty(
                            count=123
                        ),
                        input_processing_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputProcessingConfigurationProperty(
                            input_lambda_processor=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputLambdaProcessorProperty(
                                resource_arn="resourceArn"
                            )
                        ),
                        input_schema=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputSchemaProperty(
                            record_columns=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RecordColumnProperty(
                                mapping="mapping",
                                name="name",
                                sql_type="sqlType"
                            )],
                            record_encoding="recordEncoding",
                            record_format=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RecordFormatProperty(
                                mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MappingParametersProperty(
                                    csv_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                                        record_column_delimiter="recordColumnDelimiter",
                                        record_row_delimiter="recordRowDelimiter"
                                    ),
                                    json_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                                        record_row_path="recordRowPath"
                                    )
                                ),
                                record_format_type="recordFormatType"
                            )
                        ),
                        kinesis_firehose_input=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.KinesisFirehoseInputProperty(
                            resource_arn="resourceArn"
                        ),
                        kinesis_streams_input=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.KinesisStreamsInputProperty(
                            resource_arn="resourceArn"
                        ),
                        name_prefix="namePrefix"
                    )]
                ),
                vpc_configurations=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.VpcConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )],
                zeppelin_application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ZeppelinApplicationConfigurationProperty(
                    catalog_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CatalogConfigurationProperty(
                        glue_data_catalog_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.GlueDataCatalogConfigurationProperty(
                            database_arn="databaseArn"
                        )
                    ),
                    custom_artifacts_configuration=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CustomArtifactConfigurationProperty(
                        artifact_type="artifactType",
                        maven_reference=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MavenReferenceProperty(
                            artifact_id="artifactId",
                            group_id="groupId",
                            version="version"
                        ),
                        s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentLocationProperty(
                            bucket_arn="bucketArn",
                            file_key="fileKey",
                            object_version="objectVersion"
                        )
                    )],
                    deploy_as_application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.DeployAsApplicationConfigurationProperty(
                        s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentBaseLocationProperty(
                            base_path="basePath",
                            bucket_arn="bucketArn"
                        )
                    ),
                    monitoring_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ZeppelinMonitoringConfigurationProperty(
                        log_level="logLevel"
                    )
                )
            ),
            application_description="applicationDescription",
            application_maintenance_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationMaintenanceConfigurationProperty(
                application_maintenance_window_start_time="applicationMaintenanceWindowStartTime"
            ),
            application_mode="applicationMode",
            application_name="applicationName",
            run_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RunConfigurationProperty(
                application_restore_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationRestoreConfigurationProperty(
                    application_restore_type="applicationRestoreType",
                    snapshot_name="snapshotName"
                ),
                flink_run_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.FlinkRunConfigurationProperty(
                    allow_non_restored_state=False
                )
            ),
            runtime_environment="runtimeEnvironment",
            service_execution_role="serviceExecutionRole",
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
        props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::KinesisAnalyticsV2::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a2b226fa0a2379aea0b06e5b10628057fdbbbcbd9e5d29d231e3d2b45f25932)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f9f757b1ee22b84581b1b9b66b5869975c18537074e8dd6fafbcf8a97a3cba8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47976607390b06738c5eaaafa79e34dcb420a95f3b98122690228b6592698a2b)
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.ApplicationCodeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_content": "codeContent",
            "code_content_type": "codeContentType",
        },
    )
    class ApplicationCodeConfigurationProperty:
        def __init__(
            self,
            *,
            code_content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.CodeContentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            code_content_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes code configuration for an application.

            :param code_content: The location and type of the application code.
            :param code_content_type: Specifies whether the code content is in text or zip format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationcodeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                application_code_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationCodeConfigurationProperty(
                    code_content=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CodeContentProperty(
                        s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentLocationProperty(
                            bucket_arn="bucketArn",
                            file_key="fileKey",
                            object_version="objectVersion"
                        ),
                        text_content="textContent",
                        zip_file_content="zipFileContent"
                    ),
                    code_content_type="codeContentType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__752478396235b218e37a37ede09be75d978eaa050f2efbc0dc9c9844966afa86)
                check_type(argname="argument code_content", value=code_content, expected_type=type_hints["code_content"])
                check_type(argname="argument code_content_type", value=code_content_type, expected_type=type_hints["code_content_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code_content is not None:
                self._values["code_content"] = code_content
            if code_content_type is not None:
                self._values["code_content_type"] = code_content_type

        @builtins.property
        def code_content(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CodeContentProperty"]]:
            '''The location and type of the application code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationcodeconfiguration.html#cfn-kinesisanalyticsv2-application-applicationcodeconfiguration-codecontent
            '''
            result = self._values.get("code_content")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CodeContentProperty"]], result)

        @builtins.property
        def code_content_type(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the code content is in text or zip format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationcodeconfiguration.html#cfn-kinesisanalyticsv2-application-applicationcodeconfiguration-codecontenttype
            '''
            result = self._values.get("code_content_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationCodeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.ApplicationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_code_configuration": "applicationCodeConfiguration",
            "application_encryption_configuration": "applicationEncryptionConfiguration",
            "application_snapshot_configuration": "applicationSnapshotConfiguration",
            "application_system_rollback_configuration": "applicationSystemRollbackConfiguration",
            "environment_properties": "environmentProperties",
            "flink_application_configuration": "flinkApplicationConfiguration",
            "sql_application_configuration": "sqlApplicationConfiguration",
            "vpc_configurations": "vpcConfigurations",
            "zeppelin_application_configuration": "zeppelinApplicationConfiguration",
        },
    )
    class ApplicationConfigurationProperty:
        def __init__(
            self,
            *,
            application_code_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ApplicationCodeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            application_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ApplicationEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            application_snapshot_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ApplicationSnapshotConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            application_system_rollback_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ApplicationSystemRollbackConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            environment_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.EnvironmentPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            flink_application_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.FlinkApplicationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sql_application_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.SqlApplicationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            vpc_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            zeppelin_application_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ZeppelinApplicationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the creation parameters for a Managed Service for Apache Flink application.

            :param application_code_configuration: The code location and type parameters for a Managed Service for Apache Flink application.
            :param application_encryption_configuration: The configuration to manage encryption at rest.
            :param application_snapshot_configuration: Describes whether snapshots are enabled for a Managed Service for Apache Flink application.
            :param application_system_rollback_configuration: Describes whether system rollbacks are enabled for a Managed Service for Apache Flink application.
            :param environment_properties: Describes execution properties for a Managed Service for Apache Flink application.
            :param flink_application_configuration: The creation and update parameters for a Managed Service for Apache Flink application.
            :param sql_application_configuration: The creation and update parameters for a SQL-based Kinesis Data Analytics application.
            :param vpc_configurations: The array of descriptions of VPC configurations available to the application.
            :param zeppelin_application_configuration: The configuration parameters for a Kinesis Data Analytics Studio notebook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                application_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationConfigurationProperty(
                    application_code_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationCodeConfigurationProperty(
                        code_content=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CodeContentProperty(
                            s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentLocationProperty(
                                bucket_arn="bucketArn",
                                file_key="fileKey",
                                object_version="objectVersion"
                            ),
                            text_content="textContent",
                            zip_file_content="zipFileContent"
                        ),
                        code_content_type="codeContentType"
                    ),
                    application_encryption_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationEncryptionConfigurationProperty(
                        key_id="keyId",
                        key_type="keyType"
                    ),
                    application_snapshot_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationSnapshotConfigurationProperty(
                        snapshots_enabled=False
                    ),
                    application_system_rollback_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationSystemRollbackConfigurationProperty(
                        rollback_enabled=False
                    ),
                    environment_properties=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.EnvironmentPropertiesProperty(
                        property_groups=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.PropertyGroupProperty(
                            property_group_id="propertyGroupId",
                            property_map={
                                "property_map_key": "propertyMap"
                            }
                        )]
                    ),
                    flink_application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.FlinkApplicationConfigurationProperty(
                        checkpoint_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CheckpointConfigurationProperty(
                            checkpointing_enabled=False,
                            checkpoint_interval=123,
                            configuration_type="configurationType",
                            min_pause_between_checkpoints=123
                        ),
                        monitoring_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MonitoringConfigurationProperty(
                            configuration_type="configurationType",
                            log_level="logLevel",
                            metrics_level="metricsLevel"
                        ),
                        parallelism_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ParallelismConfigurationProperty(
                            auto_scaling_enabled=False,
                            configuration_type="configurationType",
                            parallelism=123,
                            parallelism_per_kpu=123
                        )
                    ),
                    sql_application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.SqlApplicationConfigurationProperty(
                        inputs=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputProperty(
                            input_parallelism=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputParallelismProperty(
                                count=123
                            ),
                            input_processing_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputProcessingConfigurationProperty(
                                input_lambda_processor=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputLambdaProcessorProperty(
                                    resource_arn="resourceArn"
                                )
                            ),
                            input_schema=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputSchemaProperty(
                                record_columns=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RecordColumnProperty(
                                    mapping="mapping",
                                    name="name",
                                    sql_type="sqlType"
                                )],
                                record_encoding="recordEncoding",
                                record_format=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RecordFormatProperty(
                                    mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MappingParametersProperty(
                                        csv_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                                            record_column_delimiter="recordColumnDelimiter",
                                            record_row_delimiter="recordRowDelimiter"
                                        ),
                                        json_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                                            record_row_path="recordRowPath"
                                        )
                                    ),
                                    record_format_type="recordFormatType"
                                )
                            ),
                            kinesis_firehose_input=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.KinesisFirehoseInputProperty(
                                resource_arn="resourceArn"
                            ),
                            kinesis_streams_input=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.KinesisStreamsInputProperty(
                                resource_arn="resourceArn"
                            ),
                            name_prefix="namePrefix"
                        )]
                    ),
                    vpc_configurations=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.VpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )],
                    zeppelin_application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ZeppelinApplicationConfigurationProperty(
                        catalog_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CatalogConfigurationProperty(
                            glue_data_catalog_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.GlueDataCatalogConfigurationProperty(
                                database_arn="databaseArn"
                            )
                        ),
                        custom_artifacts_configuration=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CustomArtifactConfigurationProperty(
                            artifact_type="artifactType",
                            maven_reference=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MavenReferenceProperty(
                                artifact_id="artifactId",
                                group_id="groupId",
                                version="version"
                            ),
                            s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentLocationProperty(
                                bucket_arn="bucketArn",
                                file_key="fileKey",
                                object_version="objectVersion"
                            )
                        )],
                        deploy_as_application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.DeployAsApplicationConfigurationProperty(
                            s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentBaseLocationProperty(
                                base_path="basePath",
                                bucket_arn="bucketArn"
                            )
                        ),
                        monitoring_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ZeppelinMonitoringConfigurationProperty(
                            log_level="logLevel"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__97d08cff34c10503084c8035bd80bdf9f7dc7d2e7bfba4288bb10ad1b7fd190c)
                check_type(argname="argument application_code_configuration", value=application_code_configuration, expected_type=type_hints["application_code_configuration"])
                check_type(argname="argument application_encryption_configuration", value=application_encryption_configuration, expected_type=type_hints["application_encryption_configuration"])
                check_type(argname="argument application_snapshot_configuration", value=application_snapshot_configuration, expected_type=type_hints["application_snapshot_configuration"])
                check_type(argname="argument application_system_rollback_configuration", value=application_system_rollback_configuration, expected_type=type_hints["application_system_rollback_configuration"])
                check_type(argname="argument environment_properties", value=environment_properties, expected_type=type_hints["environment_properties"])
                check_type(argname="argument flink_application_configuration", value=flink_application_configuration, expected_type=type_hints["flink_application_configuration"])
                check_type(argname="argument sql_application_configuration", value=sql_application_configuration, expected_type=type_hints["sql_application_configuration"])
                check_type(argname="argument vpc_configurations", value=vpc_configurations, expected_type=type_hints["vpc_configurations"])
                check_type(argname="argument zeppelin_application_configuration", value=zeppelin_application_configuration, expected_type=type_hints["zeppelin_application_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_code_configuration is not None:
                self._values["application_code_configuration"] = application_code_configuration
            if application_encryption_configuration is not None:
                self._values["application_encryption_configuration"] = application_encryption_configuration
            if application_snapshot_configuration is not None:
                self._values["application_snapshot_configuration"] = application_snapshot_configuration
            if application_system_rollback_configuration is not None:
                self._values["application_system_rollback_configuration"] = application_system_rollback_configuration
            if environment_properties is not None:
                self._values["environment_properties"] = environment_properties
            if flink_application_configuration is not None:
                self._values["flink_application_configuration"] = flink_application_configuration
            if sql_application_configuration is not None:
                self._values["sql_application_configuration"] = sql_application_configuration
            if vpc_configurations is not None:
                self._values["vpc_configurations"] = vpc_configurations
            if zeppelin_application_configuration is not None:
                self._values["zeppelin_application_configuration"] = zeppelin_application_configuration

        @builtins.property
        def application_code_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationCodeConfigurationProperty"]]:
            '''The code location and type parameters for a Managed Service for Apache Flink application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-applicationcodeconfiguration
            '''
            result = self._values.get("application_code_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationCodeConfigurationProperty"]], result)

        @builtins.property
        def application_encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationEncryptionConfigurationProperty"]]:
            '''The configuration to manage encryption at rest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-applicationencryptionconfiguration
            '''
            result = self._values.get("application_encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationEncryptionConfigurationProperty"]], result)

        @builtins.property
        def application_snapshot_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationSnapshotConfigurationProperty"]]:
            '''Describes whether snapshots are enabled for a Managed Service for Apache Flink application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-applicationsnapshotconfiguration
            '''
            result = self._values.get("application_snapshot_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationSnapshotConfigurationProperty"]], result)

        @builtins.property
        def application_system_rollback_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationSystemRollbackConfigurationProperty"]]:
            '''Describes whether system rollbacks are enabled for a Managed Service for Apache Flink application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-applicationsystemrollbackconfiguration
            '''
            result = self._values.get("application_system_rollback_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationSystemRollbackConfigurationProperty"]], result)

        @builtins.property
        def environment_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.EnvironmentPropertiesProperty"]]:
            '''Describes execution properties for a Managed Service for Apache Flink application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-environmentproperties
            '''
            result = self._values.get("environment_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.EnvironmentPropertiesProperty"]], result)

        @builtins.property
        def flink_application_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.FlinkApplicationConfigurationProperty"]]:
            '''The creation and update parameters for a Managed Service for Apache Flink application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-flinkapplicationconfiguration
            '''
            result = self._values.get("flink_application_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.FlinkApplicationConfigurationProperty"]], result)

        @builtins.property
        def sql_application_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.SqlApplicationConfigurationProperty"]]:
            '''The creation and update parameters for a SQL-based Kinesis Data Analytics application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-sqlapplicationconfiguration
            '''
            result = self._values.get("sql_application_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.SqlApplicationConfigurationProperty"]], result)

        @builtins.property
        def vpc_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.VpcConfigurationProperty"]]]]:
            '''The array of descriptions of VPC configurations available to the application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-vpcconfigurations
            '''
            result = self._values.get("vpc_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.VpcConfigurationProperty"]]]], result)

        @builtins.property
        def zeppelin_application_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ZeppelinApplicationConfigurationProperty"]]:
            '''The configuration parameters for a Kinesis Data Analytics Studio notebook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-zeppelinapplicationconfiguration
            '''
            result = self._values.get("zeppelin_application_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ZeppelinApplicationConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.ApplicationEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"key_id": "keyId", "key_type": "keyType"},
    )
    class ApplicationEncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            key_id: typing.Optional[builtins.str] = None,
            key_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration to manage encryption at rest.

            :param key_id: The key ARN, key ID, alias ARN, or alias name of the KMS key used for encryption at rest.
            :param key_type: Specifies the type of key used for encryption at rest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                application_encryption_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationEncryptionConfigurationProperty(
                    key_id="keyId",
                    key_type="keyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__761173697e7718ec1e8dcc8160dc9fffee03be812188fd3ef8199aab2814d729)
                check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_id is not None:
                self._values["key_id"] = key_id
            if key_type is not None:
                self._values["key_type"] = key_type

        @builtins.property
        def key_id(self) -> typing.Optional[builtins.str]:
            '''The key ARN, key ID, alias ARN, or alias name of the KMS key used for encryption at rest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationencryptionconfiguration.html#cfn-kinesisanalyticsv2-application-applicationencryptionconfiguration-keyid
            '''
            result = self._values.get("key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of key used for encryption at rest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationencryptionconfiguration.html#cfn-kinesisanalyticsv2-application-applicationencryptionconfiguration-keytype
            '''
            result = self._values.get("key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.ApplicationMaintenanceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_maintenance_window_start_time": "applicationMaintenanceWindowStartTime",
        },
    )
    class ApplicationMaintenanceConfigurationProperty:
        def __init__(
            self,
            *,
            application_maintenance_window_start_time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the maintenance configuration for a AKAlong .

            :param application_maintenance_window_start_time: The UTC timestamp of a day from which the eight-hour maintenance window will begin every day of the week. Maintenance of the application happens only during this eight-hour window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationmaintenanceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                application_maintenance_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationMaintenanceConfigurationProperty(
                    application_maintenance_window_start_time="applicationMaintenanceWindowStartTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b1711ef71893491d2468da166d8de55f6e11c1860237b8842648d403a45ca984)
                check_type(argname="argument application_maintenance_window_start_time", value=application_maintenance_window_start_time, expected_type=type_hints["application_maintenance_window_start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_maintenance_window_start_time is not None:
                self._values["application_maintenance_window_start_time"] = application_maintenance_window_start_time

        @builtins.property
        def application_maintenance_window_start_time(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The UTC timestamp of a day from which the eight-hour maintenance window will begin every day of the week.

            Maintenance of the application happens only during this eight-hour window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationmaintenanceconfiguration.html#cfn-kinesisanalyticsv2-application-applicationmaintenanceconfiguration-applicationmaintenancewindowstarttime
            '''
            result = self._values.get("application_maintenance_window_start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationMaintenanceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.ApplicationRestoreConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_restore_type": "applicationRestoreType",
            "snapshot_name": "snapshotName",
        },
    )
    class ApplicationRestoreConfigurationProperty:
        def __init__(
            self,
            *,
            application_restore_type: typing.Optional[builtins.str] = None,
            snapshot_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the method and snapshot to use when restarting an application using previously saved application state.

            :param application_restore_type: Specifies how the application should be restored.
            :param snapshot_name: The identifier of an existing snapshot of application state to use to restart an application. The application uses this value if ``RESTORE_FROM_CUSTOM_SNAPSHOT`` is specified for the ``ApplicationRestoreType`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationrestoreconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                application_restore_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationRestoreConfigurationProperty(
                    application_restore_type="applicationRestoreType",
                    snapshot_name="snapshotName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f2a726ab8482f2d5561b9ffd31b22ae765c24ef6e8673c587f45656ba17c461f)
                check_type(argname="argument application_restore_type", value=application_restore_type, expected_type=type_hints["application_restore_type"])
                check_type(argname="argument snapshot_name", value=snapshot_name, expected_type=type_hints["snapshot_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_restore_type is not None:
                self._values["application_restore_type"] = application_restore_type
            if snapshot_name is not None:
                self._values["snapshot_name"] = snapshot_name

        @builtins.property
        def application_restore_type(self) -> typing.Optional[builtins.str]:
            '''Specifies how the application should be restored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationrestoreconfiguration.html#cfn-kinesisanalyticsv2-application-applicationrestoreconfiguration-applicationrestoretype
            '''
            result = self._values.get("application_restore_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def snapshot_name(self) -> typing.Optional[builtins.str]:
            '''The identifier of an existing snapshot of application state to use to restart an application.

            The application uses this value if ``RESTORE_FROM_CUSTOM_SNAPSHOT`` is specified for the ``ApplicationRestoreType`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationrestoreconfiguration.html#cfn-kinesisanalyticsv2-application-applicationrestoreconfiguration-snapshotname
            '''
            result = self._values.get("snapshot_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationRestoreConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.ApplicationSnapshotConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"snapshots_enabled": "snapshotsEnabled"},
    )
    class ApplicationSnapshotConfigurationProperty:
        def __init__(
            self,
            *,
            snapshots_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Describes whether snapshots are enabled for a Managed Service for Apache Flink application.

            :param snapshots_enabled: Describes whether snapshots are enabled for a Managed Service for Apache Flink application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationsnapshotconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                application_snapshot_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationSnapshotConfigurationProperty(
                    snapshots_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de4d3bacd97a2bc27a5da895145679ae3fa7faf6845c2596264254e89ede570d)
                check_type(argname="argument snapshots_enabled", value=snapshots_enabled, expected_type=type_hints["snapshots_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if snapshots_enabled is not None:
                self._values["snapshots_enabled"] = snapshots_enabled

        @builtins.property
        def snapshots_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Describes whether snapshots are enabled for a Managed Service for Apache Flink application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationsnapshotconfiguration.html#cfn-kinesisanalyticsv2-application-applicationsnapshotconfiguration-snapshotsenabled
            '''
            result = self._values.get("snapshots_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationSnapshotConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.ApplicationSystemRollbackConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"rollback_enabled": "rollbackEnabled"},
    )
    class ApplicationSystemRollbackConfigurationProperty:
        def __init__(
            self,
            *,
            rollback_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Describes the system rollback configuration for a Managed Service for Apache Flink application.

            :param rollback_enabled: Describes whether system rollbacks are enabled for a Managed Service for Apache Flink application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationsystemrollbackconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                application_system_rollback_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationSystemRollbackConfigurationProperty(
                    rollback_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__938b6429404837bcdbc7d388f9862dee6626ea5e0f6f9477f87711761b46f685)
                check_type(argname="argument rollback_enabled", value=rollback_enabled, expected_type=type_hints["rollback_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rollback_enabled is not None:
                self._values["rollback_enabled"] = rollback_enabled

        @builtins.property
        def rollback_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Describes whether system rollbacks are enabled for a Managed Service for Apache Flink application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationsystemrollbackconfiguration.html#cfn-kinesisanalyticsv2-application-applicationsystemrollbackconfiguration-rollbackenabled
            '''
            result = self._values.get("rollback_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationSystemRollbackConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty",
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
            '''For a SQL-based Kinesis Data Analytics application, provides additional mapping information when the record format uses delimiters, such as CSV.

            For example, the following sample records use CSV format, where the records use the *'\\n'* as the row delimiter and a comma (",") as the column delimiter:

            ``"name1", "address1"``

            ``"name2", "address2"``

            :param record_column_delimiter: The column delimiter. For example, in a CSV format, a comma (",") is the typical column delimiter.
            :param record_row_delimiter: The row delimiter. For example, in a CSV format, *'\\n'* is the typical row delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-csvmappingparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                c_sVMapping_parameters_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                    record_column_delimiter="recordColumnDelimiter",
                    record_row_delimiter="recordRowDelimiter"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7ff36e66f9cc94a1577f867302d840b161a2c5cb163583742c8fae78d28cda3)
                check_type(argname="argument record_column_delimiter", value=record_column_delimiter, expected_type=type_hints["record_column_delimiter"])
                check_type(argname="argument record_row_delimiter", value=record_row_delimiter, expected_type=type_hints["record_row_delimiter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if record_column_delimiter is not None:
                self._values["record_column_delimiter"] = record_column_delimiter
            if record_row_delimiter is not None:
                self._values["record_row_delimiter"] = record_row_delimiter

        @builtins.property
        def record_column_delimiter(self) -> typing.Optional[builtins.str]:
            '''The column delimiter.

            For example, in a CSV format, a comma (",") is the typical column delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-csvmappingparameters.html#cfn-kinesisanalyticsv2-application-csvmappingparameters-recordcolumndelimiter
            '''
            result = self._values.get("record_column_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_row_delimiter(self) -> typing.Optional[builtins.str]:
            '''The row delimiter.

            For example, in a CSV format, *'\\n'* is the typical row delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-csvmappingparameters.html#cfn-kinesisanalyticsv2-application-csvmappingparameters-recordrowdelimiter
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.CatalogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "glue_data_catalog_configuration": "glueDataCatalogConfiguration",
        },
    )
    class CatalogConfigurationProperty:
        def __init__(
            self,
            *,
            glue_data_catalog_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.GlueDataCatalogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration parameters for the default Amazon Glue database.

            You use this database for SQL queries that you write in a Kinesis Data Analytics Studio notebook.

            :param glue_data_catalog_configuration: The configuration parameters for the default Amazon Glue database. You use this database for Apache Flink SQL queries and table API transforms that you write in a Kinesis Data Analytics Studio notebook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-catalogconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                catalog_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CatalogConfigurationProperty(
                    glue_data_catalog_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.GlueDataCatalogConfigurationProperty(
                        database_arn="databaseArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__07a75d22e2428fc0f860ef181c5cb7454f63574df8138c14b3cb8f938d9f6b7f)
                check_type(argname="argument glue_data_catalog_configuration", value=glue_data_catalog_configuration, expected_type=type_hints["glue_data_catalog_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if glue_data_catalog_configuration is not None:
                self._values["glue_data_catalog_configuration"] = glue_data_catalog_configuration

        @builtins.property
        def glue_data_catalog_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.GlueDataCatalogConfigurationProperty"]]:
            '''The configuration parameters for the default Amazon Glue database.

            You use this database for Apache Flink SQL queries and table API transforms that you write in a Kinesis Data Analytics Studio notebook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-catalogconfiguration.html#cfn-kinesisanalyticsv2-application-catalogconfiguration-gluedatacatalogconfiguration
            '''
            result = self._values.get("glue_data_catalog_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.GlueDataCatalogConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CatalogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.CheckpointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "checkpointing_enabled": "checkpointingEnabled",
            "checkpoint_interval": "checkpointInterval",
            "configuration_type": "configurationType",
            "min_pause_between_checkpoints": "minPauseBetweenCheckpoints",
        },
    )
    class CheckpointConfigurationProperty:
        def __init__(
            self,
            *,
            checkpointing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            checkpoint_interval: typing.Optional[jsii.Number] = None,
            configuration_type: typing.Optional[builtins.str] = None,
            min_pause_between_checkpoints: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes an application's checkpointing configuration.

            Checkpointing is the process of persisting application state for fault tolerance. For more information, see `Checkpoints for Fault Tolerance <https://docs.aws.amazon.com/https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/fault-tolerance/checkpointing/>`_ in the `Apache Flink Documentation <https://docs.aws.amazon.com/https://nightlies.apache.org/flink/flink-docs-master>`_ .

            :param checkpointing_enabled: Describes whether checkpointing is enabled for a Managed Service for Apache Flink application. .. epigraph:: If ``CheckpointConfiguration.ConfigurationType`` is ``DEFAULT`` , the application will use a ``CheckpointingEnabled`` value of ``true`` , even if this value is set to another value using this API or in application code.
            :param checkpoint_interval: Describes the interval in milliseconds between checkpoint operations. .. epigraph:: If ``CheckpointConfiguration.ConfigurationType`` is ``DEFAULT`` , the application will use a ``CheckpointInterval`` value of 60000, even if this value is set to another value using this API or in application code.
            :param configuration_type: Describes whether the application uses Managed Service for Apache Flink' default checkpointing behavior. You must set this property to ``CUSTOM`` in order to set the ``CheckpointingEnabled`` , ``CheckpointInterval`` , or ``MinPauseBetweenCheckpoints`` parameters. .. epigraph:: If this value is set to ``DEFAULT`` , the application will use the following values, even if they are set to other values using APIs or application code: - *CheckpointingEnabled:* true - *CheckpointInterval:* 60000 - *MinPauseBetweenCheckpoints:* 5000
            :param min_pause_between_checkpoints: Describes the minimum time in milliseconds after a checkpoint operation completes that a new checkpoint operation can start. If a checkpoint operation takes longer than the ``CheckpointInterval`` , the application otherwise performs continual checkpoint operations. For more information, see `Tuning Checkpointing <https://docs.aws.amazon.com/https://nightlies.apache.org/flink/flink-docs-master/docs/ops/state/large_state_tuning/#tuning-checkpointing>`_ in the `Apache Flink Documentation <https://docs.aws.amazon.com/https://nightlies.apache.org/flink/flink-docs-master>`_ . .. epigraph:: If ``CheckpointConfiguration.ConfigurationType`` is ``DEFAULT`` , the application will use a ``MinPauseBetweenCheckpoints`` value of 5000, even if this value is set using this API or in application code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                checkpoint_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CheckpointConfigurationProperty(
                    checkpointing_enabled=False,
                    checkpoint_interval=123,
                    configuration_type="configurationType",
                    min_pause_between_checkpoints=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f087798caf47698684e4b83c3d8cd688584f2f344570b5356afa28c1746cde34)
                check_type(argname="argument checkpointing_enabled", value=checkpointing_enabled, expected_type=type_hints["checkpointing_enabled"])
                check_type(argname="argument checkpoint_interval", value=checkpoint_interval, expected_type=type_hints["checkpoint_interval"])
                check_type(argname="argument configuration_type", value=configuration_type, expected_type=type_hints["configuration_type"])
                check_type(argname="argument min_pause_between_checkpoints", value=min_pause_between_checkpoints, expected_type=type_hints["min_pause_between_checkpoints"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if checkpointing_enabled is not None:
                self._values["checkpointing_enabled"] = checkpointing_enabled
            if checkpoint_interval is not None:
                self._values["checkpoint_interval"] = checkpoint_interval
            if configuration_type is not None:
                self._values["configuration_type"] = configuration_type
            if min_pause_between_checkpoints is not None:
                self._values["min_pause_between_checkpoints"] = min_pause_between_checkpoints

        @builtins.property
        def checkpointing_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Describes whether checkpointing is enabled for a Managed Service for Apache Flink application.

            .. epigraph::

               If ``CheckpointConfiguration.ConfigurationType`` is ``DEFAULT`` , the application will use a ``CheckpointingEnabled`` value of ``true`` , even if this value is set to another value using this API or in application code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html#cfn-kinesisanalyticsv2-application-checkpointconfiguration-checkpointingenabled
            '''
            result = self._values.get("checkpointing_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def checkpoint_interval(self) -> typing.Optional[jsii.Number]:
            '''Describes the interval in milliseconds between checkpoint operations.

            .. epigraph::

               If ``CheckpointConfiguration.ConfigurationType`` is ``DEFAULT`` , the application will use a ``CheckpointInterval`` value of 60000, even if this value is set to another value using this API or in application code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html#cfn-kinesisanalyticsv2-application-checkpointconfiguration-checkpointinterval
            '''
            result = self._values.get("checkpoint_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def configuration_type(self) -> typing.Optional[builtins.str]:
            '''Describes whether the application uses Managed Service for Apache Flink' default checkpointing behavior.

            You must set this property to ``CUSTOM`` in order to set the ``CheckpointingEnabled`` , ``CheckpointInterval`` , or ``MinPauseBetweenCheckpoints`` parameters.
            .. epigraph::

               If this value is set to ``DEFAULT`` , the application will use the following values, even if they are set to other values using APIs or application code:

               - *CheckpointingEnabled:* true
               - *CheckpointInterval:* 60000
               - *MinPauseBetweenCheckpoints:* 5000

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html#cfn-kinesisanalyticsv2-application-checkpointconfiguration-configurationtype
            '''
            result = self._values.get("configuration_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def min_pause_between_checkpoints(self) -> typing.Optional[jsii.Number]:
            '''Describes the minimum time in milliseconds after a checkpoint operation completes that a new checkpoint operation can start.

            If a checkpoint operation takes longer than the ``CheckpointInterval`` , the application otherwise performs continual checkpoint operations. For more information, see `Tuning Checkpointing <https://docs.aws.amazon.com/https://nightlies.apache.org/flink/flink-docs-master/docs/ops/state/large_state_tuning/#tuning-checkpointing>`_ in the `Apache Flink Documentation <https://docs.aws.amazon.com/https://nightlies.apache.org/flink/flink-docs-master>`_ .
            .. epigraph::

               If ``CheckpointConfiguration.ConfigurationType`` is ``DEFAULT`` , the application will use a ``MinPauseBetweenCheckpoints`` value of 5000, even if this value is set using this API or in application code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html#cfn-kinesisanalyticsv2-application-checkpointconfiguration-minpausebetweencheckpoints
            '''
            result = self._values.get("min_pause_between_checkpoints")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CheckpointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.CodeContentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_content_location": "s3ContentLocation",
            "text_content": "textContent",
            "zip_file_content": "zipFileContent",
        },
    )
    class CodeContentProperty:
        def __init__(
            self,
            *,
            s3_content_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.S3ContentLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            text_content: typing.Optional[builtins.str] = None,
            zip_file_content: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies either the application code, or the location of the application code, for a Managed Service for Apache Flink application.

            :param s3_content_location: Information about the Amazon S3 bucket that contains the application code.
            :param text_content: The text-format code for a Managed Service for Apache Flink application.
            :param zip_file_content: The zip-format code for a Managed Service for Apache Flink application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-codecontent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                code_content_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CodeContentProperty(
                    s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentLocationProperty(
                        bucket_arn="bucketArn",
                        file_key="fileKey",
                        object_version="objectVersion"
                    ),
                    text_content="textContent",
                    zip_file_content="zipFileContent"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a58bfd4518fc8e85e155b6ec9d967152f52d404cb7721892c791e35c2ab1ca03)
                check_type(argname="argument s3_content_location", value=s3_content_location, expected_type=type_hints["s3_content_location"])
                check_type(argname="argument text_content", value=text_content, expected_type=type_hints["text_content"])
                check_type(argname="argument zip_file_content", value=zip_file_content, expected_type=type_hints["zip_file_content"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_content_location is not None:
                self._values["s3_content_location"] = s3_content_location
            if text_content is not None:
                self._values["text_content"] = text_content
            if zip_file_content is not None:
                self._values["zip_file_content"] = zip_file_content

        @builtins.property
        def s3_content_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.S3ContentLocationProperty"]]:
            '''Information about the Amazon S3 bucket that contains the application code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-codecontent.html#cfn-kinesisanalyticsv2-application-codecontent-s3contentlocation
            '''
            result = self._values.get("s3_content_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.S3ContentLocationProperty"]], result)

        @builtins.property
        def text_content(self) -> typing.Optional[builtins.str]:
            '''The text-format code for a Managed Service for Apache Flink application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-codecontent.html#cfn-kinesisanalyticsv2-application-codecontent-textcontent
            '''
            result = self._values.get("text_content")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def zip_file_content(self) -> typing.Optional[builtins.str]:
            '''The zip-format code for a Managed Service for Apache Flink application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-codecontent.html#cfn-kinesisanalyticsv2-application-codecontent-zipfilecontent
            '''
            result = self._values.get("zip_file_content")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeContentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.CustomArtifactConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "artifact_type": "artifactType",
            "maven_reference": "mavenReference",
            "s3_content_location": "s3ContentLocation",
        },
    )
    class CustomArtifactConfigurationProperty:
        def __init__(
            self,
            *,
            artifact_type: typing.Optional[builtins.str] = None,
            maven_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.MavenReferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_content_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.S3ContentLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration of connectors and user-defined functions.

            :param artifact_type: Set this to either ``UDF`` or ``DEPENDENCY_JAR`` . ``UDF`` stands for user-defined functions. This type of artifact must be in an S3 bucket. A ``DEPENDENCY_JAR`` can be in either Maven or an S3 bucket.
            :param maven_reference: The parameters required to fully specify a Maven reference.
            :param s3_content_location: The location of the custom artifacts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-customartifactconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                custom_artifact_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CustomArtifactConfigurationProperty(
                    artifact_type="artifactType",
                    maven_reference=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MavenReferenceProperty(
                        artifact_id="artifactId",
                        group_id="groupId",
                        version="version"
                    ),
                    s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentLocationProperty(
                        bucket_arn="bucketArn",
                        file_key="fileKey",
                        object_version="objectVersion"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f82c8f95ad4cac5ffc1db091c6a1dbe19ffde8321b021ee9a6439c420f194a40)
                check_type(argname="argument artifact_type", value=artifact_type, expected_type=type_hints["artifact_type"])
                check_type(argname="argument maven_reference", value=maven_reference, expected_type=type_hints["maven_reference"])
                check_type(argname="argument s3_content_location", value=s3_content_location, expected_type=type_hints["s3_content_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if artifact_type is not None:
                self._values["artifact_type"] = artifact_type
            if maven_reference is not None:
                self._values["maven_reference"] = maven_reference
            if s3_content_location is not None:
                self._values["s3_content_location"] = s3_content_location

        @builtins.property
        def artifact_type(self) -> typing.Optional[builtins.str]:
            '''Set this to either ``UDF`` or ``DEPENDENCY_JAR`` .

            ``UDF`` stands for user-defined functions. This type of artifact must be in an S3 bucket. A ``DEPENDENCY_JAR`` can be in either Maven or an S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-customartifactconfiguration.html#cfn-kinesisanalyticsv2-application-customartifactconfiguration-artifacttype
            '''
            result = self._values.get("artifact_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def maven_reference(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MavenReferenceProperty"]]:
            '''The parameters required to fully specify a Maven reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-customartifactconfiguration.html#cfn-kinesisanalyticsv2-application-customartifactconfiguration-mavenreference
            '''
            result = self._values.get("maven_reference")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MavenReferenceProperty"]], result)

        @builtins.property
        def s3_content_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.S3ContentLocationProperty"]]:
            '''The location of the custom artifacts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-customartifactconfiguration.html#cfn-kinesisanalyticsv2-application-customartifactconfiguration-s3contentlocation
            '''
            result = self._values.get("s3_content_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.S3ContentLocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomArtifactConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.DeployAsApplicationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_content_location": "s3ContentLocation"},
    )
    class DeployAsApplicationConfigurationProperty:
        def __init__(
            self,
            *,
            s3_content_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.S3ContentBaseLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The information required to deploy a Kinesis Data Analytics Studio notebook as an application with durable state.

            :param s3_content_location: The description of an Amazon S3 object that contains the Amazon Data Analytics application, including the Amazon Resource Name (ARN) of the S3 bucket, the name of the Amazon S3 object that contains the data, and the version number of the Amazon S3 object that contains the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-deployasapplicationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                deploy_as_application_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.DeployAsApplicationConfigurationProperty(
                    s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentBaseLocationProperty(
                        base_path="basePath",
                        bucket_arn="bucketArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f07e5019f63a03dd81c792b8505d1b7113b20e96e6abe55a683d908bfaece8ee)
                check_type(argname="argument s3_content_location", value=s3_content_location, expected_type=type_hints["s3_content_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_content_location is not None:
                self._values["s3_content_location"] = s3_content_location

        @builtins.property
        def s3_content_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.S3ContentBaseLocationProperty"]]:
            '''The description of an Amazon S3 object that contains the Amazon Data Analytics application, including the Amazon Resource Name (ARN) of the S3 bucket, the name of the Amazon S3 object that contains the data, and the version number of the Amazon S3 object that contains the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-deployasapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-deployasapplicationconfiguration-s3contentlocation
            '''
            result = self._values.get("s3_content_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.S3ContentBaseLocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeployAsApplicationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.EnvironmentPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"property_groups": "propertyGroups"},
    )
    class EnvironmentPropertiesProperty:
        def __init__(
            self,
            *,
            property_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.PropertyGroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Describes execution properties for a Managed Service for Apache Flink application.

            :param property_groups: Describes the execution property groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-environmentproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                environment_properties_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.EnvironmentPropertiesProperty(
                    property_groups=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.PropertyGroupProperty(
                        property_group_id="propertyGroupId",
                        property_map={
                            "property_map_key": "propertyMap"
                        }
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b5161c95acde982e6829d227ae486f22b5580674a5f03e8e53c8401fa5ce3230)
                check_type(argname="argument property_groups", value=property_groups, expected_type=type_hints["property_groups"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if property_groups is not None:
                self._values["property_groups"] = property_groups

        @builtins.property
        def property_groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.PropertyGroupProperty"]]]]:
            '''Describes the execution property groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-environmentproperties.html#cfn-kinesisanalyticsv2-application-environmentproperties-propertygroups
            '''
            result = self._values.get("property_groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.PropertyGroupProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.FlinkApplicationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "checkpoint_configuration": "checkpointConfiguration",
            "monitoring_configuration": "monitoringConfiguration",
            "parallelism_configuration": "parallelismConfiguration",
        },
    )
    class FlinkApplicationConfigurationProperty:
        def __init__(
            self,
            *,
            checkpoint_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.CheckpointConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.MonitoringConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parallelism_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ParallelismConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes configuration parameters for a Managed Service for Apache Flink application or a Studio notebook.

            :param checkpoint_configuration: Describes an application's checkpointing configuration. Checkpointing is the process of persisting application state for fault tolerance. For more information, see `Checkpoints for Fault Tolerance <https://docs.aws.amazon.com/https://ci.apache.org/projects/flink/flink-docs-release-1.8/concepts/programming-model.html#checkpoints-for-fault-tolerance>`_ in the `Apache Flink Documentation <https://docs.aws.amazon.com/https://ci.apache.org/projects/flink/flink-docs-release-1.8/>`_ .
            :param monitoring_configuration: Describes configuration parameters for Amazon CloudWatch logging for an application.
            :param parallelism_configuration: Describes parameters for how an application executes multiple tasks simultaneously.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-flinkapplicationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                flink_application_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.FlinkApplicationConfigurationProperty(
                    checkpoint_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CheckpointConfigurationProperty(
                        checkpointing_enabled=False,
                        checkpoint_interval=123,
                        configuration_type="configurationType",
                        min_pause_between_checkpoints=123
                    ),
                    monitoring_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MonitoringConfigurationProperty(
                        configuration_type="configurationType",
                        log_level="logLevel",
                        metrics_level="metricsLevel"
                    ),
                    parallelism_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ParallelismConfigurationProperty(
                        auto_scaling_enabled=False,
                        configuration_type="configurationType",
                        parallelism=123,
                        parallelism_per_kpu=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83f092681c093bbd340f680e687fb13e9d60cda37fd43b43a9371afbbd172b7d)
                check_type(argname="argument checkpoint_configuration", value=checkpoint_configuration, expected_type=type_hints["checkpoint_configuration"])
                check_type(argname="argument monitoring_configuration", value=monitoring_configuration, expected_type=type_hints["monitoring_configuration"])
                check_type(argname="argument parallelism_configuration", value=parallelism_configuration, expected_type=type_hints["parallelism_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if checkpoint_configuration is not None:
                self._values["checkpoint_configuration"] = checkpoint_configuration
            if monitoring_configuration is not None:
                self._values["monitoring_configuration"] = monitoring_configuration
            if parallelism_configuration is not None:
                self._values["parallelism_configuration"] = parallelism_configuration

        @builtins.property
        def checkpoint_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CheckpointConfigurationProperty"]]:
            '''Describes an application's checkpointing configuration.

            Checkpointing is the process of persisting application state for fault tolerance. For more information, see `Checkpoints for Fault Tolerance <https://docs.aws.amazon.com/https://ci.apache.org/projects/flink/flink-docs-release-1.8/concepts/programming-model.html#checkpoints-for-fault-tolerance>`_ in the `Apache Flink Documentation <https://docs.aws.amazon.com/https://ci.apache.org/projects/flink/flink-docs-release-1.8/>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-flinkapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-flinkapplicationconfiguration-checkpointconfiguration
            '''
            result = self._values.get("checkpoint_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CheckpointConfigurationProperty"]], result)

        @builtins.property
        def monitoring_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MonitoringConfigurationProperty"]]:
            '''Describes configuration parameters for Amazon CloudWatch logging for an application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-flinkapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-flinkapplicationconfiguration-monitoringconfiguration
            '''
            result = self._values.get("monitoring_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MonitoringConfigurationProperty"]], result)

        @builtins.property
        def parallelism_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ParallelismConfigurationProperty"]]:
            '''Describes parameters for how an application executes multiple tasks simultaneously.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-flinkapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-flinkapplicationconfiguration-parallelismconfiguration
            '''
            result = self._values.get("parallelism_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ParallelismConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlinkApplicationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.FlinkRunConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"allow_non_restored_state": "allowNonRestoredState"},
    )
    class FlinkRunConfigurationProperty:
        def __init__(
            self,
            *,
            allow_non_restored_state: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Describes the starting parameters for a Managed Service for Apache Flink application.

            :param allow_non_restored_state: When restoring from a snapshot, specifies whether the runtime is allowed to skip a state that cannot be mapped to the new program. This will happen if the program is updated between snapshots to remove stateful parameters, and state data in the snapshot no longer corresponds to valid application data. For more information, see `Allowing Non-Restored State <https://docs.aws.amazon.com/https://nightlies.apache.org/flink/flink-docs-master/docs/ops/state/savepoints/#allowing-non-restored-state>`_ in the `Apache Flink documentation <https://docs.aws.amazon.com/https://nightlies.apache.org/flink/flink-docs-master>`_ . .. epigraph:: This value defaults to ``false`` . If you update your application without specifying this parameter, ``AllowNonRestoredState`` will be set to ``false`` , even if it was previously set to ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-flinkrunconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                flink_run_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.FlinkRunConfigurationProperty(
                    allow_non_restored_state=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3516b51a93a0d68213ff4f96465461c5b493a448aea2bd0fdead54d27ef194ca)
                check_type(argname="argument allow_non_restored_state", value=allow_non_restored_state, expected_type=type_hints["allow_non_restored_state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_non_restored_state is not None:
                self._values["allow_non_restored_state"] = allow_non_restored_state

        @builtins.property
        def allow_non_restored_state(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When restoring from a snapshot, specifies whether the runtime is allowed to skip a state that cannot be mapped to the new program.

            This will happen if the program is updated between snapshots to remove stateful parameters, and state data in the snapshot no longer corresponds to valid application data. For more information, see `Allowing Non-Restored State <https://docs.aws.amazon.com/https://nightlies.apache.org/flink/flink-docs-master/docs/ops/state/savepoints/#allowing-non-restored-state>`_ in the `Apache Flink documentation <https://docs.aws.amazon.com/https://nightlies.apache.org/flink/flink-docs-master>`_ .
            .. epigraph::

               This value defaults to ``false`` . If you update your application without specifying this parameter, ``AllowNonRestoredState`` will be set to ``false`` , even if it was previously set to ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-flinkrunconfiguration.html#cfn-kinesisanalyticsv2-application-flinkrunconfiguration-allownonrestoredstate
            '''
            result = self._values.get("allow_non_restored_state")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlinkRunConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.GlueDataCatalogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"database_arn": "databaseArn"},
    )
    class GlueDataCatalogConfigurationProperty:
        def __init__(
            self,
            *,
            database_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration of the Glue Data Catalog that you use for Apache Flink SQL queries and table API transforms that you write in an application.

            :param database_arn: The Amazon Resource Name (ARN) of the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-gluedatacatalogconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                glue_data_catalog_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.GlueDataCatalogConfigurationProperty(
                    database_arn="databaseArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__431edcad089d3f41c7ba46c2607e03c9a0f4b4d124896a9d4915a05974c7dcca)
                check_type(argname="argument database_arn", value=database_arn, expected_type=type_hints["database_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_arn is not None:
                self._values["database_arn"] = database_arn

        @builtins.property
        def database_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-gluedatacatalogconfiguration.html#cfn-kinesisanalyticsv2-application-gluedatacatalogconfiguration-databasearn
            '''
            result = self._values.get("database_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlueDataCatalogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.InputLambdaProcessorProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn"},
    )
    class InputLambdaProcessorProperty:
        def __init__(
            self,
            *,
            resource_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that contains the Amazon Resource Name (ARN) of the Amazon Lambda function that is used to preprocess records in the stream in a SQL-based Kinesis Data Analytics application.

            :param resource_arn: The ARN of the Amazon Lambda function that operates on records in the stream. .. epigraph:: To specify an earlier version of the Lambda function than the latest, include the Lambda function version in the Lambda function ARN. For more information about Lambda ARNs, see `Example ARNs: Amazon Lambda <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html#arn-syntax-lambda>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputlambdaprocessor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                input_lambda_processor_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputLambdaProcessorProperty(
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77e1e82bbf698f733ea0349809866136319a6f4c5e888506f36e8a4c8fb40937)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Amazon Lambda function that operates on records in the stream.

            .. epigraph::

               To specify an earlier version of the Lambda function than the latest, include the Lambda function version in the Lambda function ARN. For more information about Lambda ARNs, see `Example ARNs: Amazon Lambda <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html#arn-syntax-lambda>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputlambdaprocessor.html#cfn-kinesisanalyticsv2-application-inputlambdaprocessor-resourcearn
            '''
            result = self._values.get("resource_arn")
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.InputParallelismProperty",
        jsii_struct_bases=[],
        name_mapping={"count": "count"},
    )
    class InputParallelismProperty:
        def __init__(self, *, count: typing.Optional[jsii.Number] = None) -> None:
            '''For a SQL-based Kinesis Data Analytics application, describes the number of in-application streams to create for a given streaming source.

            :param count: The number of in-application streams to create.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputparallelism.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                input_parallelism_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputParallelismProperty(
                    count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f3d8dd47fb6919466212700b27a78556166641e1603279be73be43925ca2fa4)
                check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if count is not None:
                self._values["count"] = count

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            '''The number of in-application streams to create.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputparallelism.html#cfn-kinesisanalyticsv2-application-inputparallelism-count
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.InputProcessingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"input_lambda_processor": "inputLambdaProcessor"},
    )
    class InputProcessingConfigurationProperty:
        def __init__(
            self,
            *,
            input_lambda_processor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.InputLambdaProcessorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''For an SQL-based Amazon Kinesis Data Analytics application, describes a processor that is used to preprocess the records in the stream before being processed by your application code.

            Currently, the only input processor available is `Amazon Lambda <https://docs.aws.amazon.com/lambda/>`_ .

            :param input_lambda_processor: The `InputLambdaProcessor <https://docs.aws.amazon.com/managed-flink/latest/apiv2/API_InputLambdaProcessor.html>`_ that is used to preprocess the records in the stream before being processed by your application code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputprocessingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                input_processing_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputProcessingConfigurationProperty(
                    input_lambda_processor=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputLambdaProcessorProperty(
                        resource_arn="resourceArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca14663ee4e02e3b37fe8527fd1b21ccb6b1d78e51f037971bd404e21332a7b8)
                check_type(argname="argument input_lambda_processor", value=input_lambda_processor, expected_type=type_hints["input_lambda_processor"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_lambda_processor is not None:
                self._values["input_lambda_processor"] = input_lambda_processor

        @builtins.property
        def input_lambda_processor(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputLambdaProcessorProperty"]]:
            '''The `InputLambdaProcessor <https://docs.aws.amazon.com/managed-flink/latest/apiv2/API_InputLambdaProcessor.html>`_ that is used to preprocess the records in the stream before being processed by your application code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputprocessingconfiguration.html#cfn-kinesisanalyticsv2-application-inputprocessingconfiguration-inputlambdaprocessor
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.InputProperty",
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
            '''When you configure the application input for a SQL-based Kinesis Data Analytics application, you specify the streaming source, the in-application stream name that is created, and the mapping between the two.

            :param input_parallelism: Describes the number of in-application streams to create.
            :param input_processing_configuration: The `InputProcessingConfiguration <https://docs.aws.amazon.com/managed-flink/latest/apiv2/API_InputProcessingConfiguration.html>`_ for the input. An input processor transforms records as they are received from the stream, before the application's SQL code executes. Currently, the only input processing configuration available is `InputLambdaProcessor <https://docs.aws.amazon.com/managed-flink/latest/apiv2/API_InputLambdaProcessor.html>`_ .
            :param input_schema: Describes the format of the data in the streaming source, and how each data element maps to corresponding columns in the in-application stream that is being created. Also used to describe the format of the reference data source.
            :param kinesis_firehose_input: If the streaming source is an Amazon Kinesis Data Firehose delivery stream, identifies the delivery stream's ARN.
            :param kinesis_streams_input: If the streaming source is an Amazon Kinesis data stream, identifies the stream's Amazon Resource Name (ARN).
            :param name_prefix: The name prefix to use when creating an in-application stream. Suppose that you specify a prefix " ``MyInApplicationStream`` ." Kinesis Data Analytics then creates one or more (as per the ``InputParallelism`` count you specified) in-application streams with the names " ``MyInApplicationStream_001`` ," " ``MyInApplicationStream_002`` ," and so on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                input_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputProperty(
                    input_parallelism=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputParallelismProperty(
                        count=123
                    ),
                    input_processing_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputProcessingConfigurationProperty(
                        input_lambda_processor=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputLambdaProcessorProperty(
                            resource_arn="resourceArn"
                        )
                    ),
                    input_schema=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputSchemaProperty(
                        record_columns=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RecordColumnProperty(
                            mapping="mapping",
                            name="name",
                            sql_type="sqlType"
                        )],
                        record_encoding="recordEncoding",
                        record_format=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RecordFormatProperty(
                            mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MappingParametersProperty(
                                csv_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                                    record_column_delimiter="recordColumnDelimiter",
                                    record_row_delimiter="recordRowDelimiter"
                                ),
                                json_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                                    record_row_path="recordRowPath"
                                )
                            ),
                            record_format_type="recordFormatType"
                        )
                    ),
                    kinesis_firehose_input=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.KinesisFirehoseInputProperty(
                        resource_arn="resourceArn"
                    ),
                    kinesis_streams_input=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.KinesisStreamsInputProperty(
                        resource_arn="resourceArn"
                    ),
                    name_prefix="namePrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49e969fd1348039079eac20594906cd460629ae9dc6e091b0ebefc5ab0e2700f)
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

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-inputparallelism
            '''
            result = self._values.get("input_parallelism")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputParallelismProperty"]], result)

        @builtins.property
        def input_processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputProcessingConfigurationProperty"]]:
            '''The `InputProcessingConfiguration <https://docs.aws.amazon.com/managed-flink/latest/apiv2/API_InputProcessingConfiguration.html>`_ for the input. An input processor transforms records as they are received from the stream, before the application's SQL code executes. Currently, the only input processing configuration available is `InputLambdaProcessor <https://docs.aws.amazon.com/managed-flink/latest/apiv2/API_InputLambdaProcessor.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-inputprocessingconfiguration
            '''
            result = self._values.get("input_processing_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputProcessingConfigurationProperty"]], result)

        @builtins.property
        def input_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputSchemaProperty"]]:
            '''Describes the format of the data in the streaming source, and how each data element maps to corresponding columns in the in-application stream that is being created.

            Also used to describe the format of the reference data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-inputschema
            '''
            result = self._values.get("input_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputSchemaProperty"]], result)

        @builtins.property
        def kinesis_firehose_input(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.KinesisFirehoseInputProperty"]]:
            '''If the streaming source is an Amazon Kinesis Data Firehose delivery stream, identifies the delivery stream's ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-kinesisfirehoseinput
            '''
            result = self._values.get("kinesis_firehose_input")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.KinesisFirehoseInputProperty"]], result)

        @builtins.property
        def kinesis_streams_input(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.KinesisStreamsInputProperty"]]:
            '''If the streaming source is an Amazon Kinesis data stream, identifies the stream's Amazon Resource Name (ARN).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-kinesisstreamsinput
            '''
            result = self._values.get("kinesis_streams_input")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.KinesisStreamsInputProperty"]], result)

        @builtins.property
        def name_prefix(self) -> typing.Optional[builtins.str]:
            '''The name prefix to use when creating an in-application stream.

            Suppose that you specify a prefix " ``MyInApplicationStream`` ." Kinesis Data Analytics then creates one or more (as per the ``InputParallelism`` count you specified) in-application streams with the names " ``MyInApplicationStream_001`` ," " ``MyInApplicationStream_002`` ," and so on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-nameprefix
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.InputSchemaProperty",
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
            '''For a SQL-based Kinesis Data Analytics application, describes the format of the data in the streaming source, and how each data element maps to corresponding columns created in the in-application stream.

            :param record_columns: A list of ``RecordColumn`` objects.
            :param record_encoding: Specifies the encoding of the records in the streaming source. For example, UTF-8.
            :param record_format: Specifies the format of the records on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                input_schema_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputSchemaProperty(
                    record_columns=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RecordColumnProperty(
                        mapping="mapping",
                        name="name",
                        sql_type="sqlType"
                    )],
                    record_encoding="recordEncoding",
                    record_format=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RecordFormatProperty(
                        mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MappingParametersProperty(
                            csv_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                                record_column_delimiter="recordColumnDelimiter",
                                record_row_delimiter="recordRowDelimiter"
                            ),
                            json_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                                record_row_path="recordRowPath"
                            )
                        ),
                        record_format_type="recordFormatType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a9ca27d8167376bba90150d94c58a654e3692c3e73d0e88d59fb8171de003492)
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

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputschema.html#cfn-kinesisanalyticsv2-application-inputschema-recordcolumns
            '''
            result = self._values.get("record_columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.RecordColumnProperty"]]]], result)

        @builtins.property
        def record_encoding(self) -> typing.Optional[builtins.str]:
            '''Specifies the encoding of the records in the streaming source.

            For example, UTF-8.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputschema.html#cfn-kinesisanalyticsv2-application-inputschema-recordencoding
            '''
            result = self._values.get("record_encoding")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_format(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.RecordFormatProperty"]]:
            '''Specifies the format of the records on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputschema.html#cfn-kinesisanalyticsv2-application-inputschema-recordformat
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"record_row_path": "recordRowPath"},
    )
    class JSONMappingParametersProperty:
        def __init__(
            self,
            *,
            record_row_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''For a SQL-based Kinesis Data Analytics application, provides additional mapping information when JSON is the record format on the streaming source.

            :param record_row_path: The path to the top-level parent that contains the records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-jsonmappingparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                j_sONMapping_parameters_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                    record_row_path="recordRowPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c89d2f65d8167984851a5c0d310ef85f7ce6bbf0e8ac745efea02f3f77a4363)
                check_type(argname="argument record_row_path", value=record_row_path, expected_type=type_hints["record_row_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if record_row_path is not None:
                self._values["record_row_path"] = record_row_path

        @builtins.property
        def record_row_path(self) -> typing.Optional[builtins.str]:
            '''The path to the top-level parent that contains the records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-jsonmappingparameters.html#cfn-kinesisanalyticsv2-application-jsonmappingparameters-recordrowpath
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.KinesisFirehoseInputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn"},
    )
    class KinesisFirehoseInputProperty:
        def __init__(
            self,
            *,
            resource_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''For a SQL-based Kinesis Data Analytics application, identifies a Kinesis Data Firehose delivery stream as the streaming source.

            You provide the delivery stream's Amazon Resource Name (ARN).

            :param resource_arn: The Amazon Resource Name (ARN) of the delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-kinesisfirehoseinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                kinesis_firehose_input_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.KinesisFirehoseInputProperty(
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e6d9c243bf45cb70cf82e50d1f8c3bb162be7ff565211e81eb5f2c412c0e7f3)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-kinesisfirehoseinput.html#cfn-kinesisanalyticsv2-application-kinesisfirehoseinput-resourcearn
            '''
            result = self._values.get("resource_arn")
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.KinesisStreamsInputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn"},
    )
    class KinesisStreamsInputProperty:
        def __init__(
            self,
            *,
            resource_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Identifies a Kinesis data stream as the streaming source.

            You provide the stream's Amazon Resource Name (ARN).

            :param resource_arn: The ARN of the input Kinesis data stream to read.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-kinesisstreamsinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                kinesis_streams_input_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.KinesisStreamsInputProperty(
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab9a4c3149ea7f4e17e88671b295e8b1657f60e9647c1d08bc36562c16ee83f9)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the input Kinesis data stream to read.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-kinesisstreamsinput.html#cfn-kinesisanalyticsv2-application-kinesisstreamsinput-resourcearn
            '''
            result = self._values.get("resource_arn")
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.MappingParametersProperty",
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
            '''When you configure a SQL-based Kinesis Data Analytics application's input at the time of creating or updating an application, provides additional mapping information specific to the record format (such as JSON, CSV, or record fields delimited by some delimiter) on the streaming source.

            :param csv_mapping_parameters: Provides additional mapping information when the record format uses delimiters (for example, CSV).
            :param json_mapping_parameters: Provides additional mapping information when JSON is the record format on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-mappingparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                mapping_parameters_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MappingParametersProperty(
                    csv_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                        record_column_delimiter="recordColumnDelimiter",
                        record_row_delimiter="recordRowDelimiter"
                    ),
                    json_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                        record_row_path="recordRowPath"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc92baae1770cfba392206657ec11fb5f8540f654ba3d23d49bb2d3366f913c5)
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

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-mappingparameters.html#cfn-kinesisanalyticsv2-application-mappingparameters-csvmappingparameters
            '''
            result = self._values.get("csv_mapping_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CSVMappingParametersProperty"]], result)

        @builtins.property
        def json_mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.JSONMappingParametersProperty"]]:
            '''Provides additional mapping information when JSON is the record format on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-mappingparameters.html#cfn-kinesisanalyticsv2-application-mappingparameters-jsonmappingparameters
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.MavenReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "artifact_id": "artifactId",
            "group_id": "groupId",
            "version": "version",
        },
    )
    class MavenReferenceProperty:
        def __init__(
            self,
            *,
            artifact_id: typing.Optional[builtins.str] = None,
            group_id: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The information required to specify a Maven reference.

            You can use Maven references to specify dependency JAR files.

            :param artifact_id: The artifact ID of the Maven reference.
            :param group_id: The group ID of the Maven reference.
            :param version: The version of the Maven reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-mavenreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                maven_reference_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MavenReferenceProperty(
                    artifact_id="artifactId",
                    group_id="groupId",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b43bf72c87ed4d15e028e22a771b5501dd2cac46ee85aace3a13136996ec58d8)
                check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
                check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if artifact_id is not None:
                self._values["artifact_id"] = artifact_id
            if group_id is not None:
                self._values["group_id"] = group_id
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def artifact_id(self) -> typing.Optional[builtins.str]:
            '''The artifact ID of the Maven reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-mavenreference.html#cfn-kinesisanalyticsv2-application-mavenreference-artifactid
            '''
            result = self._values.get("artifact_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_id(self) -> typing.Optional[builtins.str]:
            '''The group ID of the Maven reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-mavenreference.html#cfn-kinesisanalyticsv2-application-mavenreference-groupid
            '''
            result = self._values.get("group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version of the Maven reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-mavenreference.html#cfn-kinesisanalyticsv2-application-mavenreference-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MavenReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.MonitoringConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration_type": "configurationType",
            "log_level": "logLevel",
            "metrics_level": "metricsLevel",
        },
    )
    class MonitoringConfigurationProperty:
        def __init__(
            self,
            *,
            configuration_type: typing.Optional[builtins.str] = None,
            log_level: typing.Optional[builtins.str] = None,
            metrics_level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes configuration parameters for Amazon CloudWatch logging for a Java-based Kinesis Data Analytics application.

            For more information about CloudWatch logging, see `Monitoring <https://docs.aws.amazon.com/managed-flink/latest/java/monitoring-overview>`_ .

            :param configuration_type: Describes whether to use the default CloudWatch logging configuration for an application. You must set this property to ``CUSTOM`` in order to set the ``LogLevel`` or ``MetricsLevel`` parameters.
            :param log_level: Describes the verbosity of the CloudWatch Logs for an application.
            :param metrics_level: Describes the granularity of the CloudWatch Logs for an application. The ``Parallelism`` level is not recommended for applications with a Parallelism over 64 due to excessive costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-monitoringconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                monitoring_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MonitoringConfigurationProperty(
                    configuration_type="configurationType",
                    log_level="logLevel",
                    metrics_level="metricsLevel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bb9bb6ba72074e666b568d0cbefe508b4aa6bc77d83e18d0cc3deb0c8af2b131)
                check_type(argname="argument configuration_type", value=configuration_type, expected_type=type_hints["configuration_type"])
                check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
                check_type(argname="argument metrics_level", value=metrics_level, expected_type=type_hints["metrics_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configuration_type is not None:
                self._values["configuration_type"] = configuration_type
            if log_level is not None:
                self._values["log_level"] = log_level
            if metrics_level is not None:
                self._values["metrics_level"] = metrics_level

        @builtins.property
        def configuration_type(self) -> typing.Optional[builtins.str]:
            '''Describes whether to use the default CloudWatch logging configuration for an application.

            You must set this property to ``CUSTOM`` in order to set the ``LogLevel`` or ``MetricsLevel`` parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-monitoringconfiguration.html#cfn-kinesisanalyticsv2-application-monitoringconfiguration-configurationtype
            '''
            result = self._values.get("configuration_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_level(self) -> typing.Optional[builtins.str]:
            '''Describes the verbosity of the CloudWatch Logs for an application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-monitoringconfiguration.html#cfn-kinesisanalyticsv2-application-monitoringconfiguration-loglevel
            '''
            result = self._values.get("log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metrics_level(self) -> typing.Optional[builtins.str]:
            '''Describes the granularity of the CloudWatch Logs for an application.

            The ``Parallelism`` level is not recommended for applications with a Parallelism over 64 due to excessive costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-monitoringconfiguration.html#cfn-kinesisanalyticsv2-application-monitoringconfiguration-metricslevel
            '''
            result = self._values.get("metrics_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MonitoringConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.ParallelismConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_scaling_enabled": "autoScalingEnabled",
            "configuration_type": "configurationType",
            "parallelism": "parallelism",
            "parallelism_per_kpu": "parallelismPerKpu",
        },
    )
    class ParallelismConfigurationProperty:
        def __init__(
            self,
            *,
            auto_scaling_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            configuration_type: typing.Optional[builtins.str] = None,
            parallelism: typing.Optional[jsii.Number] = None,
            parallelism_per_kpu: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes parameters for how a Flink-based Kinesis Data Analytics application executes multiple tasks simultaneously.

            For more information about parallelism, see `Parallel Execution <https://docs.aws.amazon.com/https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/execution/parallel/>`_ in the `Apache Flink Documentation <https://docs.aws.amazon.com/https://nightlies.apache.org/flink/flink-docs-master>`_ .

            :param auto_scaling_enabled: Describes whether the Managed Service for Apache Flink service can increase the parallelism of the application in response to increased throughput.
            :param configuration_type: Describes whether the application uses the default parallelism for the Managed Service for Apache Flink service. You must set this property to ``CUSTOM`` in order to change your application's ``AutoScalingEnabled`` , ``Parallelism`` , or ``ParallelismPerKPU`` properties.
            :param parallelism: Describes the initial number of parallel tasks that a Java-based Kinesis Data Analytics application can perform. The Kinesis Data Analytics service can increase this number automatically if `ParallelismConfiguration:AutoScalingEnabled <https://docs.aws.amazon.com/managed-flink/latest/apiv2/API_ParallelismConfiguration.html#kinesisanalytics-Type-ParallelismConfiguration-AutoScalingEnabled.html>`_ is set to ``true`` .
            :param parallelism_per_kpu: Describes the number of parallel tasks that a Java-based Kinesis Data Analytics application can perform per Kinesis Processing Unit (KPU) used by the application. For more information about KPUs, see `Amazon Kinesis Data Analytics Pricing <https://docs.aws.amazon.com/kinesis/data-analytics/pricing/>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                parallelism_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ParallelismConfigurationProperty(
                    auto_scaling_enabled=False,
                    configuration_type="configurationType",
                    parallelism=123,
                    parallelism_per_kpu=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ffeeecf839baccd0c19a12956247b2502c6f83cc633e58f5f88b2f4c73f77bbc)
                check_type(argname="argument auto_scaling_enabled", value=auto_scaling_enabled, expected_type=type_hints["auto_scaling_enabled"])
                check_type(argname="argument configuration_type", value=configuration_type, expected_type=type_hints["configuration_type"])
                check_type(argname="argument parallelism", value=parallelism, expected_type=type_hints["parallelism"])
                check_type(argname="argument parallelism_per_kpu", value=parallelism_per_kpu, expected_type=type_hints["parallelism_per_kpu"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_scaling_enabled is not None:
                self._values["auto_scaling_enabled"] = auto_scaling_enabled
            if configuration_type is not None:
                self._values["configuration_type"] = configuration_type
            if parallelism is not None:
                self._values["parallelism"] = parallelism
            if parallelism_per_kpu is not None:
                self._values["parallelism_per_kpu"] = parallelism_per_kpu

        @builtins.property
        def auto_scaling_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Describes whether the Managed Service for Apache Flink service can increase the parallelism of the application in response to increased throughput.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html#cfn-kinesisanalyticsv2-application-parallelismconfiguration-autoscalingenabled
            '''
            result = self._values.get("auto_scaling_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def configuration_type(self) -> typing.Optional[builtins.str]:
            '''Describes whether the application uses the default parallelism for the Managed Service for Apache Flink service.

            You must set this property to ``CUSTOM`` in order to change your application's ``AutoScalingEnabled`` , ``Parallelism`` , or ``ParallelismPerKPU`` properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html#cfn-kinesisanalyticsv2-application-parallelismconfiguration-configurationtype
            '''
            result = self._values.get("configuration_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parallelism(self) -> typing.Optional[jsii.Number]:
            '''Describes the initial number of parallel tasks that a Java-based Kinesis Data Analytics application can perform.

            The Kinesis Data Analytics service can increase this number automatically if `ParallelismConfiguration:AutoScalingEnabled <https://docs.aws.amazon.com/managed-flink/latest/apiv2/API_ParallelismConfiguration.html#kinesisanalytics-Type-ParallelismConfiguration-AutoScalingEnabled.html>`_ is set to ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html#cfn-kinesisanalyticsv2-application-parallelismconfiguration-parallelism
            '''
            result = self._values.get("parallelism")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def parallelism_per_kpu(self) -> typing.Optional[jsii.Number]:
            '''Describes the number of parallel tasks that a Java-based Kinesis Data Analytics application can perform per Kinesis Processing Unit (KPU) used by the application.

            For more information about KPUs, see `Amazon Kinesis Data Analytics Pricing <https://docs.aws.amazon.com/kinesis/data-analytics/pricing/>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html#cfn-kinesisanalyticsv2-application-parallelismconfiguration-parallelismperkpu
            '''
            result = self._values.get("parallelism_per_kpu")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParallelismConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.PropertyGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "property_group_id": "propertyGroupId",
            "property_map": "propertyMap",
        },
    )
    class PropertyGroupProperty:
        def __init__(
            self,
            *,
            property_group_id: typing.Optional[builtins.str] = None,
            property_map: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Property key-value pairs passed into an application.

            :param property_group_id: Describes the key of an application execution property key-value pair.
            :param property_map: Describes the value of an application execution property key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-propertygroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                property_group_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.PropertyGroupProperty(
                    property_group_id="propertyGroupId",
                    property_map={
                        "property_map_key": "propertyMap"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1afff2342c9f7de19d23a87e2de2365a12bda8a09033c1a7e9e45b49cf735517)
                check_type(argname="argument property_group_id", value=property_group_id, expected_type=type_hints["property_group_id"])
                check_type(argname="argument property_map", value=property_map, expected_type=type_hints["property_map"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if property_group_id is not None:
                self._values["property_group_id"] = property_group_id
            if property_map is not None:
                self._values["property_map"] = property_map

        @builtins.property
        def property_group_id(self) -> typing.Optional[builtins.str]:
            '''Describes the key of an application execution property key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-propertygroup.html#cfn-kinesisanalyticsv2-application-propertygroup-propertygroupid
            '''
            result = self._values.get("property_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_map(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Describes the value of an application execution property key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-propertygroup.html#cfn-kinesisanalyticsv2-application-propertygroup-propertymap
            '''
            result = self._values.get("property_map")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.RecordColumnProperty",
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
            '''For a SQL-based Kinesis Data Analytics application, describes the mapping of each data element in the streaming source to the corresponding column in the in-application stream.

            Also used to describe the format of the reference data source.

            :param mapping: A reference to the data element in the streaming input or the reference data source.
            :param name: The name of the column that is created in the in-application input stream or reference table.
            :param sql_type: The type of column created in the in-application input stream or reference table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordcolumn.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                record_column_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RecordColumnProperty(
                    mapping="mapping",
                    name="name",
                    sql_type="sqlType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1771b5ed12c4ab61f86d20c296c8f537403fa03dfe73cddfe9fb3f6d5fd56f9a)
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
            '''A reference to the data element in the streaming input or the reference data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordcolumn.html#cfn-kinesisanalyticsv2-application-recordcolumn-mapping
            '''
            result = self._values.get("mapping")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the column that is created in the in-application input stream or reference table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordcolumn.html#cfn-kinesisanalyticsv2-application-recordcolumn-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sql_type(self) -> typing.Optional[builtins.str]:
            '''The type of column created in the in-application input stream or reference table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordcolumn.html#cfn-kinesisanalyticsv2-application-recordcolumn-sqltype
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.RecordFormatProperty",
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
            '''For a SQL-based Kinesis Data Analytics application, describes the record format and relevant mapping information that should be applied to schematize the records on the stream.

            :param mapping_parameters: When you configure application input at the time of creating or updating an application, provides additional mapping information specific to the record format (such as JSON, CSV, or record fields delimited by some delimiter) on the streaming source.
            :param record_format_type: The type of record format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordformat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                record_format_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RecordFormatProperty(
                    mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MappingParametersProperty(
                        csv_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                            record_column_delimiter="recordColumnDelimiter",
                            record_row_delimiter="recordRowDelimiter"
                        ),
                        json_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                            record_row_path="recordRowPath"
                        )
                    ),
                    record_format_type="recordFormatType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__64ef32af36f2b89eca79ea2492a48093a1f2885d4c645dbc06417ff816f0b483)
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
            '''When you configure application input at the time of creating or updating an application, provides additional mapping information specific to the record format (such as JSON, CSV, or record fields delimited by some delimiter) on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordformat.html#cfn-kinesisanalyticsv2-application-recordformat-mappingparameters
            '''
            result = self._values.get("mapping_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MappingParametersProperty"]], result)

        @builtins.property
        def record_format_type(self) -> typing.Optional[builtins.str]:
            '''The type of record format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordformat.html#cfn-kinesisanalyticsv2-application-recordformat-recordformattype
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.RunConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_restore_configuration": "applicationRestoreConfiguration",
            "flink_run_configuration": "flinkRunConfiguration",
        },
    )
    class RunConfigurationProperty:
        def __init__(
            self,
            *,
            application_restore_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ApplicationRestoreConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            flink_run_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.FlinkRunConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the starting parameters for an Managed Service for Apache Flink application.

            :param application_restore_configuration: Describes the restore behavior of a restarting application.
            :param flink_run_configuration: Describes the starting parameters for a Managed Service for Apache Flink application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-runconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                run_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RunConfigurationProperty(
                    application_restore_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ApplicationRestoreConfigurationProperty(
                        application_restore_type="applicationRestoreType",
                        snapshot_name="snapshotName"
                    ),
                    flink_run_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.FlinkRunConfigurationProperty(
                        allow_non_restored_state=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36c8b8cb10b2b67778955feeaf6f99d739d66de64472786e2e6e43ae76307730)
                check_type(argname="argument application_restore_configuration", value=application_restore_configuration, expected_type=type_hints["application_restore_configuration"])
                check_type(argname="argument flink_run_configuration", value=flink_run_configuration, expected_type=type_hints["flink_run_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_restore_configuration is not None:
                self._values["application_restore_configuration"] = application_restore_configuration
            if flink_run_configuration is not None:
                self._values["flink_run_configuration"] = flink_run_configuration

        @builtins.property
        def application_restore_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationRestoreConfigurationProperty"]]:
            '''Describes the restore behavior of a restarting application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-runconfiguration.html#cfn-kinesisanalyticsv2-application-runconfiguration-applicationrestoreconfiguration
            '''
            result = self._values.get("application_restore_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationRestoreConfigurationProperty"]], result)

        @builtins.property
        def flink_run_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.FlinkRunConfigurationProperty"]]:
            '''Describes the starting parameters for a Managed Service for Apache Flink application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-runconfiguration.html#cfn-kinesisanalyticsv2-application-runconfiguration-flinkrunconfiguration
            '''
            result = self._values.get("flink_run_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.FlinkRunConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.S3ContentBaseLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"base_path": "basePath", "bucket_arn": "bucketArn"},
    )
    class S3ContentBaseLocationProperty:
        def __init__(
            self,
            *,
            base_path: typing.Optional[builtins.str] = None,
            bucket_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The base location of the Amazon Data Analytics application.

            :param base_path: The base path for the S3 bucket.
            :param bucket_arn: The Amazon Resource Name (ARN) of the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentbaselocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                s3_content_base_location_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentBaseLocationProperty(
                    base_path="basePath",
                    bucket_arn="bucketArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d1b5668e5aba6ed7d6373dec1973bfc8e52da27faf662f47f6bee556950b2a0c)
                check_type(argname="argument base_path", value=base_path, expected_type=type_hints["base_path"])
                check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base_path is not None:
                self._values["base_path"] = base_path
            if bucket_arn is not None:
                self._values["bucket_arn"] = bucket_arn

        @builtins.property
        def base_path(self) -> typing.Optional[builtins.str]:
            '''The base path for the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentbaselocation.html#cfn-kinesisanalyticsv2-application-s3contentbaselocation-basepath
            '''
            result = self._values.get("base_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentbaselocation.html#cfn-kinesisanalyticsv2-application-s3contentbaselocation-bucketarn
            '''
            result = self._values.get("bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ContentBaseLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.S3ContentLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_arn": "bucketArn",
            "file_key": "fileKey",
            "object_version": "objectVersion",
        },
    )
    class S3ContentLocationProperty:
        def __init__(
            self,
            *,
            bucket_arn: typing.Optional[builtins.str] = None,
            file_key: typing.Optional[builtins.str] = None,
            object_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The location of an application or a custom artifact.

            :param bucket_arn: The Amazon Resource Name (ARN) for the S3 bucket containing the application code.
            :param file_key: The file key for the object containing the application code.
            :param object_version: The version of the object containing the application code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentlocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                s3_content_location_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentLocationProperty(
                    bucket_arn="bucketArn",
                    file_key="fileKey",
                    object_version="objectVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5b2aa33170a95a3f5cd8876a3b05323efa9e12347584c36cd85456e59ba7a0ad)
                check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
                check_type(argname="argument file_key", value=file_key, expected_type=type_hints["file_key"])
                check_type(argname="argument object_version", value=object_version, expected_type=type_hints["object_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_arn is not None:
                self._values["bucket_arn"] = bucket_arn
            if file_key is not None:
                self._values["file_key"] = file_key
            if object_version is not None:
                self._values["object_version"] = object_version

        @builtins.property
        def bucket_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the S3 bucket containing the application code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentlocation.html#cfn-kinesisanalyticsv2-application-s3contentlocation-bucketarn
            '''
            result = self._values.get("bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_key(self) -> typing.Optional[builtins.str]:
            '''The file key for the object containing the application code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentlocation.html#cfn-kinesisanalyticsv2-application-s3contentlocation-filekey
            '''
            result = self._values.get("file_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_version(self) -> typing.Optional[builtins.str]:
            '''The version of the object containing the application code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentlocation.html#cfn-kinesisanalyticsv2-application-s3contentlocation-objectversion
            '''
            result = self._values.get("object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ContentLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.SqlApplicationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"inputs": "inputs"},
    )
    class SqlApplicationConfigurationProperty:
        def __init__(
            self,
            *,
            inputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.InputProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Describes the inputs, outputs, and reference data sources for a SQL-based Kinesis Data Analytics application.

            :param inputs: The array of `Input <https://docs.aws.amazon.com/managed-flink/latest/apiv2/API_Input.html>`_ objects describing the input streams used by the application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-sqlapplicationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                sql_application_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.SqlApplicationConfigurationProperty(
                    inputs=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputProperty(
                        input_parallelism=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputParallelismProperty(
                            count=123
                        ),
                        input_processing_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputProcessingConfigurationProperty(
                            input_lambda_processor=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputLambdaProcessorProperty(
                                resource_arn="resourceArn"
                            )
                        ),
                        input_schema=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.InputSchemaProperty(
                            record_columns=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RecordColumnProperty(
                                mapping="mapping",
                                name="name",
                                sql_type="sqlType"
                            )],
                            record_encoding="recordEncoding",
                            record_format=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.RecordFormatProperty(
                                mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MappingParametersProperty(
                                    csv_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                                        record_column_delimiter="recordColumnDelimiter",
                                        record_row_delimiter="recordRowDelimiter"
                                    ),
                                    json_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                                        record_row_path="recordRowPath"
                                    )
                                ),
                                record_format_type="recordFormatType"
                            )
                        ),
                        kinesis_firehose_input=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.KinesisFirehoseInputProperty(
                            resource_arn="resourceArn"
                        ),
                        kinesis_streams_input=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.KinesisStreamsInputProperty(
                            resource_arn="resourceArn"
                        ),
                        name_prefix="namePrefix"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e79886d4436c2451eadc884c8eb3551d41816a2e1c158093de3e1188cf3e377b)
                check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if inputs is not None:
                self._values["inputs"] = inputs

        @builtins.property
        def inputs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputProperty"]]]]:
            '''The array of `Input <https://docs.aws.amazon.com/managed-flink/latest/apiv2/API_Input.html>`_ objects describing the input streams used by the application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-sqlapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-sqlapplicationconfiguration-inputs
            '''
            result = self._values.get("inputs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqlApplicationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.VpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigurationProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Describes the parameters of a VPC used by the application.

            :param security_group_ids: The array of `SecurityGroup <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_SecurityGroup.html>`_ IDs used by the VPC configuration.
            :param subnet_ids: The array of `Subnet <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_Subnet.html>`_ IDs used by the VPC configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-vpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                vpc_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.VpcConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fad722a5d9fdda46edddead14cd2908750f8345159e5eaf52d9ea3e905a07bbb)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The array of `SecurityGroup <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_SecurityGroup.html>`_ IDs used by the VPC configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-vpcconfiguration.html#cfn-kinesisanalyticsv2-application-vpcconfiguration-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The array of `Subnet <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_Subnet.html>`_ IDs used by the VPC configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-vpcconfiguration.html#cfn-kinesisanalyticsv2-application-vpcconfiguration-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.ZeppelinApplicationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_configuration": "catalogConfiguration",
            "custom_artifacts_configuration": "customArtifactsConfiguration",
            "deploy_as_application_configuration": "deployAsApplicationConfiguration",
            "monitoring_configuration": "monitoringConfiguration",
        },
    )
    class ZeppelinApplicationConfigurationProperty:
        def __init__(
            self,
            *,
            catalog_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.CatalogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            custom_artifacts_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.CustomArtifactConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            deploy_as_application_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.DeployAsApplicationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ZeppelinMonitoringConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration of a Kinesis Data Analytics Studio notebook.

            :param catalog_configuration: The Amazon Glue Data Catalog that you use in queries in a Kinesis Data Analytics Studio notebook.
            :param custom_artifacts_configuration: A list of ``CustomArtifactConfiguration`` objects.
            :param deploy_as_application_configuration: The information required to deploy a Kinesis Data Analytics Studio notebook as an application with durable state.
            :param monitoring_configuration: The monitoring configuration of a Kinesis Data Analytics Studio notebook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-zeppelinapplicationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                zeppelin_application_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ZeppelinApplicationConfigurationProperty(
                    catalog_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CatalogConfigurationProperty(
                        glue_data_catalog_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.GlueDataCatalogConfigurationProperty(
                            database_arn="databaseArn"
                        )
                    ),
                    custom_artifacts_configuration=[kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.CustomArtifactConfigurationProperty(
                        artifact_type="artifactType",
                        maven_reference=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.MavenReferenceProperty(
                            artifact_id="artifactId",
                            group_id="groupId",
                            version="version"
                        ),
                        s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentLocationProperty(
                            bucket_arn="bucketArn",
                            file_key="fileKey",
                            object_version="objectVersion"
                        )
                    )],
                    deploy_as_application_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.DeployAsApplicationConfigurationProperty(
                        s3_content_location=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.S3ContentBaseLocationProperty(
                            base_path="basePath",
                            bucket_arn="bucketArn"
                        )
                    ),
                    monitoring_configuration=kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ZeppelinMonitoringConfigurationProperty(
                        log_level="logLevel"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef73001930066f0c2b5eb2d6fc580040cf8dfe7063876ad817d1a1998454e8f3)
                check_type(argname="argument catalog_configuration", value=catalog_configuration, expected_type=type_hints["catalog_configuration"])
                check_type(argname="argument custom_artifacts_configuration", value=custom_artifacts_configuration, expected_type=type_hints["custom_artifacts_configuration"])
                check_type(argname="argument deploy_as_application_configuration", value=deploy_as_application_configuration, expected_type=type_hints["deploy_as_application_configuration"])
                check_type(argname="argument monitoring_configuration", value=monitoring_configuration, expected_type=type_hints["monitoring_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_configuration is not None:
                self._values["catalog_configuration"] = catalog_configuration
            if custom_artifacts_configuration is not None:
                self._values["custom_artifacts_configuration"] = custom_artifacts_configuration
            if deploy_as_application_configuration is not None:
                self._values["deploy_as_application_configuration"] = deploy_as_application_configuration
            if monitoring_configuration is not None:
                self._values["monitoring_configuration"] = monitoring_configuration

        @builtins.property
        def catalog_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CatalogConfigurationProperty"]]:
            '''The Amazon Glue Data Catalog that you use in queries in a Kinesis Data Analytics Studio notebook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-zeppelinapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-zeppelinapplicationconfiguration-catalogconfiguration
            '''
            result = self._values.get("catalog_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CatalogConfigurationProperty"]], result)

        @builtins.property
        def custom_artifacts_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CustomArtifactConfigurationProperty"]]]]:
            '''A list of ``CustomArtifactConfiguration`` objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-zeppelinapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-zeppelinapplicationconfiguration-customartifactsconfiguration
            '''
            result = self._values.get("custom_artifacts_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CustomArtifactConfigurationProperty"]]]], result)

        @builtins.property
        def deploy_as_application_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.DeployAsApplicationConfigurationProperty"]]:
            '''The information required to deploy a Kinesis Data Analytics Studio notebook as an application with durable state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-zeppelinapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-zeppelinapplicationconfiguration-deployasapplicationconfiguration
            '''
            result = self._values.get("deploy_as_application_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.DeployAsApplicationConfigurationProperty"]], result)

        @builtins.property
        def monitoring_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ZeppelinMonitoringConfigurationProperty"]]:
            '''The monitoring configuration of a Kinesis Data Analytics Studio notebook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-zeppelinapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-zeppelinapplicationconfiguration-monitoringconfiguration
            '''
            result = self._values.get("monitoring_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ZeppelinMonitoringConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZeppelinApplicationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationPropsMixin.ZeppelinMonitoringConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_level": "logLevel"},
    )
    class ZeppelinMonitoringConfigurationProperty:
        def __init__(self, *, log_level: typing.Optional[builtins.str] = None) -> None:
            '''Describes configuration parameters for Amazon CloudWatch logging for a Kinesis Data Analytics Studio notebook.

            For more information about CloudWatch logging, see `Monitoring <https://docs.aws.amazon.com/managed-flink/latest/java/monitoring-overview.html>`_ .

            :param log_level: The verbosity of the CloudWatch Logs for an application. You can set it to ``INFO`` , ``WARN`` , ``ERROR`` , or ``DEBUG`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-zeppelinmonitoringconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                zeppelin_monitoring_configuration_property = kinesisanalyticsv2_mixins.CfnApplicationPropsMixin.ZeppelinMonitoringConfigurationProperty(
                    log_level="logLevel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e4319228428d57afae022e669e4af5a52a26d74168c274bfbb18bb2ec3f3bc43)
                check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_level is not None:
                self._values["log_level"] = log_level

        @builtins.property
        def log_level(self) -> typing.Optional[builtins.str]:
            '''The verbosity of the CloudWatch Logs for an application.

            You can set it to ``INFO`` , ``WARN`` , ``ERROR`` , or ``DEBUG`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-zeppelinmonitoringconfiguration.html#cfn-kinesisanalyticsv2-application-zeppelinmonitoringconfiguration-loglevel
            '''
            result = self._values.get("log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZeppelinMonitoringConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationReferenceDataSourceMixinProps",
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

        :param application_name: The name of the application.
        :param reference_data_source: For a SQL-based Kinesis Data Analytics application, describes the reference data source by providing the source information (Amazon S3 bucket name and object key name), the resulting in-application table name that is created, and the necessary schema to map the data elements in the Amazon S3 object to the in-application table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationreferencedatasource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
            
            cfn_application_reference_data_source_mixin_props = kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourceMixinProps(
                application_name="applicationName",
                reference_data_source=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceDataSourceProperty(
                    reference_schema=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty(
                        record_columns=[kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty(
                            mapping="mapping",
                            name="name",
                            sql_type="sqlType"
                        )],
                        record_encoding="recordEncoding",
                        record_format=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty(
                            mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty(
                                csv_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty(
                                    record_column_delimiter="recordColumnDelimiter",
                                    record_row_delimiter="recordRowDelimiter"
                                ),
                                json_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty(
                                    record_row_path="recordRowPath"
                                )
                            ),
                            record_format_type="recordFormatType"
                        )
                    ),
                    s3_reference_data_source=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty(
                        bucket_arn="bucketArn",
                        file_key="fileKey"
                    ),
                    table_name="tableName"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e16b2bd58e91d12b2ce191dbdb03722730d6c1e02ed126922b4aedaa737a39)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument reference_data_source", value=reference_data_source, expected_type=type_hints["reference_data_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if reference_data_source is not None:
            self._values["reference_data_source"] = reference_data_source

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationreferencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reference_data_source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.ReferenceDataSourceProperty"]]:
        '''For a SQL-based Kinesis Data Analytics application, describes the reference data source by providing the source information (Amazon S3 bucket name and object key name), the resulting in-application table name that is created, and the necessary schema to map the data elements in the Amazon S3 object to the in-application table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationreferencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource
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
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationReferenceDataSourcePropsMixin",
):
    '''Adds a reference data source to an existing SQL-based Kinesis Data Analytics application.

    Kinesis Data Analytics reads reference data (that is, an Amazon S3 object) and creates an in-application table within your application. In the request, you provide the source (S3 bucket name and object key name), name of the in-application table to create, and the necessary mapping information that describes how data in an Amazon S3 object maps to columns in the resulting in-application table.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationreferencedatasource.html
    :cloudformationResource: AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
        
        cfn_application_reference_data_source_props_mixin = kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin(kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourceMixinProps(
            application_name="applicationName",
            reference_data_source=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceDataSourceProperty(
                reference_schema=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty(
                    record_columns=[kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty(
                        mapping="mapping",
                        name="name",
                        sql_type="sqlType"
                    )],
                    record_encoding="recordEncoding",
                    record_format=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty(
                        mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty(
                            csv_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty(
                                record_column_delimiter="recordColumnDelimiter",
                                record_row_delimiter="recordRowDelimiter"
                            ),
                            json_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty(
                                record_row_path="recordRowPath"
                            )
                        ),
                        record_format_type="recordFormatType"
                    )
                ),
                s3_reference_data_source=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty(
                    bucket_arn="bucketArn",
                    file_key="fileKey"
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
        '''Create a mixin to apply properties to ``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2693b020006542286e76735c4a787e4ae15098233baa1c777c39a0ba6147e336)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad0c4431dbb98c4b653a07354f688bb5d710278a9fa03947ac1afe0575d1e42c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c33734493b443177a269981542395eaf414f0186a436ed418ece6a3b8d4e84)
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty",
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
            '''For a SQL-based Kinesis Data Analytics application, provides additional mapping information when the record format uses delimiters, such as CSV.

            For example, the following sample records use CSV format, where the records use the *'\\n'* as the row delimiter and a comma (",") as the column delimiter:

            ``"name1", "address1"``

            ``"name2", "address2"``

            :param record_column_delimiter: The column delimiter. For example, in a CSV format, a comma (",") is the typical column delimiter.
            :param record_row_delimiter: The row delimiter. For example, in a CSV format, *'\\n'* is the typical row delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                c_sVMapping_parameters_property = kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty(
                    record_column_delimiter="recordColumnDelimiter",
                    record_row_delimiter="recordRowDelimiter"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__00c18ea26401c428b4233f276b43862534fd0071a8c1f6d180a85a65b19ee810)
                check_type(argname="argument record_column_delimiter", value=record_column_delimiter, expected_type=type_hints["record_column_delimiter"])
                check_type(argname="argument record_row_delimiter", value=record_row_delimiter, expected_type=type_hints["record_row_delimiter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if record_column_delimiter is not None:
                self._values["record_column_delimiter"] = record_column_delimiter
            if record_row_delimiter is not None:
                self._values["record_row_delimiter"] = record_row_delimiter

        @builtins.property
        def record_column_delimiter(self) -> typing.Optional[builtins.str]:
            '''The column delimiter.

            For example, in a CSV format, a comma (",") is the typical column delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters-recordcolumndelimiter
            '''
            result = self._values.get("record_column_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_row_delimiter(self) -> typing.Optional[builtins.str]:
            '''The row delimiter.

            For example, in a CSV format, *'\\n'* is the typical row delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters-recordrowdelimiter
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"record_row_path": "recordRowPath"},
    )
    class JSONMappingParametersProperty:
        def __init__(
            self,
            *,
            record_row_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''For a SQL-based Kinesis Data Analytics application, provides additional mapping information when JSON is the record format on the streaming source.

            :param record_row_path: The path to the top-level parent that contains the records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-jsonmappingparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                j_sONMapping_parameters_property = kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty(
                    record_row_path="recordRowPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2a5d1d0fb81a1ef0133e80d5ffdde3e1cc2b5f3e9df12d12809eec87fc6c842)
                check_type(argname="argument record_row_path", value=record_row_path, expected_type=type_hints["record_row_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if record_row_path is not None:
                self._values["record_row_path"] = record_row_path

        @builtins.property
        def record_row_path(self) -> typing.Optional[builtins.str]:
            '''The path to the top-level parent that contains the records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-jsonmappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-jsonmappingparameters-recordrowpath
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty",
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
            '''When you configure a SQL-based Kinesis Data Analytics application's input at the time of creating or updating an application, provides additional mapping information specific to the record format (such as JSON, CSV, or record fields delimited by some delimiter) on the streaming source.

            :param csv_mapping_parameters: Provides additional mapping information when the record format uses delimiters (for example, CSV).
            :param json_mapping_parameters: Provides additional mapping information when JSON is the record format on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                mapping_parameters_property = kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty(
                    csv_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty(
                        record_column_delimiter="recordColumnDelimiter",
                        record_row_delimiter="recordRowDelimiter"
                    ),
                    json_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty(
                        record_row_path="recordRowPath"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__32a84e0ab8bcad68b3e0a0cd9c64963f1375bdb47240f642f97b036f599b1a6a)
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

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters-csvmappingparameters
            '''
            result = self._values.get("csv_mapping_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty"]], result)

        @builtins.property
        def json_mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty"]]:
            '''Provides additional mapping information when JSON is the record format on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters-jsonmappingparameters
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty",
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
            '''For a SQL-based Kinesis Data Analytics application, describes the mapping of each data element in the streaming source to the corresponding column in the in-application stream.

            Also used to describe the format of the reference data source.

            :param mapping: A reference to the data element in the streaming input or the reference data source.
            :param name: The name of the column that is created in the in-application input stream or reference table.
            :param sql_type: The type of column created in the in-application input stream or reference table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                record_column_property = kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty(
                    mapping="mapping",
                    name="name",
                    sql_type="sqlType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a8039247ff5023d9d4fe9ce34d1f345d6a4613f66a4effbf788daa44568e552)
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
            '''A reference to the data element in the streaming input or the reference data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn-mapping
            '''
            result = self._values.get("mapping")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the column that is created in the in-application input stream or reference table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sql_type(self) -> typing.Optional[builtins.str]:
            '''The type of column created in the in-application input stream or reference table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn-sqltype
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty",
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
            '''For a SQL-based Kinesis Data Analytics application, describes the record format and relevant mapping information that should be applied to schematize the records on the stream.

            :param mapping_parameters: When you configure application input at the time of creating or updating an application, provides additional mapping information specific to the record format (such as JSON, CSV, or record fields delimited by some delimiter) on the streaming source.
            :param record_format_type: The type of record format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordformat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                record_format_property = kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty(
                    mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty(
                        csv_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty(
                            record_column_delimiter="recordColumnDelimiter",
                            record_row_delimiter="recordRowDelimiter"
                        ),
                        json_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty(
                            record_row_path="recordRowPath"
                        )
                    ),
                    record_format_type="recordFormatType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__47c36d8fd7cf5a0adaf249dc3025ef2d16b1100bdf5796c542215eb27f673c27)
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
            '''When you configure application input at the time of creating or updating an application, provides additional mapping information specific to the record format (such as JSON, CSV, or record fields delimited by some delimiter) on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordformat.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordformat-mappingparameters
            '''
            result = self._values.get("mapping_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty"]], result)

        @builtins.property
        def record_format_type(self) -> typing.Optional[builtins.str]:
            '''The type of record format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordformat.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordformat-recordformattype
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceDataSourceProperty",
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
            '''For a SQL-based Kinesis Data Analytics application, describes the reference data source by providing the source information (Amazon S3 bucket name and object key name), the resulting in-application table name that is created, and the necessary schema to map the data elements in the Amazon S3 object to the in-application table.

            :param reference_schema: Describes the format of the data in the streaming source, and how each data element maps to corresponding columns created in the in-application stream.
            :param s3_reference_data_source: Identifies the S3 bucket and object that contains the reference data. A Kinesis Data Analytics application loads reference data only once. If the data changes, you call the `UpdateApplication <https://docs.aws.amazon.com/managed-flink/latest/apiv2/API_UpdateApplication.html>`_ operation to trigger reloading of data into your application.
            :param table_name: The name of the in-application table to create.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                reference_data_source_property = kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceDataSourceProperty(
                    reference_schema=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty(
                        record_columns=[kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty(
                            mapping="mapping",
                            name="name",
                            sql_type="sqlType"
                        )],
                        record_encoding="recordEncoding",
                        record_format=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty(
                            mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty(
                                csv_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty(
                                    record_column_delimiter="recordColumnDelimiter",
                                    record_row_delimiter="recordRowDelimiter"
                                ),
                                json_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty(
                                    record_row_path="recordRowPath"
                                )
                            ),
                            record_format_type="recordFormatType"
                        )
                    ),
                    s3_reference_data_source=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty(
                        bucket_arn="bucketArn",
                        file_key="fileKey"
                    ),
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__30b3b4a8a6a72fd30d73e4c6212fd54f9c6537cc0e902d906ecf37c508c9320b)
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

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource-referenceschema
            '''
            result = self._values.get("reference_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty"]], result)

        @builtins.property
        def s3_reference_data_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty"]]:
            '''Identifies the S3 bucket and object that contains the reference data.

            A Kinesis Data Analytics application loads reference data only once. If the data changes, you call the `UpdateApplication <https://docs.aws.amazon.com/managed-flink/latest/apiv2/API_UpdateApplication.html>`_ operation to trigger reloading of data into your application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource-s3referencedatasource
            '''
            result = self._values.get("s3_reference_data_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty"]], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the in-application table to create.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource-tablename
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty",
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
            '''For a SQL-based Kinesis Data Analytics application, describes the format of the data in the streaming source, and how each data element maps to corresponding columns created in the in-application stream.

            :param record_columns: A list of ``RecordColumn`` objects.
            :param record_encoding: Specifies the encoding of the records in the streaming source. For example, UTF-8.
            :param record_format: Specifies the format of the records on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referenceschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                reference_schema_property = kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty(
                    record_columns=[kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty(
                        mapping="mapping",
                        name="name",
                        sql_type="sqlType"
                    )],
                    record_encoding="recordEncoding",
                    record_format=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty(
                        mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty(
                            csv_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty(
                                record_column_delimiter="recordColumnDelimiter",
                                record_row_delimiter="recordRowDelimiter"
                            ),
                            json_mapping_parameters=kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty(
                                record_row_path="recordRowPath"
                            )
                        ),
                        record_format_type="recordFormatType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__425d111db279248c1cbda91957defc583a6ae83d876cd8cda7433607fde028a5)
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
            '''A list of ``RecordColumn`` objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referenceschema-recordcolumns
            '''
            result = self._values.get("record_columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty"]]]], result)

        @builtins.property
        def record_encoding(self) -> typing.Optional[builtins.str]:
            '''Specifies the encoding of the records in the streaming source.

            For example, UTF-8.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referenceschema-recordencoding
            '''
            result = self._values.get("record_encoding")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_format(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty"]]:
            '''Specifies the format of the records on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referenceschema-recordformat
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
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalyticsv2.mixins.CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_arn": "bucketArn", "file_key": "fileKey"},
    )
    class S3ReferenceDataSourceProperty:
        def __init__(
            self,
            *,
            bucket_arn: typing.Optional[builtins.str] = None,
            file_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''For an SQL-based Amazon Kinesis Data Analytics application, identifies the Amazon S3 bucket and object that contains the reference data.

            A Kinesis Data Analytics application loads reference data only once. If the data changes, you call the `UpdateApplication <https://docs.aws.amazon.com/managed-flink/latest/apiv2/API_UpdateApplication.html>`_ operation to trigger reloading of data into your application.

            :param bucket_arn: The Amazon Resource Name (ARN) of the S3 bucket.
            :param file_key: The object key name containing the reference data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalyticsv2 import mixins as kinesisanalyticsv2_mixins
                
                s3_reference_data_source_property = kinesisanalyticsv2_mixins.CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty(
                    bucket_arn="bucketArn",
                    file_key="fileKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2581e3719cce9dfe7b3453f9b77b4e927424232f87380ff7f7a30aa0648bf5b)
                check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
                check_type(argname="argument file_key", value=file_key, expected_type=type_hints["file_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_arn is not None:
                self._values["bucket_arn"] = bucket_arn
            if file_key is not None:
                self._values["file_key"] = file_key

        @builtins.property
        def bucket_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource-bucketarn
            '''
            result = self._values.get("bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_key(self) -> typing.Optional[builtins.str]:
            '''The object key name containing the reference data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource-filekey
            '''
            result = self._values.get("file_key")
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
    "CfnApplicationCloudWatchLoggingOptionMixinProps",
    "CfnApplicationCloudWatchLoggingOptionPropsMixin",
    "CfnApplicationMixinProps",
    "CfnApplicationOutputMixinProps",
    "CfnApplicationOutputPropsMixin",
    "CfnApplicationPropsMixin",
    "CfnApplicationReferenceDataSourceMixinProps",
    "CfnApplicationReferenceDataSourcePropsMixin",
]

publication.publish()

def _typecheckingstub__b452be3edc2cf79768f12326eeb61a0f09cc7602d5e4b66a916d2f83a501463f(
    *,
    application_name: typing.Optional[builtins.str] = None,
    cloud_watch_logging_option: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationCloudWatchLoggingOptionPropsMixin.CloudWatchLoggingOptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26869c70c051c38a37b4c1b92a0d0dc31f42432b034edc2017e56a47dc85f0dc(
    props: typing.Union[CfnApplicationCloudWatchLoggingOptionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a889b38540ec13f679ff743042ecc0660e8b0c7009108c1a95edbd5996a54f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1f8351d6b05c05ec9bb4d5e1e0f76022778293d342e651516a8cf4d5f7c5c6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a34de6c7bf66ee445a92951f8c595ef057bb84d32239fdf255e760270f0cf4(
    *,
    log_stream_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb090809c844b83eeb283df39e178df5a843e5f0a1feb6c082c66bab7dbf9962(
    *,
    application_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ApplicationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    application_description: typing.Optional[builtins.str] = None,
    application_maintenance_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ApplicationMaintenanceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    application_mode: typing.Optional[builtins.str] = None,
    application_name: typing.Optional[builtins.str] = None,
    run_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.RunConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    runtime_environment: typing.Optional[builtins.str] = None,
    service_execution_role: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9499736b700cabc7a0640638ae22982d46448fe7b01a820616dfd567647e6616(
    *,
    application_name: typing.Optional[builtins.str] = None,
    output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationOutputPropsMixin.OutputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b4cb94ed101faea0bbf8cc46cb18b994628d0535260878e8531d59622af706(
    props: typing.Union[CfnApplicationOutputMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8d0916b300b6e19c640c220a5c7064cd80794ac2d7e64c8e8daa7e6f6a7c4d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2e0a629eb0ed12d0fb4cf8259b03cd647cd84f3b10757e71c013e129d1571b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb95f57a5a1f98d56fae1ecd10409905e0ce52dcce1c1aef5326681abe007fb(
    *,
    record_format_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41929938915ebf2fe3b7de59a4f25536db126f3dcab0eb671bcf6fca39bd2415(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3cb8b8394f9b7ffb90efa920fe89cb779000d597c9eb48e0cc844079c81f1f(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4209998ab24d66d43f4f0353adb1e455bcaf20162cc3e090bb5dbae351107e4(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf21a8f69f385258a78658e04217a01202c91e919dc0837258654d2edab25e87(
    *,
    destination_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationOutputPropsMixin.DestinationSchemaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_firehose_output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_streams_output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationOutputPropsMixin.LambdaOutputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2b226fa0a2379aea0b06e5b10628057fdbbbcbd9e5d29d231e3d2b45f25932(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9f757b1ee22b84581b1b9b66b5869975c18537074e8dd6fafbcf8a97a3cba8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47976607390b06738c5eaaafa79e34dcb420a95f3b98122690228b6592698a2b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752478396235b218e37a37ede09be75d978eaa050f2efbc0dc9c9844966afa86(
    *,
    code_content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.CodeContentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    code_content_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d08cff34c10503084c8035bd80bdf9f7dc7d2e7bfba4288bb10ad1b7fd190c(
    *,
    application_code_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ApplicationCodeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    application_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ApplicationEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    application_snapshot_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ApplicationSnapshotConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    application_system_rollback_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ApplicationSystemRollbackConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    environment_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.EnvironmentPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    flink_application_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.FlinkApplicationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sql_application_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.SqlApplicationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    zeppelin_application_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ZeppelinApplicationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761173697e7718ec1e8dcc8160dc9fffee03be812188fd3ef8199aab2814d729(
    *,
    key_id: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1711ef71893491d2468da166d8de55f6e11c1860237b8842648d403a45ca984(
    *,
    application_maintenance_window_start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a726ab8482f2d5561b9ffd31b22ae765c24ef6e8673c587f45656ba17c461f(
    *,
    application_restore_type: typing.Optional[builtins.str] = None,
    snapshot_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4d3bacd97a2bc27a5da895145679ae3fa7faf6845c2596264254e89ede570d(
    *,
    snapshots_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938b6429404837bcdbc7d388f9862dee6626ea5e0f6f9477f87711761b46f685(
    *,
    rollback_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ff36e66f9cc94a1577f867302d840b161a2c5cb163583742c8fae78d28cda3(
    *,
    record_column_delimiter: typing.Optional[builtins.str] = None,
    record_row_delimiter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a75d22e2428fc0f860ef181c5cb7454f63574df8138c14b3cb8f938d9f6b7f(
    *,
    glue_data_catalog_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.GlueDataCatalogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f087798caf47698684e4b83c3d8cd688584f2f344570b5356afa28c1746cde34(
    *,
    checkpointing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    checkpoint_interval: typing.Optional[jsii.Number] = None,
    configuration_type: typing.Optional[builtins.str] = None,
    min_pause_between_checkpoints: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58bfd4518fc8e85e155b6ec9d967152f52d404cb7721892c791e35c2ab1ca03(
    *,
    s3_content_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.S3ContentLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    text_content: typing.Optional[builtins.str] = None,
    zip_file_content: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82c8f95ad4cac5ffc1db091c6a1dbe19ffde8321b021ee9a6439c420f194a40(
    *,
    artifact_type: typing.Optional[builtins.str] = None,
    maven_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.MavenReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_content_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.S3ContentLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07e5019f63a03dd81c792b8505d1b7113b20e96e6abe55a683d908bfaece8ee(
    *,
    s3_content_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.S3ContentBaseLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5161c95acde982e6829d227ae486f22b5580674a5f03e8e53c8401fa5ce3230(
    *,
    property_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f092681c093bbd340f680e687fb13e9d60cda37fd43b43a9371afbbd172b7d(
    *,
    checkpoint_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.CheckpointConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.MonitoringConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parallelism_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ParallelismConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3516b51a93a0d68213ff4f96465461c5b493a448aea2bd0fdead54d27ef194ca(
    *,
    allow_non_restored_state: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431edcad089d3f41c7ba46c2607e03c9a0f4b4d124896a9d4915a05974c7dcca(
    *,
    database_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e1e82bbf698f733ea0349809866136319a6f4c5e888506f36e8a4c8fb40937(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f3d8dd47fb6919466212700b27a78556166641e1603279be73be43925ca2fa4(
    *,
    count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca14663ee4e02e3b37fe8527fd1b21ccb6b1d78e51f037971bd404e21332a7b8(
    *,
    input_lambda_processor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.InputLambdaProcessorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e969fd1348039079eac20594906cd460629ae9dc6e091b0ebefc5ab0e2700f(
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

def _typecheckingstub__a9ca27d8167376bba90150d94c58a654e3692c3e73d0e88d59fb8171de003492(
    *,
    record_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.RecordColumnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    record_encoding: typing.Optional[builtins.str] = None,
    record_format: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.RecordFormatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c89d2f65d8167984851a5c0d310ef85f7ce6bbf0e8ac745efea02f3f77a4363(
    *,
    record_row_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6d9c243bf45cb70cf82e50d1f8c3bb162be7ff565211e81eb5f2c412c0e7f3(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9a4c3149ea7f4e17e88671b295e8b1657f60e9647c1d08bc36562c16ee83f9(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc92baae1770cfba392206657ec11fb5f8540f654ba3d23d49bb2d3366f913c5(
    *,
    csv_mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.CSVMappingParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    json_mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.JSONMappingParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43bf72c87ed4d15e028e22a771b5501dd2cac46ee85aace3a13136996ec58d8(
    *,
    artifact_id: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9bb6ba72074e666b568d0cbefe508b4aa6bc77d83e18d0cc3deb0c8af2b131(
    *,
    configuration_type: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    metrics_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffeeecf839baccd0c19a12956247b2502c6f83cc633e58f5f88b2f4c73f77bbc(
    *,
    auto_scaling_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    configuration_type: typing.Optional[builtins.str] = None,
    parallelism: typing.Optional[jsii.Number] = None,
    parallelism_per_kpu: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1afff2342c9f7de19d23a87e2de2365a12bda8a09033c1a7e9e45b49cf735517(
    *,
    property_group_id: typing.Optional[builtins.str] = None,
    property_map: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1771b5ed12c4ab61f86d20c296c8f537403fa03dfe73cddfe9fb3f6d5fd56f9a(
    *,
    mapping: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    sql_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ef32af36f2b89eca79ea2492a48093a1f2885d4c645dbc06417ff816f0b483(
    *,
    mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.MappingParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    record_format_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c8b8cb10b2b67778955feeaf6f99d739d66de64472786e2e6e43ae76307730(
    *,
    application_restore_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ApplicationRestoreConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    flink_run_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.FlinkRunConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b5668e5aba6ed7d6373dec1973bfc8e52da27faf662f47f6bee556950b2a0c(
    *,
    base_path: typing.Optional[builtins.str] = None,
    bucket_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b2aa33170a95a3f5cd8876a3b05323efa9e12347584c36cd85456e59ba7a0ad(
    *,
    bucket_arn: typing.Optional[builtins.str] = None,
    file_key: typing.Optional[builtins.str] = None,
    object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79886d4436c2451eadc884c8eb3551d41816a2e1c158093de3e1188cf3e377b(
    *,
    inputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.InputProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad722a5d9fdda46edddead14cd2908750f8345159e5eaf52d9ea3e905a07bbb(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef73001930066f0c2b5eb2d6fc580040cf8dfe7063876ad817d1a1998454e8f3(
    *,
    catalog_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.CatalogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_artifacts_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.CustomArtifactConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    deploy_as_application_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.DeployAsApplicationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ZeppelinMonitoringConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4319228428d57afae022e669e4af5a52a26d74168c274bfbb18bb2ec3f3bc43(
    *,
    log_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e16b2bd58e91d12b2ce191dbdb03722730d6c1e02ed126922b4aedaa737a39(
    *,
    application_name: typing.Optional[builtins.str] = None,
    reference_data_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.ReferenceDataSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2693b020006542286e76735c4a787e4ae15098233baa1c777c39a0ba6147e336(
    props: typing.Union[CfnApplicationReferenceDataSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0c4431dbb98c4b653a07354f688bb5d710278a9fa03947ac1afe0575d1e42c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c33734493b443177a269981542395eaf414f0186a436ed418ece6a3b8d4e84(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c18ea26401c428b4233f276b43862534fd0071a8c1f6d180a85a65b19ee810(
    *,
    record_column_delimiter: typing.Optional[builtins.str] = None,
    record_row_delimiter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a5d1d0fb81a1ef0133e80d5ffdde3e1cc2b5f3e9df12d12809eec87fc6c842(
    *,
    record_row_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a84e0ab8bcad68b3e0a0cd9c64963f1375bdb47240f642f97b036f599b1a6a(
    *,
    csv_mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    json_mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a8039247ff5023d9d4fe9ce34d1f345d6a4613f66a4effbf788daa44568e552(
    *,
    mapping: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    sql_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c36d8fd7cf5a0adaf249dc3025ef2d16b1100bdf5796c542215eb27f673c27(
    *,
    mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    record_format_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b3b4a8a6a72fd30d73e4c6212fd54f9c6537cc0e902d906ecf37c508c9320b(
    *,
    reference_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_reference_data_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425d111db279248c1cbda91957defc583a6ae83d876cd8cda7433607fde028a5(
    *,
    record_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    record_encoding: typing.Optional[builtins.str] = None,
    record_format: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2581e3719cce9dfe7b3453f9b77b4e927424232f87380ff7f7a30aa0648bf5b(
    *,
    bucket_arn: typing.Optional[builtins.str] = None,
    file_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
