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


class CfnPipeExecutionLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipeExecutionLogs",
):
    '''Builder for CfnPipeLogsMixin to generate EXECUTION_LOGS for CfnPipe.

    :cloudformationResource: AWS::Pipes::Pipe
    :logType: EXECUTION_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
        
        cfn_pipe_execution_logs = pipes_mixins.CfnPipeExecutionLogs()
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
    ) -> "CfnPipeLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f846d29d1d6fe535cd650445a62df46a0e4865ab5a411a9c47a4f28badb0746)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnPipeLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnPipeLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7447cdacd039b7cb64140b50c70cb4c6ce42ae5f2ca7d8f3db11622682cc01ca)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnPipeLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnPipeLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fa9cb184fb33be43ae487ce581070f095b9219c766c18456fdb6c619e0705ad)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnPipeLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnPipeLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipeLogsMixin",
):
    '''Specifies a pipe.

    Amazon EventBridge Pipes connect event sources to targets and reduces the need for specialized knowledge and integration code.
    .. epigraph::

       As an aid to help you jumpstart developing CloudFormation templates, the EventBridge console enables you to create templates from the existing pipes in your account. For more information, see `Generate an CloudFormation template from EventBridge Pipes <https://docs.aws.amazon.com/eventbridge/latest/userguide/pipes-generate-template.html>`_ in the *Amazon EventBridge User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html
    :cloudformationResource: AWS::Pipes::Pipe
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_pipe_logs_mixin = pipes_mixins.CfnPipeLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::Pipes::Pipe``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb167e33c446551a196db6c11c656c9100cd9ba152fbd016e4fc248219ab4e87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1c04e0d1247401c2ccc4dc5e80999f6074ba967709c12311fd23abafd9c4cfd)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1c452fc6c416e9cb5bfe47646e530ae7542cf73e6613d666332046ccb87628)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="EXECUTION_LOGS")
    def EXECUTION_LOGS(cls) -> CfnPipeExecutionLogs:
        return typing.cast(CfnPipeExecutionLogs, jsii.sget(cls, "EXECUTION_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "desired_state": "desiredState",
        "enrichment": "enrichment",
        "enrichment_parameters": "enrichmentParameters",
        "kms_key_identifier": "kmsKeyIdentifier",
        "log_configuration": "logConfiguration",
        "name": "name",
        "role_arn": "roleArn",
        "source": "source",
        "source_parameters": "sourceParameters",
        "tags": "tags",
        "target": "target",
        "target_parameters": "targetParameters",
    },
)
class CfnPipeMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        desired_state: typing.Optional[builtins.str] = None,
        enrichment: typing.Optional[builtins.str] = None,
        enrichment_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeEnrichmentParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_identifier: typing.Optional[builtins.str] = None,
        log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeLogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        source_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeSourceParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target: typing.Optional[builtins.str] = None,
        target_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeTargetParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPipePropsMixin.

        :param description: A description of the pipe.
        :param desired_state: The state the pipe should be in.
        :param enrichment: The ARN of the enrichment resource.
        :param enrichment_parameters: The parameters required to set up enrichment on your pipe.
        :param kms_key_identifier: The identifier of the AWS customer managed key for EventBridge to use, if you choose to use a customer managed key to encrypt pipe data. The identifier can be the key Amazon Resource Name (ARN), KeyId, key alias, or key alias ARN. To update a pipe that is using the default AWS owned key to use a customer managed key instead, or update a pipe that is using a customer managed key to use a different customer managed key, specify a customer managed key identifier. To update a pipe that is using a customer managed key to use the default AWS owned key , specify an empty string. For more information, see `Managing keys <https://docs.aws.amazon.com/kms/latest/developerguide/getting-started.html>`_ in the *AWS Key Management Service Developer Guide* .
        :param log_configuration: The logging configuration settings for the pipe.
        :param name: The name of the pipe.
        :param role_arn: The ARN of the role that allows the pipe to send data to the target.
        :param source: The ARN of the source resource.
        :param source_parameters: The parameters required to set up a source for your pipe.
        :param tags: The list of key-value pairs to associate with the pipe.
        :param target: The ARN of the target resource.
        :param target_parameters: The parameters required to set up a target for your pipe. For more information about pipe target parameters, including how to use dynamic path parameters, see `Target parameters <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-target.html>`_ in the *Amazon EventBridge User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
            
            cfn_pipe_mixin_props = pipes_mixins.CfnPipeMixinProps(
                description="description",
                desired_state="desiredState",
                enrichment="enrichment",
                enrichment_parameters=pipes_mixins.CfnPipePropsMixin.PipeEnrichmentParametersProperty(
                    http_parameters=pipes_mixins.CfnPipePropsMixin.PipeEnrichmentHttpParametersProperty(
                        header_parameters={
                            "header_parameters_key": "headerParameters"
                        },
                        path_parameter_values=["pathParameterValues"],
                        query_string_parameters={
                            "query_string_parameters_key": "queryStringParameters"
                        }
                    ),
                    input_template="inputTemplate"
                ),
                kms_key_identifier="kmsKeyIdentifier",
                log_configuration=pipes_mixins.CfnPipePropsMixin.PipeLogConfigurationProperty(
                    cloudwatch_logs_log_destination=pipes_mixins.CfnPipePropsMixin.CloudwatchLogsLogDestinationProperty(
                        log_group_arn="logGroupArn"
                    ),
                    firehose_log_destination=pipes_mixins.CfnPipePropsMixin.FirehoseLogDestinationProperty(
                        delivery_stream_arn="deliveryStreamArn"
                    ),
                    include_execution_data=["includeExecutionData"],
                    level="level",
                    s3_log_destination=pipes_mixins.CfnPipePropsMixin.S3LogDestinationProperty(
                        bucket_name="bucketName",
                        bucket_owner="bucketOwner",
                        output_format="outputFormat",
                        prefix="prefix"
                    )
                ),
                name="name",
                role_arn="roleArn",
                source="source",
                source_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceParametersProperty(
                    active_mq_broker_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceActiveMQBrokerParametersProperty(
                        batch_size=123,
                        credentials=pipes_mixins.CfnPipePropsMixin.MQBrokerAccessCredentialsProperty(
                            basic_auth="basicAuth"
                        ),
                        maximum_batching_window_in_seconds=123,
                        queue_name="queueName"
                    ),
                    dynamo_db_stream_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceDynamoDBStreamParametersProperty(
                        batch_size=123,
                        dead_letter_config=pipes_mixins.CfnPipePropsMixin.DeadLetterConfigProperty(
                            arn="arn"
                        ),
                        maximum_batching_window_in_seconds=123,
                        maximum_record_age_in_seconds=123,
                        maximum_retry_attempts=123,
                        on_partial_batch_item_failure="onPartialBatchItemFailure",
                        parallelization_factor=123,
                        starting_position="startingPosition"
                    ),
                    filter_criteria=pipes_mixins.CfnPipePropsMixin.FilterCriteriaProperty(
                        filters=[pipes_mixins.CfnPipePropsMixin.FilterProperty(
                            pattern="pattern"
                        )]
                    ),
                    kinesis_stream_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceKinesisStreamParametersProperty(
                        batch_size=123,
                        dead_letter_config=pipes_mixins.CfnPipePropsMixin.DeadLetterConfigProperty(
                            arn="arn"
                        ),
                        maximum_batching_window_in_seconds=123,
                        maximum_record_age_in_seconds=123,
                        maximum_retry_attempts=123,
                        on_partial_batch_item_failure="onPartialBatchItemFailure",
                        parallelization_factor=123,
                        starting_position="startingPosition",
                        starting_position_timestamp="startingPositionTimestamp"
                    ),
                    managed_streaming_kafka_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceManagedStreamingKafkaParametersProperty(
                        batch_size=123,
                        consumer_group_id="consumerGroupId",
                        credentials=pipes_mixins.CfnPipePropsMixin.MSKAccessCredentialsProperty(
                            client_certificate_tls_auth="clientCertificateTlsAuth",
                            sasl_scram512_auth="saslScram512Auth"
                        ),
                        maximum_batching_window_in_seconds=123,
                        starting_position="startingPosition",
                        topic_name="topicName"
                    ),
                    rabbit_mq_broker_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceRabbitMQBrokerParametersProperty(
                        batch_size=123,
                        credentials=pipes_mixins.CfnPipePropsMixin.MQBrokerAccessCredentialsProperty(
                            basic_auth="basicAuth"
                        ),
                        maximum_batching_window_in_seconds=123,
                        queue_name="queueName",
                        virtual_host="virtualHost"
                    ),
                    self_managed_kafka_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceSelfManagedKafkaParametersProperty(
                        additional_bootstrap_servers=["additionalBootstrapServers"],
                        batch_size=123,
                        consumer_group_id="consumerGroupId",
                        credentials=pipes_mixins.CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationCredentialsProperty(
                            basic_auth="basicAuth",
                            client_certificate_tls_auth="clientCertificateTlsAuth",
                            sasl_scram256_auth="saslScram256Auth",
                            sasl_scram512_auth="saslScram512Auth"
                        ),
                        maximum_batching_window_in_seconds=123,
                        server_root_ca_certificate="serverRootCaCertificate",
                        starting_position="startingPosition",
                        topic_name="topicName",
                        vpc=pipes_mixins.CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationVpcProperty(
                            security_group=["securityGroup"],
                            subnets=["subnets"]
                        )
                    ),
                    sqs_queue_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceSqsQueueParametersProperty(
                        batch_size=123,
                        maximum_batching_window_in_seconds=123
                    )
                ),
                tags={
                    "tags_key": "tags"
                },
                target="target",
                target_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetParametersProperty(
                    batch_job_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetBatchJobParametersProperty(
                        array_properties=pipes_mixins.CfnPipePropsMixin.BatchArrayPropertiesProperty(
                            size=123
                        ),
                        container_overrides=pipes_mixins.CfnPipePropsMixin.BatchContainerOverridesProperty(
                            command=["command"],
                            environment=[pipes_mixins.CfnPipePropsMixin.BatchEnvironmentVariableProperty(
                                name="name",
                                value="value"
                            )],
                            instance_type="instanceType",
                            resource_requirements=[pipes_mixins.CfnPipePropsMixin.BatchResourceRequirementProperty(
                                type="type",
                                value="value"
                            )]
                        ),
                        depends_on=[pipes_mixins.CfnPipePropsMixin.BatchJobDependencyProperty(
                            job_id="jobId",
                            type="type"
                        )],
                        job_definition="jobDefinition",
                        job_name="jobName",
                        parameters={
                            "parameters_key": "parameters"
                        },
                        retry_strategy=pipes_mixins.CfnPipePropsMixin.BatchRetryStrategyProperty(
                            attempts=123
                        )
                    ),
                    cloud_watch_logs_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetCloudWatchLogsParametersProperty(
                        log_stream_name="logStreamName",
                        timestamp="timestamp"
                    ),
                    ecs_task_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetEcsTaskParametersProperty(
                        capacity_provider_strategy=[pipes_mixins.CfnPipePropsMixin.CapacityProviderStrategyItemProperty(
                            base=123,
                            capacity_provider="capacityProvider",
                            weight=123
                        )],
                        enable_ecs_managed_tags=False,
                        enable_execute_command=False,
                        group="group",
                        launch_type="launchType",
                        network_configuration=pipes_mixins.CfnPipePropsMixin.NetworkConfigurationProperty(
                            awsvpc_configuration=pipes_mixins.CfnPipePropsMixin.AwsVpcConfigurationProperty(
                                assign_public_ip="assignPublicIp",
                                security_groups=["securityGroups"],
                                subnets=["subnets"]
                            )
                        ),
                        overrides=pipes_mixins.CfnPipePropsMixin.EcsTaskOverrideProperty(
                            container_overrides=[pipes_mixins.CfnPipePropsMixin.EcsContainerOverrideProperty(
                                command=["command"],
                                cpu=123,
                                environment=[pipes_mixins.CfnPipePropsMixin.EcsEnvironmentVariableProperty(
                                    name="name",
                                    value="value"
                                )],
                                environment_files=[pipes_mixins.CfnPipePropsMixin.EcsEnvironmentFileProperty(
                                    type="type",
                                    value="value"
                                )],
                                memory=123,
                                memory_reservation=123,
                                name="name",
                                resource_requirements=[pipes_mixins.CfnPipePropsMixin.EcsResourceRequirementProperty(
                                    type="type",
                                    value="value"
                                )]
                            )],
                            cpu="cpu",
                            ephemeral_storage=pipes_mixins.CfnPipePropsMixin.EcsEphemeralStorageProperty(
                                size_in_gi_b=123
                            ),
                            execution_role_arn="executionRoleArn",
                            inference_accelerator_overrides=[pipes_mixins.CfnPipePropsMixin.EcsInferenceAcceleratorOverrideProperty(
                                device_name="deviceName",
                                device_type="deviceType"
                            )],
                            memory="memory",
                            task_role_arn="taskRoleArn"
                        ),
                        placement_constraints=[pipes_mixins.CfnPipePropsMixin.PlacementConstraintProperty(
                            expression="expression",
                            type="type"
                        )],
                        placement_strategy=[pipes_mixins.CfnPipePropsMixin.PlacementStrategyProperty(
                            field="field",
                            type="type"
                        )],
                        platform_version="platformVersion",
                        propagate_tags="propagateTags",
                        reference_id="referenceId",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        task_count=123,
                        task_definition_arn="taskDefinitionArn"
                    ),
                    event_bridge_event_bus_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetEventBridgeEventBusParametersProperty(
                        detail_type="detailType",
                        endpoint_id="endpointId",
                        resources=["resources"],
                        source="source",
                        time="time"
                    ),
                    http_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetHttpParametersProperty(
                        header_parameters={
                            "header_parameters_key": "headerParameters"
                        },
                        path_parameter_values=["pathParameterValues"],
                        query_string_parameters={
                            "query_string_parameters_key": "queryStringParameters"
                        }
                    ),
                    input_template="inputTemplate",
                    kinesis_stream_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetKinesisStreamParametersProperty(
                        partition_key="partitionKey"
                    ),
                    lambda_function_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetLambdaFunctionParametersProperty(
                        invocation_type="invocationType"
                    ),
                    redshift_data_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetRedshiftDataParametersProperty(
                        database="database",
                        db_user="dbUser",
                        secret_manager_arn="secretManagerArn",
                        sqls=["sqls"],
                        statement_name="statementName",
                        with_event=False
                    ),
                    sage_maker_pipeline_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetSageMakerPipelineParametersProperty(
                        pipeline_parameter_list=[pipes_mixins.CfnPipePropsMixin.SageMakerPipelineParameterProperty(
                            name="name",
                            value="value"
                        )]
                    ),
                    sqs_queue_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetSqsQueueParametersProperty(
                        message_deduplication_id="messageDeduplicationId",
                        message_group_id="messageGroupId"
                    ),
                    step_function_state_machine_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetStateMachineParametersProperty(
                        invocation_type="invocationType"
                    ),
                    timestream_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetTimestreamParametersProperty(
                        dimension_mappings=[pipes_mixins.CfnPipePropsMixin.DimensionMappingProperty(
                            dimension_name="dimensionName",
                            dimension_value="dimensionValue",
                            dimension_value_type="dimensionValueType"
                        )],
                        epoch_time_unit="epochTimeUnit",
                        multi_measure_mappings=[pipes_mixins.CfnPipePropsMixin.MultiMeasureMappingProperty(
                            multi_measure_attribute_mappings=[pipes_mixins.CfnPipePropsMixin.MultiMeasureAttributeMappingProperty(
                                measure_value="measureValue",
                                measure_value_type="measureValueType",
                                multi_measure_attribute_name="multiMeasureAttributeName"
                            )],
                            multi_measure_name="multiMeasureName"
                        )],
                        single_measure_mappings=[pipes_mixins.CfnPipePropsMixin.SingleMeasureMappingProperty(
                            measure_name="measureName",
                            measure_value="measureValue",
                            measure_value_type="measureValueType"
                        )],
                        time_field_type="timeFieldType",
                        timestamp_format="timestampFormat",
                        time_value="timeValue",
                        version_value="versionValue"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c93e4d67f03c822fa8e4ed7bbf89c5a2b0543ddcd1ced99c352a46e92ef1382)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
            check_type(argname="argument enrichment", value=enrichment, expected_type=type_hints["enrichment"])
            check_type(argname="argument enrichment_parameters", value=enrichment_parameters, expected_type=type_hints["enrichment_parameters"])
            check_type(argname="argument kms_key_identifier", value=kms_key_identifier, expected_type=type_hints["kms_key_identifier"])
            check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument source_parameters", value=source_parameters, expected_type=type_hints["source_parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument target_parameters", value=target_parameters, expected_type=type_hints["target_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if desired_state is not None:
            self._values["desired_state"] = desired_state
        if enrichment is not None:
            self._values["enrichment"] = enrichment
        if enrichment_parameters is not None:
            self._values["enrichment_parameters"] = enrichment_parameters
        if kms_key_identifier is not None:
            self._values["kms_key_identifier"] = kms_key_identifier
        if log_configuration is not None:
            self._values["log_configuration"] = log_configuration
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if source is not None:
            self._values["source"] = source
        if source_parameters is not None:
            self._values["source_parameters"] = source_parameters
        if tags is not None:
            self._values["tags"] = tags
        if target is not None:
            self._values["target"] = target
        if target_parameters is not None:
            self._values["target_parameters"] = target_parameters

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the pipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desired_state(self) -> typing.Optional[builtins.str]:
        '''The state the pipe should be in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-desiredstate
        '''
        result = self._values.get("desired_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enrichment(self) -> typing.Optional[builtins.str]:
        '''The ARN of the enrichment resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-enrichment
        '''
        result = self._values.get("enrichment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enrichment_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeEnrichmentParametersProperty"]]:
        '''The parameters required to set up enrichment on your pipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-enrichmentparameters
        '''
        result = self._values.get("enrichment_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeEnrichmentParametersProperty"]], result)

    @builtins.property
    def kms_key_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the AWS  customer managed key for EventBridge to use, if you choose to use a customer managed key to encrypt pipe data.

        The identifier can be the key Amazon Resource Name (ARN), KeyId, key alias, or key alias ARN.

        To update a pipe that is using the default AWS owned key to use a customer managed key instead, or update a pipe that is using a customer managed key to use a different customer managed key, specify a customer managed key identifier.

        To update a pipe that is using a customer managed key to use the default AWS owned key , specify an empty string.

        For more information, see `Managing keys <https://docs.aws.amazon.com/kms/latest/developerguide/getting-started.html>`_ in the *AWS Key Management Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-kmskeyidentifier
        '''
        result = self._values.get("kms_key_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeLogConfigurationProperty"]]:
        '''The logging configuration settings for the pipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-logconfiguration
        '''
        result = self._values.get("log_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeLogConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the pipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the role that allows the pipe to send data to the target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''The ARN of the source resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceParametersProperty"]]:
        '''The parameters required to set up a source for your pipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-sourceparameters
        '''
        result = self._values.get("source_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceParametersProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The list of key-value pairs to associate with the pipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''The ARN of the target resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetParametersProperty"]]:
        '''The parameters required to set up a target for your pipe.

        For more information about pipe target parameters, including how to use dynamic path parameters, see `Target parameters <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-target.html>`_ in the *Amazon EventBridge User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html#cfn-pipes-pipe-targetparameters
        '''
        result = self._values.get("target_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetParametersProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPipeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPipePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin",
):
    '''Specifies a pipe.

    Amazon EventBridge Pipes connect event sources to targets and reduces the need for specialized knowledge and integration code.
    .. epigraph::

       As an aid to help you jumpstart developing CloudFormation templates, the EventBridge console enables you to create templates from the existing pipes in your account. For more information, see `Generate an CloudFormation template from EventBridge Pipes <https://docs.aws.amazon.com/eventbridge/latest/userguide/pipes-generate-template.html>`_ in the *Amazon EventBridge User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pipes-pipe.html
    :cloudformationResource: AWS::Pipes::Pipe
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
        
        cfn_pipe_props_mixin = pipes_mixins.CfnPipePropsMixin(pipes_mixins.CfnPipeMixinProps(
            description="description",
            desired_state="desiredState",
            enrichment="enrichment",
            enrichment_parameters=pipes_mixins.CfnPipePropsMixin.PipeEnrichmentParametersProperty(
                http_parameters=pipes_mixins.CfnPipePropsMixin.PipeEnrichmentHttpParametersProperty(
                    header_parameters={
                        "header_parameters_key": "headerParameters"
                    },
                    path_parameter_values=["pathParameterValues"],
                    query_string_parameters={
                        "query_string_parameters_key": "queryStringParameters"
                    }
                ),
                input_template="inputTemplate"
            ),
            kms_key_identifier="kmsKeyIdentifier",
            log_configuration=pipes_mixins.CfnPipePropsMixin.PipeLogConfigurationProperty(
                cloudwatch_logs_log_destination=pipes_mixins.CfnPipePropsMixin.CloudwatchLogsLogDestinationProperty(
                    log_group_arn="logGroupArn"
                ),
                firehose_log_destination=pipes_mixins.CfnPipePropsMixin.FirehoseLogDestinationProperty(
                    delivery_stream_arn="deliveryStreamArn"
                ),
                include_execution_data=["includeExecutionData"],
                level="level",
                s3_log_destination=pipes_mixins.CfnPipePropsMixin.S3LogDestinationProperty(
                    bucket_name="bucketName",
                    bucket_owner="bucketOwner",
                    output_format="outputFormat",
                    prefix="prefix"
                )
            ),
            name="name",
            role_arn="roleArn",
            source="source",
            source_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceParametersProperty(
                active_mq_broker_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceActiveMQBrokerParametersProperty(
                    batch_size=123,
                    credentials=pipes_mixins.CfnPipePropsMixin.MQBrokerAccessCredentialsProperty(
                        basic_auth="basicAuth"
                    ),
                    maximum_batching_window_in_seconds=123,
                    queue_name="queueName"
                ),
                dynamo_db_stream_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceDynamoDBStreamParametersProperty(
                    batch_size=123,
                    dead_letter_config=pipes_mixins.CfnPipePropsMixin.DeadLetterConfigProperty(
                        arn="arn"
                    ),
                    maximum_batching_window_in_seconds=123,
                    maximum_record_age_in_seconds=123,
                    maximum_retry_attempts=123,
                    on_partial_batch_item_failure="onPartialBatchItemFailure",
                    parallelization_factor=123,
                    starting_position="startingPosition"
                ),
                filter_criteria=pipes_mixins.CfnPipePropsMixin.FilterCriteriaProperty(
                    filters=[pipes_mixins.CfnPipePropsMixin.FilterProperty(
                        pattern="pattern"
                    )]
                ),
                kinesis_stream_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceKinesisStreamParametersProperty(
                    batch_size=123,
                    dead_letter_config=pipes_mixins.CfnPipePropsMixin.DeadLetterConfigProperty(
                        arn="arn"
                    ),
                    maximum_batching_window_in_seconds=123,
                    maximum_record_age_in_seconds=123,
                    maximum_retry_attempts=123,
                    on_partial_batch_item_failure="onPartialBatchItemFailure",
                    parallelization_factor=123,
                    starting_position="startingPosition",
                    starting_position_timestamp="startingPositionTimestamp"
                ),
                managed_streaming_kafka_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceManagedStreamingKafkaParametersProperty(
                    batch_size=123,
                    consumer_group_id="consumerGroupId",
                    credentials=pipes_mixins.CfnPipePropsMixin.MSKAccessCredentialsProperty(
                        client_certificate_tls_auth="clientCertificateTlsAuth",
                        sasl_scram512_auth="saslScram512Auth"
                    ),
                    maximum_batching_window_in_seconds=123,
                    starting_position="startingPosition",
                    topic_name="topicName"
                ),
                rabbit_mq_broker_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceRabbitMQBrokerParametersProperty(
                    batch_size=123,
                    credentials=pipes_mixins.CfnPipePropsMixin.MQBrokerAccessCredentialsProperty(
                        basic_auth="basicAuth"
                    ),
                    maximum_batching_window_in_seconds=123,
                    queue_name="queueName",
                    virtual_host="virtualHost"
                ),
                self_managed_kafka_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceSelfManagedKafkaParametersProperty(
                    additional_bootstrap_servers=["additionalBootstrapServers"],
                    batch_size=123,
                    consumer_group_id="consumerGroupId",
                    credentials=pipes_mixins.CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationCredentialsProperty(
                        basic_auth="basicAuth",
                        client_certificate_tls_auth="clientCertificateTlsAuth",
                        sasl_scram256_auth="saslScram256Auth",
                        sasl_scram512_auth="saslScram512Auth"
                    ),
                    maximum_batching_window_in_seconds=123,
                    server_root_ca_certificate="serverRootCaCertificate",
                    starting_position="startingPosition",
                    topic_name="topicName",
                    vpc=pipes_mixins.CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationVpcProperty(
                        security_group=["securityGroup"],
                        subnets=["subnets"]
                    )
                ),
                sqs_queue_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceSqsQueueParametersProperty(
                    batch_size=123,
                    maximum_batching_window_in_seconds=123
                )
            ),
            tags={
                "tags_key": "tags"
            },
            target="target",
            target_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetParametersProperty(
                batch_job_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetBatchJobParametersProperty(
                    array_properties=pipes_mixins.CfnPipePropsMixin.BatchArrayPropertiesProperty(
                        size=123
                    ),
                    container_overrides=pipes_mixins.CfnPipePropsMixin.BatchContainerOverridesProperty(
                        command=["command"],
                        environment=[pipes_mixins.CfnPipePropsMixin.BatchEnvironmentVariableProperty(
                            name="name",
                            value="value"
                        )],
                        instance_type="instanceType",
                        resource_requirements=[pipes_mixins.CfnPipePropsMixin.BatchResourceRequirementProperty(
                            type="type",
                            value="value"
                        )]
                    ),
                    depends_on=[pipes_mixins.CfnPipePropsMixin.BatchJobDependencyProperty(
                        job_id="jobId",
                        type="type"
                    )],
                    job_definition="jobDefinition",
                    job_name="jobName",
                    parameters={
                        "parameters_key": "parameters"
                    },
                    retry_strategy=pipes_mixins.CfnPipePropsMixin.BatchRetryStrategyProperty(
                        attempts=123
                    )
                ),
                cloud_watch_logs_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetCloudWatchLogsParametersProperty(
                    log_stream_name="logStreamName",
                    timestamp="timestamp"
                ),
                ecs_task_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetEcsTaskParametersProperty(
                    capacity_provider_strategy=[pipes_mixins.CfnPipePropsMixin.CapacityProviderStrategyItemProperty(
                        base=123,
                        capacity_provider="capacityProvider",
                        weight=123
                    )],
                    enable_ecs_managed_tags=False,
                    enable_execute_command=False,
                    group="group",
                    launch_type="launchType",
                    network_configuration=pipes_mixins.CfnPipePropsMixin.NetworkConfigurationProperty(
                        awsvpc_configuration=pipes_mixins.CfnPipePropsMixin.AwsVpcConfigurationProperty(
                            assign_public_ip="assignPublicIp",
                            security_groups=["securityGroups"],
                            subnets=["subnets"]
                        )
                    ),
                    overrides=pipes_mixins.CfnPipePropsMixin.EcsTaskOverrideProperty(
                        container_overrides=[pipes_mixins.CfnPipePropsMixin.EcsContainerOverrideProperty(
                            command=["command"],
                            cpu=123,
                            environment=[pipes_mixins.CfnPipePropsMixin.EcsEnvironmentVariableProperty(
                                name="name",
                                value="value"
                            )],
                            environment_files=[pipes_mixins.CfnPipePropsMixin.EcsEnvironmentFileProperty(
                                type="type",
                                value="value"
                            )],
                            memory=123,
                            memory_reservation=123,
                            name="name",
                            resource_requirements=[pipes_mixins.CfnPipePropsMixin.EcsResourceRequirementProperty(
                                type="type",
                                value="value"
                            )]
                        )],
                        cpu="cpu",
                        ephemeral_storage=pipes_mixins.CfnPipePropsMixin.EcsEphemeralStorageProperty(
                            size_in_gi_b=123
                        ),
                        execution_role_arn="executionRoleArn",
                        inference_accelerator_overrides=[pipes_mixins.CfnPipePropsMixin.EcsInferenceAcceleratorOverrideProperty(
                            device_name="deviceName",
                            device_type="deviceType"
                        )],
                        memory="memory",
                        task_role_arn="taskRoleArn"
                    ),
                    placement_constraints=[pipes_mixins.CfnPipePropsMixin.PlacementConstraintProperty(
                        expression="expression",
                        type="type"
                    )],
                    placement_strategy=[pipes_mixins.CfnPipePropsMixin.PlacementStrategyProperty(
                        field="field",
                        type="type"
                    )],
                    platform_version="platformVersion",
                    propagate_tags="propagateTags",
                    reference_id="referenceId",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    task_count=123,
                    task_definition_arn="taskDefinitionArn"
                ),
                event_bridge_event_bus_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetEventBridgeEventBusParametersProperty(
                    detail_type="detailType",
                    endpoint_id="endpointId",
                    resources=["resources"],
                    source="source",
                    time="time"
                ),
                http_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetHttpParametersProperty(
                    header_parameters={
                        "header_parameters_key": "headerParameters"
                    },
                    path_parameter_values=["pathParameterValues"],
                    query_string_parameters={
                        "query_string_parameters_key": "queryStringParameters"
                    }
                ),
                input_template="inputTemplate",
                kinesis_stream_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetKinesisStreamParametersProperty(
                    partition_key="partitionKey"
                ),
                lambda_function_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetLambdaFunctionParametersProperty(
                    invocation_type="invocationType"
                ),
                redshift_data_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetRedshiftDataParametersProperty(
                    database="database",
                    db_user="dbUser",
                    secret_manager_arn="secretManagerArn",
                    sqls=["sqls"],
                    statement_name="statementName",
                    with_event=False
                ),
                sage_maker_pipeline_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetSageMakerPipelineParametersProperty(
                    pipeline_parameter_list=[pipes_mixins.CfnPipePropsMixin.SageMakerPipelineParameterProperty(
                        name="name",
                        value="value"
                    )]
                ),
                sqs_queue_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetSqsQueueParametersProperty(
                    message_deduplication_id="messageDeduplicationId",
                    message_group_id="messageGroupId"
                ),
                step_function_state_machine_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetStateMachineParametersProperty(
                    invocation_type="invocationType"
                ),
                timestream_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetTimestreamParametersProperty(
                    dimension_mappings=[pipes_mixins.CfnPipePropsMixin.DimensionMappingProperty(
                        dimension_name="dimensionName",
                        dimension_value="dimensionValue",
                        dimension_value_type="dimensionValueType"
                    )],
                    epoch_time_unit="epochTimeUnit",
                    multi_measure_mappings=[pipes_mixins.CfnPipePropsMixin.MultiMeasureMappingProperty(
                        multi_measure_attribute_mappings=[pipes_mixins.CfnPipePropsMixin.MultiMeasureAttributeMappingProperty(
                            measure_value="measureValue",
                            measure_value_type="measureValueType",
                            multi_measure_attribute_name="multiMeasureAttributeName"
                        )],
                        multi_measure_name="multiMeasureName"
                    )],
                    single_measure_mappings=[pipes_mixins.CfnPipePropsMixin.SingleMeasureMappingProperty(
                        measure_name="measureName",
                        measure_value="measureValue",
                        measure_value_type="measureValueType"
                    )],
                    time_field_type="timeFieldType",
                    timestamp_format="timestampFormat",
                    time_value="timeValue",
                    version_value="versionValue"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPipeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Pipes::Pipe``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b4cfc248bf3421337b859e918d823b790fd6561f131b34fc3f27c825e709a6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93e15d70561958cb4106b8785d295315803f96dfd162b4acfba938d67acb297b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb3346da746b98bb40e27489a958300b1dff5af318579957602350a0208d9c70)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPipeMixinProps:
        return typing.cast(CfnPipeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.AwsVpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "assign_public_ip": "assignPublicIp",
            "security_groups": "securityGroups",
            "subnets": "subnets",
        },
    )
    class AwsVpcConfigurationProperty:
        def __init__(
            self,
            *,
            assign_public_ip: typing.Optional[builtins.str] = None,
            security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This structure specifies the VPC subnets and security groups for the task, and whether a public IP address is to be used.

            This structure is relevant only for ECS tasks that use the ``awsvpc`` network mode.

            :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. You can specify ``ENABLED`` only when ``LaunchType`` in ``EcsParameters`` is set to ``FARGATE`` .
            :param security_groups: Specifies the security groups associated with the task. These security groups must all be in the same VPC. You can specify as many as five security groups. If you do not specify a security group, the default security group for the VPC is used.
            :param subnets: Specifies the subnets associated with the task. These subnets must all be in the same VPC. You can specify as many as 16 subnets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-awsvpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                aws_vpc_configuration_property = pipes_mixins.CfnPipePropsMixin.AwsVpcConfigurationProperty(
                    assign_public_ip="assignPublicIp",
                    security_groups=["securityGroups"],
                    subnets=["subnets"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__44b5ad67af28c0af0427637f3c6336b8c898959627fb40394b86705ce3238829)
                check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
                check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if assign_public_ip is not None:
                self._values["assign_public_ip"] = assign_public_ip
            if security_groups is not None:
                self._values["security_groups"] = security_groups
            if subnets is not None:
                self._values["subnets"] = subnets

        @builtins.property
        def assign_public_ip(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the task's elastic network interface receives a public IP address.

            You can specify ``ENABLED`` only when ``LaunchType`` in ``EcsParameters`` is set to ``FARGATE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-awsvpcconfiguration.html#cfn-pipes-pipe-awsvpcconfiguration-assignpublicip
            '''
            result = self._values.get("assign_public_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the security groups associated with the task.

            These security groups must all be in the same VPC. You can specify as many as five security groups. If you do not specify a security group, the default security group for the VPC is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-awsvpcconfiguration.html#cfn-pipes-pipe-awsvpcconfiguration-securitygroups
            '''
            result = self._values.get("security_groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the subnets associated with the task.

            These subnets must all be in the same VPC. You can specify as many as 16 subnets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-awsvpcconfiguration.html#cfn-pipes-pipe-awsvpcconfiguration-subnets
            '''
            result = self._values.get("subnets")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsVpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.BatchArrayPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"size": "size"},
    )
    class BatchArrayPropertiesProperty:
        def __init__(self, *, size: typing.Optional[jsii.Number] = None) -> None:
            '''The array properties for the submitted job, such as the size of the array.

            The array size can be between 2 and 10,000. If you specify array properties for a job, it becomes an array job. This parameter is used only if the target is an AWS Batch job.

            :param size: The size of the array, if this is an array batch job. Default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batcharrayproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                batch_array_properties_property = pipes_mixins.CfnPipePropsMixin.BatchArrayPropertiesProperty(
                    size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef19a87f06dc54331b8bf075cff1aa806435790709444ae65b9e04b7238b2cf2)
                check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if size is not None:
                self._values["size"] = size

        @builtins.property
        def size(self) -> typing.Optional[jsii.Number]:
            '''The size of the array, if this is an array batch job.

            :default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batcharrayproperties.html#cfn-pipes-pipe-batcharrayproperties-size
            '''
            result = self._values.get("size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchArrayPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.BatchContainerOverridesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "command": "command",
            "environment": "environment",
            "instance_type": "instanceType",
            "resource_requirements": "resourceRequirements",
        },
    )
    class BatchContainerOverridesProperty:
        def __init__(
            self,
            *,
            command: typing.Optional[typing.Sequence[builtins.str]] = None,
            environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.BatchEnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            instance_type: typing.Optional[builtins.str] = None,
            resource_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.BatchResourceRequirementProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The overrides that are sent to a container.

            :param command: The command to send to the container that overrides the default command from the Docker image or the task definition.
            :param environment: The environment variables to send to the container. You can add new environment variables, which are added to the container at launch, or you can override the existing environment variables from the Docker image or the task definition. .. epigraph:: Environment variables cannot start with " ``AWS Batch`` ". This naming convention is reserved for variables that AWS Batch sets.
            :param instance_type: The instance type to use for a multi-node parallel job. .. epigraph:: This parameter isn't applicable to single-node container jobs or jobs that run on Fargate resources, and shouldn't be provided.
            :param resource_requirements: The type and amount of resources to assign to a container. This overrides the settings in the job definition. The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchcontaineroverrides.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                batch_container_overrides_property = pipes_mixins.CfnPipePropsMixin.BatchContainerOverridesProperty(
                    command=["command"],
                    environment=[pipes_mixins.CfnPipePropsMixin.BatchEnvironmentVariableProperty(
                        name="name",
                        value="value"
                    )],
                    instance_type="instanceType",
                    resource_requirements=[pipes_mixins.CfnPipePropsMixin.BatchResourceRequirementProperty(
                        type="type",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6e2e5f61dfc1dd4f95551f261830fb9417c356503bed9c866a08210b9b3b5d02)
                check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument resource_requirements", value=resource_requirements, expected_type=type_hints["resource_requirements"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if command is not None:
                self._values["command"] = command
            if environment is not None:
                self._values["environment"] = environment
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if resource_requirements is not None:
                self._values["resource_requirements"] = resource_requirements

        @builtins.property
        def command(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The command to send to the container that overrides the default command from the Docker image or the task definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchcontaineroverrides.html#cfn-pipes-pipe-batchcontaineroverrides-command
            '''
            result = self._values.get("command")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def environment(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.BatchEnvironmentVariableProperty"]]]]:
            '''The environment variables to send to the container.

            You can add new environment variables, which are added to the container at launch, or you can override the existing environment variables from the Docker image or the task definition.
            .. epigraph::

               Environment variables cannot start with " ``AWS Batch`` ". This naming convention is reserved for variables that AWS Batch sets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchcontaineroverrides.html#cfn-pipes-pipe-batchcontaineroverrides-environment
            '''
            result = self._values.get("environment")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.BatchEnvironmentVariableProperty"]]]], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''The instance type to use for a multi-node parallel job.

            .. epigraph::

               This parameter isn't applicable to single-node container jobs or jobs that run on Fargate resources, and shouldn't be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchcontaineroverrides.html#cfn-pipes-pipe-batchcontaineroverrides-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_requirements(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.BatchResourceRequirementProperty"]]]]:
            '''The type and amount of resources to assign to a container.

            This overrides the settings in the job definition. The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchcontaineroverrides.html#cfn-pipes-pipe-batchcontaineroverrides-resourcerequirements
            '''
            result = self._values.get("resource_requirements")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.BatchResourceRequirementProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchContainerOverridesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.BatchEnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class BatchEnvironmentVariableProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The environment variables to send to the container.

            You can add new environment variables, which are added to the container at launch, or you can override the existing environment variables from the Docker image or the task definition.
            .. epigraph::

               Environment variables cannot start with " ``AWS Batch`` ". This naming convention is reserved for variables that AWS Batch sets.

            :param name: The name of the key-value pair. For environment variables, this is the name of the environment variable.
            :param value: The value of the key-value pair. For environment variables, this is the value of the environment variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchenvironmentvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                batch_environment_variable_property = pipes_mixins.CfnPipePropsMixin.BatchEnvironmentVariableProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6f6bcb246ae94b0471945891fed1d9e022ef0fd87247cbc6a485b895eb974491)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the key-value pair.

            For environment variables, this is the name of the environment variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchenvironmentvariable.html#cfn-pipes-pipe-batchenvironmentvariable-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the key-value pair.

            For environment variables, this is the value of the environment variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchenvironmentvariable.html#cfn-pipes-pipe-batchenvironmentvariable-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchEnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.BatchJobDependencyProperty",
        jsii_struct_bases=[],
        name_mapping={"job_id": "jobId", "type": "type"},
    )
    class BatchJobDependencyProperty:
        def __init__(
            self,
            *,
            job_id: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents an AWS Batch job dependency.

            :param job_id: The job ID of the AWS Batch job that's associated with this dependency.
            :param type: The type of the job dependency.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchjobdependency.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                batch_job_dependency_property = pipes_mixins.CfnPipePropsMixin.BatchJobDependencyProperty(
                    job_id="jobId",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__afc784218091b0612f74293033c6fbaee141346985fbd9b5ba71e8590b51c364)
                check_type(argname="argument job_id", value=job_id, expected_type=type_hints["job_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if job_id is not None:
                self._values["job_id"] = job_id
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def job_id(self) -> typing.Optional[builtins.str]:
            '''The job ID of the AWS Batch job that's associated with this dependency.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchjobdependency.html#cfn-pipes-pipe-batchjobdependency-jobid
            '''
            result = self._values.get("job_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the job dependency.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchjobdependency.html#cfn-pipes-pipe-batchjobdependency-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchJobDependencyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.BatchResourceRequirementProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class BatchResourceRequirementProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The type and amount of a resource to assign to a container.

            The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .

            :param type: The type of resource to assign to a container. The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .
            :param value: The quantity of the specified resource to reserve for the container. The values vary based on the ``type`` specified. - **type="GPU"** - The number of physical GPUs to reserve for the container. Make sure that the number of GPUs reserved for all containers in a job doesn't exceed the number of available GPUs on the compute resource that the job is launched on. .. epigraph:: GPUs aren't available for jobs that are running on Fargate resources. - **type="MEMORY"** - The memory hard limit (in MiB) present to the container. This parameter is supported for jobs that are running on EC2 resources. If your container attempts to exceed the memory specified, the container is terminated. This parameter maps to ``Memory`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--memory`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . You must specify at least 4 MiB of memory for a job. This is required but can be specified in several places for multi-node parallel (MNP) jobs. It must be specified for each node at least once. This parameter maps to ``Memory`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--memory`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: If you're trying to maximize your resource utilization by providing your jobs as much memory as possible for a particular instance type, see `Memory management <https://docs.aws.amazon.com/batch/latest/userguide/memory-management.html>`_ in the *AWS Batch User Guide* . For jobs that are running on Fargate resources, then ``value`` is the hard limit (in MiB), and must match one of the supported values and the ``VCPU`` values must be one of the values supported for that memory value. - **value = 512** - ``VCPU`` = 0.25 - **value = 1024** - ``VCPU`` = 0.25 or 0.5 - **value = 2048** - ``VCPU`` = 0.25, 0.5, or 1 - **value = 3072** - ``VCPU`` = 0.5, or 1 - **value = 4096** - ``VCPU`` = 0.5, 1, or 2 - **value = 5120, 6144, or 7168** - ``VCPU`` = 1 or 2 - **value = 8192** - ``VCPU`` = 1, 2, 4, or 8 - **value = 9216, 10240, 11264, 12288, 13312, 14336, or 15360** - ``VCPU`` = 2 or 4 - **value = 16384** - ``VCPU`` = 2, 4, or 8 - **value = 17408, 18432, 19456, 21504, 22528, 23552, 25600, 26624, 27648, 29696, or 30720** - ``VCPU`` = 4 - **value = 20480, 24576, or 28672** - ``VCPU`` = 4 or 8 - **value = 36864, 45056, 53248, or 61440** - ``VCPU`` = 8 - **value = 32768, 40960, 49152, or 57344** - ``VCPU`` = 8 or 16 - **value = 65536, 73728, 81920, 90112, 98304, 106496, 114688, or 122880** - ``VCPU`` = 16 - **type="VCPU"** - The number of vCPUs reserved for the container. This parameter maps to ``CpuShares`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--cpu-shares`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . Each vCPU is equivalent to 1,024 CPU shares. For EC2 resources, you must specify at least one vCPU. This is required but can be specified in several places; it must be specified for each node at least once. The default for the Fargate On-Demand vCPU resource count quota is 6 vCPUs. For more information about Fargate quotas, see `AWS Fargate quotas <https://docs.aws.amazon.com/general/latest/gr/ecs-service.html#service-quotas-fargate>`_ in the *AWS General Reference* . For jobs that are running on Fargate resources, then ``value`` must match one of the supported values and the ``MEMORY`` values must be one of the values supported for that ``VCPU`` value. The supported values are 0.25, 0.5, 1, 2, 4, 8, and 16 - **value = 0.25** - ``MEMORY`` = 512, 1024, or 2048 - **value = 0.5** - ``MEMORY`` = 1024, 2048, 3072, or 4096 - **value = 1** - ``MEMORY`` = 2048, 3072, 4096, 5120, 6144, 7168, or 8192 - **value = 2** - ``MEMORY`` = 4096, 5120, 6144, 7168, 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360, or 16384 - **value = 4** - ``MEMORY`` = 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360, 16384, 17408, 18432, 19456, 20480, 21504, 22528, 23552, 24576, 25600, 26624, 27648, 28672, 29696, or 30720 - **value = 8** - ``MEMORY`` = 16384, 20480, 24576, 28672, 32768, 36864, 40960, 45056, 49152, 53248, 57344, or 61440 - **value = 16** - ``MEMORY`` = 32768, 40960, 49152, 57344, 65536, 73728, 81920, 90112, 98304, 106496, 114688, or 122880

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchresourcerequirement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                batch_resource_requirement_property = pipes_mixins.CfnPipePropsMixin.BatchResourceRequirementProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2498914d3d5154bd88a1b325f8f97b80b5740f9483a65ab1a3b295888acd33d)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of resource to assign to a container.

            The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchresourcerequirement.html#cfn-pipes-pipe-batchresourcerequirement-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The quantity of the specified resource to reserve for the container. The values vary based on the ``type`` specified.

            - **type="GPU"** - The number of physical GPUs to reserve for the container. Make sure that the number of GPUs reserved for all containers in a job doesn't exceed the number of available GPUs on the compute resource that the job is launched on.

            .. epigraph::

               GPUs aren't available for jobs that are running on Fargate resources.

            - **type="MEMORY"** - The memory hard limit (in MiB) present to the container. This parameter is supported for jobs that are running on EC2 resources. If your container attempts to exceed the memory specified, the container is terminated. This parameter maps to ``Memory`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--memory`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . You must specify at least 4 MiB of memory for a job. This is required but can be specified in several places for multi-node parallel (MNP) jobs. It must be specified for each node at least once. This parameter maps to ``Memory`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--memory`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .

            .. epigraph::

               If you're trying to maximize your resource utilization by providing your jobs as much memory as possible for a particular instance type, see `Memory management <https://docs.aws.amazon.com/batch/latest/userguide/memory-management.html>`_ in the *AWS Batch User Guide* .

            For jobs that are running on Fargate resources, then ``value`` is the hard limit (in MiB), and must match one of the supported values and the ``VCPU`` values must be one of the values supported for that memory value.

            - **value = 512** - ``VCPU`` = 0.25
            - **value = 1024** - ``VCPU`` = 0.25 or 0.5
            - **value = 2048** - ``VCPU`` = 0.25, 0.5, or 1
            - **value = 3072** - ``VCPU`` = 0.5, or 1
            - **value = 4096** - ``VCPU`` = 0.5, 1, or 2
            - **value = 5120, 6144, or 7168** - ``VCPU`` = 1 or 2
            - **value = 8192** - ``VCPU`` = 1, 2, 4, or 8
            - **value = 9216, 10240, 11264, 12288, 13312, 14336, or 15360** - ``VCPU`` = 2 or 4
            - **value = 16384** - ``VCPU`` = 2, 4, or 8
            - **value = 17408, 18432, 19456, 21504, 22528, 23552, 25600, 26624, 27648, 29696, or 30720** - ``VCPU`` = 4
            - **value = 20480, 24576, or 28672** - ``VCPU`` = 4 or 8
            - **value = 36864, 45056, 53248, or 61440** - ``VCPU`` = 8
            - **value = 32768, 40960, 49152, or 57344** - ``VCPU`` = 8 or 16
            - **value = 65536, 73728, 81920, 90112, 98304, 106496, 114688, or 122880** - ``VCPU`` = 16
            - **type="VCPU"** - The number of vCPUs reserved for the container. This parameter maps to ``CpuShares`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--cpu-shares`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . Each vCPU is equivalent to 1,024 CPU shares. For EC2 resources, you must specify at least one vCPU. This is required but can be specified in several places; it must be specified for each node at least once.

            The default for the Fargate On-Demand vCPU resource count quota is 6 vCPUs. For more information about Fargate quotas, see `AWS Fargate quotas <https://docs.aws.amazon.com/general/latest/gr/ecs-service.html#service-quotas-fargate>`_ in the *AWS General Reference* .

            For jobs that are running on Fargate resources, then ``value`` must match one of the supported values and the ``MEMORY`` values must be one of the values supported for that ``VCPU`` value. The supported values are 0.25, 0.5, 1, 2, 4, 8, and 16

            - **value = 0.25** - ``MEMORY`` = 512, 1024, or 2048
            - **value = 0.5** - ``MEMORY`` = 1024, 2048, 3072, or 4096
            - **value = 1** - ``MEMORY`` = 2048, 3072, 4096, 5120, 6144, 7168, or 8192
            - **value = 2** - ``MEMORY`` = 4096, 5120, 6144, 7168, 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360, or 16384
            - **value = 4** - ``MEMORY`` = 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360, 16384, 17408, 18432, 19456, 20480, 21504, 22528, 23552, 24576, 25600, 26624, 27648, 28672, 29696, or 30720
            - **value = 8** - ``MEMORY`` = 16384, 20480, 24576, 28672, 32768, 36864, 40960, 45056, 49152, 53248, 57344, or 61440
            - **value = 16** - ``MEMORY`` = 32768, 40960, 49152, 57344, 65536, 73728, 81920, 90112, 98304, 106496, 114688, or 122880

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchresourcerequirement.html#cfn-pipes-pipe-batchresourcerequirement-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchResourceRequirementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.BatchRetryStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"attempts": "attempts"},
    )
    class BatchRetryStrategyProperty:
        def __init__(self, *, attempts: typing.Optional[jsii.Number] = None) -> None:
            '''The retry strategy that's associated with a job.

            For more information, see `Automated job retries <https://docs.aws.amazon.com/batch/latest/userguide/job_retries.html>`_ in the *AWS Batch User Guide* .

            :param attempts: The number of times to move a job to the ``RUNNABLE`` status. If the value of ``attempts`` is greater than one, the job is retried on failure the same number of attempts as the value. Default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchretrystrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                batch_retry_strategy_property = pipes_mixins.CfnPipePropsMixin.BatchRetryStrategyProperty(
                    attempts=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c245577631e8125d8bdc4038215eef32af92c2097c984c27b4b499239bfe7ce)
                check_type(argname="argument attempts", value=attempts, expected_type=type_hints["attempts"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attempts is not None:
                self._values["attempts"] = attempts

        @builtins.property
        def attempts(self) -> typing.Optional[jsii.Number]:
            '''The number of times to move a job to the ``RUNNABLE`` status.

            If the value of ``attempts`` is greater than one, the job is retried on failure the same number of attempts as the value.

            :default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-batchretrystrategy.html#cfn-pipes-pipe-batchretrystrategy-attempts
            '''
            result = self._values.get("attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchRetryStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.CapacityProviderStrategyItemProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base": "base",
            "capacity_provider": "capacityProvider",
            "weight": "weight",
        },
    )
    class CapacityProviderStrategyItemProperty:
        def __init__(
            self,
            *,
            base: typing.Optional[jsii.Number] = None,
            capacity_provider: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The details of a capacity provider strategy.

            To learn more, see `CapacityProviderStrategyItem <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_CapacityProviderStrategyItem.html>`_ in the Amazon ECS API Reference.

            :param base: The base value designates how many tasks, at a minimum, to run on the specified capacity provider. Only one capacity provider in a capacity provider strategy can have a base defined. If no value is specified, the default value of 0 is used. Default: - 0
            :param capacity_provider: The short name of the capacity provider.
            :param weight: The weight value designates the relative percentage of the total number of tasks launched that should use the specified capacity provider. The weight value is taken into consideration after the base value, if defined, is satisfied. Default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-capacityproviderstrategyitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                capacity_provider_strategy_item_property = pipes_mixins.CfnPipePropsMixin.CapacityProviderStrategyItemProperty(
                    base=123,
                    capacity_provider="capacityProvider",
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__399ae0a41ca3179f16fb8a41bd0500408118cca193b50b01aa507ec343a19128)
                check_type(argname="argument base", value=base, expected_type=type_hints["base"])
                check_type(argname="argument capacity_provider", value=capacity_provider, expected_type=type_hints["capacity_provider"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base is not None:
                self._values["base"] = base
            if capacity_provider is not None:
                self._values["capacity_provider"] = capacity_provider
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def base(self) -> typing.Optional[jsii.Number]:
            '''The base value designates how many tasks, at a minimum, to run on the specified capacity provider.

            Only one capacity provider in a capacity provider strategy can have a base defined. If no value is specified, the default value of 0 is used.

            :default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-capacityproviderstrategyitem.html#cfn-pipes-pipe-capacityproviderstrategyitem-base
            '''
            result = self._values.get("base")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def capacity_provider(self) -> typing.Optional[builtins.str]:
            '''The short name of the capacity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-capacityproviderstrategyitem.html#cfn-pipes-pipe-capacityproviderstrategyitem-capacityprovider
            '''
            result = self._values.get("capacity_provider")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''The weight value designates the relative percentage of the total number of tasks launched that should use the specified capacity provider.

            The weight value is taken into consideration after the base value, if defined, is satisfied.

            :default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-capacityproviderstrategyitem.html#cfn-pipes-pipe-capacityproviderstrategyitem-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityProviderStrategyItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.CloudwatchLogsLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_arn": "logGroupArn"},
    )
    class CloudwatchLogsLogDestinationProperty:
        def __init__(
            self,
            *,
            log_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the Amazon CloudWatch Logs logging configuration settings for the pipe.

            :param log_group_arn: The AWS Resource Name (ARN) for the CloudWatch log group to which EventBridge sends the log records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-cloudwatchlogslogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                cloudwatch_logs_log_destination_property = pipes_mixins.CfnPipePropsMixin.CloudwatchLogsLogDestinationProperty(
                    log_group_arn="logGroupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d5b7e1182e1d0c8aa6ac059365a50dde3cbaad0d5572b1af1e9d3ee6cdf7b43)
                check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_arn is not None:
                self._values["log_group_arn"] = log_group_arn

        @builtins.property
        def log_group_arn(self) -> typing.Optional[builtins.str]:
            '''The AWS Resource Name (ARN) for the CloudWatch log group to which EventBridge sends the log records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-cloudwatchlogslogdestination.html#cfn-pipes-pipe-cloudwatchlogslogdestination-loggrouparn
            '''
            result = self._values.get("log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudwatchLogsLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.DeadLetterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class DeadLetterConfigProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''A ``DeadLetterConfig`` object that contains information about a dead-letter queue configuration.

            :param arn: The ARN of the specified target for the dead-letter queue. For Amazon Kinesis stream and Amazon DynamoDB stream sources, specify either an Amazon SNS topic or Amazon SQS queue ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-deadletterconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                dead_letter_config_property = pipes_mixins.CfnPipePropsMixin.DeadLetterConfigProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6ce541cfa1113e7f395c36b8943c0a3a9f9bc55ded0114477c5887b6a510acb)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the specified target for the dead-letter queue.

            For Amazon Kinesis stream and Amazon DynamoDB stream sources, specify either an Amazon SNS topic or Amazon SQS queue ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-deadletterconfig.html#cfn-pipes-pipe-deadletterconfig-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeadLetterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.DimensionMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimension_name": "dimensionName",
            "dimension_value": "dimensionValue",
            "dimension_value_type": "dimensionValueType",
        },
    )
    class DimensionMappingProperty:
        def __init__(
            self,
            *,
            dimension_name: typing.Optional[builtins.str] = None,
            dimension_value: typing.Optional[builtins.str] = None,
            dimension_value_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Maps source data to a dimension in the target Timestream for LiveAnalytics table.

            For more information, see `Amazon Timestream for LiveAnalytics concepts <https://docs.aws.amazon.com/timestream/latest/developerguide/concepts.html>`_

            :param dimension_name: The metadata attributes of the time series. For example, the name and Availability Zone of an Amazon EC2 instance or the name of the manufacturer of a wind turbine are dimensions.
            :param dimension_value: Dynamic path to the dimension value in the source event.
            :param dimension_value_type: The data type of the dimension for the time-series data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-dimensionmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                dimension_mapping_property = pipes_mixins.CfnPipePropsMixin.DimensionMappingProperty(
                    dimension_name="dimensionName",
                    dimension_value="dimensionValue",
                    dimension_value_type="dimensionValueType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__983fb71a5f947c6deaf4d59cc8129647811ee17f98182b649aedbd0058774dd0)
                check_type(argname="argument dimension_name", value=dimension_name, expected_type=type_hints["dimension_name"])
                check_type(argname="argument dimension_value", value=dimension_value, expected_type=type_hints["dimension_value"])
                check_type(argname="argument dimension_value_type", value=dimension_value_type, expected_type=type_hints["dimension_value_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_name is not None:
                self._values["dimension_name"] = dimension_name
            if dimension_value is not None:
                self._values["dimension_value"] = dimension_value
            if dimension_value_type is not None:
                self._values["dimension_value_type"] = dimension_value_type

        @builtins.property
        def dimension_name(self) -> typing.Optional[builtins.str]:
            '''The metadata attributes of the time series.

            For example, the name and Availability Zone of an Amazon EC2 instance or the name of the manufacturer of a wind turbine are dimensions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-dimensionmapping.html#cfn-pipes-pipe-dimensionmapping-dimensionname
            '''
            result = self._values.get("dimension_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dimension_value(self) -> typing.Optional[builtins.str]:
            '''Dynamic path to the dimension value in the source event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-dimensionmapping.html#cfn-pipes-pipe-dimensionmapping-dimensionvalue
            '''
            result = self._values.get("dimension_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dimension_value_type(self) -> typing.Optional[builtins.str]:
            '''The data type of the dimension for the time-series data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-dimensionmapping.html#cfn-pipes-pipe-dimensionmapping-dimensionvaluetype
            '''
            result = self._values.get("dimension_value_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.EcsContainerOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={
            "command": "command",
            "cpu": "cpu",
            "environment": "environment",
            "environment_files": "environmentFiles",
            "memory": "memory",
            "memory_reservation": "memoryReservation",
            "name": "name",
            "resource_requirements": "resourceRequirements",
        },
    )
    class EcsContainerOverrideProperty:
        def __init__(
            self,
            *,
            command: typing.Optional[typing.Sequence[builtins.str]] = None,
            cpu: typing.Optional[jsii.Number] = None,
            environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.EcsEnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            environment_files: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.EcsEnvironmentFileProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            memory: typing.Optional[jsii.Number] = None,
            memory_reservation: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
            resource_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.EcsResourceRequirementProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The overrides that are sent to a container.

            An empty container override can be passed in. An example of an empty container override is ``{"containerOverrides": [ ] }`` . If a non-empty container override is specified, the ``name`` parameter must be included.

            :param command: The command to send to the container that overrides the default command from the Docker image or the task definition. You must also specify a container name.
            :param cpu: The number of ``cpu`` units reserved for the container, instead of the default value from the task definition. You must also specify a container name.
            :param environment: The environment variables to send to the container. You can add new environment variables, which are added to the container at launch, or you can override the existing environment variables from the Docker image or the task definition. You must also specify a container name.
            :param environment_files: A list of files containing the environment variables to pass to a container, instead of the value from the container definition.
            :param memory: The hard limit (in MiB) of memory to present to the container, instead of the default value from the task definition. If your container attempts to exceed the memory specified here, the container is killed. You must also specify a container name.
            :param memory_reservation: The soft limit (in MiB) of memory to reserve for the container, instead of the default value from the task definition. You must also specify a container name.
            :param name: The name of the container that receives the override. This parameter is required if any override is specified.
            :param resource_requirements: The type and amount of a resource to assign to a container, instead of the default value from the task definition. The only supported resource is a GPU.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecscontaineroverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                ecs_container_override_property = pipes_mixins.CfnPipePropsMixin.EcsContainerOverrideProperty(
                    command=["command"],
                    cpu=123,
                    environment=[pipes_mixins.CfnPipePropsMixin.EcsEnvironmentVariableProperty(
                        name="name",
                        value="value"
                    )],
                    environment_files=[pipes_mixins.CfnPipePropsMixin.EcsEnvironmentFileProperty(
                        type="type",
                        value="value"
                    )],
                    memory=123,
                    memory_reservation=123,
                    name="name",
                    resource_requirements=[pipes_mixins.CfnPipePropsMixin.EcsResourceRequirementProperty(
                        type="type",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94c363acbf007019d44a8037f7251d00d23d526c9d63e543f705f02dc06cca93)
                check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
                check_type(argname="argument environment_files", value=environment_files, expected_type=type_hints["environment_files"])
                check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
                check_type(argname="argument memory_reservation", value=memory_reservation, expected_type=type_hints["memory_reservation"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument resource_requirements", value=resource_requirements, expected_type=type_hints["resource_requirements"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if command is not None:
                self._values["command"] = command
            if cpu is not None:
                self._values["cpu"] = cpu
            if environment is not None:
                self._values["environment"] = environment
            if environment_files is not None:
                self._values["environment_files"] = environment_files
            if memory is not None:
                self._values["memory"] = memory
            if memory_reservation is not None:
                self._values["memory_reservation"] = memory_reservation
            if name is not None:
                self._values["name"] = name
            if resource_requirements is not None:
                self._values["resource_requirements"] = resource_requirements

        @builtins.property
        def command(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The command to send to the container that overrides the default command from the Docker image or the task definition.

            You must also specify a container name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecscontaineroverride.html#cfn-pipes-pipe-ecscontaineroverride-command
            '''
            result = self._values.get("command")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def cpu(self) -> typing.Optional[jsii.Number]:
            '''The number of ``cpu`` units reserved for the container, instead of the default value from the task definition.

            You must also specify a container name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecscontaineroverride.html#cfn-pipes-pipe-ecscontaineroverride-cpu
            '''
            result = self._values.get("cpu")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def environment(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.EcsEnvironmentVariableProperty"]]]]:
            '''The environment variables to send to the container.

            You can add new environment variables, which are added to the container at launch, or you can override the existing environment variables from the Docker image or the task definition. You must also specify a container name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecscontaineroverride.html#cfn-pipes-pipe-ecscontaineroverride-environment
            '''
            result = self._values.get("environment")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.EcsEnvironmentVariableProperty"]]]], result)

        @builtins.property
        def environment_files(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.EcsEnvironmentFileProperty"]]]]:
            '''A list of files containing the environment variables to pass to a container, instead of the value from the container definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecscontaineroverride.html#cfn-pipes-pipe-ecscontaineroverride-environmentfiles
            '''
            result = self._values.get("environment_files")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.EcsEnvironmentFileProperty"]]]], result)

        @builtins.property
        def memory(self) -> typing.Optional[jsii.Number]:
            '''The hard limit (in MiB) of memory to present to the container, instead of the default value from the task definition.

            If your container attempts to exceed the memory specified here, the container is killed. You must also specify a container name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecscontaineroverride.html#cfn-pipes-pipe-ecscontaineroverride-memory
            '''
            result = self._values.get("memory")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def memory_reservation(self) -> typing.Optional[jsii.Number]:
            '''The soft limit (in MiB) of memory to reserve for the container, instead of the default value from the task definition.

            You must also specify a container name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecscontaineroverride.html#cfn-pipes-pipe-ecscontaineroverride-memoryreservation
            '''
            result = self._values.get("memory_reservation")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the container that receives the override.

            This parameter is required if any override is specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecscontaineroverride.html#cfn-pipes-pipe-ecscontaineroverride-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_requirements(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.EcsResourceRequirementProperty"]]]]:
            '''The type and amount of a resource to assign to a container, instead of the default value from the task definition.

            The only supported resource is a GPU.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecscontaineroverride.html#cfn-pipes-pipe-ecscontaineroverride-resourcerequirements
            '''
            result = self._values.get("resource_requirements")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.EcsResourceRequirementProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsContainerOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.EcsEnvironmentFileProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class EcsEnvironmentFileProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of files containing the environment variables to pass to a container.

            You can specify up to ten environment files. The file must have a ``.env`` file extension. Each line in an environment file should contain an environment variable in ``VARIABLE=VALUE`` format. Lines beginning with ``#`` are treated as comments and are ignored. For more information about the environment variable file syntax, see `Declare default environment variables in file <https://docs.aws.amazon.com/https://docs.docker.com/compose/env-file/>`_ .

            If there are environment variables specified using the ``environment`` parameter in a container definition, they take precedence over the variables contained within an environment file. If multiple environment files are specified that contain the same variable, they're processed from the top down. We recommend that you use unique variable names. For more information, see `Specifying environment variables <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/taskdef-envfiles.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            This parameter is only supported for tasks hosted on Fargate using the following platform versions:

            - Linux platform version ``1.4.0`` or later.
            - Windows platform version ``1.0.0`` or later.

            :param type: The file type to use. The only supported value is ``s3`` .
            :param value: The Amazon Resource Name (ARN) of the Amazon S3 object containing the environment variable file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecsenvironmentfile.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                ecs_environment_file_property = pipes_mixins.CfnPipePropsMixin.EcsEnvironmentFileProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f911845708b5d561986e78a483aff0106fcf26968ff2c96ab2468c413fdf719d)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The file type to use.

            The only supported value is ``s3`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecsenvironmentfile.html#cfn-pipes-pipe-ecsenvironmentfile-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon S3 object containing the environment variable file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecsenvironmentfile.html#cfn-pipes-pipe-ecsenvironmentfile-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsEnvironmentFileProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.EcsEnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EcsEnvironmentVariableProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The environment variables to send to the container.

            You can add new environment variables, which are added to the container at launch, or you can override the existing environment variables from the Docker image or the task definition. You must also specify a container name.

            :param name: The name of the key-value pair. For environment variables, this is the name of the environment variable.
            :param value: The value of the key-value pair. For environment variables, this is the value of the environment variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecsenvironmentvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                ecs_environment_variable_property = pipes_mixins.CfnPipePropsMixin.EcsEnvironmentVariableProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4dcccc46f199ca32ec6a98f721697780bb9504613a0317fab947fa141c6be581)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the key-value pair.

            For environment variables, this is the name of the environment variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecsenvironmentvariable.html#cfn-pipes-pipe-ecsenvironmentvariable-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the key-value pair.

            For environment variables, this is the value of the environment variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecsenvironmentvariable.html#cfn-pipes-pipe-ecsenvironmentvariable-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsEnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.EcsEphemeralStorageProperty",
        jsii_struct_bases=[],
        name_mapping={"size_in_gib": "sizeInGiB"},
    )
    class EcsEphemeralStorageProperty:
        def __init__(self, *, size_in_gib: typing.Optional[jsii.Number] = None) -> None:
            '''The amount of ephemeral storage to allocate for the task.

            This parameter is used to expand the total amount of ephemeral storage available, beyond the default amount, for tasks hosted on Fargate. For more information, see `Fargate task storage <https://docs.aws.amazon.com/AmazonECS/latest/userguide/using_data_volumes.html>`_ in the *Amazon ECS User Guide for Fargate* .
            .. epigraph::

               This parameter is only supported for tasks hosted on Fargate using Linux platform version ``1.4.0`` or later. This parameter is not supported for Windows containers on Fargate.

            :param size_in_gib: The total amount, in GiB, of ephemeral storage to set for the task. The minimum supported value is ``21`` GiB and the maximum supported value is ``200`` GiB. Default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecsephemeralstorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                ecs_ephemeral_storage_property = pipes_mixins.CfnPipePropsMixin.EcsEphemeralStorageProperty(
                    size_in_gi_b=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8abbcabfba8de1a4ffcd5f64ffcb0c757672a9a96ae6252b400cd3961dce3956)
                check_type(argname="argument size_in_gib", value=size_in_gib, expected_type=type_hints["size_in_gib"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if size_in_gib is not None:
                self._values["size_in_gib"] = size_in_gib

        @builtins.property
        def size_in_gib(self) -> typing.Optional[jsii.Number]:
            '''The total amount, in GiB, of ephemeral storage to set for the task.

            The minimum supported value is ``21`` GiB and the maximum supported value is ``200`` GiB.

            :default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecsephemeralstorage.html#cfn-pipes-pipe-ecsephemeralstorage-sizeingib
            '''
            result = self._values.get("size_in_gib")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsEphemeralStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.EcsInferenceAcceleratorOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={"device_name": "deviceName", "device_type": "deviceType"},
    )
    class EcsInferenceAcceleratorOverrideProperty:
        def __init__(
            self,
            *,
            device_name: typing.Optional[builtins.str] = None,
            device_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details on an Elastic Inference accelerator task override.

            This parameter is used to override the Elastic Inference accelerator specified in the task definition. For more information, see `Working with Amazon Elastic Inference on Amazon ECS <https://docs.aws.amazon.com/AmazonECS/latest/userguide/ecs-inference.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :param device_name: The Elastic Inference accelerator device name to override for the task. This parameter must match a ``deviceName`` specified in the task definition.
            :param device_type: The Elastic Inference accelerator type to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecsinferenceacceleratoroverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                ecs_inference_accelerator_override_property = pipes_mixins.CfnPipePropsMixin.EcsInferenceAcceleratorOverrideProperty(
                    device_name="deviceName",
                    device_type="deviceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b8dafbf43d2c1a129c02808296de4532f727a5ceb1947aa8c07fc2e7002dce80)
                check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
                check_type(argname="argument device_type", value=device_type, expected_type=type_hints["device_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if device_name is not None:
                self._values["device_name"] = device_name
            if device_type is not None:
                self._values["device_type"] = device_type

        @builtins.property
        def device_name(self) -> typing.Optional[builtins.str]:
            '''The Elastic Inference accelerator device name to override for the task.

            This parameter must match a ``deviceName`` specified in the task definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecsinferenceacceleratoroverride.html#cfn-pipes-pipe-ecsinferenceacceleratoroverride-devicename
            '''
            result = self._values.get("device_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_type(self) -> typing.Optional[builtins.str]:
            '''The Elastic Inference accelerator type to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecsinferenceacceleratoroverride.html#cfn-pipes-pipe-ecsinferenceacceleratoroverride-devicetype
            '''
            result = self._values.get("device_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsInferenceAcceleratorOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.EcsResourceRequirementProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class EcsResourceRequirementProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The type and amount of a resource to assign to a container.

            The supported resource types are GPUs and Elastic Inference accelerators. For more information, see `Working with GPUs on Amazon ECS <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-gpu.html>`_ or `Working with Amazon Elastic Inference on Amazon ECS <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-inference.html>`_ in the *Amazon Elastic Container Service Developer Guide*

            :param type: The type of resource to assign to a container. The supported values are ``GPU`` or ``InferenceAccelerator`` .
            :param value: The value for the specified resource type. If the ``GPU`` type is used, the value is the number of physical ``GPUs`` the Amazon ECS container agent reserves for the container. The number of GPUs that's reserved for all containers in a task can't exceed the number of available GPUs on the container instance that the task is launched on. If the ``InferenceAccelerator`` type is used, the ``value`` matches the ``deviceName`` for an InferenceAccelerator specified in a task definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecsresourcerequirement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                ecs_resource_requirement_property = pipes_mixins.CfnPipePropsMixin.EcsResourceRequirementProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1af0a0a3f0c62f933a27ff2f5a4aa11b3d41b51121f3fd0c5cf2bb4fc8481bcb)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of resource to assign to a container.

            The supported values are ``GPU`` or ``InferenceAccelerator`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecsresourcerequirement.html#cfn-pipes-pipe-ecsresourcerequirement-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value for the specified resource type.

            If the ``GPU`` type is used, the value is the number of physical ``GPUs`` the Amazon ECS container agent reserves for the container. The number of GPUs that's reserved for all containers in a task can't exceed the number of available GPUs on the container instance that the task is launched on.

            If the ``InferenceAccelerator`` type is used, the ``value`` matches the ``deviceName`` for an InferenceAccelerator specified in a task definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecsresourcerequirement.html#cfn-pipes-pipe-ecsresourcerequirement-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsResourceRequirementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.EcsTaskOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_overrides": "containerOverrides",
            "cpu": "cpu",
            "ephemeral_storage": "ephemeralStorage",
            "execution_role_arn": "executionRoleArn",
            "inference_accelerator_overrides": "inferenceAcceleratorOverrides",
            "memory": "memory",
            "task_role_arn": "taskRoleArn",
        },
    )
    class EcsTaskOverrideProperty:
        def __init__(
            self,
            *,
            container_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.EcsContainerOverrideProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            cpu: typing.Optional[builtins.str] = None,
            ephemeral_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.EcsEphemeralStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            execution_role_arn: typing.Optional[builtins.str] = None,
            inference_accelerator_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.EcsInferenceAcceleratorOverrideProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            memory: typing.Optional[builtins.str] = None,
            task_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The overrides that are associated with a task.

            :param container_overrides: One or more container overrides that are sent to a task.
            :param cpu: The cpu override for the task.
            :param ephemeral_storage: The ephemeral storage setting override for the task. .. epigraph:: This parameter is only supported for tasks hosted on Fargate that use the following platform versions: - Linux platform version ``1.4.0`` or later. - Windows platform version ``1.0.0`` or later.
            :param execution_role_arn: The Amazon Resource Name (ARN) of the task execution IAM role override for the task. For more information, see `Amazon ECS task execution IAM role <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param inference_accelerator_overrides: The Elastic Inference accelerator override for the task.
            :param memory: The memory override for the task.
            :param task_role_arn: The Amazon Resource Name (ARN) of the IAM role that containers in this task can assume. All containers in this task are granted the permissions that are specified in this role. For more information, see `IAM Role for Tasks <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecstaskoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                ecs_task_override_property = pipes_mixins.CfnPipePropsMixin.EcsTaskOverrideProperty(
                    container_overrides=[pipes_mixins.CfnPipePropsMixin.EcsContainerOverrideProperty(
                        command=["command"],
                        cpu=123,
                        environment=[pipes_mixins.CfnPipePropsMixin.EcsEnvironmentVariableProperty(
                            name="name",
                            value="value"
                        )],
                        environment_files=[pipes_mixins.CfnPipePropsMixin.EcsEnvironmentFileProperty(
                            type="type",
                            value="value"
                        )],
                        memory=123,
                        memory_reservation=123,
                        name="name",
                        resource_requirements=[pipes_mixins.CfnPipePropsMixin.EcsResourceRequirementProperty(
                            type="type",
                            value="value"
                        )]
                    )],
                    cpu="cpu",
                    ephemeral_storage=pipes_mixins.CfnPipePropsMixin.EcsEphemeralStorageProperty(
                        size_in_gi_b=123
                    ),
                    execution_role_arn="executionRoleArn",
                    inference_accelerator_overrides=[pipes_mixins.CfnPipePropsMixin.EcsInferenceAcceleratorOverrideProperty(
                        device_name="deviceName",
                        device_type="deviceType"
                    )],
                    memory="memory",
                    task_role_arn="taskRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d704c6da4d6cad333ded62101495044551d08f8b8dce9fb02f29cab2af51a243)
                check_type(argname="argument container_overrides", value=container_overrides, expected_type=type_hints["container_overrides"])
                check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                check_type(argname="argument ephemeral_storage", value=ephemeral_storage, expected_type=type_hints["ephemeral_storage"])
                check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
                check_type(argname="argument inference_accelerator_overrides", value=inference_accelerator_overrides, expected_type=type_hints["inference_accelerator_overrides"])
                check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
                check_type(argname="argument task_role_arn", value=task_role_arn, expected_type=type_hints["task_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_overrides is not None:
                self._values["container_overrides"] = container_overrides
            if cpu is not None:
                self._values["cpu"] = cpu
            if ephemeral_storage is not None:
                self._values["ephemeral_storage"] = ephemeral_storage
            if execution_role_arn is not None:
                self._values["execution_role_arn"] = execution_role_arn
            if inference_accelerator_overrides is not None:
                self._values["inference_accelerator_overrides"] = inference_accelerator_overrides
            if memory is not None:
                self._values["memory"] = memory
            if task_role_arn is not None:
                self._values["task_role_arn"] = task_role_arn

        @builtins.property
        def container_overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.EcsContainerOverrideProperty"]]]]:
            '''One or more container overrides that are sent to a task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecstaskoverride.html#cfn-pipes-pipe-ecstaskoverride-containeroverrides
            '''
            result = self._values.get("container_overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.EcsContainerOverrideProperty"]]]], result)

        @builtins.property
        def cpu(self) -> typing.Optional[builtins.str]:
            '''The cpu override for the task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecstaskoverride.html#cfn-pipes-pipe-ecstaskoverride-cpu
            '''
            result = self._values.get("cpu")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ephemeral_storage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.EcsEphemeralStorageProperty"]]:
            '''The ephemeral storage setting override for the task.

            .. epigraph::

               This parameter is only supported for tasks hosted on Fargate that use the following platform versions:

               - Linux platform version ``1.4.0`` or later.
               - Windows platform version ``1.0.0`` or later.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecstaskoverride.html#cfn-pipes-pipe-ecstaskoverride-ephemeralstorage
            '''
            result = self._values.get("ephemeral_storage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.EcsEphemeralStorageProperty"]], result)

        @builtins.property
        def execution_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the task execution IAM role override for the task.

            For more information, see `Amazon ECS task execution IAM role <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecstaskoverride.html#cfn-pipes-pipe-ecstaskoverride-executionrolearn
            '''
            result = self._values.get("execution_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inference_accelerator_overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.EcsInferenceAcceleratorOverrideProperty"]]]]:
            '''The Elastic Inference accelerator override for the task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecstaskoverride.html#cfn-pipes-pipe-ecstaskoverride-inferenceacceleratoroverrides
            '''
            result = self._values.get("inference_accelerator_overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.EcsInferenceAcceleratorOverrideProperty"]]]], result)

        @builtins.property
        def memory(self) -> typing.Optional[builtins.str]:
            '''The memory override for the task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecstaskoverride.html#cfn-pipes-pipe-ecstaskoverride-memory
            '''
            result = self._values.get("memory")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def task_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role that containers in this task can assume.

            All containers in this task are granted the permissions that are specified in this role. For more information, see `IAM Role for Tasks <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-ecstaskoverride.html#cfn-pipes-pipe-ecstaskoverride-taskrolearn
            '''
            result = self._values.get("task_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsTaskOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.FilterCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={"filters": "filters"},
    )
    class FilterCriteriaProperty:
        def __init__(
            self,
            *,
            filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.FilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The collection of event patterns used to filter events.

            To remove a filter, specify a ``FilterCriteria`` object with an empty array of ``Filter`` objects.

            For more information, see `Events and Event Patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html>`_ in the *Amazon EventBridge User Guide* .

            :param filters: The event patterns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-filtercriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                filter_criteria_property = pipes_mixins.CfnPipePropsMixin.FilterCriteriaProperty(
                    filters=[pipes_mixins.CfnPipePropsMixin.FilterProperty(
                        pattern="pattern"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4091d89f1289b8be0c72adc12a05d0ced68fe183292011373cb6f5668c6cc8f2)
                check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filters is not None:
                self._values["filters"] = filters

        @builtins.property
        def filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.FilterProperty"]]]]:
            '''The event patterns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-filtercriteria.html#cfn-pipes-pipe-filtercriteria-filters
            '''
            result = self._values.get("filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.FilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={"pattern": "pattern"},
    )
    class FilterProperty:
        def __init__(self, *, pattern: typing.Optional[builtins.str] = None) -> None:
            '''Filter events using an event pattern.

            For more information, see `Events and Event Patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html>`_ in the *Amazon EventBridge User Guide* .

            :param pattern: The event pattern.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                filter_property = pipes_mixins.CfnPipePropsMixin.FilterProperty(
                    pattern="pattern"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80e8987ab978bce880b6acc30f89c0e585fd2629ca8fef9a1d1d9cc2eb96d4c4)
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pattern is not None:
                self._values["pattern"] = pattern

        @builtins.property
        def pattern(self) -> typing.Optional[builtins.str]:
            '''The event pattern.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-filter.html#cfn-pipes-pipe-filter-pattern
            '''
            result = self._values.get("pattern")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.FirehoseLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"delivery_stream_arn": "deliveryStreamArn"},
    )
    class FirehoseLogDestinationProperty:
        def __init__(
            self,
            *,
            delivery_stream_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the Amazon Data Firehose logging configuration settings for the pipe.

            :param delivery_stream_arn: The Amazon Resource Name (ARN) of the Firehose delivery stream to which EventBridge delivers the pipe log records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-firehoselogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                firehose_log_destination_property = pipes_mixins.CfnPipePropsMixin.FirehoseLogDestinationProperty(
                    delivery_stream_arn="deliveryStreamArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a5ef8091a17304671903e693e5afff6cd6162a073f4bdccf4328f86951b637ac)
                check_type(argname="argument delivery_stream_arn", value=delivery_stream_arn, expected_type=type_hints["delivery_stream_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_stream_arn is not None:
                self._values["delivery_stream_arn"] = delivery_stream_arn

        @builtins.property
        def delivery_stream_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Firehose delivery stream to which EventBridge delivers the pipe log records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-firehoselogdestination.html#cfn-pipes-pipe-firehoselogdestination-deliverystreamarn
            '''
            result = self._values.get("delivery_stream_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirehoseLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.MQBrokerAccessCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"basic_auth": "basicAuth"},
    )
    class MQBrokerAccessCredentialsProperty:
        def __init__(self, *, basic_auth: typing.Optional[builtins.str] = None) -> None:
            '''The AWS Secrets Manager secret that stores your broker credentials.

            :param basic_auth: The ARN of the Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-mqbrokeraccesscredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                m_qBroker_access_credentials_property = pipes_mixins.CfnPipePropsMixin.MQBrokerAccessCredentialsProperty(
                    basic_auth="basicAuth"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d3bfbf3a39f65b35c30e1e0763be6278ece6c909b7b6bfd2e3416862b3e0c992)
                check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if basic_auth is not None:
                self._values["basic_auth"] = basic_auth

        @builtins.property
        def basic_auth(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-mqbrokeraccesscredentials.html#cfn-pipes-pipe-mqbrokeraccesscredentials-basicauth
            '''
            result = self._values.get("basic_auth")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MQBrokerAccessCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.MSKAccessCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_certificate_tls_auth": "clientCertificateTlsAuth",
            "sasl_scram512_auth": "saslScram512Auth",
        },
    )
    class MSKAccessCredentialsProperty:
        def __init__(
            self,
            *,
            client_certificate_tls_auth: typing.Optional[builtins.str] = None,
            sasl_scram512_auth: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The AWS Secrets Manager secret that stores your stream credentials.

            :param client_certificate_tls_auth: The ARN of the Secrets Manager secret.
            :param sasl_scram512_auth: The ARN of the Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-mskaccesscredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                m_sKAccess_credentials_property = pipes_mixins.CfnPipePropsMixin.MSKAccessCredentialsProperty(
                    client_certificate_tls_auth="clientCertificateTlsAuth",
                    sasl_scram512_auth="saslScram512Auth"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b57aeccd892e83487efdb948f5d1d34e6d922e063aacfd83671024417574fba5)
                check_type(argname="argument client_certificate_tls_auth", value=client_certificate_tls_auth, expected_type=type_hints["client_certificate_tls_auth"])
                check_type(argname="argument sasl_scram512_auth", value=sasl_scram512_auth, expected_type=type_hints["sasl_scram512_auth"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_certificate_tls_auth is not None:
                self._values["client_certificate_tls_auth"] = client_certificate_tls_auth
            if sasl_scram512_auth is not None:
                self._values["sasl_scram512_auth"] = sasl_scram512_auth

        @builtins.property
        def client_certificate_tls_auth(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-mskaccesscredentials.html#cfn-pipes-pipe-mskaccesscredentials-clientcertificatetlsauth
            '''
            result = self._values.get("client_certificate_tls_auth")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sasl_scram512_auth(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-mskaccesscredentials.html#cfn-pipes-pipe-mskaccesscredentials-saslscram512auth
            '''
            result = self._values.get("sasl_scram512_auth")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MSKAccessCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.MultiMeasureAttributeMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "measure_value": "measureValue",
            "measure_value_type": "measureValueType",
            "multi_measure_attribute_name": "multiMeasureAttributeName",
        },
    )
    class MultiMeasureAttributeMappingProperty:
        def __init__(
            self,
            *,
            measure_value: typing.Optional[builtins.str] = None,
            measure_value_type: typing.Optional[builtins.str] = None,
            multi_measure_attribute_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A mapping of a source event data field to a measure in a Timestream for LiveAnalytics record.

            :param measure_value: Dynamic path to the measurement attribute in the source event.
            :param measure_value_type: Data type of the measurement attribute in the source event.
            :param multi_measure_attribute_name: Target measure name to be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-multimeasureattributemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                multi_measure_attribute_mapping_property = pipes_mixins.CfnPipePropsMixin.MultiMeasureAttributeMappingProperty(
                    measure_value="measureValue",
                    measure_value_type="measureValueType",
                    multi_measure_attribute_name="multiMeasureAttributeName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3fc725bd50cde770d498874e1eb83cfe44ee9d8af620cc35fc0944671cf2fdc4)
                check_type(argname="argument measure_value", value=measure_value, expected_type=type_hints["measure_value"])
                check_type(argname="argument measure_value_type", value=measure_value_type, expected_type=type_hints["measure_value_type"])
                check_type(argname="argument multi_measure_attribute_name", value=multi_measure_attribute_name, expected_type=type_hints["multi_measure_attribute_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if measure_value is not None:
                self._values["measure_value"] = measure_value
            if measure_value_type is not None:
                self._values["measure_value_type"] = measure_value_type
            if multi_measure_attribute_name is not None:
                self._values["multi_measure_attribute_name"] = multi_measure_attribute_name

        @builtins.property
        def measure_value(self) -> typing.Optional[builtins.str]:
            '''Dynamic path to the measurement attribute in the source event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-multimeasureattributemapping.html#cfn-pipes-pipe-multimeasureattributemapping-measurevalue
            '''
            result = self._values.get("measure_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def measure_value_type(self) -> typing.Optional[builtins.str]:
            '''Data type of the measurement attribute in the source event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-multimeasureattributemapping.html#cfn-pipes-pipe-multimeasureattributemapping-measurevaluetype
            '''
            result = self._values.get("measure_value_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def multi_measure_attribute_name(self) -> typing.Optional[builtins.str]:
            '''Target measure name to be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-multimeasureattributemapping.html#cfn-pipes-pipe-multimeasureattributemapping-multimeasureattributename
            '''
            result = self._values.get("multi_measure_attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiMeasureAttributeMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.MultiMeasureMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "multi_measure_attribute_mappings": "multiMeasureAttributeMappings",
            "multi_measure_name": "multiMeasureName",
        },
    )
    class MultiMeasureMappingProperty:
        def __init__(
            self,
            *,
            multi_measure_attribute_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.MultiMeasureAttributeMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            multi_measure_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Maps multiple measures from the source event to the same Timestream for LiveAnalytics record.

            For more information, see `Amazon Timestream for LiveAnalytics concepts <https://docs.aws.amazon.com/timestream/latest/developerguide/concepts.html>`_

            :param multi_measure_attribute_mappings: Mappings that represent multiple source event fields mapped to measures in the same Timestream for LiveAnalytics record.
            :param multi_measure_name: The name of the multiple measurements per record (multi-measure).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-multimeasuremapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                multi_measure_mapping_property = pipes_mixins.CfnPipePropsMixin.MultiMeasureMappingProperty(
                    multi_measure_attribute_mappings=[pipes_mixins.CfnPipePropsMixin.MultiMeasureAttributeMappingProperty(
                        measure_value="measureValue",
                        measure_value_type="measureValueType",
                        multi_measure_attribute_name="multiMeasureAttributeName"
                    )],
                    multi_measure_name="multiMeasureName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8cc5761092dfc246134e09326490d476a35311ea71d3a848167091bba604a093)
                check_type(argname="argument multi_measure_attribute_mappings", value=multi_measure_attribute_mappings, expected_type=type_hints["multi_measure_attribute_mappings"])
                check_type(argname="argument multi_measure_name", value=multi_measure_name, expected_type=type_hints["multi_measure_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if multi_measure_attribute_mappings is not None:
                self._values["multi_measure_attribute_mappings"] = multi_measure_attribute_mappings
            if multi_measure_name is not None:
                self._values["multi_measure_name"] = multi_measure_name

        @builtins.property
        def multi_measure_attribute_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.MultiMeasureAttributeMappingProperty"]]]]:
            '''Mappings that represent multiple source event fields mapped to measures in the same Timestream for LiveAnalytics record.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-multimeasuremapping.html#cfn-pipes-pipe-multimeasuremapping-multimeasureattributemappings
            '''
            result = self._values.get("multi_measure_attribute_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.MultiMeasureAttributeMappingProperty"]]]], result)

        @builtins.property
        def multi_measure_name(self) -> typing.Optional[builtins.str]:
            '''The name of the multiple measurements per record (multi-measure).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-multimeasuremapping.html#cfn-pipes-pipe-multimeasuremapping-multimeasurename
            '''
            result = self._values.get("multi_measure_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiMeasureMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"awsvpc_configuration": "awsvpcConfiguration"},
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            awsvpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.AwsVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This structure specifies the network configuration for an Amazon ECS task.

            :param awsvpc_configuration: Use this structure to specify the VPC subnets and security groups for the task, and whether a public IP address is to be used. This structure is relevant only for ECS tasks that use the ``awsvpc`` network mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                network_configuration_property = pipes_mixins.CfnPipePropsMixin.NetworkConfigurationProperty(
                    awsvpc_configuration=pipes_mixins.CfnPipePropsMixin.AwsVpcConfigurationProperty(
                        assign_public_ip="assignPublicIp",
                        security_groups=["securityGroups"],
                        subnets=["subnets"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d5f6a45b025e0955b608e58280390ac549fd05326bc0b45912440abd33b96d8)
                check_type(argname="argument awsvpc_configuration", value=awsvpc_configuration, expected_type=type_hints["awsvpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if awsvpc_configuration is not None:
                self._values["awsvpc_configuration"] = awsvpc_configuration

        @builtins.property
        def awsvpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.AwsVpcConfigurationProperty"]]:
            '''Use this structure to specify the VPC subnets and security groups for the task, and whether a public IP address is to be used.

            This structure is relevant only for ECS tasks that use the ``awsvpc`` network mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-networkconfiguration.html#cfn-pipes-pipe-networkconfiguration-awsvpcconfiguration
            '''
            result = self._values.get("awsvpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.AwsVpcConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeEnrichmentHttpParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "header_parameters": "headerParameters",
            "path_parameter_values": "pathParameterValues",
            "query_string_parameters": "queryStringParameters",
        },
    )
    class PipeEnrichmentHttpParametersProperty:
        def __init__(
            self,
            *,
            header_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            query_string_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''These are custom parameter to be used when the target is an API Gateway REST APIs or EventBridge ApiDestinations.

            In the latter case, these are merged with any InvocationParameters specified on the Connection, with any values from the Connection taking precedence.

            :param header_parameters: The headers that need to be sent as part of request invoking the API Gateway REST API or EventBridge ApiDestination.
            :param path_parameter_values: The path parameter values to be used to populate API Gateway REST API or EventBridge ApiDestination path wildcards ("*").
            :param query_string_parameters: The query string keys/values that need to be sent as part of request invoking the API Gateway REST API or EventBridge ApiDestination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipeenrichmenthttpparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_enrichment_http_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeEnrichmentHttpParametersProperty(
                    header_parameters={
                        "header_parameters_key": "headerParameters"
                    },
                    path_parameter_values=["pathParameterValues"],
                    query_string_parameters={
                        "query_string_parameters_key": "queryStringParameters"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__54107ffcd4574854c8f4ab89c71e40ecd055b79bbd914f11a2d96133090ddc23)
                check_type(argname="argument header_parameters", value=header_parameters, expected_type=type_hints["header_parameters"])
                check_type(argname="argument path_parameter_values", value=path_parameter_values, expected_type=type_hints["path_parameter_values"])
                check_type(argname="argument query_string_parameters", value=query_string_parameters, expected_type=type_hints["query_string_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if header_parameters is not None:
                self._values["header_parameters"] = header_parameters
            if path_parameter_values is not None:
                self._values["path_parameter_values"] = path_parameter_values
            if query_string_parameters is not None:
                self._values["query_string_parameters"] = query_string_parameters

        @builtins.property
        def header_parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The headers that need to be sent as part of request invoking the API Gateway REST API or EventBridge ApiDestination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipeenrichmenthttpparameters.html#cfn-pipes-pipe-pipeenrichmenthttpparameters-headerparameters
            '''
            result = self._values.get("header_parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def path_parameter_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The path parameter values to be used to populate API Gateway REST API or EventBridge ApiDestination path wildcards ("*").

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipeenrichmenthttpparameters.html#cfn-pipes-pipe-pipeenrichmenthttpparameters-pathparametervalues
            '''
            result = self._values.get("path_parameter_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def query_string_parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The query string keys/values that need to be sent as part of request invoking the API Gateway REST API or EventBridge ApiDestination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipeenrichmenthttpparameters.html#cfn-pipes-pipe-pipeenrichmenthttpparameters-querystringparameters
            '''
            result = self._values.get("query_string_parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeEnrichmentHttpParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeEnrichmentParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "http_parameters": "httpParameters",
            "input_template": "inputTemplate",
        },
    )
    class PipeEnrichmentParametersProperty:
        def __init__(
            self,
            *,
            http_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeEnrichmentHttpParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            input_template: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters required to set up enrichment on your pipe.

            :param http_parameters: Contains the HTTP parameters to use when the target is a API Gateway REST endpoint or EventBridge ApiDestination. If you specify an API Gateway REST API or EventBridge ApiDestination as a target, you can use this parameter to specify headers, path parameters, and query string keys/values as part of your target invoking request. If you're using ApiDestinations, the corresponding Connection can also have these values configured. In case of any conflicting keys, values from the Connection take precedence.
            :param input_template: Valid JSON text passed to the enrichment. In this case, nothing from the event itself is passed to the enrichment. For more information, see `The JavaScript Object Notation (JSON) Data Interchange Format <https://docs.aws.amazon.com/http://www.rfc-editor.org/rfc/rfc7159.txt>`_ . To remove an input template, specify an empty string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipeenrichmentparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_enrichment_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeEnrichmentParametersProperty(
                    http_parameters=pipes_mixins.CfnPipePropsMixin.PipeEnrichmentHttpParametersProperty(
                        header_parameters={
                            "header_parameters_key": "headerParameters"
                        },
                        path_parameter_values=["pathParameterValues"],
                        query_string_parameters={
                            "query_string_parameters_key": "queryStringParameters"
                        }
                    ),
                    input_template="inputTemplate"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02ec0ce5d674929b75b59ac5fdd5d585585786f3effb966afe90711886492653)
                check_type(argname="argument http_parameters", value=http_parameters, expected_type=type_hints["http_parameters"])
                check_type(argname="argument input_template", value=input_template, expected_type=type_hints["input_template"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if http_parameters is not None:
                self._values["http_parameters"] = http_parameters
            if input_template is not None:
                self._values["input_template"] = input_template

        @builtins.property
        def http_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeEnrichmentHttpParametersProperty"]]:
            '''Contains the HTTP parameters to use when the target is a API Gateway REST endpoint or EventBridge ApiDestination.

            If you specify an API Gateway REST API or EventBridge ApiDestination as a target, you can use this parameter to specify headers, path parameters, and query string keys/values as part of your target invoking request. If you're using ApiDestinations, the corresponding Connection can also have these values configured. In case of any conflicting keys, values from the Connection take precedence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipeenrichmentparameters.html#cfn-pipes-pipe-pipeenrichmentparameters-httpparameters
            '''
            result = self._values.get("http_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeEnrichmentHttpParametersProperty"]], result)

        @builtins.property
        def input_template(self) -> typing.Optional[builtins.str]:
            '''Valid JSON text passed to the enrichment.

            In this case, nothing from the event itself is passed to the enrichment. For more information, see `The JavaScript Object Notation (JSON) Data Interchange Format <https://docs.aws.amazon.com/http://www.rfc-editor.org/rfc/rfc7159.txt>`_ .

            To remove an input template, specify an empty string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipeenrichmentparameters.html#cfn-pipes-pipe-pipeenrichmentparameters-inputtemplate
            '''
            result = self._values.get("input_template")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeEnrichmentParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeLogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloudwatch_logs_log_destination": "cloudwatchLogsLogDestination",
            "firehose_log_destination": "firehoseLogDestination",
            "include_execution_data": "includeExecutionData",
            "level": "level",
            "s3_log_destination": "s3LogDestination",
        },
    )
    class PipeLogConfigurationProperty:
        def __init__(
            self,
            *,
            cloudwatch_logs_log_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.CloudwatchLogsLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            firehose_log_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.FirehoseLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            include_execution_data: typing.Optional[typing.Sequence[builtins.str]] = None,
            level: typing.Optional[builtins.str] = None,
            s3_log_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.S3LogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents the configuration settings for the logs to which this pipe should report events.

            :param cloudwatch_logs_log_destination: The logging configuration settings for the pipe.
            :param firehose_log_destination: The Amazon Data Firehose logging configuration settings for the pipe.
            :param include_execution_data: Whether the execution data (specifically, the ``payload`` , ``awsRequest`` , and ``awsResponse`` fields) is included in the log messages for this pipe. This applies to all log destinations for the pipe. For more information, see `Including execution data in logs <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-logs.html#eb-pipes-logs-execution-data>`_ in the *Amazon EventBridge User Guide* . *Allowed values:* ``ALL``
            :param level: The level of logging detail to include. This applies to all log destinations for the pipe.
            :param s3_log_destination: The Amazon S3 logging configuration settings for the pipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipelogconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_log_configuration_property = pipes_mixins.CfnPipePropsMixin.PipeLogConfigurationProperty(
                    cloudwatch_logs_log_destination=pipes_mixins.CfnPipePropsMixin.CloudwatchLogsLogDestinationProperty(
                        log_group_arn="logGroupArn"
                    ),
                    firehose_log_destination=pipes_mixins.CfnPipePropsMixin.FirehoseLogDestinationProperty(
                        delivery_stream_arn="deliveryStreamArn"
                    ),
                    include_execution_data=["includeExecutionData"],
                    level="level",
                    s3_log_destination=pipes_mixins.CfnPipePropsMixin.S3LogDestinationProperty(
                        bucket_name="bucketName",
                        bucket_owner="bucketOwner",
                        output_format="outputFormat",
                        prefix="prefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2aa069717f194d153d123b85c6e5f1c700c6a56908f8676e5789bbd232c8d5f2)
                check_type(argname="argument cloudwatch_logs_log_destination", value=cloudwatch_logs_log_destination, expected_type=type_hints["cloudwatch_logs_log_destination"])
                check_type(argname="argument firehose_log_destination", value=firehose_log_destination, expected_type=type_hints["firehose_log_destination"])
                check_type(argname="argument include_execution_data", value=include_execution_data, expected_type=type_hints["include_execution_data"])
                check_type(argname="argument level", value=level, expected_type=type_hints["level"])
                check_type(argname="argument s3_log_destination", value=s3_log_destination, expected_type=type_hints["s3_log_destination"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloudwatch_logs_log_destination is not None:
                self._values["cloudwatch_logs_log_destination"] = cloudwatch_logs_log_destination
            if firehose_log_destination is not None:
                self._values["firehose_log_destination"] = firehose_log_destination
            if include_execution_data is not None:
                self._values["include_execution_data"] = include_execution_data
            if level is not None:
                self._values["level"] = level
            if s3_log_destination is not None:
                self._values["s3_log_destination"] = s3_log_destination

        @builtins.property
        def cloudwatch_logs_log_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.CloudwatchLogsLogDestinationProperty"]]:
            '''The logging configuration settings for the pipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipelogconfiguration.html#cfn-pipes-pipe-pipelogconfiguration-cloudwatchlogslogdestination
            '''
            result = self._values.get("cloudwatch_logs_log_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.CloudwatchLogsLogDestinationProperty"]], result)

        @builtins.property
        def firehose_log_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.FirehoseLogDestinationProperty"]]:
            '''The Amazon Data Firehose logging configuration settings for the pipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipelogconfiguration.html#cfn-pipes-pipe-pipelogconfiguration-firehoselogdestination
            '''
            result = self._values.get("firehose_log_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.FirehoseLogDestinationProperty"]], result)

        @builtins.property
        def include_execution_data(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Whether the execution data (specifically, the ``payload`` , ``awsRequest`` , and ``awsResponse`` fields) is included in the log messages for this pipe.

            This applies to all log destinations for the pipe.

            For more information, see `Including execution data in logs <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-logs.html#eb-pipes-logs-execution-data>`_ in the *Amazon EventBridge User Guide* .

            *Allowed values:* ``ALL``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipelogconfiguration.html#cfn-pipes-pipe-pipelogconfiguration-includeexecutiondata
            '''
            result = self._values.get("include_execution_data")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def level(self) -> typing.Optional[builtins.str]:
            '''The level of logging detail to include.

            This applies to all log destinations for the pipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipelogconfiguration.html#cfn-pipes-pipe-pipelogconfiguration-level
            '''
            result = self._values.get("level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_log_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.S3LogDestinationProperty"]]:
            '''The Amazon S3 logging configuration settings for the pipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipelogconfiguration.html#cfn-pipes-pipe-pipelogconfiguration-s3logdestination
            '''
            result = self._values.get("s3_log_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.S3LogDestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeLogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeSourceActiveMQBrokerParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "batch_size": "batchSize",
            "credentials": "credentials",
            "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
            "queue_name": "queueName",
        },
    )
    class PipeSourceActiveMQBrokerParametersProperty:
        def __init__(
            self,
            *,
            batch_size: typing.Optional[jsii.Number] = None,
            credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.MQBrokerAccessCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
            queue_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for using an Active MQ broker as a source.

            :param batch_size: The maximum number of records to include in each batch.
            :param credentials: The credentials needed to access the resource.
            :param maximum_batching_window_in_seconds: The maximum length of a time to wait for events.
            :param queue_name: The name of the destination queue to consume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceactivemqbrokerparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_source_active_mQBroker_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeSourceActiveMQBrokerParametersProperty(
                    batch_size=123,
                    credentials=pipes_mixins.CfnPipePropsMixin.MQBrokerAccessCredentialsProperty(
                        basic_auth="basicAuth"
                    ),
                    maximum_batching_window_in_seconds=123,
                    queue_name="queueName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__63b5d107e820fa15e6b27722aa98e9409d6a021f76a5da0a91b8caac478f5d84)
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
                check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
                check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if credentials is not None:
                self._values["credentials"] = credentials
            if maximum_batching_window_in_seconds is not None:
                self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
            if queue_name is not None:
                self._values["queue_name"] = queue_name

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of records to include in each batch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceactivemqbrokerparameters.html#cfn-pipes-pipe-pipesourceactivemqbrokerparameters-batchsize
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.MQBrokerAccessCredentialsProperty"]]:
            '''The credentials needed to access the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceactivemqbrokerparameters.html#cfn-pipes-pipe-pipesourceactivemqbrokerparameters-credentials
            '''
            result = self._values.get("credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.MQBrokerAccessCredentialsProperty"]], result)

        @builtins.property
        def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum length of a time to wait for events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceactivemqbrokerparameters.html#cfn-pipes-pipe-pipesourceactivemqbrokerparameters-maximumbatchingwindowinseconds
            '''
            result = self._values.get("maximum_batching_window_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def queue_name(self) -> typing.Optional[builtins.str]:
            '''The name of the destination queue to consume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceactivemqbrokerparameters.html#cfn-pipes-pipe-pipesourceactivemqbrokerparameters-queuename
            '''
            result = self._values.get("queue_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeSourceActiveMQBrokerParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeSourceDynamoDBStreamParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "batch_size": "batchSize",
            "dead_letter_config": "deadLetterConfig",
            "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
            "maximum_record_age_in_seconds": "maximumRecordAgeInSeconds",
            "maximum_retry_attempts": "maximumRetryAttempts",
            "on_partial_batch_item_failure": "onPartialBatchItemFailure",
            "parallelization_factor": "parallelizationFactor",
            "starting_position": "startingPosition",
        },
    )
    class PipeSourceDynamoDBStreamParametersProperty:
        def __init__(
            self,
            *,
            batch_size: typing.Optional[jsii.Number] = None,
            dead_letter_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.DeadLetterConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_retry_attempts: typing.Optional[jsii.Number] = None,
            on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
            parallelization_factor: typing.Optional[jsii.Number] = None,
            starting_position: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for using a DynamoDB stream as a source.

            :param batch_size: The maximum number of records to include in each batch.
            :param dead_letter_config: Define the target queue to send dead-letter queue events to.
            :param maximum_batching_window_in_seconds: The maximum length of a time to wait for events.
            :param maximum_record_age_in_seconds: Discard records older than the specified age. The default value is -1, which sets the maximum age to infinite. When the value is set to infinite, EventBridge never discards old records.
            :param maximum_retry_attempts: Discard records after the specified number of retries. The default value is -1, which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, EventBridge retries failed records until the record expires in the event source.
            :param on_partial_batch_item_failure: Define how to handle item process failures. ``AUTOMATIC_BISECT`` halves each batch and retry each half until all the records are processed or there is one failed message left in the batch.
            :param parallelization_factor: The number of batches to process concurrently from each shard. The default value is 1.
            :param starting_position: (Streams only) The position in a stream from which to start reading. *Valid values* : ``TRIM_HORIZON | LATEST``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcedynamodbstreamparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_source_dynamo_dBStream_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeSourceDynamoDBStreamParametersProperty(
                    batch_size=123,
                    dead_letter_config=pipes_mixins.CfnPipePropsMixin.DeadLetterConfigProperty(
                        arn="arn"
                    ),
                    maximum_batching_window_in_seconds=123,
                    maximum_record_age_in_seconds=123,
                    maximum_retry_attempts=123,
                    on_partial_batch_item_failure="onPartialBatchItemFailure",
                    parallelization_factor=123,
                    starting_position="startingPosition"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4579ed308bf27d245e737dd1e7f0dd1ef56b5ba56b2240022a84ab22d6b23206)
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument dead_letter_config", value=dead_letter_config, expected_type=type_hints["dead_letter_config"])
                check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
                check_type(argname="argument maximum_record_age_in_seconds", value=maximum_record_age_in_seconds, expected_type=type_hints["maximum_record_age_in_seconds"])
                check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
                check_type(argname="argument on_partial_batch_item_failure", value=on_partial_batch_item_failure, expected_type=type_hints["on_partial_batch_item_failure"])
                check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
                check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if dead_letter_config is not None:
                self._values["dead_letter_config"] = dead_letter_config
            if maximum_batching_window_in_seconds is not None:
                self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
            if maximum_record_age_in_seconds is not None:
                self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
            if maximum_retry_attempts is not None:
                self._values["maximum_retry_attempts"] = maximum_retry_attempts
            if on_partial_batch_item_failure is not None:
                self._values["on_partial_batch_item_failure"] = on_partial_batch_item_failure
            if parallelization_factor is not None:
                self._values["parallelization_factor"] = parallelization_factor
            if starting_position is not None:
                self._values["starting_position"] = starting_position

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of records to include in each batch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcedynamodbstreamparameters.html#cfn-pipes-pipe-pipesourcedynamodbstreamparameters-batchsize
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dead_letter_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.DeadLetterConfigProperty"]]:
            '''Define the target queue to send dead-letter queue events to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcedynamodbstreamparameters.html#cfn-pipes-pipe-pipesourcedynamodbstreamparameters-deadletterconfig
            '''
            result = self._values.get("dead_letter_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.DeadLetterConfigProperty"]], result)

        @builtins.property
        def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum length of a time to wait for events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcedynamodbstreamparameters.html#cfn-pipes-pipe-pipesourcedynamodbstreamparameters-maximumbatchingwindowinseconds
            '''
            result = self._values.get("maximum_batching_window_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''Discard records older than the specified age.

            The default value is -1, which sets the maximum age to infinite. When the value is set to infinite, EventBridge never discards old records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcedynamodbstreamparameters.html#cfn-pipes-pipe-pipesourcedynamodbstreamparameters-maximumrecordageinseconds
            '''
            result = self._values.get("maximum_record_age_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
            '''Discard records after the specified number of retries.

            The default value is -1, which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, EventBridge retries failed records until the record expires in the event source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcedynamodbstreamparameters.html#cfn-pipes-pipe-pipesourcedynamodbstreamparameters-maximumretryattempts
            '''
            result = self._values.get("maximum_retry_attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def on_partial_batch_item_failure(self) -> typing.Optional[builtins.str]:
            '''Define how to handle item process failures.

            ``AUTOMATIC_BISECT`` halves each batch and retry each half until all the records are processed or there is one failed message left in the batch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcedynamodbstreamparameters.html#cfn-pipes-pipe-pipesourcedynamodbstreamparameters-onpartialbatchitemfailure
            '''
            result = self._values.get("on_partial_batch_item_failure")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parallelization_factor(self) -> typing.Optional[jsii.Number]:
            '''The number of batches to process concurrently from each shard.

            The default value is 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcedynamodbstreamparameters.html#cfn-pipes-pipe-pipesourcedynamodbstreamparameters-parallelizationfactor
            '''
            result = self._values.get("parallelization_factor")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def starting_position(self) -> typing.Optional[builtins.str]:
            '''(Streams only) The position in a stream from which to start reading.

            *Valid values* : ``TRIM_HORIZON | LATEST``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcedynamodbstreamparameters.html#cfn-pipes-pipe-pipesourcedynamodbstreamparameters-startingposition
            '''
            result = self._values.get("starting_position")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeSourceDynamoDBStreamParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeSourceKinesisStreamParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "batch_size": "batchSize",
            "dead_letter_config": "deadLetterConfig",
            "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
            "maximum_record_age_in_seconds": "maximumRecordAgeInSeconds",
            "maximum_retry_attempts": "maximumRetryAttempts",
            "on_partial_batch_item_failure": "onPartialBatchItemFailure",
            "parallelization_factor": "parallelizationFactor",
            "starting_position": "startingPosition",
            "starting_position_timestamp": "startingPositionTimestamp",
        },
    )
    class PipeSourceKinesisStreamParametersProperty:
        def __init__(
            self,
            *,
            batch_size: typing.Optional[jsii.Number] = None,
            dead_letter_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.DeadLetterConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_retry_attempts: typing.Optional[jsii.Number] = None,
            on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
            parallelization_factor: typing.Optional[jsii.Number] = None,
            starting_position: typing.Optional[builtins.str] = None,
            starting_position_timestamp: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for using a Kinesis stream as a source.

            :param batch_size: The maximum number of records to include in each batch.
            :param dead_letter_config: Define the target queue to send dead-letter queue events to.
            :param maximum_batching_window_in_seconds: The maximum length of a time to wait for events.
            :param maximum_record_age_in_seconds: Discard records older than the specified age. The default value is -1, which sets the maximum age to infinite. When the value is set to infinite, EventBridge never discards old records.
            :param maximum_retry_attempts: Discard records after the specified number of retries. The default value is -1, which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, EventBridge retries failed records until the record expires in the event source.
            :param on_partial_batch_item_failure: Define how to handle item process failures. ``AUTOMATIC_BISECT`` halves each batch and retry each half until all the records are processed or there is one failed message left in the batch.
            :param parallelization_factor: The number of batches to process concurrently from each shard. The default value is 1.
            :param starting_position: The position in a stream from which to start reading.
            :param starting_position_timestamp: With ``StartingPosition`` set to ``AT_TIMESTAMP`` , the time from which to start reading, in Unix time seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_source_kinesis_stream_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeSourceKinesisStreamParametersProperty(
                    batch_size=123,
                    dead_letter_config=pipes_mixins.CfnPipePropsMixin.DeadLetterConfigProperty(
                        arn="arn"
                    ),
                    maximum_batching_window_in_seconds=123,
                    maximum_record_age_in_seconds=123,
                    maximum_retry_attempts=123,
                    on_partial_batch_item_failure="onPartialBatchItemFailure",
                    parallelization_factor=123,
                    starting_position="startingPosition",
                    starting_position_timestamp="startingPositionTimestamp"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93ce316faa6206e09724df001ad75d6ebfc6af86cfc2c0a7ce5d21cbdff43a1e)
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument dead_letter_config", value=dead_letter_config, expected_type=type_hints["dead_letter_config"])
                check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
                check_type(argname="argument maximum_record_age_in_seconds", value=maximum_record_age_in_seconds, expected_type=type_hints["maximum_record_age_in_seconds"])
                check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
                check_type(argname="argument on_partial_batch_item_failure", value=on_partial_batch_item_failure, expected_type=type_hints["on_partial_batch_item_failure"])
                check_type(argname="argument parallelization_factor", value=parallelization_factor, expected_type=type_hints["parallelization_factor"])
                check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
                check_type(argname="argument starting_position_timestamp", value=starting_position_timestamp, expected_type=type_hints["starting_position_timestamp"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if dead_letter_config is not None:
                self._values["dead_letter_config"] = dead_letter_config
            if maximum_batching_window_in_seconds is not None:
                self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
            if maximum_record_age_in_seconds is not None:
                self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
            if maximum_retry_attempts is not None:
                self._values["maximum_retry_attempts"] = maximum_retry_attempts
            if on_partial_batch_item_failure is not None:
                self._values["on_partial_batch_item_failure"] = on_partial_batch_item_failure
            if parallelization_factor is not None:
                self._values["parallelization_factor"] = parallelization_factor
            if starting_position is not None:
                self._values["starting_position"] = starting_position
            if starting_position_timestamp is not None:
                self._values["starting_position_timestamp"] = starting_position_timestamp

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of records to include in each batch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-batchsize
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dead_letter_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.DeadLetterConfigProperty"]]:
            '''Define the target queue to send dead-letter queue events to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-deadletterconfig
            '''
            result = self._values.get("dead_letter_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.DeadLetterConfigProperty"]], result)

        @builtins.property
        def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum length of a time to wait for events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-maximumbatchingwindowinseconds
            '''
            result = self._values.get("maximum_batching_window_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''Discard records older than the specified age.

            The default value is -1, which sets the maximum age to infinite. When the value is set to infinite, EventBridge never discards old records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-maximumrecordageinseconds
            '''
            result = self._values.get("maximum_record_age_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
            '''Discard records after the specified number of retries.

            The default value is -1, which sets the maximum number of retries to infinite. When MaximumRetryAttempts is infinite, EventBridge retries failed records until the record expires in the event source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-maximumretryattempts
            '''
            result = self._values.get("maximum_retry_attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def on_partial_batch_item_failure(self) -> typing.Optional[builtins.str]:
            '''Define how to handle item process failures.

            ``AUTOMATIC_BISECT`` halves each batch and retry each half until all the records are processed or there is one failed message left in the batch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-onpartialbatchitemfailure
            '''
            result = self._values.get("on_partial_batch_item_failure")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parallelization_factor(self) -> typing.Optional[jsii.Number]:
            '''The number of batches to process concurrently from each shard.

            The default value is 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-parallelizationfactor
            '''
            result = self._values.get("parallelization_factor")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def starting_position(self) -> typing.Optional[builtins.str]:
            '''The position in a stream from which to start reading.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-startingposition
            '''
            result = self._values.get("starting_position")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def starting_position_timestamp(self) -> typing.Optional[builtins.str]:
            '''With ``StartingPosition`` set to ``AT_TIMESTAMP`` , the time from which to start reading, in Unix time seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcekinesisstreamparameters.html#cfn-pipes-pipe-pipesourcekinesisstreamparameters-startingpositiontimestamp
            '''
            result = self._values.get("starting_position_timestamp")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeSourceKinesisStreamParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeSourceManagedStreamingKafkaParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "batch_size": "batchSize",
            "consumer_group_id": "consumerGroupId",
            "credentials": "credentials",
            "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
            "starting_position": "startingPosition",
            "topic_name": "topicName",
        },
    )
    class PipeSourceManagedStreamingKafkaParametersProperty:
        def __init__(
            self,
            *,
            batch_size: typing.Optional[jsii.Number] = None,
            consumer_group_id: typing.Optional[builtins.str] = None,
            credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.MSKAccessCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
            starting_position: typing.Optional[builtins.str] = None,
            topic_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for using an MSK stream as a source.

            :param batch_size: The maximum number of records to include in each batch.
            :param consumer_group_id: The name of the destination queue to consume.
            :param credentials: The credentials needed to access the resource.
            :param maximum_batching_window_in_seconds: The maximum length of a time to wait for events.
            :param starting_position: The position in a stream from which to start reading.
            :param topic_name: The name of the topic that the pipe will read from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcemanagedstreamingkafkaparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_source_managed_streaming_kafka_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeSourceManagedStreamingKafkaParametersProperty(
                    batch_size=123,
                    consumer_group_id="consumerGroupId",
                    credentials=pipes_mixins.CfnPipePropsMixin.MSKAccessCredentialsProperty(
                        client_certificate_tls_auth="clientCertificateTlsAuth",
                        sasl_scram512_auth="saslScram512Auth"
                    ),
                    maximum_batching_window_in_seconds=123,
                    starting_position="startingPosition",
                    topic_name="topicName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__caa518ab3584bac527ff4b57ad8373e6372c7d56a19cc275678369405cc77b04)
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument consumer_group_id", value=consumer_group_id, expected_type=type_hints["consumer_group_id"])
                check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
                check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
                check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
                check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if consumer_group_id is not None:
                self._values["consumer_group_id"] = consumer_group_id
            if credentials is not None:
                self._values["credentials"] = credentials
            if maximum_batching_window_in_seconds is not None:
                self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
            if starting_position is not None:
                self._values["starting_position"] = starting_position
            if topic_name is not None:
                self._values["topic_name"] = topic_name

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of records to include in each batch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcemanagedstreamingkafkaparameters.html#cfn-pipes-pipe-pipesourcemanagedstreamingkafkaparameters-batchsize
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def consumer_group_id(self) -> typing.Optional[builtins.str]:
            '''The name of the destination queue to consume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcemanagedstreamingkafkaparameters.html#cfn-pipes-pipe-pipesourcemanagedstreamingkafkaparameters-consumergroupid
            '''
            result = self._values.get("consumer_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.MSKAccessCredentialsProperty"]]:
            '''The credentials needed to access the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcemanagedstreamingkafkaparameters.html#cfn-pipes-pipe-pipesourcemanagedstreamingkafkaparameters-credentials
            '''
            result = self._values.get("credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.MSKAccessCredentialsProperty"]], result)

        @builtins.property
        def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum length of a time to wait for events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcemanagedstreamingkafkaparameters.html#cfn-pipes-pipe-pipesourcemanagedstreamingkafkaparameters-maximumbatchingwindowinseconds
            '''
            result = self._values.get("maximum_batching_window_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def starting_position(self) -> typing.Optional[builtins.str]:
            '''The position in a stream from which to start reading.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcemanagedstreamingkafkaparameters.html#cfn-pipes-pipe-pipesourcemanagedstreamingkafkaparameters-startingposition
            '''
            result = self._values.get("starting_position")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_name(self) -> typing.Optional[builtins.str]:
            '''The name of the topic that the pipe will read from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcemanagedstreamingkafkaparameters.html#cfn-pipes-pipe-pipesourcemanagedstreamingkafkaparameters-topicname
            '''
            result = self._values.get("topic_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeSourceManagedStreamingKafkaParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeSourceParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "active_mq_broker_parameters": "activeMqBrokerParameters",
            "dynamo_db_stream_parameters": "dynamoDbStreamParameters",
            "filter_criteria": "filterCriteria",
            "kinesis_stream_parameters": "kinesisStreamParameters",
            "managed_streaming_kafka_parameters": "managedStreamingKafkaParameters",
            "rabbit_mq_broker_parameters": "rabbitMqBrokerParameters",
            "self_managed_kafka_parameters": "selfManagedKafkaParameters",
            "sqs_queue_parameters": "sqsQueueParameters",
        },
    )
    class PipeSourceParametersProperty:
        def __init__(
            self,
            *,
            active_mq_broker_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeSourceActiveMQBrokerParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_db_stream_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeSourceDynamoDBStreamParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            filter_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.FilterCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kinesis_stream_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeSourceKinesisStreamParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            managed_streaming_kafka_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeSourceManagedStreamingKafkaParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rabbit_mq_broker_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeSourceRabbitMQBrokerParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            self_managed_kafka_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeSourceSelfManagedKafkaParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sqs_queue_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeSourceSqsQueueParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The parameters required to set up a source for your pipe.

            :param active_mq_broker_parameters: The parameters for using an Active MQ broker as a source.
            :param dynamo_db_stream_parameters: The parameters for using a DynamoDB stream as a source.
            :param filter_criteria: The collection of event patterns used to filter events. To remove a filter, specify a ``FilterCriteria`` object with an empty array of ``Filter`` objects. For more information, see `Events and Event Patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html>`_ in the *Amazon EventBridge User Guide* .
            :param kinesis_stream_parameters: The parameters for using a Kinesis stream as a source.
            :param managed_streaming_kafka_parameters: The parameters for using an MSK stream as a source.
            :param rabbit_mq_broker_parameters: The parameters for using a Rabbit MQ broker as a source.
            :param self_managed_kafka_parameters: The parameters for using a self-managed Apache Kafka stream as a source. A *self managed* cluster refers to any Apache Kafka cluster not hosted by AWS . This includes both clusters you manage yourself, as well as those hosted by a third-party provider, such as `Confluent Cloud <https://docs.aws.amazon.com/https://www.confluent.io/>`_ , `CloudKarafka <https://docs.aws.amazon.com/https://www.cloudkarafka.com/>`_ , or `Redpanda <https://docs.aws.amazon.com/https://redpanda.com/>`_ . For more information, see `Apache Kafka streams as a source <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-kafka.html>`_ in the *Amazon EventBridge User Guide* .
            :param sqs_queue_parameters: The parameters for using a Amazon SQS stream as a source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_source_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeSourceParametersProperty(
                    active_mq_broker_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceActiveMQBrokerParametersProperty(
                        batch_size=123,
                        credentials=pipes_mixins.CfnPipePropsMixin.MQBrokerAccessCredentialsProperty(
                            basic_auth="basicAuth"
                        ),
                        maximum_batching_window_in_seconds=123,
                        queue_name="queueName"
                    ),
                    dynamo_db_stream_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceDynamoDBStreamParametersProperty(
                        batch_size=123,
                        dead_letter_config=pipes_mixins.CfnPipePropsMixin.DeadLetterConfigProperty(
                            arn="arn"
                        ),
                        maximum_batching_window_in_seconds=123,
                        maximum_record_age_in_seconds=123,
                        maximum_retry_attempts=123,
                        on_partial_batch_item_failure="onPartialBatchItemFailure",
                        parallelization_factor=123,
                        starting_position="startingPosition"
                    ),
                    filter_criteria=pipes_mixins.CfnPipePropsMixin.FilterCriteriaProperty(
                        filters=[pipes_mixins.CfnPipePropsMixin.FilterProperty(
                            pattern="pattern"
                        )]
                    ),
                    kinesis_stream_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceKinesisStreamParametersProperty(
                        batch_size=123,
                        dead_letter_config=pipes_mixins.CfnPipePropsMixin.DeadLetterConfigProperty(
                            arn="arn"
                        ),
                        maximum_batching_window_in_seconds=123,
                        maximum_record_age_in_seconds=123,
                        maximum_retry_attempts=123,
                        on_partial_batch_item_failure="onPartialBatchItemFailure",
                        parallelization_factor=123,
                        starting_position="startingPosition",
                        starting_position_timestamp="startingPositionTimestamp"
                    ),
                    managed_streaming_kafka_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceManagedStreamingKafkaParametersProperty(
                        batch_size=123,
                        consumer_group_id="consumerGroupId",
                        credentials=pipes_mixins.CfnPipePropsMixin.MSKAccessCredentialsProperty(
                            client_certificate_tls_auth="clientCertificateTlsAuth",
                            sasl_scram512_auth="saslScram512Auth"
                        ),
                        maximum_batching_window_in_seconds=123,
                        starting_position="startingPosition",
                        topic_name="topicName"
                    ),
                    rabbit_mq_broker_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceRabbitMQBrokerParametersProperty(
                        batch_size=123,
                        credentials=pipes_mixins.CfnPipePropsMixin.MQBrokerAccessCredentialsProperty(
                            basic_auth="basicAuth"
                        ),
                        maximum_batching_window_in_seconds=123,
                        queue_name="queueName",
                        virtual_host="virtualHost"
                    ),
                    self_managed_kafka_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceSelfManagedKafkaParametersProperty(
                        additional_bootstrap_servers=["additionalBootstrapServers"],
                        batch_size=123,
                        consumer_group_id="consumerGroupId",
                        credentials=pipes_mixins.CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationCredentialsProperty(
                            basic_auth="basicAuth",
                            client_certificate_tls_auth="clientCertificateTlsAuth",
                            sasl_scram256_auth="saslScram256Auth",
                            sasl_scram512_auth="saslScram512Auth"
                        ),
                        maximum_batching_window_in_seconds=123,
                        server_root_ca_certificate="serverRootCaCertificate",
                        starting_position="startingPosition",
                        topic_name="topicName",
                        vpc=pipes_mixins.CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationVpcProperty(
                            security_group=["securityGroup"],
                            subnets=["subnets"]
                        )
                    ),
                    sqs_queue_parameters=pipes_mixins.CfnPipePropsMixin.PipeSourceSqsQueueParametersProperty(
                        batch_size=123,
                        maximum_batching_window_in_seconds=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9a888186ff6f7b488986feea8c07b1314b93a07a27cfbb907635133352d0807)
                check_type(argname="argument active_mq_broker_parameters", value=active_mq_broker_parameters, expected_type=type_hints["active_mq_broker_parameters"])
                check_type(argname="argument dynamo_db_stream_parameters", value=dynamo_db_stream_parameters, expected_type=type_hints["dynamo_db_stream_parameters"])
                check_type(argname="argument filter_criteria", value=filter_criteria, expected_type=type_hints["filter_criteria"])
                check_type(argname="argument kinesis_stream_parameters", value=kinesis_stream_parameters, expected_type=type_hints["kinesis_stream_parameters"])
                check_type(argname="argument managed_streaming_kafka_parameters", value=managed_streaming_kafka_parameters, expected_type=type_hints["managed_streaming_kafka_parameters"])
                check_type(argname="argument rabbit_mq_broker_parameters", value=rabbit_mq_broker_parameters, expected_type=type_hints["rabbit_mq_broker_parameters"])
                check_type(argname="argument self_managed_kafka_parameters", value=self_managed_kafka_parameters, expected_type=type_hints["self_managed_kafka_parameters"])
                check_type(argname="argument sqs_queue_parameters", value=sqs_queue_parameters, expected_type=type_hints["sqs_queue_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if active_mq_broker_parameters is not None:
                self._values["active_mq_broker_parameters"] = active_mq_broker_parameters
            if dynamo_db_stream_parameters is not None:
                self._values["dynamo_db_stream_parameters"] = dynamo_db_stream_parameters
            if filter_criteria is not None:
                self._values["filter_criteria"] = filter_criteria
            if kinesis_stream_parameters is not None:
                self._values["kinesis_stream_parameters"] = kinesis_stream_parameters
            if managed_streaming_kafka_parameters is not None:
                self._values["managed_streaming_kafka_parameters"] = managed_streaming_kafka_parameters
            if rabbit_mq_broker_parameters is not None:
                self._values["rabbit_mq_broker_parameters"] = rabbit_mq_broker_parameters
            if self_managed_kafka_parameters is not None:
                self._values["self_managed_kafka_parameters"] = self_managed_kafka_parameters
            if sqs_queue_parameters is not None:
                self._values["sqs_queue_parameters"] = sqs_queue_parameters

        @builtins.property
        def active_mq_broker_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceActiveMQBrokerParametersProperty"]]:
            '''The parameters for using an Active MQ broker as a source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceparameters.html#cfn-pipes-pipe-pipesourceparameters-activemqbrokerparameters
            '''
            result = self._values.get("active_mq_broker_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceActiveMQBrokerParametersProperty"]], result)

        @builtins.property
        def dynamo_db_stream_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceDynamoDBStreamParametersProperty"]]:
            '''The parameters for using a DynamoDB stream as a source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceparameters.html#cfn-pipes-pipe-pipesourceparameters-dynamodbstreamparameters
            '''
            result = self._values.get("dynamo_db_stream_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceDynamoDBStreamParametersProperty"]], result)

        @builtins.property
        def filter_criteria(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.FilterCriteriaProperty"]]:
            '''The collection of event patterns used to filter events.

            To remove a filter, specify a ``FilterCriteria`` object with an empty array of ``Filter`` objects.

            For more information, see `Events and Event Patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html>`_ in the *Amazon EventBridge User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceparameters.html#cfn-pipes-pipe-pipesourceparameters-filtercriteria
            '''
            result = self._values.get("filter_criteria")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.FilterCriteriaProperty"]], result)

        @builtins.property
        def kinesis_stream_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceKinesisStreamParametersProperty"]]:
            '''The parameters for using a Kinesis stream as a source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceparameters.html#cfn-pipes-pipe-pipesourceparameters-kinesisstreamparameters
            '''
            result = self._values.get("kinesis_stream_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceKinesisStreamParametersProperty"]], result)

        @builtins.property
        def managed_streaming_kafka_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceManagedStreamingKafkaParametersProperty"]]:
            '''The parameters for using an MSK stream as a source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceparameters.html#cfn-pipes-pipe-pipesourceparameters-managedstreamingkafkaparameters
            '''
            result = self._values.get("managed_streaming_kafka_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceManagedStreamingKafkaParametersProperty"]], result)

        @builtins.property
        def rabbit_mq_broker_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceRabbitMQBrokerParametersProperty"]]:
            '''The parameters for using a Rabbit MQ broker as a source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceparameters.html#cfn-pipes-pipe-pipesourceparameters-rabbitmqbrokerparameters
            '''
            result = self._values.get("rabbit_mq_broker_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceRabbitMQBrokerParametersProperty"]], result)

        @builtins.property
        def self_managed_kafka_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceSelfManagedKafkaParametersProperty"]]:
            '''The parameters for using a self-managed Apache Kafka stream as a source.

            A *self managed* cluster refers to any Apache Kafka cluster not hosted by AWS . This includes both clusters you manage yourself, as well as those hosted by a third-party provider, such as `Confluent Cloud <https://docs.aws.amazon.com/https://www.confluent.io/>`_ , `CloudKarafka <https://docs.aws.amazon.com/https://www.cloudkarafka.com/>`_ , or `Redpanda <https://docs.aws.amazon.com/https://redpanda.com/>`_ . For more information, see `Apache Kafka streams as a source <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-kafka.html>`_ in the *Amazon EventBridge User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceparameters.html#cfn-pipes-pipe-pipesourceparameters-selfmanagedkafkaparameters
            '''
            result = self._values.get("self_managed_kafka_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceSelfManagedKafkaParametersProperty"]], result)

        @builtins.property
        def sqs_queue_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceSqsQueueParametersProperty"]]:
            '''The parameters for using a Amazon SQS stream as a source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceparameters.html#cfn-pipes-pipe-pipesourceparameters-sqsqueueparameters
            '''
            result = self._values.get("sqs_queue_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeSourceSqsQueueParametersProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeSourceParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeSourceRabbitMQBrokerParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "batch_size": "batchSize",
            "credentials": "credentials",
            "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
            "queue_name": "queueName",
            "virtual_host": "virtualHost",
        },
    )
    class PipeSourceRabbitMQBrokerParametersProperty:
        def __init__(
            self,
            *,
            batch_size: typing.Optional[jsii.Number] = None,
            credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.MQBrokerAccessCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
            queue_name: typing.Optional[builtins.str] = None,
            virtual_host: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for using a Rabbit MQ broker as a source.

            :param batch_size: The maximum number of records to include in each batch.
            :param credentials: The credentials needed to access the resource.
            :param maximum_batching_window_in_seconds: The maximum length of a time to wait for events.
            :param queue_name: The name of the destination queue to consume.
            :param virtual_host: The name of the virtual host associated with the source broker.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcerabbitmqbrokerparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_source_rabbit_mQBroker_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeSourceRabbitMQBrokerParametersProperty(
                    batch_size=123,
                    credentials=pipes_mixins.CfnPipePropsMixin.MQBrokerAccessCredentialsProperty(
                        basic_auth="basicAuth"
                    ),
                    maximum_batching_window_in_seconds=123,
                    queue_name="queueName",
                    virtual_host="virtualHost"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e35e2d337ff3ac75db7e8afd7728e712225503d9984e8f69a1724e985621459e)
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
                check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
                check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
                check_type(argname="argument virtual_host", value=virtual_host, expected_type=type_hints["virtual_host"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if credentials is not None:
                self._values["credentials"] = credentials
            if maximum_batching_window_in_seconds is not None:
                self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
            if queue_name is not None:
                self._values["queue_name"] = queue_name
            if virtual_host is not None:
                self._values["virtual_host"] = virtual_host

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of records to include in each batch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcerabbitmqbrokerparameters.html#cfn-pipes-pipe-pipesourcerabbitmqbrokerparameters-batchsize
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.MQBrokerAccessCredentialsProperty"]]:
            '''The credentials needed to access the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcerabbitmqbrokerparameters.html#cfn-pipes-pipe-pipesourcerabbitmqbrokerparameters-credentials
            '''
            result = self._values.get("credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.MQBrokerAccessCredentialsProperty"]], result)

        @builtins.property
        def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum length of a time to wait for events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcerabbitmqbrokerparameters.html#cfn-pipes-pipe-pipesourcerabbitmqbrokerparameters-maximumbatchingwindowinseconds
            '''
            result = self._values.get("maximum_batching_window_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def queue_name(self) -> typing.Optional[builtins.str]:
            '''The name of the destination queue to consume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcerabbitmqbrokerparameters.html#cfn-pipes-pipe-pipesourcerabbitmqbrokerparameters-queuename
            '''
            result = self._values.get("queue_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def virtual_host(self) -> typing.Optional[builtins.str]:
            '''The name of the virtual host associated with the source broker.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcerabbitmqbrokerparameters.html#cfn-pipes-pipe-pipesourcerabbitmqbrokerparameters-virtualhost
            '''
            result = self._values.get("virtual_host")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeSourceRabbitMQBrokerParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeSourceSelfManagedKafkaParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_bootstrap_servers": "additionalBootstrapServers",
            "batch_size": "batchSize",
            "consumer_group_id": "consumerGroupId",
            "credentials": "credentials",
            "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
            "server_root_ca_certificate": "serverRootCaCertificate",
            "starting_position": "startingPosition",
            "topic_name": "topicName",
            "vpc": "vpc",
        },
    )
    class PipeSourceSelfManagedKafkaParametersProperty:
        def __init__(
            self,
            *,
            additional_bootstrap_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
            batch_size: typing.Optional[jsii.Number] = None,
            consumer_group_id: typing.Optional[builtins.str] = None,
            credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
            server_root_ca_certificate: typing.Optional[builtins.str] = None,
            starting_position: typing.Optional[builtins.str] = None,
            topic_name: typing.Optional[builtins.str] = None,
            vpc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationVpcProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The parameters for using a self-managed Apache Kafka stream as a source.

            A *self managed* cluster refers to any Apache Kafka cluster not hosted by AWS . This includes both clusters you manage yourself, as well as those hosted by a third-party provider, such as `Confluent Cloud <https://docs.aws.amazon.com/https://www.confluent.io/>`_ , `CloudKarafka <https://docs.aws.amazon.com/https://www.cloudkarafka.com/>`_ , or `Redpanda <https://docs.aws.amazon.com/https://redpanda.com/>`_ . For more information, see `Apache Kafka streams as a source <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-kafka.html>`_ in the *Amazon EventBridge User Guide* .

            :param additional_bootstrap_servers: An array of server URLs.
            :param batch_size: The maximum number of records to include in each batch.
            :param consumer_group_id: The name of the destination queue to consume.
            :param credentials: The credentials needed to access the resource.
            :param maximum_batching_window_in_seconds: The maximum length of a time to wait for events.
            :param server_root_ca_certificate: The ARN of the Secrets Manager secret used for certification.
            :param starting_position: The position in a stream from which to start reading.
            :param topic_name: The name of the topic that the pipe will read from.
            :param vpc: This structure specifies the VPC subnets and security groups for the stream, and whether a public IP address is to be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceselfmanagedkafkaparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_source_self_managed_kafka_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeSourceSelfManagedKafkaParametersProperty(
                    additional_bootstrap_servers=["additionalBootstrapServers"],
                    batch_size=123,
                    consumer_group_id="consumerGroupId",
                    credentials=pipes_mixins.CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationCredentialsProperty(
                        basic_auth="basicAuth",
                        client_certificate_tls_auth="clientCertificateTlsAuth",
                        sasl_scram256_auth="saslScram256Auth",
                        sasl_scram512_auth="saslScram512Auth"
                    ),
                    maximum_batching_window_in_seconds=123,
                    server_root_ca_certificate="serverRootCaCertificate",
                    starting_position="startingPosition",
                    topic_name="topicName",
                    vpc=pipes_mixins.CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationVpcProperty(
                        security_group=["securityGroup"],
                        subnets=["subnets"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed226e689beda79446361bdfeb1cca7819d52d537c328c161abc0a57215fd1a2)
                check_type(argname="argument additional_bootstrap_servers", value=additional_bootstrap_servers, expected_type=type_hints["additional_bootstrap_servers"])
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument consumer_group_id", value=consumer_group_id, expected_type=type_hints["consumer_group_id"])
                check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
                check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
                check_type(argname="argument server_root_ca_certificate", value=server_root_ca_certificate, expected_type=type_hints["server_root_ca_certificate"])
                check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
                check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
                check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_bootstrap_servers is not None:
                self._values["additional_bootstrap_servers"] = additional_bootstrap_servers
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if consumer_group_id is not None:
                self._values["consumer_group_id"] = consumer_group_id
            if credentials is not None:
                self._values["credentials"] = credentials
            if maximum_batching_window_in_seconds is not None:
                self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
            if server_root_ca_certificate is not None:
                self._values["server_root_ca_certificate"] = server_root_ca_certificate
            if starting_position is not None:
                self._values["starting_position"] = starting_position
            if topic_name is not None:
                self._values["topic_name"] = topic_name
            if vpc is not None:
                self._values["vpc"] = vpc

        @builtins.property
        def additional_bootstrap_servers(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of server URLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceselfmanagedkafkaparameters.html#cfn-pipes-pipe-pipesourceselfmanagedkafkaparameters-additionalbootstrapservers
            '''
            result = self._values.get("additional_bootstrap_servers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of records to include in each batch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceselfmanagedkafkaparameters.html#cfn-pipes-pipe-pipesourceselfmanagedkafkaparameters-batchsize
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def consumer_group_id(self) -> typing.Optional[builtins.str]:
            '''The name of the destination queue to consume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceselfmanagedkafkaparameters.html#cfn-pipes-pipe-pipesourceselfmanagedkafkaparameters-consumergroupid
            '''
            result = self._values.get("consumer_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationCredentialsProperty"]]:
            '''The credentials needed to access the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceselfmanagedkafkaparameters.html#cfn-pipes-pipe-pipesourceselfmanagedkafkaparameters-credentials
            '''
            result = self._values.get("credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationCredentialsProperty"]], result)

        @builtins.property
        def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum length of a time to wait for events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceselfmanagedkafkaparameters.html#cfn-pipes-pipe-pipesourceselfmanagedkafkaparameters-maximumbatchingwindowinseconds
            '''
            result = self._values.get("maximum_batching_window_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def server_root_ca_certificate(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Secrets Manager secret used for certification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceselfmanagedkafkaparameters.html#cfn-pipes-pipe-pipesourceselfmanagedkafkaparameters-serverrootcacertificate
            '''
            result = self._values.get("server_root_ca_certificate")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def starting_position(self) -> typing.Optional[builtins.str]:
            '''The position in a stream from which to start reading.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceselfmanagedkafkaparameters.html#cfn-pipes-pipe-pipesourceselfmanagedkafkaparameters-startingposition
            '''
            result = self._values.get("starting_position")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_name(self) -> typing.Optional[builtins.str]:
            '''The name of the topic that the pipe will read from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceselfmanagedkafkaparameters.html#cfn-pipes-pipe-pipesourceselfmanagedkafkaparameters-topicname
            '''
            result = self._values.get("topic_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationVpcProperty"]]:
            '''This structure specifies the VPC subnets and security groups for the stream, and whether a public IP address is to be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourceselfmanagedkafkaparameters.html#cfn-pipes-pipe-pipesourceselfmanagedkafkaparameters-vpc
            '''
            result = self._values.get("vpc")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationVpcProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeSourceSelfManagedKafkaParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeSourceSqsQueueParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "batch_size": "batchSize",
            "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
        },
    )
    class PipeSourceSqsQueueParametersProperty:
        def __init__(
            self,
            *,
            batch_size: typing.Optional[jsii.Number] = None,
            maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The parameters for using a Amazon SQS stream as a source.

            :param batch_size: The maximum number of records to include in each batch.
            :param maximum_batching_window_in_seconds: The maximum length of a time to wait for events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcesqsqueueparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_source_sqs_queue_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeSourceSqsQueueParametersProperty(
                    batch_size=123,
                    maximum_batching_window_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__286e2e2fb4d2dc263784f0b4f06f0f5b86460d0493517534bcded22065c39513)
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument maximum_batching_window_in_seconds", value=maximum_batching_window_in_seconds, expected_type=type_hints["maximum_batching_window_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if maximum_batching_window_in_seconds is not None:
                self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of records to include in each batch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcesqsqueueparameters.html#cfn-pipes-pipe-pipesourcesqsqueueparameters-batchsize
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum length of a time to wait for events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipesourcesqsqueueparameters.html#cfn-pipes-pipe-pipesourcesqsqueueparameters-maximumbatchingwindowinseconds
            '''
            result = self._values.get("maximum_batching_window_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeSourceSqsQueueParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeTargetBatchJobParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "array_properties": "arrayProperties",
            "container_overrides": "containerOverrides",
            "depends_on": "dependsOn",
            "job_definition": "jobDefinition",
            "job_name": "jobName",
            "parameters": "parameters",
            "retry_strategy": "retryStrategy",
        },
    )
    class PipeTargetBatchJobParametersProperty:
        def __init__(
            self,
            *,
            array_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.BatchArrayPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            container_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.BatchContainerOverridesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            depends_on: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.BatchJobDependencyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            job_definition: typing.Optional[builtins.str] = None,
            job_name: typing.Optional[builtins.str] = None,
            parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            retry_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.BatchRetryStrategyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The parameters for using an AWS Batch job as a target.

            :param array_properties: The array properties for the submitted job, such as the size of the array. The array size can be between 2 and 10,000. If you specify array properties for a job, it becomes an array job. This parameter is used only if the target is an AWS Batch job.
            :param container_overrides: The overrides that are sent to a container.
            :param depends_on: A list of dependencies for the job. A job can depend upon a maximum of 20 jobs. You can specify a ``SEQUENTIAL`` type dependency without specifying a job ID for array jobs so that each child array job completes sequentially, starting at index 0. You can also specify an ``N_TO_N`` type dependency with a job ID for array jobs. In that case, each index child of this job must wait for the corresponding index child of each dependency to complete before it can begin.
            :param job_definition: The job definition used by this job. This value can be one of ``name`` , ``name:revision`` , or the Amazon Resource Name (ARN) for the job definition. If name is specified without a revision then the latest active revision is used.
            :param job_name: The name of the job. It can be up to 128 letters long. The first character must be alphanumeric, can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).
            :param parameters: Additional parameters passed to the job that replace parameter substitution placeholders that are set in the job definition. Parameters are specified as a key and value pair mapping. Parameters included here override any corresponding parameter defaults from the job definition.
            :param retry_strategy: The retry strategy to use for failed jobs. When a retry strategy is specified here, it overrides the retry strategy defined in the job definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetbatchjobparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_target_batch_job_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeTargetBatchJobParametersProperty(
                    array_properties=pipes_mixins.CfnPipePropsMixin.BatchArrayPropertiesProperty(
                        size=123
                    ),
                    container_overrides=pipes_mixins.CfnPipePropsMixin.BatchContainerOverridesProperty(
                        command=["command"],
                        environment=[pipes_mixins.CfnPipePropsMixin.BatchEnvironmentVariableProperty(
                            name="name",
                            value="value"
                        )],
                        instance_type="instanceType",
                        resource_requirements=[pipes_mixins.CfnPipePropsMixin.BatchResourceRequirementProperty(
                            type="type",
                            value="value"
                        )]
                    ),
                    depends_on=[pipes_mixins.CfnPipePropsMixin.BatchJobDependencyProperty(
                        job_id="jobId",
                        type="type"
                    )],
                    job_definition="jobDefinition",
                    job_name="jobName",
                    parameters={
                        "parameters_key": "parameters"
                    },
                    retry_strategy=pipes_mixins.CfnPipePropsMixin.BatchRetryStrategyProperty(
                        attempts=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6fd08d0376c810aeb6354cd97a5851a60ce95181348df48b61710def8608784)
                check_type(argname="argument array_properties", value=array_properties, expected_type=type_hints["array_properties"])
                check_type(argname="argument container_overrides", value=container_overrides, expected_type=type_hints["container_overrides"])
                check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
                check_type(argname="argument job_definition", value=job_definition, expected_type=type_hints["job_definition"])
                check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument retry_strategy", value=retry_strategy, expected_type=type_hints["retry_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if array_properties is not None:
                self._values["array_properties"] = array_properties
            if container_overrides is not None:
                self._values["container_overrides"] = container_overrides
            if depends_on is not None:
                self._values["depends_on"] = depends_on
            if job_definition is not None:
                self._values["job_definition"] = job_definition
            if job_name is not None:
                self._values["job_name"] = job_name
            if parameters is not None:
                self._values["parameters"] = parameters
            if retry_strategy is not None:
                self._values["retry_strategy"] = retry_strategy

        @builtins.property
        def array_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.BatchArrayPropertiesProperty"]]:
            '''The array properties for the submitted job, such as the size of the array.

            The array size can be between 2 and 10,000. If you specify array properties for a job, it becomes an array job. This parameter is used only if the target is an AWS Batch job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetbatchjobparameters.html#cfn-pipes-pipe-pipetargetbatchjobparameters-arrayproperties
            '''
            result = self._values.get("array_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.BatchArrayPropertiesProperty"]], result)

        @builtins.property
        def container_overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.BatchContainerOverridesProperty"]]:
            '''The overrides that are sent to a container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetbatchjobparameters.html#cfn-pipes-pipe-pipetargetbatchjobparameters-containeroverrides
            '''
            result = self._values.get("container_overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.BatchContainerOverridesProperty"]], result)

        @builtins.property
        def depends_on(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.BatchJobDependencyProperty"]]]]:
            '''A list of dependencies for the job.

            A job can depend upon a maximum of 20 jobs. You can specify a ``SEQUENTIAL`` type dependency without specifying a job ID for array jobs so that each child array job completes sequentially, starting at index 0. You can also specify an ``N_TO_N`` type dependency with a job ID for array jobs. In that case, each index child of this job must wait for the corresponding index child of each dependency to complete before it can begin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetbatchjobparameters.html#cfn-pipes-pipe-pipetargetbatchjobparameters-dependson
            '''
            result = self._values.get("depends_on")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.BatchJobDependencyProperty"]]]], result)

        @builtins.property
        def job_definition(self) -> typing.Optional[builtins.str]:
            '''The job definition used by this job.

            This value can be one of ``name`` , ``name:revision`` , or the Amazon Resource Name (ARN) for the job definition. If name is specified without a revision then the latest active revision is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetbatchjobparameters.html#cfn-pipes-pipe-pipetargetbatchjobparameters-jobdefinition
            '''
            result = self._values.get("job_definition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def job_name(self) -> typing.Optional[builtins.str]:
            '''The name of the job.

            It can be up to 128 letters long. The first character must be alphanumeric, can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetbatchjobparameters.html#cfn-pipes-pipe-pipetargetbatchjobparameters-jobname
            '''
            result = self._values.get("job_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Additional parameters passed to the job that replace parameter substitution placeholders that are set in the job definition.

            Parameters are specified as a key and value pair mapping. Parameters included here override any corresponding parameter defaults from the job definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetbatchjobparameters.html#cfn-pipes-pipe-pipetargetbatchjobparameters-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def retry_strategy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.BatchRetryStrategyProperty"]]:
            '''The retry strategy to use for failed jobs.

            When a retry strategy is specified here, it overrides the retry strategy defined in the job definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetbatchjobparameters.html#cfn-pipes-pipe-pipetargetbatchjobparameters-retrystrategy
            '''
            result = self._values.get("retry_strategy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.BatchRetryStrategyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeTargetBatchJobParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeTargetCloudWatchLogsParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"log_stream_name": "logStreamName", "timestamp": "timestamp"},
    )
    class PipeTargetCloudWatchLogsParametersProperty:
        def __init__(
            self,
            *,
            log_stream_name: typing.Optional[builtins.str] = None,
            timestamp: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for using an CloudWatch Logs log stream as a target.

            :param log_stream_name: The name of the log stream.
            :param timestamp: A `dynamic path parameter <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-target.html>`_ to a field in the payload containing the time the event occurred, expressed as the number of milliseconds after Jan 1, 1970 00:00:00 UTC. The value cannot be a static timestamp as the provided timestamp would be applied to all events delivered by the Pipe, regardless of when they are actually delivered. If no dynamic path parameter is provided, the default value is the time the invocation is processed by the Pipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetcloudwatchlogsparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_target_cloud_watch_logs_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeTargetCloudWatchLogsParametersProperty(
                    log_stream_name="logStreamName",
                    timestamp="timestamp"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7cc264f643e41c3a115542e3341618770a7199b88e61fcf6571ee60352e9b98)
                check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
                check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_stream_name is not None:
                self._values["log_stream_name"] = log_stream_name
            if timestamp is not None:
                self._values["timestamp"] = timestamp

        @builtins.property
        def log_stream_name(self) -> typing.Optional[builtins.str]:
            '''The name of the log stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetcloudwatchlogsparameters.html#cfn-pipes-pipe-pipetargetcloudwatchlogsparameters-logstreamname
            '''
            result = self._values.get("log_stream_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timestamp(self) -> typing.Optional[builtins.str]:
            '''A `dynamic path parameter <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-target.html>`_ to a field in the payload containing the time the event occurred, expressed as the number of milliseconds after Jan 1, 1970 00:00:00 UTC.

            The value cannot be a static timestamp as the provided timestamp would be applied to all events delivered by the Pipe, regardless of when they are actually delivered.

            If no dynamic path parameter is provided, the default value is the time the invocation is processed by the Pipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetcloudwatchlogsparameters.html#cfn-pipes-pipe-pipetargetcloudwatchlogsparameters-timestamp
            '''
            result = self._values.get("timestamp")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeTargetCloudWatchLogsParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeTargetEcsTaskParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_provider_strategy": "capacityProviderStrategy",
            "enable_ecs_managed_tags": "enableEcsManagedTags",
            "enable_execute_command": "enableExecuteCommand",
            "group": "group",
            "launch_type": "launchType",
            "network_configuration": "networkConfiguration",
            "overrides": "overrides",
            "placement_constraints": "placementConstraints",
            "placement_strategy": "placementStrategy",
            "platform_version": "platformVersion",
            "propagate_tags": "propagateTags",
            "reference_id": "referenceId",
            "tags": "tags",
            "task_count": "taskCount",
            "task_definition_arn": "taskDefinitionArn",
        },
    )
    class PipeTargetEcsTaskParametersProperty:
        def __init__(
            self,
            *,
            capacity_provider_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.CapacityProviderStrategyItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            enable_ecs_managed_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enable_execute_command: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            group: typing.Optional[builtins.str] = None,
            launch_type: typing.Optional[builtins.str] = None,
            network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.EcsTaskOverrideProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            placement_constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PlacementConstraintProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            placement_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PlacementStrategyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            platform_version: typing.Optional[builtins.str] = None,
            propagate_tags: typing.Optional[builtins.str] = None,
            reference_id: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
            task_count: typing.Optional[jsii.Number] = None,
            task_definition_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for using an Amazon ECS task as a target.

            :param capacity_provider_strategy: The capacity provider strategy to use for the task. If a ``capacityProviderStrategy`` is specified, the ``launchType`` parameter must be omitted. If no ``capacityProviderStrategy`` or launchType is specified, the ``defaultCapacityProviderStrategy`` for the cluster is used.
            :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the task. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: - false
            :param enable_execute_command: Whether or not to enable the execute command functionality for the containers in this task. If true, this enables execute command functionality on all containers in the task. Default: - false
            :param group: Specifies an Amazon ECS task group for the task. The maximum length is 255 characters.
            :param launch_type: Specifies the launch type on which your task is running. The launch type that you specify here must match one of the launch type (compatibilities) of the target task. The ``FARGATE`` value is supported only in the Regions where AWS Fargate with Amazon ECS is supported. For more information, see `AWS Fargate on Amazon ECS <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS-Fargate.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param network_configuration: Use this structure if the Amazon ECS task uses the ``awsvpc`` network mode. This structure specifies the VPC subnets and security groups associated with the task, and whether a public IP address is to be used. This structure is required if ``LaunchType`` is ``FARGATE`` because the ``awsvpc`` mode is required for Fargate tasks. If you specify ``NetworkConfiguration`` when the target ECS task does not use the ``awsvpc`` network mode, the task fails.
            :param overrides: The overrides that are associated with a task.
            :param placement_constraints: An array of placement constraint objects to use for the task. You can specify up to 10 constraints per task (including constraints in the task definition and those specified at runtime).
            :param placement_strategy: The placement strategy objects to use for the task. You can specify a maximum of five strategy rules per task.
            :param platform_version: Specifies the platform version for the task. Specify only the numeric portion of the platform version, such as ``1.1.0`` . This structure is used only if ``LaunchType`` is ``FARGATE`` . For more information about valid platform versions, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param propagate_tags: Specifies whether to propagate the tags from the task definition to the task. If no value is specified, the tags are not propagated. Tags can only be propagated to the task during task creation. To add tags to a task after task creation, use the ``TagResource`` API action.
            :param reference_id: The reference ID to use for the task.
            :param tags: The metadata that you apply to the task to help you categorize and organize them. Each tag consists of a key and an optional value, both of which you define. To learn more, see `RunTask <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html#ECS-RunTask-request-tags>`_ in the Amazon ECS API Reference.
            :param task_count: The number of tasks to create based on ``TaskDefinition`` . The default is 1.
            :param task_definition_arn: The ARN of the task definition to use if the event target is an Amazon ECS task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_target_ecs_task_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeTargetEcsTaskParametersProperty(
                    capacity_provider_strategy=[pipes_mixins.CfnPipePropsMixin.CapacityProviderStrategyItemProperty(
                        base=123,
                        capacity_provider="capacityProvider",
                        weight=123
                    )],
                    enable_ecs_managed_tags=False,
                    enable_execute_command=False,
                    group="group",
                    launch_type="launchType",
                    network_configuration=pipes_mixins.CfnPipePropsMixin.NetworkConfigurationProperty(
                        awsvpc_configuration=pipes_mixins.CfnPipePropsMixin.AwsVpcConfigurationProperty(
                            assign_public_ip="assignPublicIp",
                            security_groups=["securityGroups"],
                            subnets=["subnets"]
                        )
                    ),
                    overrides=pipes_mixins.CfnPipePropsMixin.EcsTaskOverrideProperty(
                        container_overrides=[pipes_mixins.CfnPipePropsMixin.EcsContainerOverrideProperty(
                            command=["command"],
                            cpu=123,
                            environment=[pipes_mixins.CfnPipePropsMixin.EcsEnvironmentVariableProperty(
                                name="name",
                                value="value"
                            )],
                            environment_files=[pipes_mixins.CfnPipePropsMixin.EcsEnvironmentFileProperty(
                                type="type",
                                value="value"
                            )],
                            memory=123,
                            memory_reservation=123,
                            name="name",
                            resource_requirements=[pipes_mixins.CfnPipePropsMixin.EcsResourceRequirementProperty(
                                type="type",
                                value="value"
                            )]
                        )],
                        cpu="cpu",
                        ephemeral_storage=pipes_mixins.CfnPipePropsMixin.EcsEphemeralStorageProperty(
                            size_in_gi_b=123
                        ),
                        execution_role_arn="executionRoleArn",
                        inference_accelerator_overrides=[pipes_mixins.CfnPipePropsMixin.EcsInferenceAcceleratorOverrideProperty(
                            device_name="deviceName",
                            device_type="deviceType"
                        )],
                        memory="memory",
                        task_role_arn="taskRoleArn"
                    ),
                    placement_constraints=[pipes_mixins.CfnPipePropsMixin.PlacementConstraintProperty(
                        expression="expression",
                        type="type"
                    )],
                    placement_strategy=[pipes_mixins.CfnPipePropsMixin.PlacementStrategyProperty(
                        field="field",
                        type="type"
                    )],
                    platform_version="platformVersion",
                    propagate_tags="propagateTags",
                    reference_id="referenceId",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    task_count=123,
                    task_definition_arn="taskDefinitionArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df966888dfb055801962dc014e71d1bb2fb4ddeda2991385903c7fdbe8696dbe)
                check_type(argname="argument capacity_provider_strategy", value=capacity_provider_strategy, expected_type=type_hints["capacity_provider_strategy"])
                check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
                check_type(argname="argument enable_execute_command", value=enable_execute_command, expected_type=type_hints["enable_execute_command"])
                check_type(argname="argument group", value=group, expected_type=type_hints["group"])
                check_type(argname="argument launch_type", value=launch_type, expected_type=type_hints["launch_type"])
                check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
                check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
                check_type(argname="argument placement_constraints", value=placement_constraints, expected_type=type_hints["placement_constraints"])
                check_type(argname="argument placement_strategy", value=placement_strategy, expected_type=type_hints["placement_strategy"])
                check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
                check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
                check_type(argname="argument reference_id", value=reference_id, expected_type=type_hints["reference_id"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                check_type(argname="argument task_count", value=task_count, expected_type=type_hints["task_count"])
                check_type(argname="argument task_definition_arn", value=task_definition_arn, expected_type=type_hints["task_definition_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_provider_strategy is not None:
                self._values["capacity_provider_strategy"] = capacity_provider_strategy
            if enable_ecs_managed_tags is not None:
                self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
            if enable_execute_command is not None:
                self._values["enable_execute_command"] = enable_execute_command
            if group is not None:
                self._values["group"] = group
            if launch_type is not None:
                self._values["launch_type"] = launch_type
            if network_configuration is not None:
                self._values["network_configuration"] = network_configuration
            if overrides is not None:
                self._values["overrides"] = overrides
            if placement_constraints is not None:
                self._values["placement_constraints"] = placement_constraints
            if placement_strategy is not None:
                self._values["placement_strategy"] = placement_strategy
            if platform_version is not None:
                self._values["platform_version"] = platform_version
            if propagate_tags is not None:
                self._values["propagate_tags"] = propagate_tags
            if reference_id is not None:
                self._values["reference_id"] = reference_id
            if tags is not None:
                self._values["tags"] = tags
            if task_count is not None:
                self._values["task_count"] = task_count
            if task_definition_arn is not None:
                self._values["task_definition_arn"] = task_definition_arn

        @builtins.property
        def capacity_provider_strategy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.CapacityProviderStrategyItemProperty"]]]]:
            '''The capacity provider strategy to use for the task.

            If a ``capacityProviderStrategy`` is specified, the ``launchType`` parameter must be omitted. If no ``capacityProviderStrategy`` or launchType is specified, the ``defaultCapacityProviderStrategy`` for the cluster is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-capacityproviderstrategy
            '''
            result = self._values.get("capacity_provider_strategy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.CapacityProviderStrategyItemProperty"]]]], result)

        @builtins.property
        def enable_ecs_managed_tags(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to enable Amazon ECS managed tags for the task.

            For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ in the Amazon Elastic Container Service Developer Guide.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-enableecsmanagedtags
            '''
            result = self._values.get("enable_ecs_managed_tags")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enable_execute_command(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether or not to enable the execute command functionality for the containers in this task.

            If true, this enables execute command functionality on all containers in the task.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-enableexecutecommand
            '''
            result = self._values.get("enable_execute_command")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def group(self) -> typing.Optional[builtins.str]:
            '''Specifies an Amazon ECS task group for the task.

            The maximum length is 255 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-group
            '''
            result = self._values.get("group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def launch_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the launch type on which your task is running.

            The launch type that you specify here must match one of the launch type (compatibilities) of the target task. The ``FARGATE`` value is supported only in the Regions where AWS Fargate with Amazon ECS is supported. For more information, see `AWS Fargate on Amazon ECS <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS-Fargate.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-launchtype
            '''
            result = self._values.get("launch_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.NetworkConfigurationProperty"]]:
            '''Use this structure if the Amazon ECS task uses the ``awsvpc`` network mode.

            This structure specifies the VPC subnets and security groups associated with the task, and whether a public IP address is to be used. This structure is required if ``LaunchType`` is ``FARGATE`` because the ``awsvpc`` mode is required for Fargate tasks.

            If you specify ``NetworkConfiguration`` when the target ECS task does not use the ``awsvpc`` network mode, the task fails.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-networkconfiguration
            '''
            result = self._values.get("network_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.NetworkConfigurationProperty"]], result)

        @builtins.property
        def overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.EcsTaskOverrideProperty"]]:
            '''The overrides that are associated with a task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-overrides
            '''
            result = self._values.get("overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.EcsTaskOverrideProperty"]], result)

        @builtins.property
        def placement_constraints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PlacementConstraintProperty"]]]]:
            '''An array of placement constraint objects to use for the task.

            You can specify up to 10 constraints per task (including constraints in the task definition and those specified at runtime).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-placementconstraints
            '''
            result = self._values.get("placement_constraints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PlacementConstraintProperty"]]]], result)

        @builtins.property
        def placement_strategy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PlacementStrategyProperty"]]]]:
            '''The placement strategy objects to use for the task.

            You can specify a maximum of five strategy rules per task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-placementstrategy
            '''
            result = self._values.get("placement_strategy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PlacementStrategyProperty"]]]], result)

        @builtins.property
        def platform_version(self) -> typing.Optional[builtins.str]:
            '''Specifies the platform version for the task.

            Specify only the numeric portion of the platform version, such as ``1.1.0`` .

            This structure is used only if ``LaunchType`` is ``FARGATE`` . For more information about valid platform versions, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-platformversion
            '''
            result = self._values.get("platform_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def propagate_tags(self) -> typing.Optional[builtins.str]:
            '''Specifies whether to propagate the tags from the task definition to the task.

            If no value is specified, the tags are not propagated. Tags can only be propagated to the task during task creation. To add tags to a task after task creation, use the ``TagResource`` API action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-propagatetags
            '''
            result = self._values.get("propagate_tags")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def reference_id(self) -> typing.Optional[builtins.str]:
            '''The reference ID to use for the task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-referenceid
            '''
            result = self._values.get("reference_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''The metadata that you apply to the task to help you categorize and organize them.

            Each tag consists of a key and an optional value, both of which you define. To learn more, see `RunTask <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html#ECS-RunTask-request-tags>`_ in the Amazon ECS API Reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        @builtins.property
        def task_count(self) -> typing.Optional[jsii.Number]:
            '''The number of tasks to create based on ``TaskDefinition`` .

            The default is 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-taskcount
            '''
            result = self._values.get("task_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def task_definition_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the task definition to use if the event target is an Amazon ECS task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetecstaskparameters.html#cfn-pipes-pipe-pipetargetecstaskparameters-taskdefinitionarn
            '''
            result = self._values.get("task_definition_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeTargetEcsTaskParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeTargetEventBridgeEventBusParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "detail_type": "detailType",
            "endpoint_id": "endpointId",
            "resources": "resources",
            "source": "source",
            "time": "time",
        },
    )
    class PipeTargetEventBridgeEventBusParametersProperty:
        def __init__(
            self,
            *,
            detail_type: typing.Optional[builtins.str] = None,
            endpoint_id: typing.Optional[builtins.str] = None,
            resources: typing.Optional[typing.Sequence[builtins.str]] = None,
            source: typing.Optional[builtins.str] = None,
            time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for using an EventBridge event bus as a target.

            :param detail_type: A free-form string, with a maximum of 128 characters, used to decide what fields to expect in the event detail.
            :param endpoint_id: The URL subdomain of the endpoint. For example, if the URL for Endpoint is https://abcde.veo.endpoints.event.amazonaws.com, then the EndpointId is ``abcde.veo`` .
            :param resources: AWS resources, identified by Amazon Resource Name (ARN), which the event primarily concerns. Any number, including zero, may be present.
            :param source: The source of the event.
            :param time: The time stamp of the event, per `RFC3339 <https://docs.aws.amazon.com/https://www.rfc-editor.org/rfc/rfc3339.txt>`_ . If no time stamp is provided, the time stamp of the `PutEvents <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutEvents.html>`_ call is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargeteventbridgeeventbusparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_target_event_bridge_event_bus_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeTargetEventBridgeEventBusParametersProperty(
                    detail_type="detailType",
                    endpoint_id="endpointId",
                    resources=["resources"],
                    source="source",
                    time="time"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c57f87b545e905597356e0e85ed67dc2c3d334ff59d37be6e461767b5bcaea5)
                check_type(argname="argument detail_type", value=detail_type, expected_type=type_hints["detail_type"])
                check_type(argname="argument endpoint_id", value=endpoint_id, expected_type=type_hints["endpoint_id"])
                check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument time", value=time, expected_type=type_hints["time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if detail_type is not None:
                self._values["detail_type"] = detail_type
            if endpoint_id is not None:
                self._values["endpoint_id"] = endpoint_id
            if resources is not None:
                self._values["resources"] = resources
            if source is not None:
                self._values["source"] = source
            if time is not None:
                self._values["time"] = time

        @builtins.property
        def detail_type(self) -> typing.Optional[builtins.str]:
            '''A free-form string, with a maximum of 128 characters, used to decide what fields to expect in the event detail.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargeteventbridgeeventbusparameters.html#cfn-pipes-pipe-pipetargeteventbridgeeventbusparameters-detailtype
            '''
            result = self._values.get("detail_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint_id(self) -> typing.Optional[builtins.str]:
            '''The URL subdomain of the endpoint.

            For example, if the URL for Endpoint is https://abcde.veo.endpoints.event.amazonaws.com, then the EndpointId is ``abcde.veo`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargeteventbridgeeventbusparameters.html#cfn-pipes-pipe-pipetargeteventbridgeeventbusparameters-endpointid
            '''
            result = self._values.get("endpoint_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resources(self) -> typing.Optional[typing.List[builtins.str]]:
            '''AWS resources, identified by Amazon Resource Name (ARN), which the event primarily concerns.

            Any number, including zero, may be present.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargeteventbridgeeventbusparameters.html#cfn-pipes-pipe-pipetargeteventbridgeeventbusparameters-resources
            '''
            result = self._values.get("resources")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The source of the event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargeteventbridgeeventbusparameters.html#cfn-pipes-pipe-pipetargeteventbridgeeventbusparameters-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time(self) -> typing.Optional[builtins.str]:
            '''The time stamp of the event, per `RFC3339 <https://docs.aws.amazon.com/https://www.rfc-editor.org/rfc/rfc3339.txt>`_ . If no time stamp is provided, the time stamp of the `PutEvents <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutEvents.html>`_ call is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargeteventbridgeeventbusparameters.html#cfn-pipes-pipe-pipetargeteventbridgeeventbusparameters-time
            '''
            result = self._values.get("time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeTargetEventBridgeEventBusParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeTargetHttpParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "header_parameters": "headerParameters",
            "path_parameter_values": "pathParameterValues",
            "query_string_parameters": "queryStringParameters",
        },
    )
    class PipeTargetHttpParametersProperty:
        def __init__(
            self,
            *,
            header_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            query_string_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''These are custom parameter to be used when the target is an API Gateway REST APIs or EventBridge ApiDestinations.

            :param header_parameters: The headers that need to be sent as part of request invoking the API Gateway REST API or EventBridge ApiDestination.
            :param path_parameter_values: The path parameter values to be used to populate API Gateway REST API or EventBridge ApiDestination path wildcards ("*").
            :param query_string_parameters: The query string keys/values that need to be sent as part of request invoking the API Gateway REST API or EventBridge ApiDestination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargethttpparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_target_http_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeTargetHttpParametersProperty(
                    header_parameters={
                        "header_parameters_key": "headerParameters"
                    },
                    path_parameter_values=["pathParameterValues"],
                    query_string_parameters={
                        "query_string_parameters_key": "queryStringParameters"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fadf710f198bab019580591eb1c16f6657fb9d74fd8df047d8a9679cc872ff70)
                check_type(argname="argument header_parameters", value=header_parameters, expected_type=type_hints["header_parameters"])
                check_type(argname="argument path_parameter_values", value=path_parameter_values, expected_type=type_hints["path_parameter_values"])
                check_type(argname="argument query_string_parameters", value=query_string_parameters, expected_type=type_hints["query_string_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if header_parameters is not None:
                self._values["header_parameters"] = header_parameters
            if path_parameter_values is not None:
                self._values["path_parameter_values"] = path_parameter_values
            if query_string_parameters is not None:
                self._values["query_string_parameters"] = query_string_parameters

        @builtins.property
        def header_parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The headers that need to be sent as part of request invoking the API Gateway REST API or EventBridge ApiDestination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargethttpparameters.html#cfn-pipes-pipe-pipetargethttpparameters-headerparameters
            '''
            result = self._values.get("header_parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def path_parameter_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The path parameter values to be used to populate API Gateway REST API or EventBridge ApiDestination path wildcards ("*").

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargethttpparameters.html#cfn-pipes-pipe-pipetargethttpparameters-pathparametervalues
            '''
            result = self._values.get("path_parameter_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def query_string_parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The query string keys/values that need to be sent as part of request invoking the API Gateway REST API or EventBridge ApiDestination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargethttpparameters.html#cfn-pipes-pipe-pipetargethttpparameters-querystringparameters
            '''
            result = self._values.get("query_string_parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeTargetHttpParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeTargetKinesisStreamParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"partition_key": "partitionKey"},
    )
    class PipeTargetKinesisStreamParametersProperty:
        def __init__(
            self,
            *,
            partition_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for using a Kinesis stream as a target.

            :param partition_key: Determines which shard in the stream the data record is assigned to. Partition keys are Unicode strings with a maximum length limit of 256 characters for each key. Amazon Kinesis Data Streams uses the partition key as input to a hash function that maps the partition key and associated data to a specific shard. Specifically, an MD5 hash function is used to map partition keys to 128-bit integer values and to map associated data records to shards. As a result of this hashing mechanism, all data records with the same partition key map to the same shard within the stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetkinesisstreamparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_target_kinesis_stream_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeTargetKinesisStreamParametersProperty(
                    partition_key="partitionKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba21cf038ee03e611a3daf8728fccb5a3fed46d36dd74a60f5de5e862320b308)
                check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if partition_key is not None:
                self._values["partition_key"] = partition_key

        @builtins.property
        def partition_key(self) -> typing.Optional[builtins.str]:
            '''Determines which shard in the stream the data record is assigned to.

            Partition keys are Unicode strings with a maximum length limit of 256 characters for each key. Amazon Kinesis Data Streams uses the partition key as input to a hash function that maps the partition key and associated data to a specific shard. Specifically, an MD5 hash function is used to map partition keys to 128-bit integer values and to map associated data records to shards. As a result of this hashing mechanism, all data records with the same partition key map to the same shard within the stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetkinesisstreamparameters.html#cfn-pipes-pipe-pipetargetkinesisstreamparameters-partitionkey
            '''
            result = self._values.get("partition_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeTargetKinesisStreamParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeTargetLambdaFunctionParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"invocation_type": "invocationType"},
    )
    class PipeTargetLambdaFunctionParametersProperty:
        def __init__(
            self,
            *,
            invocation_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for using a Lambda function as a target.

            :param invocation_type: Specify whether to invoke the function synchronously or asynchronously. - ``REQUEST_RESPONSE`` (default) - Invoke synchronously. This corresponds to the ``RequestResponse`` option in the ``InvocationType`` parameter for the Lambda `Invoke <https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html#API_Invoke_RequestSyntax>`_ API. - ``FIRE_AND_FORGET`` - Invoke asynchronously. This corresponds to the ``Event`` option in the ``InvocationType`` parameter for the Lambda `Invoke <https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html#API_Invoke_RequestSyntax>`_ API. For more information, see `Invocation types <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes.html#pipes-invocation>`_ in the *Amazon EventBridge User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetlambdafunctionparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_target_lambda_function_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeTargetLambdaFunctionParametersProperty(
                    invocation_type="invocationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83e376464d2a67d109c81240aa633c109a56168f4658895f7b05167cfaebd032)
                check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if invocation_type is not None:
                self._values["invocation_type"] = invocation_type

        @builtins.property
        def invocation_type(self) -> typing.Optional[builtins.str]:
            '''Specify whether to invoke the function synchronously or asynchronously.

            - ``REQUEST_RESPONSE`` (default) - Invoke synchronously. This corresponds to the ``RequestResponse`` option in the ``InvocationType`` parameter for the Lambda `Invoke <https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html#API_Invoke_RequestSyntax>`_ API.
            - ``FIRE_AND_FORGET`` - Invoke asynchronously. This corresponds to the ``Event`` option in the ``InvocationType`` parameter for the Lambda `Invoke <https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html#API_Invoke_RequestSyntax>`_ API.

            For more information, see `Invocation types <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes.html#pipes-invocation>`_ in the *Amazon EventBridge User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetlambdafunctionparameters.html#cfn-pipes-pipe-pipetargetlambdafunctionparameters-invocationtype
            '''
            result = self._values.get("invocation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeTargetLambdaFunctionParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeTargetParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "batch_job_parameters": "batchJobParameters",
            "cloud_watch_logs_parameters": "cloudWatchLogsParameters",
            "ecs_task_parameters": "ecsTaskParameters",
            "event_bridge_event_bus_parameters": "eventBridgeEventBusParameters",
            "http_parameters": "httpParameters",
            "input_template": "inputTemplate",
            "kinesis_stream_parameters": "kinesisStreamParameters",
            "lambda_function_parameters": "lambdaFunctionParameters",
            "redshift_data_parameters": "redshiftDataParameters",
            "sage_maker_pipeline_parameters": "sageMakerPipelineParameters",
            "sqs_queue_parameters": "sqsQueueParameters",
            "step_function_state_machine_parameters": "stepFunctionStateMachineParameters",
            "timestream_parameters": "timestreamParameters",
        },
    )
    class PipeTargetParametersProperty:
        def __init__(
            self,
            *,
            batch_job_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeTargetBatchJobParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloud_watch_logs_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeTargetCloudWatchLogsParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ecs_task_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeTargetEcsTaskParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            event_bridge_event_bus_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeTargetEventBridgeEventBusParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            http_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeTargetHttpParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            input_template: typing.Optional[builtins.str] = None,
            kinesis_stream_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeTargetKinesisStreamParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_function_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeTargetLambdaFunctionParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            redshift_data_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeTargetRedshiftDataParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sage_maker_pipeline_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeTargetSageMakerPipelineParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sqs_queue_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeTargetSqsQueueParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            step_function_state_machine_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeTargetStateMachineParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timestream_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.PipeTargetTimestreamParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The parameters required to set up a target for your pipe.

            For more information about pipe target parameters, including how to use dynamic path parameters, see `Target parameters <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-target.html>`_ in the *Amazon EventBridge User Guide* .

            :param batch_job_parameters: The parameters for using an AWS Batch job as a target.
            :param cloud_watch_logs_parameters: The parameters for using an CloudWatch Logs log stream as a target.
            :param ecs_task_parameters: The parameters for using an Amazon ECS task as a target.
            :param event_bridge_event_bus_parameters: The parameters for using an EventBridge event bus as a target.
            :param http_parameters: These are custom parameter to be used when the target is an API Gateway REST APIs or EventBridge ApiDestinations.
            :param input_template: Valid JSON text passed to the target. In this case, nothing from the event itself is passed to the target. For more information, see `The JavaScript Object Notation (JSON) Data Interchange Format <https://docs.aws.amazon.com/http://www.rfc-editor.org/rfc/rfc7159.txt>`_ . To remove an input template, specify an empty string.
            :param kinesis_stream_parameters: The parameters for using a Kinesis stream as a target.
            :param lambda_function_parameters: The parameters for using a Lambda function as a target.
            :param redshift_data_parameters: These are custom parameters to be used when the target is a Amazon Redshift cluster to invoke the Amazon Redshift Data API BatchExecuteStatement.
            :param sage_maker_pipeline_parameters: The parameters for using a SageMaker AI pipeline as a target.
            :param sqs_queue_parameters: The parameters for using a Amazon SQS stream as a target.
            :param step_function_state_machine_parameters: The parameters for using a Step Functions state machine as a target.
            :param timestream_parameters: The parameters for using a Timestream for LiveAnalytics table as a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_target_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeTargetParametersProperty(
                    batch_job_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetBatchJobParametersProperty(
                        array_properties=pipes_mixins.CfnPipePropsMixin.BatchArrayPropertiesProperty(
                            size=123
                        ),
                        container_overrides=pipes_mixins.CfnPipePropsMixin.BatchContainerOverridesProperty(
                            command=["command"],
                            environment=[pipes_mixins.CfnPipePropsMixin.BatchEnvironmentVariableProperty(
                                name="name",
                                value="value"
                            )],
                            instance_type="instanceType",
                            resource_requirements=[pipes_mixins.CfnPipePropsMixin.BatchResourceRequirementProperty(
                                type="type",
                                value="value"
                            )]
                        ),
                        depends_on=[pipes_mixins.CfnPipePropsMixin.BatchJobDependencyProperty(
                            job_id="jobId",
                            type="type"
                        )],
                        job_definition="jobDefinition",
                        job_name="jobName",
                        parameters={
                            "parameters_key": "parameters"
                        },
                        retry_strategy=pipes_mixins.CfnPipePropsMixin.BatchRetryStrategyProperty(
                            attempts=123
                        )
                    ),
                    cloud_watch_logs_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetCloudWatchLogsParametersProperty(
                        log_stream_name="logStreamName",
                        timestamp="timestamp"
                    ),
                    ecs_task_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetEcsTaskParametersProperty(
                        capacity_provider_strategy=[pipes_mixins.CfnPipePropsMixin.CapacityProviderStrategyItemProperty(
                            base=123,
                            capacity_provider="capacityProvider",
                            weight=123
                        )],
                        enable_ecs_managed_tags=False,
                        enable_execute_command=False,
                        group="group",
                        launch_type="launchType",
                        network_configuration=pipes_mixins.CfnPipePropsMixin.NetworkConfigurationProperty(
                            awsvpc_configuration=pipes_mixins.CfnPipePropsMixin.AwsVpcConfigurationProperty(
                                assign_public_ip="assignPublicIp",
                                security_groups=["securityGroups"],
                                subnets=["subnets"]
                            )
                        ),
                        overrides=pipes_mixins.CfnPipePropsMixin.EcsTaskOverrideProperty(
                            container_overrides=[pipes_mixins.CfnPipePropsMixin.EcsContainerOverrideProperty(
                                command=["command"],
                                cpu=123,
                                environment=[pipes_mixins.CfnPipePropsMixin.EcsEnvironmentVariableProperty(
                                    name="name",
                                    value="value"
                                )],
                                environment_files=[pipes_mixins.CfnPipePropsMixin.EcsEnvironmentFileProperty(
                                    type="type",
                                    value="value"
                                )],
                                memory=123,
                                memory_reservation=123,
                                name="name",
                                resource_requirements=[pipes_mixins.CfnPipePropsMixin.EcsResourceRequirementProperty(
                                    type="type",
                                    value="value"
                                )]
                            )],
                            cpu="cpu",
                            ephemeral_storage=pipes_mixins.CfnPipePropsMixin.EcsEphemeralStorageProperty(
                                size_in_gi_b=123
                            ),
                            execution_role_arn="executionRoleArn",
                            inference_accelerator_overrides=[pipes_mixins.CfnPipePropsMixin.EcsInferenceAcceleratorOverrideProperty(
                                device_name="deviceName",
                                device_type="deviceType"
                            )],
                            memory="memory",
                            task_role_arn="taskRoleArn"
                        ),
                        placement_constraints=[pipes_mixins.CfnPipePropsMixin.PlacementConstraintProperty(
                            expression="expression",
                            type="type"
                        )],
                        placement_strategy=[pipes_mixins.CfnPipePropsMixin.PlacementStrategyProperty(
                            field="field",
                            type="type"
                        )],
                        platform_version="platformVersion",
                        propagate_tags="propagateTags",
                        reference_id="referenceId",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        task_count=123,
                        task_definition_arn="taskDefinitionArn"
                    ),
                    event_bridge_event_bus_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetEventBridgeEventBusParametersProperty(
                        detail_type="detailType",
                        endpoint_id="endpointId",
                        resources=["resources"],
                        source="source",
                        time="time"
                    ),
                    http_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetHttpParametersProperty(
                        header_parameters={
                            "header_parameters_key": "headerParameters"
                        },
                        path_parameter_values=["pathParameterValues"],
                        query_string_parameters={
                            "query_string_parameters_key": "queryStringParameters"
                        }
                    ),
                    input_template="inputTemplate",
                    kinesis_stream_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetKinesisStreamParametersProperty(
                        partition_key="partitionKey"
                    ),
                    lambda_function_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetLambdaFunctionParametersProperty(
                        invocation_type="invocationType"
                    ),
                    redshift_data_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetRedshiftDataParametersProperty(
                        database="database",
                        db_user="dbUser",
                        secret_manager_arn="secretManagerArn",
                        sqls=["sqls"],
                        statement_name="statementName",
                        with_event=False
                    ),
                    sage_maker_pipeline_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetSageMakerPipelineParametersProperty(
                        pipeline_parameter_list=[pipes_mixins.CfnPipePropsMixin.SageMakerPipelineParameterProperty(
                            name="name",
                            value="value"
                        )]
                    ),
                    sqs_queue_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetSqsQueueParametersProperty(
                        message_deduplication_id="messageDeduplicationId",
                        message_group_id="messageGroupId"
                    ),
                    step_function_state_machine_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetStateMachineParametersProperty(
                        invocation_type="invocationType"
                    ),
                    timestream_parameters=pipes_mixins.CfnPipePropsMixin.PipeTargetTimestreamParametersProperty(
                        dimension_mappings=[pipes_mixins.CfnPipePropsMixin.DimensionMappingProperty(
                            dimension_name="dimensionName",
                            dimension_value="dimensionValue",
                            dimension_value_type="dimensionValueType"
                        )],
                        epoch_time_unit="epochTimeUnit",
                        multi_measure_mappings=[pipes_mixins.CfnPipePropsMixin.MultiMeasureMappingProperty(
                            multi_measure_attribute_mappings=[pipes_mixins.CfnPipePropsMixin.MultiMeasureAttributeMappingProperty(
                                measure_value="measureValue",
                                measure_value_type="measureValueType",
                                multi_measure_attribute_name="multiMeasureAttributeName"
                            )],
                            multi_measure_name="multiMeasureName"
                        )],
                        single_measure_mappings=[pipes_mixins.CfnPipePropsMixin.SingleMeasureMappingProperty(
                            measure_name="measureName",
                            measure_value="measureValue",
                            measure_value_type="measureValueType"
                        )],
                        time_field_type="timeFieldType",
                        timestamp_format="timestampFormat",
                        time_value="timeValue",
                        version_value="versionValue"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5822bf44f36a9423ca7880cefc68b40da74e84a591bc8b8f65d30c203b1e90ac)
                check_type(argname="argument batch_job_parameters", value=batch_job_parameters, expected_type=type_hints["batch_job_parameters"])
                check_type(argname="argument cloud_watch_logs_parameters", value=cloud_watch_logs_parameters, expected_type=type_hints["cloud_watch_logs_parameters"])
                check_type(argname="argument ecs_task_parameters", value=ecs_task_parameters, expected_type=type_hints["ecs_task_parameters"])
                check_type(argname="argument event_bridge_event_bus_parameters", value=event_bridge_event_bus_parameters, expected_type=type_hints["event_bridge_event_bus_parameters"])
                check_type(argname="argument http_parameters", value=http_parameters, expected_type=type_hints["http_parameters"])
                check_type(argname="argument input_template", value=input_template, expected_type=type_hints["input_template"])
                check_type(argname="argument kinesis_stream_parameters", value=kinesis_stream_parameters, expected_type=type_hints["kinesis_stream_parameters"])
                check_type(argname="argument lambda_function_parameters", value=lambda_function_parameters, expected_type=type_hints["lambda_function_parameters"])
                check_type(argname="argument redshift_data_parameters", value=redshift_data_parameters, expected_type=type_hints["redshift_data_parameters"])
                check_type(argname="argument sage_maker_pipeline_parameters", value=sage_maker_pipeline_parameters, expected_type=type_hints["sage_maker_pipeline_parameters"])
                check_type(argname="argument sqs_queue_parameters", value=sqs_queue_parameters, expected_type=type_hints["sqs_queue_parameters"])
                check_type(argname="argument step_function_state_machine_parameters", value=step_function_state_machine_parameters, expected_type=type_hints["step_function_state_machine_parameters"])
                check_type(argname="argument timestream_parameters", value=timestream_parameters, expected_type=type_hints["timestream_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch_job_parameters is not None:
                self._values["batch_job_parameters"] = batch_job_parameters
            if cloud_watch_logs_parameters is not None:
                self._values["cloud_watch_logs_parameters"] = cloud_watch_logs_parameters
            if ecs_task_parameters is not None:
                self._values["ecs_task_parameters"] = ecs_task_parameters
            if event_bridge_event_bus_parameters is not None:
                self._values["event_bridge_event_bus_parameters"] = event_bridge_event_bus_parameters
            if http_parameters is not None:
                self._values["http_parameters"] = http_parameters
            if input_template is not None:
                self._values["input_template"] = input_template
            if kinesis_stream_parameters is not None:
                self._values["kinesis_stream_parameters"] = kinesis_stream_parameters
            if lambda_function_parameters is not None:
                self._values["lambda_function_parameters"] = lambda_function_parameters
            if redshift_data_parameters is not None:
                self._values["redshift_data_parameters"] = redshift_data_parameters
            if sage_maker_pipeline_parameters is not None:
                self._values["sage_maker_pipeline_parameters"] = sage_maker_pipeline_parameters
            if sqs_queue_parameters is not None:
                self._values["sqs_queue_parameters"] = sqs_queue_parameters
            if step_function_state_machine_parameters is not None:
                self._values["step_function_state_machine_parameters"] = step_function_state_machine_parameters
            if timestream_parameters is not None:
                self._values["timestream_parameters"] = timestream_parameters

        @builtins.property
        def batch_job_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetBatchJobParametersProperty"]]:
            '''The parameters for using an AWS Batch job as a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-batchjobparameters
            '''
            result = self._values.get("batch_job_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetBatchJobParametersProperty"]], result)

        @builtins.property
        def cloud_watch_logs_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetCloudWatchLogsParametersProperty"]]:
            '''The parameters for using an CloudWatch Logs log stream as a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-cloudwatchlogsparameters
            '''
            result = self._values.get("cloud_watch_logs_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetCloudWatchLogsParametersProperty"]], result)

        @builtins.property
        def ecs_task_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetEcsTaskParametersProperty"]]:
            '''The parameters for using an Amazon ECS task as a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-ecstaskparameters
            '''
            result = self._values.get("ecs_task_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetEcsTaskParametersProperty"]], result)

        @builtins.property
        def event_bridge_event_bus_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetEventBridgeEventBusParametersProperty"]]:
            '''The parameters for using an EventBridge event bus as a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-eventbridgeeventbusparameters
            '''
            result = self._values.get("event_bridge_event_bus_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetEventBridgeEventBusParametersProperty"]], result)

        @builtins.property
        def http_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetHttpParametersProperty"]]:
            '''These are custom parameter to be used when the target is an API Gateway REST APIs or EventBridge ApiDestinations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-httpparameters
            '''
            result = self._values.get("http_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetHttpParametersProperty"]], result)

        @builtins.property
        def input_template(self) -> typing.Optional[builtins.str]:
            '''Valid JSON text passed to the target.

            In this case, nothing from the event itself is passed to the target. For more information, see `The JavaScript Object Notation (JSON) Data Interchange Format <https://docs.aws.amazon.com/http://www.rfc-editor.org/rfc/rfc7159.txt>`_ .

            To remove an input template, specify an empty string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-inputtemplate
            '''
            result = self._values.get("input_template")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kinesis_stream_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetKinesisStreamParametersProperty"]]:
            '''The parameters for using a Kinesis stream as a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-kinesisstreamparameters
            '''
            result = self._values.get("kinesis_stream_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetKinesisStreamParametersProperty"]], result)

        @builtins.property
        def lambda_function_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetLambdaFunctionParametersProperty"]]:
            '''The parameters for using a Lambda function as a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-lambdafunctionparameters
            '''
            result = self._values.get("lambda_function_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetLambdaFunctionParametersProperty"]], result)

        @builtins.property
        def redshift_data_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetRedshiftDataParametersProperty"]]:
            '''These are custom parameters to be used when the target is a Amazon Redshift cluster to invoke the Amazon Redshift Data API BatchExecuteStatement.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-redshiftdataparameters
            '''
            result = self._values.get("redshift_data_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetRedshiftDataParametersProperty"]], result)

        @builtins.property
        def sage_maker_pipeline_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetSageMakerPipelineParametersProperty"]]:
            '''The parameters for using a SageMaker AI pipeline as a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-sagemakerpipelineparameters
            '''
            result = self._values.get("sage_maker_pipeline_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetSageMakerPipelineParametersProperty"]], result)

        @builtins.property
        def sqs_queue_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetSqsQueueParametersProperty"]]:
            '''The parameters for using a Amazon SQS stream as a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-sqsqueueparameters
            '''
            result = self._values.get("sqs_queue_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetSqsQueueParametersProperty"]], result)

        @builtins.property
        def step_function_state_machine_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetStateMachineParametersProperty"]]:
            '''The parameters for using a Step Functions state machine as a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-stepfunctionstatemachineparameters
            '''
            result = self._values.get("step_function_state_machine_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetStateMachineParametersProperty"]], result)

        @builtins.property
        def timestream_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetTimestreamParametersProperty"]]:
            '''The parameters for using a Timestream for LiveAnalytics table as a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-timestreamparameters
            '''
            result = self._values.get("timestream_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.PipeTargetTimestreamParametersProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeTargetParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeTargetRedshiftDataParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database": "database",
            "db_user": "dbUser",
            "secret_manager_arn": "secretManagerArn",
            "sqls": "sqls",
            "statement_name": "statementName",
            "with_event": "withEvent",
        },
    )
    class PipeTargetRedshiftDataParametersProperty:
        def __init__(
            self,
            *,
            database: typing.Optional[builtins.str] = None,
            db_user: typing.Optional[builtins.str] = None,
            secret_manager_arn: typing.Optional[builtins.str] = None,
            sqls: typing.Optional[typing.Sequence[builtins.str]] = None,
            statement_name: typing.Optional[builtins.str] = None,
            with_event: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''These are custom parameters to be used when the target is a Amazon Redshift cluster to invoke the Amazon Redshift Data API BatchExecuteStatement.

            :param database: The name of the database. Required when authenticating using temporary credentials.
            :param db_user: The database user name. Required when authenticating using temporary credentials.
            :param secret_manager_arn: The name or ARN of the secret that enables access to the database. Required when authenticating using Secrets Manager.
            :param sqls: The SQL statement text to run.
            :param statement_name: The name of the SQL statement. You can name the SQL statement when you create it to identify the query.
            :param with_event: Indicates whether to send an event back to EventBridge after the SQL statement runs. Default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetredshiftdataparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_target_redshift_data_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeTargetRedshiftDataParametersProperty(
                    database="database",
                    db_user="dbUser",
                    secret_manager_arn="secretManagerArn",
                    sqls=["sqls"],
                    statement_name="statementName",
                    with_event=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d09b7f8fe65076799be624ecbdf63ea4a6f314d051165f310ca27b638ded3f7c)
                check_type(argname="argument database", value=database, expected_type=type_hints["database"])
                check_type(argname="argument db_user", value=db_user, expected_type=type_hints["db_user"])
                check_type(argname="argument secret_manager_arn", value=secret_manager_arn, expected_type=type_hints["secret_manager_arn"])
                check_type(argname="argument sqls", value=sqls, expected_type=type_hints["sqls"])
                check_type(argname="argument statement_name", value=statement_name, expected_type=type_hints["statement_name"])
                check_type(argname="argument with_event", value=with_event, expected_type=type_hints["with_event"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database is not None:
                self._values["database"] = database
            if db_user is not None:
                self._values["db_user"] = db_user
            if secret_manager_arn is not None:
                self._values["secret_manager_arn"] = secret_manager_arn
            if sqls is not None:
                self._values["sqls"] = sqls
            if statement_name is not None:
                self._values["statement_name"] = statement_name
            if with_event is not None:
                self._values["with_event"] = with_event

        @builtins.property
        def database(self) -> typing.Optional[builtins.str]:
            '''The name of the database.

            Required when authenticating using temporary credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetredshiftdataparameters.html#cfn-pipes-pipe-pipetargetredshiftdataparameters-database
            '''
            result = self._values.get("database")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def db_user(self) -> typing.Optional[builtins.str]:
            '''The database user name.

            Required when authenticating using temporary credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetredshiftdataparameters.html#cfn-pipes-pipe-pipetargetredshiftdataparameters-dbuser
            '''
            result = self._values.get("db_user")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_manager_arn(self) -> typing.Optional[builtins.str]:
            '''The name or ARN of the secret that enables access to the database.

            Required when authenticating using Secrets Manager.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetredshiftdataparameters.html#cfn-pipes-pipe-pipetargetredshiftdataparameters-secretmanagerarn
            '''
            result = self._values.get("secret_manager_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sqls(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The SQL statement text to run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetredshiftdataparameters.html#cfn-pipes-pipe-pipetargetredshiftdataparameters-sqls
            '''
            result = self._values.get("sqls")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def statement_name(self) -> typing.Optional[builtins.str]:
            '''The name of the SQL statement.

            You can name the SQL statement when you create it to identify the query.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetredshiftdataparameters.html#cfn-pipes-pipe-pipetargetredshiftdataparameters-statementname
            '''
            result = self._values.get("statement_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def with_event(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to send an event back to EventBridge after the SQL statement runs.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetredshiftdataparameters.html#cfn-pipes-pipe-pipetargetredshiftdataparameters-withevent
            '''
            result = self._values.get("with_event")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeTargetRedshiftDataParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeTargetSageMakerPipelineParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"pipeline_parameter_list": "pipelineParameterList"},
    )
    class PipeTargetSageMakerPipelineParametersProperty:
        def __init__(
            self,
            *,
            pipeline_parameter_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.SageMakerPipelineParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The parameters for using a SageMaker AI pipeline as a target.

            :param pipeline_parameter_list: List of Parameter names and values for SageMaker AI Model Building Pipeline execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetsagemakerpipelineparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_target_sage_maker_pipeline_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeTargetSageMakerPipelineParametersProperty(
                    pipeline_parameter_list=[pipes_mixins.CfnPipePropsMixin.SageMakerPipelineParameterProperty(
                        name="name",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__46f4ad678fdf91a91e7b59e0af6034c0d6725cb9dc98f6c0bbcc50cb1c22e331)
                check_type(argname="argument pipeline_parameter_list", value=pipeline_parameter_list, expected_type=type_hints["pipeline_parameter_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pipeline_parameter_list is not None:
                self._values["pipeline_parameter_list"] = pipeline_parameter_list

        @builtins.property
        def pipeline_parameter_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.SageMakerPipelineParameterProperty"]]]]:
            '''List of Parameter names and values for SageMaker AI Model Building Pipeline execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetsagemakerpipelineparameters.html#cfn-pipes-pipe-pipetargetsagemakerpipelineparameters-pipelineparameterlist
            '''
            result = self._values.get("pipeline_parameter_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.SageMakerPipelineParameterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeTargetSageMakerPipelineParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeTargetSqsQueueParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "message_deduplication_id": "messageDeduplicationId",
            "message_group_id": "messageGroupId",
        },
    )
    class PipeTargetSqsQueueParametersProperty:
        def __init__(
            self,
            *,
            message_deduplication_id: typing.Optional[builtins.str] = None,
            message_group_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for using a Amazon SQS stream as a target.

            :param message_deduplication_id: This parameter applies only to FIFO (first-in-first-out) queues. The token used for deduplication of sent messages.
            :param message_group_id: The FIFO message group ID to use as the target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetsqsqueueparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_target_sqs_queue_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeTargetSqsQueueParametersProperty(
                    message_deduplication_id="messageDeduplicationId",
                    message_group_id="messageGroupId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dbb19f843c1c25cee6954d6cb6f02e99d81bc7cff0c21bdd6e0e011cae80a083)
                check_type(argname="argument message_deduplication_id", value=message_deduplication_id, expected_type=type_hints["message_deduplication_id"])
                check_type(argname="argument message_group_id", value=message_group_id, expected_type=type_hints["message_group_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if message_deduplication_id is not None:
                self._values["message_deduplication_id"] = message_deduplication_id
            if message_group_id is not None:
                self._values["message_group_id"] = message_group_id

        @builtins.property
        def message_deduplication_id(self) -> typing.Optional[builtins.str]:
            '''This parameter applies only to FIFO (first-in-first-out) queues.

            The token used for deduplication of sent messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetsqsqueueparameters.html#cfn-pipes-pipe-pipetargetsqsqueueparameters-messagededuplicationid
            '''
            result = self._values.get("message_deduplication_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message_group_id(self) -> typing.Optional[builtins.str]:
            '''The FIFO message group ID to use as the target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetsqsqueueparameters.html#cfn-pipes-pipe-pipetargetsqsqueueparameters-messagegroupid
            '''
            result = self._values.get("message_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeTargetSqsQueueParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeTargetStateMachineParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"invocation_type": "invocationType"},
    )
    class PipeTargetStateMachineParametersProperty:
        def __init__(
            self,
            *,
            invocation_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for using a Step Functions state machine as a target.

            :param invocation_type: Specify whether to invoke the Step Functions state machine synchronously or asynchronously. - ``REQUEST_RESPONSE`` (default) - Invoke synchronously. For more information, see `StartSyncExecution <https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartSyncExecution.html>`_ in the *AWS Step Functions API Reference* . .. epigraph:: ``REQUEST_RESPONSE`` is not supported for ``STANDARD`` state machine workflows. - ``FIRE_AND_FORGET`` - Invoke asynchronously. For more information, see `StartExecution <https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html>`_ in the *AWS Step Functions API Reference* . For more information, see `Invocation types <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes.html#pipes-invocation>`_ in the *Amazon EventBridge User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetstatemachineparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_target_state_machine_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeTargetStateMachineParametersProperty(
                    invocation_type="invocationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__55f511d445110258f1db8ee1b6d238b4408d4d3170eec5c2e6a85259dc3f2a84)
                check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if invocation_type is not None:
                self._values["invocation_type"] = invocation_type

        @builtins.property
        def invocation_type(self) -> typing.Optional[builtins.str]:
            '''Specify whether to invoke the Step Functions state machine synchronously or asynchronously.

            - ``REQUEST_RESPONSE`` (default) - Invoke synchronously. For more information, see `StartSyncExecution <https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartSyncExecution.html>`_ in the *AWS Step Functions API Reference* .

            .. epigraph::

               ``REQUEST_RESPONSE`` is not supported for ``STANDARD`` state machine workflows.

            - ``FIRE_AND_FORGET`` - Invoke asynchronously. For more information, see `StartExecution <https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html>`_ in the *AWS Step Functions API Reference* .

            For more information, see `Invocation types <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes.html#pipes-invocation>`_ in the *Amazon EventBridge User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetstatemachineparameters.html#cfn-pipes-pipe-pipetargetstatemachineparameters-invocationtype
            '''
            result = self._values.get("invocation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeTargetStateMachineParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PipeTargetTimestreamParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimension_mappings": "dimensionMappings",
            "epoch_time_unit": "epochTimeUnit",
            "multi_measure_mappings": "multiMeasureMappings",
            "single_measure_mappings": "singleMeasureMappings",
            "time_field_type": "timeFieldType",
            "timestamp_format": "timestampFormat",
            "time_value": "timeValue",
            "version_value": "versionValue",
        },
    )
    class PipeTargetTimestreamParametersProperty:
        def __init__(
            self,
            *,
            dimension_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.DimensionMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            epoch_time_unit: typing.Optional[builtins.str] = None,
            multi_measure_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.MultiMeasureMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            single_measure_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipePropsMixin.SingleMeasureMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            time_field_type: typing.Optional[builtins.str] = None,
            timestamp_format: typing.Optional[builtins.str] = None,
            time_value: typing.Optional[builtins.str] = None,
            version_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters for using a Timestream for LiveAnalytics table as a target.

            :param dimension_mappings: Map source data to dimensions in the target Timestream for LiveAnalytics table. For more information, see `Amazon Timestream for LiveAnalytics concepts <https://docs.aws.amazon.com/timestream/latest/developerguide/concepts.html>`_
            :param epoch_time_unit: The granularity of the time units used. Default is ``MILLISECONDS`` . Required if ``TimeFieldType`` is specified as ``EPOCH`` .
            :param multi_measure_mappings: Maps multiple measures from the source event to the same record in the specified Timestream for LiveAnalytics table.
            :param single_measure_mappings: Mappings of single source data fields to individual records in the specified Timestream for LiveAnalytics table.
            :param time_field_type: The type of time value used. The default is ``EPOCH`` .
            :param timestamp_format: How to format the timestamps. For example, ``yyyy-MM-dd'T'HH:mm:ss'Z'`` . Required if ``TimeFieldType`` is specified as ``TIMESTAMP_FORMAT`` .
            :param time_value: Dynamic path to the source data field that represents the time value for your data.
            :param version_value: 64 bit version value or source data field that represents the version value for your data. Write requests with a higher version number will update the existing measure values of the record and version. In cases where the measure value is the same, the version will still be updated. Default value is 1. Timestream for LiveAnalytics does not support updating partial measure values in a record. Write requests for duplicate data with a higher version number will update the existing measure value and version. In cases where the measure value is the same, ``Version`` will still be updated. Default value is ``1`` . .. epigraph:: ``Version`` must be ``1`` or greater, or you will receive a ``ValidationException`` error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargettimestreamparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                pipe_target_timestream_parameters_property = pipes_mixins.CfnPipePropsMixin.PipeTargetTimestreamParametersProperty(
                    dimension_mappings=[pipes_mixins.CfnPipePropsMixin.DimensionMappingProperty(
                        dimension_name="dimensionName",
                        dimension_value="dimensionValue",
                        dimension_value_type="dimensionValueType"
                    )],
                    epoch_time_unit="epochTimeUnit",
                    multi_measure_mappings=[pipes_mixins.CfnPipePropsMixin.MultiMeasureMappingProperty(
                        multi_measure_attribute_mappings=[pipes_mixins.CfnPipePropsMixin.MultiMeasureAttributeMappingProperty(
                            measure_value="measureValue",
                            measure_value_type="measureValueType",
                            multi_measure_attribute_name="multiMeasureAttributeName"
                        )],
                        multi_measure_name="multiMeasureName"
                    )],
                    single_measure_mappings=[pipes_mixins.CfnPipePropsMixin.SingleMeasureMappingProperty(
                        measure_name="measureName",
                        measure_value="measureValue",
                        measure_value_type="measureValueType"
                    )],
                    time_field_type="timeFieldType",
                    timestamp_format="timestampFormat",
                    time_value="timeValue",
                    version_value="versionValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c35d0c0c4e83ac8dd41f1d34927c0d9097c255e241f117315a16e984a6745b29)
                check_type(argname="argument dimension_mappings", value=dimension_mappings, expected_type=type_hints["dimension_mappings"])
                check_type(argname="argument epoch_time_unit", value=epoch_time_unit, expected_type=type_hints["epoch_time_unit"])
                check_type(argname="argument multi_measure_mappings", value=multi_measure_mappings, expected_type=type_hints["multi_measure_mappings"])
                check_type(argname="argument single_measure_mappings", value=single_measure_mappings, expected_type=type_hints["single_measure_mappings"])
                check_type(argname="argument time_field_type", value=time_field_type, expected_type=type_hints["time_field_type"])
                check_type(argname="argument timestamp_format", value=timestamp_format, expected_type=type_hints["timestamp_format"])
                check_type(argname="argument time_value", value=time_value, expected_type=type_hints["time_value"])
                check_type(argname="argument version_value", value=version_value, expected_type=type_hints["version_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_mappings is not None:
                self._values["dimension_mappings"] = dimension_mappings
            if epoch_time_unit is not None:
                self._values["epoch_time_unit"] = epoch_time_unit
            if multi_measure_mappings is not None:
                self._values["multi_measure_mappings"] = multi_measure_mappings
            if single_measure_mappings is not None:
                self._values["single_measure_mappings"] = single_measure_mappings
            if time_field_type is not None:
                self._values["time_field_type"] = time_field_type
            if timestamp_format is not None:
                self._values["timestamp_format"] = timestamp_format
            if time_value is not None:
                self._values["time_value"] = time_value
            if version_value is not None:
                self._values["version_value"] = version_value

        @builtins.property
        def dimension_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.DimensionMappingProperty"]]]]:
            '''Map source data to dimensions in the target Timestream for LiveAnalytics table.

            For more information, see `Amazon Timestream for LiveAnalytics concepts <https://docs.aws.amazon.com/timestream/latest/developerguide/concepts.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargettimestreamparameters.html#cfn-pipes-pipe-pipetargettimestreamparameters-dimensionmappings
            '''
            result = self._values.get("dimension_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.DimensionMappingProperty"]]]], result)

        @builtins.property
        def epoch_time_unit(self) -> typing.Optional[builtins.str]:
            '''The granularity of the time units used. Default is ``MILLISECONDS`` .

            Required if ``TimeFieldType`` is specified as ``EPOCH`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargettimestreamparameters.html#cfn-pipes-pipe-pipetargettimestreamparameters-epochtimeunit
            '''
            result = self._values.get("epoch_time_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def multi_measure_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.MultiMeasureMappingProperty"]]]]:
            '''Maps multiple measures from the source event to the same record in the specified Timestream for LiveAnalytics table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargettimestreamparameters.html#cfn-pipes-pipe-pipetargettimestreamparameters-multimeasuremappings
            '''
            result = self._values.get("multi_measure_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.MultiMeasureMappingProperty"]]]], result)

        @builtins.property
        def single_measure_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.SingleMeasureMappingProperty"]]]]:
            '''Mappings of single source data fields to individual records in the specified Timestream for LiveAnalytics table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargettimestreamparameters.html#cfn-pipes-pipe-pipetargettimestreamparameters-singlemeasuremappings
            '''
            result = self._values.get("single_measure_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipePropsMixin.SingleMeasureMappingProperty"]]]], result)

        @builtins.property
        def time_field_type(self) -> typing.Optional[builtins.str]:
            '''The type of time value used.

            The default is ``EPOCH`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargettimestreamparameters.html#cfn-pipes-pipe-pipetargettimestreamparameters-timefieldtype
            '''
            result = self._values.get("time_field_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timestamp_format(self) -> typing.Optional[builtins.str]:
            '''How to format the timestamps. For example, ``yyyy-MM-dd'T'HH:mm:ss'Z'`` .

            Required if ``TimeFieldType`` is specified as ``TIMESTAMP_FORMAT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargettimestreamparameters.html#cfn-pipes-pipe-pipetargettimestreamparameters-timestampformat
            '''
            result = self._values.get("timestamp_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time_value(self) -> typing.Optional[builtins.str]:
            '''Dynamic path to the source data field that represents the time value for your data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargettimestreamparameters.html#cfn-pipes-pipe-pipetargettimestreamparameters-timevalue
            '''
            result = self._values.get("time_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version_value(self) -> typing.Optional[builtins.str]:
            '''64 bit version value or source data field that represents the version value for your data.

            Write requests with a higher version number will update the existing measure values of the record and version. In cases where the measure value is the same, the version will still be updated.

            Default value is 1.

            Timestream for LiveAnalytics does not support updating partial measure values in a record.

            Write requests for duplicate data with a higher version number will update the existing measure value and version. In cases where the measure value is the same, ``Version`` will still be updated. Default value is ``1`` .
            .. epigraph::

               ``Version`` must be ``1`` or greater, or you will receive a ``ValidationException`` error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargettimestreamparameters.html#cfn-pipes-pipe-pipetargettimestreamparameters-versionvalue
            '''
            result = self._values.get("version_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipeTargetTimestreamParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PlacementConstraintProperty",
        jsii_struct_bases=[],
        name_mapping={"expression": "expression", "type": "type"},
    )
    class PlacementConstraintProperty:
        def __init__(
            self,
            *,
            expression: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing a constraint on task placement.

            To learn more, see `Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_ in the Amazon Elastic Container Service Developer Guide.

            :param expression: A cluster query language expression to apply to the constraint. You cannot specify an expression if the constraint type is ``distinctInstance`` . To learn more, see `Cluster Query Language <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html>`_ in the Amazon Elastic Container Service Developer Guide.
            :param type: The type of constraint. Use distinctInstance to ensure that each task in a particular group is running on a different container instance. Use memberOf to restrict the selection to a group of valid candidates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-placementconstraint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                placement_constraint_property = pipes_mixins.CfnPipePropsMixin.PlacementConstraintProperty(
                    expression="expression",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac676569baa0bb2c6e0b2c4463ebd98c4a0be67c8a627f96cf145332a7ade37b)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''A cluster query language expression to apply to the constraint.

            You cannot specify an expression if the constraint type is ``distinctInstance`` . To learn more, see `Cluster Query Language <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html>`_ in the Amazon Elastic Container Service Developer Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-placementconstraint.html#cfn-pipes-pipe-placementconstraint-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of constraint.

            Use distinctInstance to ensure that each task in a particular group is running on a different container instance. Use memberOf to restrict the selection to a group of valid candidates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-placementconstraint.html#cfn-pipes-pipe-placementconstraint-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementConstraintProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.PlacementStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"field": "field", "type": "type"},
    )
    class PlacementStrategyProperty:
        def __init__(
            self,
            *,
            field: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The task placement strategy for a task or service.

            To learn more, see `Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_ in the Amazon Elastic Container Service Service Developer Guide.

            :param field: The field to apply the placement strategy against. For the spread placement strategy, valid values are instanceId (or host, which has the same effect), or any platform or custom attribute that is applied to a container instance, such as attribute:ecs.availability-zone. For the binpack placement strategy, valid values are cpu and memory. For the random placement strategy, this field is not used.
            :param type: The type of placement strategy. The random placement strategy randomly places tasks on available candidates. The spread placement strategy spreads placement across available candidates evenly based on the field parameter. The binpack strategy places tasks on available candidates that have the least available amount of the resource that is specified with the field parameter. For example, if you binpack on memory, a task is placed on the instance with the least amount of remaining memory (but still enough to run the task).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-placementstrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                placement_strategy_property = pipes_mixins.CfnPipePropsMixin.PlacementStrategyProperty(
                    field="field",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee0ed5dc81044c375f98837a6e920f8e5d7a0394d5f1e9e5ad6f5796c5f803f6)
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field is not None:
                self._values["field"] = field
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The field to apply the placement strategy against.

            For the spread placement strategy, valid values are instanceId (or host, which has the same effect), or any platform or custom attribute that is applied to a container instance, such as attribute:ecs.availability-zone. For the binpack placement strategy, valid values are cpu and memory. For the random placement strategy, this field is not used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-placementstrategy.html#cfn-pipes-pipe-placementstrategy-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of placement strategy.

            The random placement strategy randomly places tasks on available candidates. The spread placement strategy spreads placement across available candidates evenly based on the field parameter. The binpack strategy places tasks on available candidates that have the least available amount of the resource that is specified with the field parameter. For example, if you binpack on memory, a task is placed on the instance with the least amount of remaining memory (but still enough to run the task).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-placementstrategy.html#cfn-pipes-pipe-placementstrategy-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.S3LogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_owner": "bucketOwner",
            "output_format": "outputFormat",
            "prefix": "prefix",
        },
    )
    class S3LogDestinationProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_owner: typing.Optional[builtins.str] = None,
            output_format: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the Amazon S3 logging configuration settings for the pipe.

            :param bucket_name: The name of the Amazon S3 bucket to which EventBridge delivers the log records for the pipe.
            :param bucket_owner: The AWS account that owns the Amazon S3 bucket to which EventBridge delivers the log records for the pipe.
            :param output_format: The format EventBridge uses for the log records. EventBridge currently only supports ``json`` formatting.
            :param prefix: The prefix text with which to begin Amazon S3 log object names. For more information, see `Organizing objects using prefixes <https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html>`_ in the *Amazon Simple Storage Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-s3logdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                s3_log_destination_property = pipes_mixins.CfnPipePropsMixin.S3LogDestinationProperty(
                    bucket_name="bucketName",
                    bucket_owner="bucketOwner",
                    output_format="outputFormat",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f7129990eedc7520809bd06acf0cadd63a7e2742f3d3f73f8019772a7057e028)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_owner", value=bucket_owner, expected_type=type_hints["bucket_owner"])
                check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_owner is not None:
                self._values["bucket_owner"] = bucket_owner
            if output_format is not None:
                self._values["output_format"] = output_format
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket to which EventBridge delivers the log records for the pipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-s3logdestination.html#cfn-pipes-pipe-s3logdestination-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_owner(self) -> typing.Optional[builtins.str]:
            '''The AWS account that owns the Amazon S3 bucket to which EventBridge delivers the log records for the pipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-s3logdestination.html#cfn-pipes-pipe-s3logdestination-bucketowner
            '''
            result = self._values.get("bucket_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_format(self) -> typing.Optional[builtins.str]:
            '''The format EventBridge uses for the log records.

            EventBridge currently only supports ``json`` formatting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-s3logdestination.html#cfn-pipes-pipe-s3logdestination-outputformat
            '''
            result = self._values.get("output_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix text with which to begin Amazon S3 log object names.

            For more information, see `Organizing objects using prefixes <https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html>`_ in the *Amazon Simple Storage Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-s3logdestination.html#cfn-pipes-pipe-s3logdestination-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.SageMakerPipelineParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class SageMakerPipelineParameterProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Name/Value pair of a parameter to start execution of a SageMaker AI Model Building Pipeline.

            :param name: Name of parameter to start execution of a SageMaker AI Model Building Pipeline.
            :param value: Value of parameter to start execution of a SageMaker AI Model Building Pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-sagemakerpipelineparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                sage_maker_pipeline_parameter_property = pipes_mixins.CfnPipePropsMixin.SageMakerPipelineParameterProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42adc5cc99d7410ea8d1dcd0f43571bf9e330bcab2d76328650f373ca026da3f)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Name of parameter to start execution of a SageMaker AI Model Building Pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-sagemakerpipelineparameter.html#cfn-pipes-pipe-sagemakerpipelineparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Value of parameter to start execution of a SageMaker AI Model Building Pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-sagemakerpipelineparameter.html#cfn-pipes-pipe-sagemakerpipelineparameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SageMakerPipelineParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "basic_auth": "basicAuth",
            "client_certificate_tls_auth": "clientCertificateTlsAuth",
            "sasl_scram256_auth": "saslScram256Auth",
            "sasl_scram512_auth": "saslScram512Auth",
        },
    )
    class SelfManagedKafkaAccessConfigurationCredentialsProperty:
        def __init__(
            self,
            *,
            basic_auth: typing.Optional[builtins.str] = None,
            client_certificate_tls_auth: typing.Optional[builtins.str] = None,
            sasl_scram256_auth: typing.Optional[builtins.str] = None,
            sasl_scram512_auth: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The AWS Secrets Manager secret that stores your stream credentials.

            :param basic_auth: The ARN of the Secrets Manager secret.
            :param client_certificate_tls_auth: The ARN of the Secrets Manager secret.
            :param sasl_scram256_auth: The ARN of the Secrets Manager secret.
            :param sasl_scram512_auth: The ARN of the Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-selfmanagedkafkaaccessconfigurationcredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                self_managed_kafka_access_configuration_credentials_property = pipes_mixins.CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationCredentialsProperty(
                    basic_auth="basicAuth",
                    client_certificate_tls_auth="clientCertificateTlsAuth",
                    sasl_scram256_auth="saslScram256Auth",
                    sasl_scram512_auth="saslScram512Auth"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0390f948961dcc3677983b7a2942badaaee5c36c345a6f624188d3a2a77fd75f)
                check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
                check_type(argname="argument client_certificate_tls_auth", value=client_certificate_tls_auth, expected_type=type_hints["client_certificate_tls_auth"])
                check_type(argname="argument sasl_scram256_auth", value=sasl_scram256_auth, expected_type=type_hints["sasl_scram256_auth"])
                check_type(argname="argument sasl_scram512_auth", value=sasl_scram512_auth, expected_type=type_hints["sasl_scram512_auth"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if basic_auth is not None:
                self._values["basic_auth"] = basic_auth
            if client_certificate_tls_auth is not None:
                self._values["client_certificate_tls_auth"] = client_certificate_tls_auth
            if sasl_scram256_auth is not None:
                self._values["sasl_scram256_auth"] = sasl_scram256_auth
            if sasl_scram512_auth is not None:
                self._values["sasl_scram512_auth"] = sasl_scram512_auth

        @builtins.property
        def basic_auth(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-selfmanagedkafkaaccessconfigurationcredentials.html#cfn-pipes-pipe-selfmanagedkafkaaccessconfigurationcredentials-basicauth
            '''
            result = self._values.get("basic_auth")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_certificate_tls_auth(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-selfmanagedkafkaaccessconfigurationcredentials.html#cfn-pipes-pipe-selfmanagedkafkaaccessconfigurationcredentials-clientcertificatetlsauth
            '''
            result = self._values.get("client_certificate_tls_auth")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sasl_scram256_auth(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-selfmanagedkafkaaccessconfigurationcredentials.html#cfn-pipes-pipe-selfmanagedkafkaaccessconfigurationcredentials-saslscram256auth
            '''
            result = self._values.get("sasl_scram256_auth")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sasl_scram512_auth(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Secrets Manager secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-selfmanagedkafkaaccessconfigurationcredentials.html#cfn-pipes-pipe-selfmanagedkafkaaccessconfigurationcredentials-saslscram512auth
            '''
            result = self._values.get("sasl_scram512_auth")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SelfManagedKafkaAccessConfigurationCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationVpcProperty",
        jsii_struct_bases=[],
        name_mapping={"security_group": "securityGroup", "subnets": "subnets"},
    )
    class SelfManagedKafkaAccessConfigurationVpcProperty:
        def __init__(
            self,
            *,
            security_group: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This structure specifies the VPC subnets and security groups for the stream, and whether a public IP address is to be used.

            :param security_group: Specifies the security groups associated with the stream. These security groups must all be in the same VPC. You can specify as many as five security groups.
            :param subnets: Specifies the subnets associated with the stream. These subnets must all be in the same VPC. You can specify as many as 16 subnets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-selfmanagedkafkaaccessconfigurationvpc.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                self_managed_kafka_access_configuration_vpc_property = pipes_mixins.CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationVpcProperty(
                    security_group=["securityGroup"],
                    subnets=["subnets"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eb5edd62ce139a885152c9de1715544afcdeaebc5a6053eea00ab3aad59551ff)
                check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group is not None:
                self._values["security_group"] = security_group
            if subnets is not None:
                self._values["subnets"] = subnets

        @builtins.property
        def security_group(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the security groups associated with the stream.

            These security groups must all be in the same VPC. You can specify as many as five security groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-selfmanagedkafkaaccessconfigurationvpc.html#cfn-pipes-pipe-selfmanagedkafkaaccessconfigurationvpc-securitygroup
            '''
            result = self._values.get("security_group")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the subnets associated with the stream.

            These subnets must all be in the same VPC. You can specify as many as 16 subnets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-selfmanagedkafkaaccessconfigurationvpc.html#cfn-pipes-pipe-selfmanagedkafkaaccessconfigurationvpc-subnets
            '''
            result = self._values.get("subnets")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SelfManagedKafkaAccessConfigurationVpcProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pipes.mixins.CfnPipePropsMixin.SingleMeasureMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "measure_name": "measureName",
            "measure_value": "measureValue",
            "measure_value_type": "measureValueType",
        },
    )
    class SingleMeasureMappingProperty:
        def __init__(
            self,
            *,
            measure_name: typing.Optional[builtins.str] = None,
            measure_value: typing.Optional[builtins.str] = None,
            measure_value_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Maps a single source data field to a single record in the specified Timestream for LiveAnalytics table.

            For more information, see `Amazon Timestream for LiveAnalytics concepts <https://docs.aws.amazon.com/timestream/latest/developerguide/concepts.html>`_

            :param measure_name: Target measure name for the measurement attribute in the Timestream table.
            :param measure_value: Dynamic path of the source field to map to the measure in the record.
            :param measure_value_type: Data type of the source field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-singlemeasuremapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pipes import mixins as pipes_mixins
                
                single_measure_mapping_property = pipes_mixins.CfnPipePropsMixin.SingleMeasureMappingProperty(
                    measure_name="measureName",
                    measure_value="measureValue",
                    measure_value_type="measureValueType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__78bd9802fbe941d48cee73e63049c845ba690da35652e7d36e326dac1b6d780d)
                check_type(argname="argument measure_name", value=measure_name, expected_type=type_hints["measure_name"])
                check_type(argname="argument measure_value", value=measure_value, expected_type=type_hints["measure_value"])
                check_type(argname="argument measure_value_type", value=measure_value_type, expected_type=type_hints["measure_value_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if measure_name is not None:
                self._values["measure_name"] = measure_name
            if measure_value is not None:
                self._values["measure_value"] = measure_value
            if measure_value_type is not None:
                self._values["measure_value_type"] = measure_value_type

        @builtins.property
        def measure_name(self) -> typing.Optional[builtins.str]:
            '''Target measure name for the measurement attribute in the Timestream table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-singlemeasuremapping.html#cfn-pipes-pipe-singlemeasuremapping-measurename
            '''
            result = self._values.get("measure_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def measure_value(self) -> typing.Optional[builtins.str]:
            '''Dynamic path of the source field to map to the measure in the record.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-singlemeasuremapping.html#cfn-pipes-pipe-singlemeasuremapping-measurevalue
            '''
            result = self._values.get("measure_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def measure_value_type(self) -> typing.Optional[builtins.str]:
            '''Data type of the source field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-singlemeasuremapping.html#cfn-pipes-pipe-singlemeasuremapping-measurevaluetype
            '''
            result = self._values.get("measure_value_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SingleMeasureMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnPipeExecutionLogs",
    "CfnPipeLogsMixin",
    "CfnPipeMixinProps",
    "CfnPipePropsMixin",
]

publication.publish()

def _typecheckingstub__8f846d29d1d6fe535cd650445a62df46a0e4865ab5a411a9c47a4f28badb0746(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7447cdacd039b7cb64140b50c70cb4c6ce42ae5f2ca7d8f3db11622682cc01ca(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa9cb184fb33be43ae487ce581070f095b9219c766c18456fdb6c619e0705ad(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb167e33c446551a196db6c11c656c9100cd9ba152fbd016e4fc248219ab4e87(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c04e0d1247401c2ccc4dc5e80999f6074ba967709c12311fd23abafd9c4cfd(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1c452fc6c416e9cb5bfe47646e530ae7542cf73e6613d666332046ccb87628(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c93e4d67f03c822fa8e4ed7bbf89c5a2b0543ddcd1ced99c352a46e92ef1382(
    *,
    description: typing.Optional[builtins.str] = None,
    desired_state: typing.Optional[builtins.str] = None,
    enrichment: typing.Optional[builtins.str] = None,
    enrichment_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeEnrichmentParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_identifier: typing.Optional[builtins.str] = None,
    log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeLogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    source_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeSourceParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target: typing.Optional[builtins.str] = None,
    target_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeTargetParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4cfc248bf3421337b859e918d823b790fd6561f131b34fc3f27c825e709a6a(
    props: typing.Union[CfnPipeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e15d70561958cb4106b8785d295315803f96dfd162b4acfba938d67acb297b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3346da746b98bb40e27489a958300b1dff5af318579957602350a0208d9c70(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b5ad67af28c0af0427637f3c6336b8c898959627fb40394b86705ce3238829(
    *,
    assign_public_ip: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef19a87f06dc54331b8bf075cff1aa806435790709444ae65b9e04b7238b2cf2(
    *,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2e5f61dfc1dd4f95551f261830fb9417c356503bed9c866a08210b9b3b5d02(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.BatchEnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    resource_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.BatchResourceRequirementProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6bcb246ae94b0471945891fed1d9e022ef0fd87247cbc6a485b895eb974491(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc784218091b0612f74293033c6fbaee141346985fbd9b5ba71e8590b51c364(
    *,
    job_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2498914d3d5154bd88a1b325f8f97b80b5740f9483a65ab1a3b295888acd33d(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c245577631e8125d8bdc4038215eef32af92c2097c984c27b4b499239bfe7ce(
    *,
    attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399ae0a41ca3179f16fb8a41bd0500408118cca193b50b01aa507ec343a19128(
    *,
    base: typing.Optional[jsii.Number] = None,
    capacity_provider: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5b7e1182e1d0c8aa6ac059365a50dde3cbaad0d5572b1af1e9d3ee6cdf7b43(
    *,
    log_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ce541cfa1113e7f395c36b8943c0a3a9f9bc55ded0114477c5887b6a510acb(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__983fb71a5f947c6deaf4d59cc8129647811ee17f98182b649aedbd0058774dd0(
    *,
    dimension_name: typing.Optional[builtins.str] = None,
    dimension_value: typing.Optional[builtins.str] = None,
    dimension_value_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c363acbf007019d44a8037f7251d00d23d526c9d63e543f705f02dc06cca93(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu: typing.Optional[jsii.Number] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.EcsEnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    environment_files: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.EcsEnvironmentFileProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    memory: typing.Optional[jsii.Number] = None,
    memory_reservation: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    resource_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.EcsResourceRequirementProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f911845708b5d561986e78a483aff0106fcf26968ff2c96ab2468c413fdf719d(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dcccc46f199ca32ec6a98f721697780bb9504613a0317fab947fa141c6be581(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abbcabfba8de1a4ffcd5f64ffcb0c757672a9a96ae6252b400cd3961dce3956(
    *,
    size_in_gib: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8dafbf43d2c1a129c02808296de4532f727a5ceb1947aa8c07fc2e7002dce80(
    *,
    device_name: typing.Optional[builtins.str] = None,
    device_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af0a0a3f0c62f933a27ff2f5a4aa11b3d41b51121f3fd0c5cf2bb4fc8481bcb(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d704c6da4d6cad333ded62101495044551d08f8b8dce9fb02f29cab2af51a243(
    *,
    container_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.EcsContainerOverrideProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    cpu: typing.Optional[builtins.str] = None,
    ephemeral_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.EcsEphemeralStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    inference_accelerator_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.EcsInferenceAcceleratorOverrideProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    memory: typing.Optional[builtins.str] = None,
    task_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4091d89f1289b8be0c72adc12a05d0ced68fe183292011373cb6f5668c6cc8f2(
    *,
    filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.FilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e8987ab978bce880b6acc30f89c0e585fd2629ca8fef9a1d1d9cc2eb96d4c4(
    *,
    pattern: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ef8091a17304671903e693e5afff6cd6162a073f4bdccf4328f86951b637ac(
    *,
    delivery_stream_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3bfbf3a39f65b35c30e1e0763be6278ece6c909b7b6bfd2e3416862b3e0c992(
    *,
    basic_auth: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57aeccd892e83487efdb948f5d1d34e6d922e063aacfd83671024417574fba5(
    *,
    client_certificate_tls_auth: typing.Optional[builtins.str] = None,
    sasl_scram512_auth: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc725bd50cde770d498874e1eb83cfe44ee9d8af620cc35fc0944671cf2fdc4(
    *,
    measure_value: typing.Optional[builtins.str] = None,
    measure_value_type: typing.Optional[builtins.str] = None,
    multi_measure_attribute_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc5761092dfc246134e09326490d476a35311ea71d3a848167091bba604a093(
    *,
    multi_measure_attribute_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.MultiMeasureAttributeMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    multi_measure_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5f6a45b025e0955b608e58280390ac549fd05326bc0b45912440abd33b96d8(
    *,
    awsvpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.AwsVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54107ffcd4574854c8f4ab89c71e40ecd055b79bbd914f11a2d96133090ddc23(
    *,
    header_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ec0ce5d674929b75b59ac5fdd5d585585786f3effb966afe90711886492653(
    *,
    http_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeEnrichmentHttpParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    input_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa069717f194d153d123b85c6e5f1c700c6a56908f8676e5789bbd232c8d5f2(
    *,
    cloudwatch_logs_log_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.CloudwatchLogsLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    firehose_log_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.FirehoseLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    include_execution_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    level: typing.Optional[builtins.str] = None,
    s3_log_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.S3LogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b5d107e820fa15e6b27722aa98e9409d6a021f76a5da0a91b8caac478f5d84(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.MQBrokerAccessCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    queue_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4579ed308bf27d245e737dd1e7f0dd1ef56b5ba56b2240022a84ab22d6b23206(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    dead_letter_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.DeadLetterConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    starting_position: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ce316faa6206e09724df001ad75d6ebfc6af86cfc2c0a7ce5d21cbdff43a1e(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    dead_letter_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.DeadLetterConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
    on_partial_batch_item_failure: typing.Optional[builtins.str] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    starting_position: typing.Optional[builtins.str] = None,
    starting_position_timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa518ab3584bac527ff4b57ad8373e6372c7d56a19cc275678369405cc77b04(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    consumer_group_id: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.MSKAccessCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    starting_position: typing.Optional[builtins.str] = None,
    topic_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a888186ff6f7b488986feea8c07b1314b93a07a27cfbb907635133352d0807(
    *,
    active_mq_broker_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeSourceActiveMQBrokerParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_db_stream_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeSourceDynamoDBStreamParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    filter_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.FilterCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_stream_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeSourceKinesisStreamParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    managed_streaming_kafka_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeSourceManagedStreamingKafkaParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rabbit_mq_broker_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeSourceRabbitMQBrokerParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    self_managed_kafka_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeSourceSelfManagedKafkaParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sqs_queue_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeSourceSqsQueueParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35e2d337ff3ac75db7e8afd7728e712225503d9984e8f69a1724e985621459e(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.MQBrokerAccessCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    queue_name: typing.Optional[builtins.str] = None,
    virtual_host: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed226e689beda79446361bdfeb1cca7819d52d537c328c161abc0a57215fd1a2(
    *,
    additional_bootstrap_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    batch_size: typing.Optional[jsii.Number] = None,
    consumer_group_id: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
    server_root_ca_certificate: typing.Optional[builtins.str] = None,
    starting_position: typing.Optional[builtins.str] = None,
    topic_name: typing.Optional[builtins.str] = None,
    vpc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.SelfManagedKafkaAccessConfigurationVpcProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286e2e2fb4d2dc263784f0b4f06f0f5b86460d0493517534bcded22065c39513(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6fd08d0376c810aeb6354cd97a5851a60ce95181348df48b61710def8608784(
    *,
    array_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.BatchArrayPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    container_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.BatchContainerOverridesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    depends_on: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.BatchJobDependencyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    job_definition: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    retry_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.BatchRetryStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7cc264f643e41c3a115542e3341618770a7199b88e61fcf6571ee60352e9b98(
    *,
    log_stream_name: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df966888dfb055801962dc014e71d1bb2fb4ddeda2991385903c7fdbe8696dbe(
    *,
    capacity_provider_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.CapacityProviderStrategyItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    enable_ecs_managed_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_execute_command: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    group: typing.Optional[builtins.str] = None,
    launch_type: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.EcsTaskOverrideProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    placement_constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PlacementConstraintProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    placement_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PlacementStrategyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    platform_version: typing.Optional[builtins.str] = None,
    propagate_tags: typing.Optional[builtins.str] = None,
    reference_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_count: typing.Optional[jsii.Number] = None,
    task_definition_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c57f87b545e905597356e0e85ed67dc2c3d334ff59d37be6e461767b5bcaea5(
    *,
    detail_type: typing.Optional[builtins.str] = None,
    endpoint_id: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    source: typing.Optional[builtins.str] = None,
    time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fadf710f198bab019580591eb1c16f6657fb9d74fd8df047d8a9679cc872ff70(
    *,
    header_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba21cf038ee03e611a3daf8728fccb5a3fed46d36dd74a60f5de5e862320b308(
    *,
    partition_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e376464d2a67d109c81240aa633c109a56168f4658895f7b05167cfaebd032(
    *,
    invocation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5822bf44f36a9423ca7880cefc68b40da74e84a591bc8b8f65d30c203b1e90ac(
    *,
    batch_job_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeTargetBatchJobParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_logs_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeTargetCloudWatchLogsParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ecs_task_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeTargetEcsTaskParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    event_bridge_event_bus_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeTargetEventBridgeEventBusParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeTargetHttpParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    input_template: typing.Optional[builtins.str] = None,
    kinesis_stream_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeTargetKinesisStreamParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_function_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeTargetLambdaFunctionParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    redshift_data_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeTargetRedshiftDataParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sage_maker_pipeline_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeTargetSageMakerPipelineParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sqs_queue_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeTargetSqsQueueParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    step_function_state_machine_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeTargetStateMachineParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timestream_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.PipeTargetTimestreamParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09b7f8fe65076799be624ecbdf63ea4a6f314d051165f310ca27b638ded3f7c(
    *,
    database: typing.Optional[builtins.str] = None,
    db_user: typing.Optional[builtins.str] = None,
    secret_manager_arn: typing.Optional[builtins.str] = None,
    sqls: typing.Optional[typing.Sequence[builtins.str]] = None,
    statement_name: typing.Optional[builtins.str] = None,
    with_event: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f4ad678fdf91a91e7b59e0af6034c0d6725cb9dc98f6c0bbcc50cb1c22e331(
    *,
    pipeline_parameter_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.SageMakerPipelineParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb19f843c1c25cee6954d6cb6f02e99d81bc7cff0c21bdd6e0e011cae80a083(
    *,
    message_deduplication_id: typing.Optional[builtins.str] = None,
    message_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f511d445110258f1db8ee1b6d238b4408d4d3170eec5c2e6a85259dc3f2a84(
    *,
    invocation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35d0c0c4e83ac8dd41f1d34927c0d9097c255e241f117315a16e984a6745b29(
    *,
    dimension_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.DimensionMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    epoch_time_unit: typing.Optional[builtins.str] = None,
    multi_measure_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.MultiMeasureMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    single_measure_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipePropsMixin.SingleMeasureMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    time_field_type: typing.Optional[builtins.str] = None,
    timestamp_format: typing.Optional[builtins.str] = None,
    time_value: typing.Optional[builtins.str] = None,
    version_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac676569baa0bb2c6e0b2c4463ebd98c4a0be67c8a627f96cf145332a7ade37b(
    *,
    expression: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0ed5dc81044c375f98837a6e920f8e5d7a0394d5f1e9e5ad6f5796c5f803f6(
    *,
    field: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7129990eedc7520809bd06acf0cadd63a7e2742f3d3f73f8019772a7057e028(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_owner: typing.Optional[builtins.str] = None,
    output_format: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42adc5cc99d7410ea8d1dcd0f43571bf9e330bcab2d76328650f373ca026da3f(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0390f948961dcc3677983b7a2942badaaee5c36c345a6f624188d3a2a77fd75f(
    *,
    basic_auth: typing.Optional[builtins.str] = None,
    client_certificate_tls_auth: typing.Optional[builtins.str] = None,
    sasl_scram256_auth: typing.Optional[builtins.str] = None,
    sasl_scram512_auth: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb5edd62ce139a885152c9de1715544afcdeaebc5a6053eea00ab3aad59551ff(
    *,
    security_group: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78bd9802fbe941d48cee73e63049c845ba690da35652e7d36e326dac1b6d780d(
    *,
    measure_name: typing.Optional[builtins.str] = None,
    measure_value: typing.Optional[builtins.str] = None,
    measure_value_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
