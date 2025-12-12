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


@jsii.implements(_IMixin_11e4b965)
class CfnPipelineLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_osis.mixins.CfnPipelineLogsMixin",
):
    '''The AWS::OSIS::Pipeline resource creates an Amazon OpenSearch Ingestion pipeline.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-osis-pipeline.html
    :cloudformationResource: AWS::OSIS::Pipeline
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_osis import mixins as osis_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_pipeline_logs_mixin = osis_mixins.CfnPipelineLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::OSIS::Pipeline``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5fb71cd9c07f08daa4b34af71c842b8b8093d9c781f1a311e5b2b822537c51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26fc9cc6677ece8240351c6f58912a53289275e6d0fdbd8d92c7a4bee28c3459)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c8d513344e9f4be2d8d915b49684071b1a79779dd073eafefe2bfa99bf454b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PIPELINE_LOGS")
    def PIPELINE_LOGS(cls) -> "CfnPipelinePipelineLogs":
        return typing.cast("CfnPipelinePipelineLogs", jsii.sget(cls, "PIPELINE_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_osis.mixins.CfnPipelineMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "buffer_options": "bufferOptions",
        "encryption_at_rest_options": "encryptionAtRestOptions",
        "log_publishing_options": "logPublishingOptions",
        "max_units": "maxUnits",
        "min_units": "minUnits",
        "pipeline_configuration_body": "pipelineConfigurationBody",
        "pipeline_name": "pipelineName",
        "pipeline_role_arn": "pipelineRoleArn",
        "resource_policy": "resourcePolicy",
        "tags": "tags",
        "vpc_options": "vpcOptions",
    },
)
class CfnPipelineMixinProps:
    def __init__(
        self,
        *,
        buffer_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.BufferOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        encryption_at_rest_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.EncryptionAtRestOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        log_publishing_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.LogPublishingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        max_units: typing.Optional[jsii.Number] = None,
        min_units: typing.Optional[jsii.Number] = None,
        pipeline_configuration_body: typing.Optional[builtins.str] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        pipeline_role_arn: typing.Optional[builtins.str] = None,
        resource_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.ResourcePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.VpcOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPipelinePropsMixin.

        :param buffer_options: Options that specify the configuration of a persistent buffer. To configure how OpenSearch Ingestion encrypts this data, set the ``EncryptionAtRestOptions`` . For more information, see `Persistent buffering <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/osis-features-overview.html#persistent-buffering>`_ .
        :param encryption_at_rest_options: Options to control how OpenSearch encrypts buffer data.
        :param log_publishing_options: Key-value pairs that represent log publishing settings.
        :param max_units: The maximum pipeline capacity, in Ingestion Compute Units (ICUs).
        :param min_units: The minimum pipeline capacity, in Ingestion Compute Units (ICUs).
        :param pipeline_configuration_body: The Data Prepper pipeline configuration in YAML format.
        :param pipeline_name: The name of the pipeline.
        :param pipeline_role_arn: The Amazon Resource Name (ARN) of the IAM role that the pipeline uses to access AWS resources.
        :param resource_policy: 
        :param tags: List of tags to add to the pipeline upon creation.
        :param vpc_options: Options that specify the subnets and security groups for an OpenSearch Ingestion VPC endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-osis-pipeline.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_osis import mixins as osis_mixins
            
            # policy: Any
            
            cfn_pipeline_mixin_props = osis_mixins.CfnPipelineMixinProps(
                buffer_options=osis_mixins.CfnPipelinePropsMixin.BufferOptionsProperty(
                    persistent_buffer_enabled=False
                ),
                encryption_at_rest_options=osis_mixins.CfnPipelinePropsMixin.EncryptionAtRestOptionsProperty(
                    kms_key_arn="kmsKeyArn"
                ),
                log_publishing_options=osis_mixins.CfnPipelinePropsMixin.LogPublishingOptionsProperty(
                    cloud_watch_log_destination=osis_mixins.CfnPipelinePropsMixin.CloudWatchLogDestinationProperty(
                        log_group="logGroup"
                    ),
                    is_logging_enabled=False
                ),
                max_units=123,
                min_units=123,
                pipeline_configuration_body="pipelineConfigurationBody",
                pipeline_name="pipelineName",
                pipeline_role_arn="pipelineRoleArn",
                resource_policy=osis_mixins.CfnPipelinePropsMixin.ResourcePolicyProperty(
                    policy=policy
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_options=osis_mixins.CfnPipelinePropsMixin.VpcOptionsProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"],
                    vpc_attachment_options=osis_mixins.CfnPipelinePropsMixin.VpcAttachmentOptionsProperty(
                        attach_to_vpc=False,
                        cidr_block="cidrBlock"
                    ),
                    vpc_endpoint_management="vpcEndpointManagement"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0917017cb84f550a2995bce613a49bffb658080cc36f0fb8e3dc62ef3cd7be0a)
            check_type(argname="argument buffer_options", value=buffer_options, expected_type=type_hints["buffer_options"])
            check_type(argname="argument encryption_at_rest_options", value=encryption_at_rest_options, expected_type=type_hints["encryption_at_rest_options"])
            check_type(argname="argument log_publishing_options", value=log_publishing_options, expected_type=type_hints["log_publishing_options"])
            check_type(argname="argument max_units", value=max_units, expected_type=type_hints["max_units"])
            check_type(argname="argument min_units", value=min_units, expected_type=type_hints["min_units"])
            check_type(argname="argument pipeline_configuration_body", value=pipeline_configuration_body, expected_type=type_hints["pipeline_configuration_body"])
            check_type(argname="argument pipeline_name", value=pipeline_name, expected_type=type_hints["pipeline_name"])
            check_type(argname="argument pipeline_role_arn", value=pipeline_role_arn, expected_type=type_hints["pipeline_role_arn"])
            check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_options", value=vpc_options, expected_type=type_hints["vpc_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if buffer_options is not None:
            self._values["buffer_options"] = buffer_options
        if encryption_at_rest_options is not None:
            self._values["encryption_at_rest_options"] = encryption_at_rest_options
        if log_publishing_options is not None:
            self._values["log_publishing_options"] = log_publishing_options
        if max_units is not None:
            self._values["max_units"] = max_units
        if min_units is not None:
            self._values["min_units"] = min_units
        if pipeline_configuration_body is not None:
            self._values["pipeline_configuration_body"] = pipeline_configuration_body
        if pipeline_name is not None:
            self._values["pipeline_name"] = pipeline_name
        if pipeline_role_arn is not None:
            self._values["pipeline_role_arn"] = pipeline_role_arn
        if resource_policy is not None:
            self._values["resource_policy"] = resource_policy
        if tags is not None:
            self._values["tags"] = tags
        if vpc_options is not None:
            self._values["vpc_options"] = vpc_options

    @builtins.property
    def buffer_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.BufferOptionsProperty"]]:
        '''Options that specify the configuration of a persistent buffer.

        To configure how OpenSearch Ingestion encrypts this data, set the ``EncryptionAtRestOptions`` . For more information, see `Persistent buffering <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/osis-features-overview.html#persistent-buffering>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-osis-pipeline.html#cfn-osis-pipeline-bufferoptions
        '''
        result = self._values.get("buffer_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.BufferOptionsProperty"]], result)

    @builtins.property
    def encryption_at_rest_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.EncryptionAtRestOptionsProperty"]]:
        '''Options to control how OpenSearch encrypts buffer data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-osis-pipeline.html#cfn-osis-pipeline-encryptionatrestoptions
        '''
        result = self._values.get("encryption_at_rest_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.EncryptionAtRestOptionsProperty"]], result)

    @builtins.property
    def log_publishing_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.LogPublishingOptionsProperty"]]:
        '''Key-value pairs that represent log publishing settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-osis-pipeline.html#cfn-osis-pipeline-logpublishingoptions
        '''
        result = self._values.get("log_publishing_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.LogPublishingOptionsProperty"]], result)

    @builtins.property
    def max_units(self) -> typing.Optional[jsii.Number]:
        '''The maximum pipeline capacity, in Ingestion Compute Units (ICUs).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-osis-pipeline.html#cfn-osis-pipeline-maxunits
        '''
        result = self._values.get("max_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_units(self) -> typing.Optional[jsii.Number]:
        '''The minimum pipeline capacity, in Ingestion Compute Units (ICUs).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-osis-pipeline.html#cfn-osis-pipeline-minunits
        '''
        result = self._values.get("min_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pipeline_configuration_body(self) -> typing.Optional[builtins.str]:
        '''The Data Prepper pipeline configuration in YAML format.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-osis-pipeline.html#cfn-osis-pipeline-pipelineconfigurationbody
        '''
        result = self._values.get("pipeline_configuration_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipeline_name(self) -> typing.Optional[builtins.str]:
        '''The name of the pipeline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-osis-pipeline.html#cfn-osis-pipeline-pipelinename
        '''
        result = self._values.get("pipeline_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipeline_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role that the pipeline uses to access AWS resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-osis-pipeline.html#cfn-osis-pipeline-pipelinerolearn
        '''
        result = self._values.get("pipeline_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ResourcePolicyProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-osis-pipeline.html#cfn-osis-pipeline-resourcepolicy
        '''
        result = self._values.get("resource_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.ResourcePolicyProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''List of tags to add to the pipeline upon creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-osis-pipeline.html#cfn-osis-pipeline-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.VpcOptionsProperty"]]:
        '''Options that specify the subnets and security groups for an OpenSearch Ingestion VPC endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-osis-pipeline.html#cfn-osis-pipeline-vpcoptions
        '''
        result = self._values.get("vpc_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.VpcOptionsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPipelineMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfnPipelinePipelineLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_osis.mixins.CfnPipelinePipelineLogs",
):
    '''Builder for CfnPipelineLogsMixin to generate PIPELINE_LOGS for CfnPipeline.

    :cloudformationResource: AWS::OSIS::Pipeline
    :logType: PIPELINE_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_osis import mixins as osis_mixins
        
        cfn_pipeline_pipeline_logs = osis_mixins.CfnPipelinePipelineLogs()
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
    ) -> CfnPipelineLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7518fea5d8e59e3d962fcdfb32298f2855a257929aad2717ce8c257d738639b9)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnPipelineLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnPipelineLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ca89022e5b2d331aa3234b96a6bf3b205d5bfe85047d4fa927bd02384067ee2)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnPipelineLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnPipelineLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad3d660ecd4cb4f9bf09e8a00f28e2ab16f2c9d3635e9ee37000406ed9873203)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnPipelineLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnPipelinePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_osis.mixins.CfnPipelinePropsMixin",
):
    '''The AWS::OSIS::Pipeline resource creates an Amazon OpenSearch Ingestion pipeline.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-osis-pipeline.html
    :cloudformationResource: AWS::OSIS::Pipeline
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_osis import mixins as osis_mixins
        
        # policy: Any
        
        cfn_pipeline_props_mixin = osis_mixins.CfnPipelinePropsMixin(osis_mixins.CfnPipelineMixinProps(
            buffer_options=osis_mixins.CfnPipelinePropsMixin.BufferOptionsProperty(
                persistent_buffer_enabled=False
            ),
            encryption_at_rest_options=osis_mixins.CfnPipelinePropsMixin.EncryptionAtRestOptionsProperty(
                kms_key_arn="kmsKeyArn"
            ),
            log_publishing_options=osis_mixins.CfnPipelinePropsMixin.LogPublishingOptionsProperty(
                cloud_watch_log_destination=osis_mixins.CfnPipelinePropsMixin.CloudWatchLogDestinationProperty(
                    log_group="logGroup"
                ),
                is_logging_enabled=False
            ),
            max_units=123,
            min_units=123,
            pipeline_configuration_body="pipelineConfigurationBody",
            pipeline_name="pipelineName",
            pipeline_role_arn="pipelineRoleArn",
            resource_policy=osis_mixins.CfnPipelinePropsMixin.ResourcePolicyProperty(
                policy=policy
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_options=osis_mixins.CfnPipelinePropsMixin.VpcOptionsProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"],
                vpc_attachment_options=osis_mixins.CfnPipelinePropsMixin.VpcAttachmentOptionsProperty(
                    attach_to_vpc=False,
                    cidr_block="cidrBlock"
                ),
                vpc_endpoint_management="vpcEndpointManagement"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPipelineMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OSIS::Pipeline``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c87100351edb22f47feb4145045689eef53ca73e5c82694b879529b96e94ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79afbc826d2ae86c1e97ec7e1f179d99a9053b2f1b7fc9b6b5f789d0b551df19)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a12169fadef0d03c479be876125d4c22b1be68d16f9a6894e18f51fcdbad53dc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPipelineMixinProps:
        return typing.cast(CfnPipelineMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_osis.mixins.CfnPipelinePropsMixin.BufferOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"persistent_buffer_enabled": "persistentBufferEnabled"},
    )
    class BufferOptionsProperty:
        def __init__(
            self,
            *,
            persistent_buffer_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Options that specify the configuration of a persistent buffer.

            To configure how OpenSearch Ingestion encrypts this data, set the ``EncryptionAtRestOptions`` . For more information, see `Persistent buffering <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/osis-features-overview.html#persistent-buffering>`_ .

            :param persistent_buffer_enabled: Whether persistent buffering should be enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-bufferoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_osis import mixins as osis_mixins
                
                buffer_options_property = osis_mixins.CfnPipelinePropsMixin.BufferOptionsProperty(
                    persistent_buffer_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8599efebfc36a9fef6443f8ca18264eeb9754bdf739315e2edda93adbc5c6967)
                check_type(argname="argument persistent_buffer_enabled", value=persistent_buffer_enabled, expected_type=type_hints["persistent_buffer_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if persistent_buffer_enabled is not None:
                self._values["persistent_buffer_enabled"] = persistent_buffer_enabled

        @builtins.property
        def persistent_buffer_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether persistent buffering should be enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-bufferoptions.html#cfn-osis-pipeline-bufferoptions-persistentbufferenabled
            '''
            result = self._values.get("persistent_buffer_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BufferOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_osis.mixins.CfnPipelinePropsMixin.CloudWatchLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group": "logGroup"},
    )
    class CloudWatchLogDestinationProperty:
        def __init__(self, *, log_group: typing.Optional[builtins.str] = None) -> None:
            '''The destination for OpenSearch Ingestion logs sent to Amazon CloudWatch.

            :param log_group: The name of the CloudWatch Logs group to send pipeline logs to. You can specify an existing log group or create a new one. For example, ``/aws/vendedlogs/OpenSearchService/pipelines`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-cloudwatchlogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_osis import mixins as osis_mixins
                
                cloud_watch_log_destination_property = osis_mixins.CfnPipelinePropsMixin.CloudWatchLogDestinationProperty(
                    log_group="logGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f0577ba9af8df914bbd3d9ff78e45e09e84123b3315a04e115152aad57daaaa1)
                check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group is not None:
                self._values["log_group"] = log_group

        @builtins.property
        def log_group(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch Logs group to send pipeline logs to.

            You can specify an existing log group or create a new one. For example, ``/aws/vendedlogs/OpenSearchService/pipelines`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-cloudwatchlogdestination.html#cfn-osis-pipeline-cloudwatchlogdestination-loggroup
            '''
            result = self._values.get("log_group")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_osis.mixins.CfnPipelinePropsMixin.EncryptionAtRestOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_arn": "kmsKeyArn"},
    )
    class EncryptionAtRestOptionsProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Options to control how OpenSearch encrypts buffer data.

            :param kms_key_arn: The ARN of the KMS key used to encrypt buffer data. By default, data is encrypted using an AWS owned key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-encryptionatrestoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_osis import mixins as osis_mixins
                
                encryption_at_rest_options_property = osis_mixins.CfnPipelinePropsMixin.EncryptionAtRestOptionsProperty(
                    kms_key_arn="kmsKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c765b1897334d6e644902117cabc5dad1dfba83b48def76129536317d7e94880)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the KMS key used to encrypt buffer data.

            By default, data is encrypted using an AWS owned key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-encryptionatrestoptions.html#cfn-osis-pipeline-encryptionatrestoptions-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionAtRestOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_osis.mixins.CfnPipelinePropsMixin.LogPublishingOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_log_destination": "cloudWatchLogDestination",
            "is_logging_enabled": "isLoggingEnabled",
        },
    )
    class LogPublishingOptionsProperty:
        def __init__(
            self,
            *,
            cloud_watch_log_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.CloudWatchLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            is_logging_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Container for the values required to configure logging for the pipeline.

            If you don't specify these values, OpenSearch Ingestion will not publish logs from your application to CloudWatch Logs.

            :param cloud_watch_log_destination: The destination for OpenSearch Ingestion logs sent to Amazon CloudWatch Logs. This parameter is required if ``IsLoggingEnabled`` is set to ``true`` .
            :param is_logging_enabled: Whether logs should be published.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-logpublishingoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_osis import mixins as osis_mixins
                
                log_publishing_options_property = osis_mixins.CfnPipelinePropsMixin.LogPublishingOptionsProperty(
                    cloud_watch_log_destination=osis_mixins.CfnPipelinePropsMixin.CloudWatchLogDestinationProperty(
                        log_group="logGroup"
                    ),
                    is_logging_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9dca8479d310af24e4039bd59677777ae16eae9a85a1fec4b2360decb1aff3a3)
                check_type(argname="argument cloud_watch_log_destination", value=cloud_watch_log_destination, expected_type=type_hints["cloud_watch_log_destination"])
                check_type(argname="argument is_logging_enabled", value=is_logging_enabled, expected_type=type_hints["is_logging_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_log_destination is not None:
                self._values["cloud_watch_log_destination"] = cloud_watch_log_destination
            if is_logging_enabled is not None:
                self._values["is_logging_enabled"] = is_logging_enabled

        @builtins.property
        def cloud_watch_log_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.CloudWatchLogDestinationProperty"]]:
            '''The destination for OpenSearch Ingestion logs sent to Amazon CloudWatch Logs.

            This parameter is required if ``IsLoggingEnabled`` is set to ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-logpublishingoptions.html#cfn-osis-pipeline-logpublishingoptions-cloudwatchlogdestination
            '''
            result = self._values.get("cloud_watch_log_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.CloudWatchLogDestinationProperty"]], result)

        @builtins.property
        def is_logging_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether logs should be published.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-logpublishingoptions.html#cfn-osis-pipeline-logpublishingoptions-isloggingenabled
            '''
            result = self._values.get("is_logging_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogPublishingOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_osis.mixins.CfnPipelinePropsMixin.ResourcePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"policy": "policy"},
    )
    class ResourcePolicyProperty:
        def __init__(self, *, policy: typing.Any = None) -> None:
            '''
            :param policy: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-resourcepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_osis import mixins as osis_mixins
                
                # policy: Any
                
                resource_policy_property = osis_mixins.CfnPipelinePropsMixin.ResourcePolicyProperty(
                    policy=policy
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6982719bd9dca0afd3d4556353b04fa35cf150b3ba42bd7c98357d8a520a8b7)
                check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy is not None:
                self._values["policy"] = policy

        @builtins.property
        def policy(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-resourcepolicy.html#cfn-osis-pipeline-resourcepolicy-policy
            '''
            result = self._values.get("policy")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourcePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_osis.mixins.CfnPipelinePropsMixin.VpcAttachmentOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"attach_to_vpc": "attachToVpc", "cidr_block": "cidrBlock"},
    )
    class VpcAttachmentOptionsProperty:
        def __init__(
            self,
            *,
            attach_to_vpc: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            cidr_block: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Options for attaching a VPC to pipeline.

            :param attach_to_vpc: Whether a VPC is attached to the pipeline.
            :param cidr_block: The CIDR block to be reserved for OpenSearch Ingestion to create elastic network interfaces (ENIs).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-vpcattachmentoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_osis import mixins as osis_mixins
                
                vpc_attachment_options_property = osis_mixins.CfnPipelinePropsMixin.VpcAttachmentOptionsProperty(
                    attach_to_vpc=False,
                    cidr_block="cidrBlock"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6d4a637552a712f601e5897092b65f8487c3ad78408738385b7569c05e36d5be)
                check_type(argname="argument attach_to_vpc", value=attach_to_vpc, expected_type=type_hints["attach_to_vpc"])
                check_type(argname="argument cidr_block", value=cidr_block, expected_type=type_hints["cidr_block"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attach_to_vpc is not None:
                self._values["attach_to_vpc"] = attach_to_vpc
            if cidr_block is not None:
                self._values["cidr_block"] = cidr_block

        @builtins.property
        def attach_to_vpc(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether a VPC is attached to the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-vpcattachmentoptions.html#cfn-osis-pipeline-vpcattachmentoptions-attachtovpc
            '''
            result = self._values.get("attach_to_vpc")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def cidr_block(self) -> typing.Optional[builtins.str]:
            '''The CIDR block to be reserved for OpenSearch Ingestion to create elastic network interfaces (ENIs).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-vpcattachmentoptions.html#cfn-osis-pipeline-vpcattachmentoptions-cidrblock
            '''
            result = self._values.get("cidr_block")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcAttachmentOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_osis.mixins.CfnPipelinePropsMixin.VpcEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "vpc_endpoint_id": "vpcEndpointId",
            "vpc_id": "vpcId",
            "vpc_options": "vpcOptions",
        },
    )
    class VpcEndpointProperty:
        def __init__(
            self,
            *,
            vpc_endpoint_id: typing.Optional[builtins.str] = None,
            vpc_id: typing.Optional[builtins.str] = None,
            vpc_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.VpcOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An OpenSearch Ingestion-managed VPC endpoint that will access one or more pipelines.

            :param vpc_endpoint_id: The unique identifier of the endpoint.
            :param vpc_id: The ID for your VPC. AWS PrivateLink generates this value when you create a VPC.
            :param vpc_options: Information about the VPC, including associated subnets and security groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-vpcendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_osis import mixins as osis_mixins
                
                vpc_endpoint_property = osis_mixins.CfnPipelinePropsMixin.VpcEndpointProperty(
                    vpc_endpoint_id="vpcEndpointId",
                    vpc_id="vpcId",
                    vpc_options=osis_mixins.CfnPipelinePropsMixin.VpcOptionsProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"],
                        vpc_attachment_options=osis_mixins.CfnPipelinePropsMixin.VpcAttachmentOptionsProperty(
                            attach_to_vpc=False,
                            cidr_block="cidrBlock"
                        ),
                        vpc_endpoint_management="vpcEndpointManagement"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89a20e77717784dd759d9fc4ecb6314031c73c49567b36cf606d2fbf130f2b2a)
                check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
                check_type(argname="argument vpc_options", value=vpc_options, expected_type=type_hints["vpc_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_endpoint_id is not None:
                self._values["vpc_endpoint_id"] = vpc_endpoint_id
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id
            if vpc_options is not None:
                self._values["vpc_options"] = vpc_options

        @builtins.property
        def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-vpcendpoint.html#cfn-osis-pipeline-vpcendpoint-vpcendpointid
            '''
            result = self._values.get("vpc_endpoint_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''The ID for your VPC.

            AWS PrivateLink generates this value when you create a VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-vpcendpoint.html#cfn-osis-pipeline-vpcendpoint-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.VpcOptionsProperty"]]:
            '''Information about the VPC, including associated subnets and security groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-vpcendpoint.html#cfn-osis-pipeline-vpcendpoint-vpcoptions
            '''
            result = self._values.get("vpc_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.VpcOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_osis.mixins.CfnPipelinePropsMixin.VpcOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
            "vpc_attachment_options": "vpcAttachmentOptions",
            "vpc_endpoint_management": "vpcEndpointManagement",
        },
    )
    class VpcOptionsProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            vpc_attachment_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPipelinePropsMixin.VpcAttachmentOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            vpc_endpoint_management: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Options that specify the subnets and security groups for an OpenSearch Ingestion VPC endpoint.

            :param security_group_ids: A list of security groups associated with the VPC endpoint.
            :param subnet_ids: A list of subnet IDs associated with the VPC endpoint.
            :param vpc_attachment_options: Options for attaching a VPC to a pipeline.
            :param vpc_endpoint_management: Defines whether you or Amazon OpenSearch Ingestion service create and manage the VPC endpoint configured for the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-vpcoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_osis import mixins as osis_mixins
                
                vpc_options_property = osis_mixins.CfnPipelinePropsMixin.VpcOptionsProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"],
                    vpc_attachment_options=osis_mixins.CfnPipelinePropsMixin.VpcAttachmentOptionsProperty(
                        attach_to_vpc=False,
                        cidr_block="cidrBlock"
                    ),
                    vpc_endpoint_management="vpcEndpointManagement"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6cc613467c7657623d7da117334a66f56d16cdcaf7db14af822cc732f2b12023)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
                check_type(argname="argument vpc_attachment_options", value=vpc_attachment_options, expected_type=type_hints["vpc_attachment_options"])
                check_type(argname="argument vpc_endpoint_management", value=vpc_endpoint_management, expected_type=type_hints["vpc_endpoint_management"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids
            if vpc_attachment_options is not None:
                self._values["vpc_attachment_options"] = vpc_attachment_options
            if vpc_endpoint_management is not None:
                self._values["vpc_endpoint_management"] = vpc_endpoint_management

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of security groups associated with the VPC endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-vpcoptions.html#cfn-osis-pipeline-vpcoptions-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of subnet IDs associated with the VPC endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-vpcoptions.html#cfn-osis-pipeline-vpcoptions-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def vpc_attachment_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.VpcAttachmentOptionsProperty"]]:
            '''Options for attaching a VPC to a pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-vpcoptions.html#cfn-osis-pipeline-vpcoptions-vpcattachmentoptions
            '''
            result = self._values.get("vpc_attachment_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPipelinePropsMixin.VpcAttachmentOptionsProperty"]], result)

        @builtins.property
        def vpc_endpoint_management(self) -> typing.Optional[builtins.str]:
            '''Defines whether you or Amazon OpenSearch Ingestion service create and manage the VPC endpoint configured for the pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-osis-pipeline-vpcoptions.html#cfn-osis-pipeline-vpcoptions-vpcendpointmanagement
            '''
            result = self._values.get("vpc_endpoint_management")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnPipelineLogsMixin",
    "CfnPipelineMixinProps",
    "CfnPipelinePipelineLogs",
    "CfnPipelinePropsMixin",
]

publication.publish()

def _typecheckingstub__ef5fb71cd9c07f08daa4b34af71c842b8b8093d9c781f1a311e5b2b822537c51(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fc9cc6677ece8240351c6f58912a53289275e6d0fdbd8d92c7a4bee28c3459(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c8d513344e9f4be2d8d915b49684071b1a79779dd073eafefe2bfa99bf454b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0917017cb84f550a2995bce613a49bffb658080cc36f0fb8e3dc62ef3cd7be0a(
    *,
    buffer_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.BufferOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_at_rest_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.EncryptionAtRestOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    log_publishing_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.LogPublishingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_units: typing.Optional[jsii.Number] = None,
    min_units: typing.Optional[jsii.Number] = None,
    pipeline_configuration_body: typing.Optional[builtins.str] = None,
    pipeline_name: typing.Optional[builtins.str] = None,
    pipeline_role_arn: typing.Optional[builtins.str] = None,
    resource_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.ResourcePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.VpcOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7518fea5d8e59e3d962fcdfb32298f2855a257929aad2717ce8c257d738639b9(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca89022e5b2d331aa3234b96a6bf3b205d5bfe85047d4fa927bd02384067ee2(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3d660ecd4cb4f9bf09e8a00f28e2ab16f2c9d3635e9ee37000406ed9873203(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c87100351edb22f47feb4145045689eef53ca73e5c82694b879529b96e94ed(
    props: typing.Union[CfnPipelineMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79afbc826d2ae86c1e97ec7e1f179d99a9053b2f1b7fc9b6b5f789d0b551df19(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12169fadef0d03c479be876125d4c22b1be68d16f9a6894e18f51fcdbad53dc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8599efebfc36a9fef6443f8ca18264eeb9754bdf739315e2edda93adbc5c6967(
    *,
    persistent_buffer_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0577ba9af8df914bbd3d9ff78e45e09e84123b3315a04e115152aad57daaaa1(
    *,
    log_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c765b1897334d6e644902117cabc5dad1dfba83b48def76129536317d7e94880(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dca8479d310af24e4039bd59677777ae16eae9a85a1fec4b2360decb1aff3a3(
    *,
    cloud_watch_log_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.CloudWatchLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_logging_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6982719bd9dca0afd3d4556353b04fa35cf150b3ba42bd7c98357d8a520a8b7(
    *,
    policy: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d4a637552a712f601e5897092b65f8487c3ad78408738385b7569c05e36d5be(
    *,
    attach_to_vpc: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cidr_block: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a20e77717784dd759d9fc4ecb6314031c73c49567b36cf606d2fbf130f2b2a(
    *,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
    vpc_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.VpcOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc613467c7657623d7da117334a66f56d16cdcaf7db14af822cc732f2b12023(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_attachment_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPipelinePropsMixin.VpcAttachmentOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_endpoint_management: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
