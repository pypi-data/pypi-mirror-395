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
    jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnCanaryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_config": "artifactConfig",
        "artifact_s3_location": "artifactS3Location",
        "browser_configs": "browserConfigs",
        "code": "code",
        "delete_lambda_resources_on_canary_deletion": "deleteLambdaResourcesOnCanaryDeletion",
        "dry_run_and_update": "dryRunAndUpdate",
        "execution_role_arn": "executionRoleArn",
        "failure_retention_period": "failureRetentionPeriod",
        "name": "name",
        "provisioned_resource_cleanup": "provisionedResourceCleanup",
        "resources_to_replicate_tags": "resourcesToReplicateTags",
        "run_config": "runConfig",
        "runtime_version": "runtimeVersion",
        "schedule": "schedule",
        "start_canary_after_creation": "startCanaryAfterCreation",
        "success_retention_period": "successRetentionPeriod",
        "tags": "tags",
        "visual_reference": "visualReference",
        "visual_references": "visualReferences",
        "vpc_config": "vpcConfig",
    },
)
class CfnCanaryMixinProps:
    def __init__(
        self,
        *,
        artifact_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCanaryPropsMixin.ArtifactConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        artifact_s3_location: typing.Optional[builtins.str] = None,
        browser_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCanaryPropsMixin.BrowserConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        code: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCanaryPropsMixin.CodeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        delete_lambda_resources_on_canary_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        dry_run_and_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        failure_retention_period: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        provisioned_resource_cleanup: typing.Optional[builtins.str] = None,
        resources_to_replicate_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        run_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCanaryPropsMixin.RunConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCanaryPropsMixin.ScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        start_canary_after_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        success_retention_period: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        visual_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCanaryPropsMixin.VisualReferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        visual_references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCanaryPropsMixin.VisualReferenceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCanaryPropsMixin.VPCConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCanaryPropsMixin.

        :param artifact_config: A structure that contains the configuration for canary artifacts, including the encryption-at-rest settings for artifacts that the canary uploads to Amazon S3.
        :param artifact_s3_location: The location in Amazon S3 where Synthetics stores artifacts from the runs of this canary. Artifacts include the log file, screenshots, and HAR files. Specify the full location path, including ``s3://`` at the beginning of the path.
        :param browser_configs: A structure that specifies the browser type to use for a canary run. CloudWatch Synthetics supports running canaries on both ``CHROME`` and ``FIREFOX`` browsers. .. epigraph:: If not specified, ``browserConfigs`` defaults to Chrome.
        :param code: Use this structure to input your script code for the canary. This structure contains the Lambda handler with the location where the canary should start running the script. If the script is stored in an S3 bucket, the bucket name, key, and version are also included. If the script is passed into the canary directly, the script code is contained in the value of ``Script`` .
        :param delete_lambda_resources_on_canary_deletion: (deprecated) Deletes associated lambda resources created by Synthetics if set to True. Default is False
        :param dry_run_and_update: Specifies whether to perform a dry run before updating the canary. If set to ``true`` , CloudFormation will execute a dry run to validate the changes before applying them to the canary. If the dry run succeeds, the canary will be updated with the changes. If the dry run fails, the CloudFormation deployment will fail with the dry run’s failure reason. If set to ``false`` or omitted, the canary will be updated directly without first performing a dry run. The default value is ``false`` . For more information, see `Performing safe canary updates <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/performing-safe-canary-upgrades.html>`_ .
        :param execution_role_arn: The ARN of the IAM role to be used to run the canary. This role must already exist, and must include ``lambda.amazonaws.com`` as a principal in the trust policy. The role must also have the following permissions: - ``s3:PutObject`` - ``s3:GetBucketLocation`` - ``s3:ListAllMyBuckets`` - ``cloudwatch:PutMetricData`` - ``logs:CreateLogGroup`` - ``logs:CreateLogStream`` - ``logs:PutLogEvents``
        :param failure_retention_period: The number of days to retain data about failed runs of this canary. If you omit this field, the default of 31 days is used. The valid range is 1 to 455 days. This setting affects the range of information returned by `GetCanaryRuns <https://docs.aws.amazon.com/AmazonSynthetics/latest/APIReference/API_GetCanaryRuns.html>`_ , as well as the range of information displayed in the Synthetics console.
        :param name: The name for this canary. Be sure to give it a descriptive name that distinguishes it from other canaries in your account. Do not include secrets or proprietary information in your canary names. The canary name makes up part of the canary ARN, and the ARN is included in outbound calls over the internet. For more information, see `Security Considerations for Synthetics Canaries <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/servicelens_canaries_security.html>`_ .
        :param provisioned_resource_cleanup: Specifies whether to also delete the Lambda functions and layers used by this canary when the canary is deleted. If it is ``AUTOMATIC`` , the Lambda functions and layers will be deleted when the canary is deleted. If the value of this parameter is ``OFF`` , then the value of the ``DeleteLambda`` parameter of the `DeleteCanary <https://docs.aws.amazon.com/AmazonSynthetics/latest/APIReference/API_DeleteCanary.html>`_ operation determines whether the Lambda functions and layers will be deleted.
        :param resources_to_replicate_tags: To have the tags that you apply to this canary also be applied to the Lambda function that the canary uses, specify this property with the value ``lambda-function`` . If you do this, CloudWatch Synthetics will keep the tags of the canary and the Lambda function synchronized. Any future changes you make to the canary's tags will also be applied to the function.
        :param run_config: A structure that contains input information for a canary run. If you omit this structure, the frequency of the canary is used as canary's timeout value, up to a maximum of 900 seconds.
        :param runtime_version: Specifies the runtime version to use for the canary. For more information about runtime versions, see `Canary Runtime Versions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Library.html>`_ .
        :param schedule: A structure that contains information about how often the canary is to run, and when these runs are to stop.
        :param start_canary_after_creation: Specify TRUE to have the canary start making runs immediately after it is created. A canary that you create using CloudFormation can't be used to monitor the CloudFormation stack that creates the canary or to roll back that stack if there is a failure.
        :param success_retention_period: The number of days to retain data about successful runs of this canary. If you omit this field, the default of 31 days is used. The valid range is 1 to 455 days. This setting affects the range of information returned by `GetCanaryRuns <https://docs.aws.amazon.com/AmazonSynthetics/latest/APIReference/API_GetCanaryRuns.html>`_ , as well as the range of information displayed in the Synthetics console.
        :param tags: The list of key-value pairs that are associated with the canary.
        :param visual_reference: 
        :param visual_references: A list of visual reference configurations for the canary, one for each browser type that the canary is configured to run on. Visual references are used for visual monitoring comparisons. ``syn-nodejs-puppeteer-11.0`` and above, and ``syn-nodejs-playwright-3.0`` and above, only supports ``visualReferences`` . ``visualReference`` field is not supported. Versions older than ``syn-nodejs-puppeteer-11.0`` supports both ``visualReference`` and ``visualReferences`` for backward compatibility. It is recommended to use ``visualReferences`` for consistency and future compatibility.
        :param vpc_config: If this canary is to test an endpoint in a VPC, this structure contains information about the subnet and security groups of the VPC endpoint. For more information, see `Running a Canary in a VPC <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_VPC.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
            
            cfn_canary_mixin_props = synthetics_mixins.CfnCanaryMixinProps(
                artifact_config=synthetics_mixins.CfnCanaryPropsMixin.ArtifactConfigProperty(
                    s3_encryption=synthetics_mixins.CfnCanaryPropsMixin.S3EncryptionProperty(
                        encryption_mode="encryptionMode",
                        kms_key_arn="kmsKeyArn"
                    )
                ),
                artifact_s3_location="artifactS3Location",
                browser_configs=[synthetics_mixins.CfnCanaryPropsMixin.BrowserConfigProperty(
                    browser_type="browserType"
                )],
                code=synthetics_mixins.CfnCanaryPropsMixin.CodeProperty(
                    blueprint_types=["blueprintTypes"],
                    dependencies=[synthetics_mixins.CfnCanaryPropsMixin.DependencyProperty(
                        reference="reference",
                        type="type"
                    )],
                    handler="handler",
                    s3_bucket="s3Bucket",
                    s3_key="s3Key",
                    s3_object_version="s3ObjectVersion",
                    script="script",
                    source_location_arn="sourceLocationArn"
                ),
                delete_lambda_resources_on_canary_deletion=False,
                dry_run_and_update=False,
                execution_role_arn="executionRoleArn",
                failure_retention_period=123,
                name="name",
                provisioned_resource_cleanup="provisionedResourceCleanup",
                resources_to_replicate_tags=["resourcesToReplicateTags"],
                run_config=synthetics_mixins.CfnCanaryPropsMixin.RunConfigProperty(
                    active_tracing=False,
                    environment_variables={
                        "environment_variables_key": "environmentVariables"
                    },
                    ephemeral_storage=123,
                    memory_in_mb=123,
                    timeout_in_seconds=123
                ),
                runtime_version="runtimeVersion",
                schedule=synthetics_mixins.CfnCanaryPropsMixin.ScheduleProperty(
                    duration_in_seconds="durationInSeconds",
                    expression="expression",
                    retry_config=synthetics_mixins.CfnCanaryPropsMixin.RetryConfigProperty(
                        max_retries=123
                    )
                ),
                start_canary_after_creation=False,
                success_retention_period=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                visual_reference=synthetics_mixins.CfnCanaryPropsMixin.VisualReferenceProperty(
                    base_canary_run_id="baseCanaryRunId",
                    base_screenshots=[synthetics_mixins.CfnCanaryPropsMixin.BaseScreenshotProperty(
                        ignore_coordinates=["ignoreCoordinates"],
                        screenshot_name="screenshotName"
                    )],
                    browser_type="browserType"
                ),
                visual_references=[synthetics_mixins.CfnCanaryPropsMixin.VisualReferenceProperty(
                    base_canary_run_id="baseCanaryRunId",
                    base_screenshots=[synthetics_mixins.CfnCanaryPropsMixin.BaseScreenshotProperty(
                        ignore_coordinates=["ignoreCoordinates"],
                        screenshot_name="screenshotName"
                    )],
                    browser_type="browserType"
                )],
                vpc_config=synthetics_mixins.CfnCanaryPropsMixin.VPCConfigProperty(
                    ipv6_allowed_for_dual_stack=False,
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"],
                    vpc_id="vpcId"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab3e2359ab3e4871bd5a046c76d4c4fd03e4b53c80b90a1cdb06f75afcf36ec6)
            check_type(argname="argument artifact_config", value=artifact_config, expected_type=type_hints["artifact_config"])
            check_type(argname="argument artifact_s3_location", value=artifact_s3_location, expected_type=type_hints["artifact_s3_location"])
            check_type(argname="argument browser_configs", value=browser_configs, expected_type=type_hints["browser_configs"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument delete_lambda_resources_on_canary_deletion", value=delete_lambda_resources_on_canary_deletion, expected_type=type_hints["delete_lambda_resources_on_canary_deletion"])
            check_type(argname="argument dry_run_and_update", value=dry_run_and_update, expected_type=type_hints["dry_run_and_update"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument failure_retention_period", value=failure_retention_period, expected_type=type_hints["failure_retention_period"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument provisioned_resource_cleanup", value=provisioned_resource_cleanup, expected_type=type_hints["provisioned_resource_cleanup"])
            check_type(argname="argument resources_to_replicate_tags", value=resources_to_replicate_tags, expected_type=type_hints["resources_to_replicate_tags"])
            check_type(argname="argument run_config", value=run_config, expected_type=type_hints["run_config"])
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument start_canary_after_creation", value=start_canary_after_creation, expected_type=type_hints["start_canary_after_creation"])
            check_type(argname="argument success_retention_period", value=success_retention_period, expected_type=type_hints["success_retention_period"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument visual_reference", value=visual_reference, expected_type=type_hints["visual_reference"])
            check_type(argname="argument visual_references", value=visual_references, expected_type=type_hints["visual_references"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if artifact_config is not None:
            self._values["artifact_config"] = artifact_config
        if artifact_s3_location is not None:
            self._values["artifact_s3_location"] = artifact_s3_location
        if browser_configs is not None:
            self._values["browser_configs"] = browser_configs
        if code is not None:
            self._values["code"] = code
        if delete_lambda_resources_on_canary_deletion is not None:
            self._values["delete_lambda_resources_on_canary_deletion"] = delete_lambda_resources_on_canary_deletion
        if dry_run_and_update is not None:
            self._values["dry_run_and_update"] = dry_run_and_update
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if failure_retention_period is not None:
            self._values["failure_retention_period"] = failure_retention_period
        if name is not None:
            self._values["name"] = name
        if provisioned_resource_cleanup is not None:
            self._values["provisioned_resource_cleanup"] = provisioned_resource_cleanup
        if resources_to_replicate_tags is not None:
            self._values["resources_to_replicate_tags"] = resources_to_replicate_tags
        if run_config is not None:
            self._values["run_config"] = run_config
        if runtime_version is not None:
            self._values["runtime_version"] = runtime_version
        if schedule is not None:
            self._values["schedule"] = schedule
        if start_canary_after_creation is not None:
            self._values["start_canary_after_creation"] = start_canary_after_creation
        if success_retention_period is not None:
            self._values["success_retention_period"] = success_retention_period
        if tags is not None:
            self._values["tags"] = tags
        if visual_reference is not None:
            self._values["visual_reference"] = visual_reference
        if visual_references is not None:
            self._values["visual_references"] = visual_references
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def artifact_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.ArtifactConfigProperty"]]:
        '''A structure that contains the configuration for canary artifacts, including the encryption-at-rest settings for artifacts that the canary uploads to Amazon S3.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-artifactconfig
        '''
        result = self._values.get("artifact_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.ArtifactConfigProperty"]], result)

    @builtins.property
    def artifact_s3_location(self) -> typing.Optional[builtins.str]:
        '''The location in Amazon S3 where Synthetics stores artifacts from the runs of this canary.

        Artifacts include the log file, screenshots, and HAR files. Specify the full location path, including ``s3://`` at the beginning of the path.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-artifacts3location
        '''
        result = self._values.get("artifact_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def browser_configs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.BrowserConfigProperty"]]]]:
        '''A structure that specifies the browser type to use for a canary run.

        CloudWatch Synthetics supports running canaries on both ``CHROME`` and ``FIREFOX`` browsers.
        .. epigraph::

           If not specified, ``browserConfigs`` defaults to Chrome.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-browserconfigs
        '''
        result = self._values.get("browser_configs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.BrowserConfigProperty"]]]], result)

    @builtins.property
    def code(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.CodeProperty"]]:
        '''Use this structure to input your script code for the canary.

        This structure contains the Lambda handler with the location where the canary should start running the script. If the script is stored in an S3 bucket, the bucket name, key, and version are also included. If the script is passed into the canary directly, the script code is contained in the value of ``Script`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-code
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.CodeProperty"]], result)

    @builtins.property
    def delete_lambda_resources_on_canary_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''(deprecated) Deletes associated lambda resources created by Synthetics if set to True.

        Default is False

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-deletelambdaresourcesoncanarydeletion
        :stability: deprecated
        '''
        result = self._values.get("delete_lambda_resources_on_canary_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def dry_run_and_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to perform a dry run before updating the canary.

        If set to ``true`` , CloudFormation will execute a dry run to validate the changes before applying them to the canary. If the dry run succeeds, the canary will be updated with the changes. If the dry run fails, the CloudFormation deployment will fail with the dry run’s failure reason.

        If set to ``false`` or omitted, the canary will be updated directly without first performing a dry run. The default value is ``false`` .

        For more information, see `Performing safe canary updates <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/performing-safe-canary-upgrades.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-dryrunandupdate
        '''
        result = self._values.get("dry_run_and_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role to be used to run the canary.

        This role must already exist, and must include ``lambda.amazonaws.com`` as a principal in the trust policy. The role must also have the following permissions:

        - ``s3:PutObject``
        - ``s3:GetBucketLocation``
        - ``s3:ListAllMyBuckets``
        - ``cloudwatch:PutMetricData``
        - ``logs:CreateLogGroup``
        - ``logs:CreateLogStream``
        - ``logs:PutLogEvents``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain data about failed runs of this canary.

        If you omit this field, the default of 31 days is used. The valid range is 1 to 455 days.

        This setting affects the range of information returned by `GetCanaryRuns <https://docs.aws.amazon.com/AmazonSynthetics/latest/APIReference/API_GetCanaryRuns.html>`_ , as well as the range of information displayed in the Synthetics console.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-failureretentionperiod
        '''
        result = self._values.get("failure_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for this canary.

        Be sure to give it a descriptive name that distinguishes it from other canaries in your account.

        Do not include secrets or proprietary information in your canary names. The canary name makes up part of the canary ARN, and the ARN is included in outbound calls over the internet. For more information, see `Security Considerations for Synthetics Canaries <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/servicelens_canaries_security.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioned_resource_cleanup(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to also delete the Lambda functions and layers used by this canary when the canary is deleted.

        If it is ``AUTOMATIC`` , the Lambda functions and layers will be deleted when the canary is deleted.

        If the value of this parameter is ``OFF`` , then the value of the ``DeleteLambda`` parameter of the `DeleteCanary <https://docs.aws.amazon.com/AmazonSynthetics/latest/APIReference/API_DeleteCanary.html>`_ operation determines whether the Lambda functions and layers will be deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-provisionedresourcecleanup
        '''
        result = self._values.get("provisioned_resource_cleanup")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resources_to_replicate_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''To have the tags that you apply to this canary also be applied to the Lambda function that the canary uses, specify this property with the value ``lambda-function`` .

        If you do this, CloudWatch Synthetics will keep the tags of the canary and the Lambda function synchronized. Any future changes you make to the canary's tags will also be applied to the function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-resourcestoreplicatetags
        '''
        result = self._values.get("resources_to_replicate_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def run_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.RunConfigProperty"]]:
        '''A structure that contains input information for a canary run.

        If you omit this structure, the frequency of the canary is used as canary's timeout value, up to a maximum of 900 seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runconfig
        '''
        result = self._values.get("run_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.RunConfigProperty"]], result)

    @builtins.property
    def runtime_version(self) -> typing.Optional[builtins.str]:
        '''Specifies the runtime version to use for the canary.

        For more information about runtime versions, see `Canary Runtime Versions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Library.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runtimeversion
        '''
        result = self._values.get("runtime_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.ScheduleProperty"]]:
        '''A structure that contains information about how often the canary is to run, and when these runs are to stop.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.ScheduleProperty"]], result)

    @builtins.property
    def start_canary_after_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specify TRUE to have the canary start making runs immediately after it is created.

        A canary that you create using CloudFormation can't be used to monitor the CloudFormation stack that creates the canary or to roll back that stack if there is a failure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-startcanaryaftercreation
        '''
        result = self._values.get("start_canary_after_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def success_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain data about successful runs of this canary.

        If you omit this field, the default of 31 days is used. The valid range is 1 to 455 days.

        This setting affects the range of information returned by `GetCanaryRuns <https://docs.aws.amazon.com/AmazonSynthetics/latest/APIReference/API_GetCanaryRuns.html>`_ , as well as the range of information displayed in the Synthetics console.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-successretentionperiod
        '''
        result = self._values.get("success_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of key-value pairs that are associated with the canary.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def visual_reference(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.VisualReferenceProperty"]]:
        '''
        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-visualreference
        :stability: deprecated
        '''
        result = self._values.get("visual_reference")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.VisualReferenceProperty"]], result)

    @builtins.property
    def visual_references(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.VisualReferenceProperty"]]]]:
        '''A list of visual reference configurations for the canary, one for each browser type that the canary is configured to run on.

        Visual references are used for visual monitoring comparisons.

        ``syn-nodejs-puppeteer-11.0`` and above, and ``syn-nodejs-playwright-3.0`` and above, only supports ``visualReferences`` . ``visualReference`` field is not supported.

        Versions older than ``syn-nodejs-puppeteer-11.0`` supports both ``visualReference`` and ``visualReferences`` for backward compatibility. It is recommended to use ``visualReferences`` for consistency and future compatibility.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-visualreferences
        '''
        result = self._values.get("visual_references")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.VisualReferenceProperty"]]]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.VPCConfigProperty"]]:
        '''If this canary is to test an endpoint in a VPC, this structure contains information about the subnet and security groups of the VPC endpoint.

        For more information, see `Running a Canary in a VPC <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_VPC.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.VPCConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCanaryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCanaryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnCanaryPropsMixin",
):
    '''Creates or updates a canary.

    Canaries are scripts that monitor your endpoints and APIs from the outside-in. Canaries help you check the availability and latency of your web services and troubleshoot anomalies by investigating load time data, screenshots of the UI, logs, and metrics. You can set up a canary to run continuously or just once.

    Canaries are automated scripts that run at specified intervals against an endpoint. They include Python or Node.js code to create a Lambda function. This code needs to be packaged in a certain way, depending on the language. For more information, see `Writing a canary script <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_WritingCanary.html>`_ .

    To create canaries, you must have the ``CloudWatchSyntheticsFullAccess`` policy. If you are creating a new IAM role for the canary, you also need the the ``iam:CreateRole`` , ``iam:CreatePolicy`` and ``iam:AttachRolePolicy`` permissions. For more information, see `Necessary Roles and Permissions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Roles>`_ .

    Do not include secrets or proprietary information in your canary names. The canary name makes up part of the Amazon Resource Name (ARN) for the canary, and the ARN is included in outbound calls over the internet. For more information, see `Security Considerations for Synthetics Canaries <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/servicelens_canaries_security.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html
    :cloudformationResource: AWS::Synthetics::Canary
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
        
        cfn_canary_props_mixin = synthetics_mixins.CfnCanaryPropsMixin(synthetics_mixins.CfnCanaryMixinProps(
            artifact_config=synthetics_mixins.CfnCanaryPropsMixin.ArtifactConfigProperty(
                s3_encryption=synthetics_mixins.CfnCanaryPropsMixin.S3EncryptionProperty(
                    encryption_mode="encryptionMode",
                    kms_key_arn="kmsKeyArn"
                )
            ),
            artifact_s3_location="artifactS3Location",
            browser_configs=[synthetics_mixins.CfnCanaryPropsMixin.BrowserConfigProperty(
                browser_type="browserType"
            )],
            code=synthetics_mixins.CfnCanaryPropsMixin.CodeProperty(
                blueprint_types=["blueprintTypes"],
                dependencies=[synthetics_mixins.CfnCanaryPropsMixin.DependencyProperty(
                    reference="reference",
                    type="type"
                )],
                handler="handler",
                s3_bucket="s3Bucket",
                s3_key="s3Key",
                s3_object_version="s3ObjectVersion",
                script="script",
                source_location_arn="sourceLocationArn"
            ),
            delete_lambda_resources_on_canary_deletion=False,
            dry_run_and_update=False,
            execution_role_arn="executionRoleArn",
            failure_retention_period=123,
            name="name",
            provisioned_resource_cleanup="provisionedResourceCleanup",
            resources_to_replicate_tags=["resourcesToReplicateTags"],
            run_config=synthetics_mixins.CfnCanaryPropsMixin.RunConfigProperty(
                active_tracing=False,
                environment_variables={
                    "environment_variables_key": "environmentVariables"
                },
                ephemeral_storage=123,
                memory_in_mb=123,
                timeout_in_seconds=123
            ),
            runtime_version="runtimeVersion",
            schedule=synthetics_mixins.CfnCanaryPropsMixin.ScheduleProperty(
                duration_in_seconds="durationInSeconds",
                expression="expression",
                retry_config=synthetics_mixins.CfnCanaryPropsMixin.RetryConfigProperty(
                    max_retries=123
                )
            ),
            start_canary_after_creation=False,
            success_retention_period=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            visual_reference=synthetics_mixins.CfnCanaryPropsMixin.VisualReferenceProperty(
                base_canary_run_id="baseCanaryRunId",
                base_screenshots=[synthetics_mixins.CfnCanaryPropsMixin.BaseScreenshotProperty(
                    ignore_coordinates=["ignoreCoordinates"],
                    screenshot_name="screenshotName"
                )],
                browser_type="browserType"
            ),
            visual_references=[synthetics_mixins.CfnCanaryPropsMixin.VisualReferenceProperty(
                base_canary_run_id="baseCanaryRunId",
                base_screenshots=[synthetics_mixins.CfnCanaryPropsMixin.BaseScreenshotProperty(
                    ignore_coordinates=["ignoreCoordinates"],
                    screenshot_name="screenshotName"
                )],
                browser_type="browserType"
            )],
            vpc_config=synthetics_mixins.CfnCanaryPropsMixin.VPCConfigProperty(
                ipv6_allowed_for_dual_stack=False,
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"],
                vpc_id="vpcId"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCanaryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Synthetics::Canary``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89848ff58375ae3da523b39bcfcf2f19f8f28d0fe03654bef2706837ddb4e92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2202dff3d20b488596d4d745ffd432a6f90938dba53318ca013cd94e524f85a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721765c759ee37be13763cf115af4efbab6c6ab510a7b98ce1e94fb8c012e099)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCanaryMixinProps:
        return typing.cast(CfnCanaryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnCanaryPropsMixin.ArtifactConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_encryption": "s3Encryption"},
    )
    class ArtifactConfigProperty:
        def __init__(
            self,
            *,
            s3_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCanaryPropsMixin.S3EncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure that contains the configuration for canary artifacts, including the encryption-at-rest settings for artifacts that the canary uploads to Amazon S3 .

            :param s3_encryption: A structure that contains the configuration of the encryption-at-rest settings for artifacts that the canary uploads to Amazon S3 . Artifact encryption functionality is available only for canaries that use Synthetics runtime version syn-nodejs-puppeteer-3.3 or later. For more information, see `Encrypting canary artifacts <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_artifact_encryption.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-artifactconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
                
                artifact_config_property = synthetics_mixins.CfnCanaryPropsMixin.ArtifactConfigProperty(
                    s3_encryption=synthetics_mixins.CfnCanaryPropsMixin.S3EncryptionProperty(
                        encryption_mode="encryptionMode",
                        kms_key_arn="kmsKeyArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dd56f9f1e2f6994deecbf333dcd8a1902e973b6dc700558fc26b354c449d930f)
                check_type(argname="argument s3_encryption", value=s3_encryption, expected_type=type_hints["s3_encryption"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_encryption is not None:
                self._values["s3_encryption"] = s3_encryption

        @builtins.property
        def s3_encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.S3EncryptionProperty"]]:
            '''A structure that contains the configuration of the encryption-at-rest settings for artifacts that the canary uploads to Amazon S3 .

            Artifact encryption functionality is available only for canaries that use Synthetics runtime version syn-nodejs-puppeteer-3.3 or later. For more information, see `Encrypting canary artifacts <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_artifact_encryption.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-artifactconfig.html#cfn-synthetics-canary-artifactconfig-s3encryption
            '''
            result = self._values.get("s3_encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.S3EncryptionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArtifactConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnCanaryPropsMixin.BaseScreenshotProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ignore_coordinates": "ignoreCoordinates",
            "screenshot_name": "screenshotName",
        },
    )
    class BaseScreenshotProperty:
        def __init__(
            self,
            *,
            ignore_coordinates: typing.Optional[typing.Sequence[builtins.str]] = None,
            screenshot_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure representing a screenshot that is used as a baseline during visual monitoring comparisons made by the canary.

            :param ignore_coordinates: Coordinates that define the part of a screen to ignore during screenshot comparisons. To obtain the coordinates to use here, use the CloudWatch console to draw the boundaries on the screen. For more information, see `Edit or delete a canary <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/synthetics_canaries_deletion.html>`_ .
            :param screenshot_name: The name of the screenshot. This is generated the first time the canary is run after the ``UpdateCanary`` operation that specified for this canary to perform visual monitoring.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-basescreenshot.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
                
                base_screenshot_property = synthetics_mixins.CfnCanaryPropsMixin.BaseScreenshotProperty(
                    ignore_coordinates=["ignoreCoordinates"],
                    screenshot_name="screenshotName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__41f85528d7080f9a5186982e840bcc8f32c930778fe6ad8c068e676b29df0c8d)
                check_type(argname="argument ignore_coordinates", value=ignore_coordinates, expected_type=type_hints["ignore_coordinates"])
                check_type(argname="argument screenshot_name", value=screenshot_name, expected_type=type_hints["screenshot_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ignore_coordinates is not None:
                self._values["ignore_coordinates"] = ignore_coordinates
            if screenshot_name is not None:
                self._values["screenshot_name"] = screenshot_name

        @builtins.property
        def ignore_coordinates(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Coordinates that define the part of a screen to ignore during screenshot comparisons.

            To obtain the coordinates to use here, use the CloudWatch console to draw the boundaries on the screen. For more information, see `Edit or delete a canary <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/synthetics_canaries_deletion.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-basescreenshot.html#cfn-synthetics-canary-basescreenshot-ignorecoordinates
            '''
            result = self._values.get("ignore_coordinates")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def screenshot_name(self) -> typing.Optional[builtins.str]:
            '''The name of the screenshot.

            This is generated the first time the canary is run after the ``UpdateCanary`` operation that specified for this canary to perform visual monitoring.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-basescreenshot.html#cfn-synthetics-canary-basescreenshot-screenshotname
            '''
            result = self._values.get("screenshot_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BaseScreenshotProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnCanaryPropsMixin.BrowserConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"browser_type": "browserType"},
    )
    class BrowserConfigProperty:
        def __init__(
            self,
            *,
            browser_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that specifies the browser type to use for a canary run.

            :param browser_type: The browser type associated with this browser configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-browserconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
                
                browser_config_property = synthetics_mixins.CfnCanaryPropsMixin.BrowserConfigProperty(
                    browser_type="browserType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b91ff2a49e5ea2236c846f02018e368e8c5f724b3b84677a3379ae6f52f9c6db)
                check_type(argname="argument browser_type", value=browser_type, expected_type=type_hints["browser_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if browser_type is not None:
                self._values["browser_type"] = browser_type

        @builtins.property
        def browser_type(self) -> typing.Optional[builtins.str]:
            '''The browser type associated with this browser configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-browserconfig.html#cfn-synthetics-canary-browserconfig-browsertype
            '''
            result = self._values.get("browser_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BrowserConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnCanaryPropsMixin.CodeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "blueprint_types": "blueprintTypes",
            "dependencies": "dependencies",
            "handler": "handler",
            "s3_bucket": "s3Bucket",
            "s3_key": "s3Key",
            "s3_object_version": "s3ObjectVersion",
            "script": "script",
            "source_location_arn": "sourceLocationArn",
        },
    )
    class CodeProperty:
        def __init__(
            self,
            *,
            blueprint_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            dependencies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCanaryPropsMixin.DependencyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            handler: typing.Optional[builtins.str] = None,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_key: typing.Optional[builtins.str] = None,
            s3_object_version: typing.Optional[builtins.str] = None,
            script: typing.Optional[builtins.str] = None,
            source_location_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use this structure to input your script code for the canary.

            This structure contains the Lambda handler with the location where the canary should start running the script. If the script is stored in an S3 bucket, the bucket name, key, and version are also included. If the script is passed into the canary directly, the script code is contained in the value of ``Script`` .

            :param blueprint_types: ``BlueprintTypes`` are a list of templates that enable simplified canary creation. You can create canaries for common monitoring scenarios by providing only a JSON configuration file instead of writing custom scripts. ``multi-checks`` is the only supported value. When you specify ``BlueprintTypes`` , the ``Handler`` field cannot be specified since the blueprint provides a pre-defined entry point.
            :param dependencies: List of Lambda layers to attach to the canary.
            :param handler: The entry point to use for the source code when running the canary. For canaries that use the ``syn-python-selenium-1.0`` runtime or a ``syn-nodejs.puppeteer`` runtime earlier than ``syn-nodejs.puppeteer-3.4`` , the handler must be specified as ``*fileName* .handler`` . For ``syn-python-selenium-1.1`` , ``syn-nodejs.puppeteer-3.4`` , and later runtimes, the handler can be specified as ``*fileName* . *functionName*`` , or you can specify a folder where canary scripts reside as ``*folder* / *fileName* . *functionName*`` . This field is required when you don't specify ``BlueprintTypes`` and is not allowed when you specify ``BlueprintTypes`` .
            :param s3_bucket: If your canary script is located in S3, specify the bucket name here. The bucket must already exist.
            :param s3_key: The Amazon S3 key of your script. For more information, see `Working with Amazon S3 Objects <https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingObjects.html>`_ .
            :param s3_object_version: The Amazon S3 version ID of your script.
            :param script: If you input your canary script directly into the canary instead of referring to an S3 location, the value of this parameter is the script in plain text. It can be up to 5 MB.
            :param source_location_arn: The ARN of the Lambda layer where Synthetics stores the canary script code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
                
                code_property = synthetics_mixins.CfnCanaryPropsMixin.CodeProperty(
                    blueprint_types=["blueprintTypes"],
                    dependencies=[synthetics_mixins.CfnCanaryPropsMixin.DependencyProperty(
                        reference="reference",
                        type="type"
                    )],
                    handler="handler",
                    s3_bucket="s3Bucket",
                    s3_key="s3Key",
                    s3_object_version="s3ObjectVersion",
                    script="script",
                    source_location_arn="sourceLocationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__54c5aa09e21caa97087afb4b60925f1c69729253167e5eb9f0607c2a69552a6f)
                check_type(argname="argument blueprint_types", value=blueprint_types, expected_type=type_hints["blueprint_types"])
                check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
                check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
                check_type(argname="argument s3_object_version", value=s3_object_version, expected_type=type_hints["s3_object_version"])
                check_type(argname="argument script", value=script, expected_type=type_hints["script"])
                check_type(argname="argument source_location_arn", value=source_location_arn, expected_type=type_hints["source_location_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if blueprint_types is not None:
                self._values["blueprint_types"] = blueprint_types
            if dependencies is not None:
                self._values["dependencies"] = dependencies
            if handler is not None:
                self._values["handler"] = handler
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_key is not None:
                self._values["s3_key"] = s3_key
            if s3_object_version is not None:
                self._values["s3_object_version"] = s3_object_version
            if script is not None:
                self._values["script"] = script
            if source_location_arn is not None:
                self._values["source_location_arn"] = source_location_arn

        @builtins.property
        def blueprint_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``BlueprintTypes`` are a list of templates that enable simplified canary creation.

            You can create canaries for common monitoring scenarios by providing only a JSON configuration file instead of writing custom scripts. ``multi-checks`` is the only supported value.

            When you specify ``BlueprintTypes`` , the ``Handler`` field cannot be specified since the blueprint provides a pre-defined entry point.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-blueprinttypes
            '''
            result = self._values.get("blueprint_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def dependencies(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.DependencyProperty"]]]]:
            '''List of Lambda layers to attach to the canary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-dependencies
            '''
            result = self._values.get("dependencies")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.DependencyProperty"]]]], result)

        @builtins.property
        def handler(self) -> typing.Optional[builtins.str]:
            '''The entry point to use for the source code when running the canary.

            For canaries that use the ``syn-python-selenium-1.0`` runtime or a ``syn-nodejs.puppeteer`` runtime earlier than ``syn-nodejs.puppeteer-3.4`` , the handler must be specified as ``*fileName* .handler`` . For ``syn-python-selenium-1.1`` , ``syn-nodejs.puppeteer-3.4`` , and later runtimes, the handler can be specified as ``*fileName* . *functionName*`` , or you can specify a folder where canary scripts reside as ``*folder* / *fileName* . *functionName*`` .

            This field is required when you don't specify ``BlueprintTypes`` and is not allowed when you specify ``BlueprintTypes`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-handler
            '''
            result = self._values.get("handler")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''If your canary script is located in S3, specify the bucket name here.

            The bucket must already exist.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 key of your script.

            For more information, see `Working with Amazon S3 Objects <https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingObjects.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3key
            '''
            result = self._values.get("s3_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_object_version(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 version ID of your script.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3objectversion
            '''
            result = self._values.get("s3_object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def script(self) -> typing.Optional[builtins.str]:
            '''If you input your canary script directly into the canary instead of referring to an S3 location, the value of this parameter is the script in plain text.

            It can be up to 5 MB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-script
            '''
            result = self._values.get("script")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_location_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Lambda layer where Synthetics stores the canary script code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-sourcelocationarn
            '''
            result = self._values.get("source_location_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnCanaryPropsMixin.DependencyProperty",
        jsii_struct_bases=[],
        name_mapping={"reference": "reference", "type": "type"},
    )
    class DependencyProperty:
        def __init__(
            self,
            *,
            reference: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains information about a dependency for a canary.

            :param reference: The dependency reference. For Lambda layers, this is the ARN of the Lambda layer. For more information about Lambda ARN format, see `Lambda <https://docs.aws.amazon.com/lambda/latest/api/API_Layer.html>`_ .
            :param type: The type of dependency. Valid value is ``LambdaLayer`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-dependency.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
                
                dependency_property = synthetics_mixins.CfnCanaryPropsMixin.DependencyProperty(
                    reference="reference",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c708ed943796a863f11d2d419470664cdc4209bfe6823c64f7a45ddabebd8327)
                check_type(argname="argument reference", value=reference, expected_type=type_hints["reference"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if reference is not None:
                self._values["reference"] = reference
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def reference(self) -> typing.Optional[builtins.str]:
            '''The dependency reference.

            For Lambda layers, this is the ARN of the Lambda layer. For more information about Lambda ARN format, see `Lambda <https://docs.aws.amazon.com/lambda/latest/api/API_Layer.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-dependency.html#cfn-synthetics-canary-dependency-reference
            '''
            result = self._values.get("reference")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of dependency.

            Valid value is ``LambdaLayer`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-dependency.html#cfn-synthetics-canary-dependency-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DependencyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnCanaryPropsMixin.RetryConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"max_retries": "maxRetries"},
    )
    class RetryConfigProperty:
        def __init__(self, *, max_retries: typing.Optional[jsii.Number] = None) -> None:
            '''The canary's retry configuration information.

            :param max_retries: The maximum number of retries. The value must be less than or equal to two.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-retryconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
                
                retry_config_property = synthetics_mixins.CfnCanaryPropsMixin.RetryConfigProperty(
                    max_retries=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be3f0b216530311e6a17cbd48757de6dad3a33033c63cfe5ce7f4f0b86563e40)
                check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_retries is not None:
                self._values["max_retries"] = max_retries

        @builtins.property
        def max_retries(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of retries.

            The value must be less than or equal to two.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-retryconfig.html#cfn-synthetics-canary-retryconfig-maxretries
            '''
            result = self._values.get("max_retries")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetryConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnCanaryPropsMixin.RunConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "active_tracing": "activeTracing",
            "environment_variables": "environmentVariables",
            "ephemeral_storage": "ephemeralStorage",
            "memory_in_mb": "memoryInMb",
            "timeout_in_seconds": "timeoutInSeconds",
        },
    )
    class RunConfigProperty:
        def __init__(
            self,
            *,
            active_tracing: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            environment_variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            ephemeral_storage: typing.Optional[jsii.Number] = None,
            memory_in_mb: typing.Optional[jsii.Number] = None,
            timeout_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A structure that contains input information for a canary run.

            This structure is required.

            :param active_tracing: Specifies whether this canary is to use active AWS X-Ray tracing when it runs. Active tracing enables this canary run to be displayed in the ServiceLens and X-Ray service maps even if the canary does not hit an endpoint that has X-Ray tracing enabled. Using X-Ray tracing incurs charges. For more information, see `Canaries and X-Ray tracing <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_tracing.html>`_ . You can enable active tracing only for canaries that use version ``syn-nodejs-2.0`` or later for their canary runtime.
            :param environment_variables: Specifies the keys and values to use for any environment variables used in the canary script. Use the following format: { "key1" : "value1", "key2" : "value2", ...} Keys must start with a letter and be at least two characters. The total size of your environment variables cannot exceed 4 KB. You can't specify any Lambda reserved environment variables as the keys for your environment variables. For more information about reserved keys, see `Runtime environment variables <https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-runtime>`_ .
            :param ephemeral_storage: Specifies the amount of ephemeral storage (in MB) to allocate for the canary run during execution. This temporary storage is used for storing canary run artifacts (which are uploaded to an Amazon S3 bucket at the end of the run), and any canary browser operations. This temporary storage is cleared after the run is completed. Default storage value is 1024 MB.
            :param memory_in_mb: The maximum amount of memory that the canary can use while running. This value must be a multiple of 64. The range is 960 to 3008.
            :param timeout_in_seconds: How long the canary is allowed to run before it must stop. You can't set this time to be longer than the frequency of the runs of this canary. If you omit this field, the frequency of the canary is used as this value, up to a maximum of 900 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
                
                run_config_property = synthetics_mixins.CfnCanaryPropsMixin.RunConfigProperty(
                    active_tracing=False,
                    environment_variables={
                        "environment_variables_key": "environmentVariables"
                    },
                    ephemeral_storage=123,
                    memory_in_mb=123,
                    timeout_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7cc2dba13ed1744348e3a2f0f973b3ff3dcd132972192813771e9c51273b352b)
                check_type(argname="argument active_tracing", value=active_tracing, expected_type=type_hints["active_tracing"])
                check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
                check_type(argname="argument ephemeral_storage", value=ephemeral_storage, expected_type=type_hints["ephemeral_storage"])
                check_type(argname="argument memory_in_mb", value=memory_in_mb, expected_type=type_hints["memory_in_mb"])
                check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if active_tracing is not None:
                self._values["active_tracing"] = active_tracing
            if environment_variables is not None:
                self._values["environment_variables"] = environment_variables
            if ephemeral_storage is not None:
                self._values["ephemeral_storage"] = ephemeral_storage
            if memory_in_mb is not None:
                self._values["memory_in_mb"] = memory_in_mb
            if timeout_in_seconds is not None:
                self._values["timeout_in_seconds"] = timeout_in_seconds

        @builtins.property
        def active_tracing(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether this canary is to use active AWS X-Ray tracing when it runs.

            Active tracing enables this canary run to be displayed in the ServiceLens and X-Ray service maps even if the canary does not hit an endpoint that has X-Ray tracing enabled. Using X-Ray tracing incurs charges. For more information, see `Canaries and X-Ray tracing <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_tracing.html>`_ .

            You can enable active tracing only for canaries that use version ``syn-nodejs-2.0`` or later for their canary runtime.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-activetracing
            '''
            result = self._values.get("active_tracing")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def environment_variables(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies the keys and values to use for any environment variables used in the canary script.

            Use the following format:

            { "key1" : "value1", "key2" : "value2", ...}

            Keys must start with a letter and be at least two characters. The total size of your environment variables cannot exceed 4 KB. You can't specify any Lambda reserved environment variables as the keys for your environment variables. For more information about reserved keys, see `Runtime environment variables <https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-runtime>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-environmentvariables
            '''
            result = self._values.get("environment_variables")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ephemeral_storage(self) -> typing.Optional[jsii.Number]:
            '''Specifies the amount of ephemeral storage (in MB) to allocate for the canary run during execution.

            This temporary storage is used for storing canary run artifacts (which are uploaded to an Amazon S3 bucket at the end of the run), and any canary browser operations. This temporary storage is cleared after the run is completed. Default storage value is 1024 MB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-ephemeralstorage
            '''
            result = self._values.get("ephemeral_storage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def memory_in_mb(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of memory that the canary can use while running.

            This value must be a multiple of 64. The range is 960 to 3008.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-memoryinmb
            '''
            result = self._values.get("memory_in_mb")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''How long the canary is allowed to run before it must stop.

            You can't set this time to be longer than the frequency of the runs of this canary.

            If you omit this field, the frequency of the canary is used as this value, up to a maximum of 900 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnCanaryPropsMixin.S3EncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_mode": "encryptionMode", "kms_key_arn": "kmsKeyArn"},
    )
    class S3EncryptionProperty:
        def __init__(
            self,
            *,
            encryption_mode: typing.Optional[builtins.str] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains the configuration of the encryption-at-rest settings for artifacts that the canary uploads to Amazon S3 .

            Artifact encryption functionality is available only for canaries that use Synthetics runtime version syn-nodejs-puppeteer-3.3 or later. For more information, see `Encrypting canary artifacts <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_artifact_encryption.html>`_ .

            :param encryption_mode: The encryption method to use for artifacts created by this canary. Specify ``SSE_S3`` to use server-side encryption (SSE) with an Amazon S3-managed key. Specify ``SSE-KMS`` to use server-side encryption with a customer-managed AWS key. If you omit this parameter, an AWS -managed AWS key is used.
            :param kms_key_arn: The ARN of the customer-managed AWS key to use, if you specify ``SSE-KMS`` for ``EncryptionMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-s3encryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
                
                s3_encryption_property = synthetics_mixins.CfnCanaryPropsMixin.S3EncryptionProperty(
                    encryption_mode="encryptionMode",
                    kms_key_arn="kmsKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f574b28e0967ac0e21764dbbbc6975aa820f0cab4defa6bf002769928ca89d0a)
                check_type(argname="argument encryption_mode", value=encryption_mode, expected_type=type_hints["encryption_mode"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_mode is not None:
                self._values["encryption_mode"] = encryption_mode
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def encryption_mode(self) -> typing.Optional[builtins.str]:
            '''The encryption method to use for artifacts created by this canary.

            Specify ``SSE_S3`` to use server-side encryption (SSE) with an Amazon S3-managed key. Specify ``SSE-KMS`` to use server-side encryption with a customer-managed AWS  key.

            If you omit this parameter, an AWS -managed AWS  key is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-s3encryption.html#cfn-synthetics-canary-s3encryption-encryptionmode
            '''
            result = self._values.get("encryption_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the customer-managed AWS  key to use, if you specify ``SSE-KMS`` for ``EncryptionMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-s3encryption.html#cfn-synthetics-canary-s3encryption-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3EncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnCanaryPropsMixin.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "duration_in_seconds": "durationInSeconds",
            "expression": "expression",
            "retry_config": "retryConfig",
        },
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            duration_in_seconds: typing.Optional[builtins.str] = None,
            expression: typing.Optional[builtins.str] = None,
            retry_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCanaryPropsMixin.RetryConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This structure specifies how often a canary is to make runs and the date and time when it should stop making runs.

            :param duration_in_seconds: How long, in seconds, for the canary to continue making regular runs according to the schedule in the ``Expression`` value. If you specify 0, the canary continues making runs until you stop it. If you omit this field, the default of 0 is used.
            :param expression: A ``rate`` expression or a ``cron`` expression that defines how often the canary is to run. For a rate expression, The syntax is ``rate( *number unit* )`` . *unit* can be ``minute`` , ``minutes`` , or ``hour`` . For example, ``rate(1 minute)`` runs the canary once a minute, ``rate(10 minutes)`` runs it once every 10 minutes, and ``rate(1 hour)`` runs it once every hour. You can specify a frequency between ``rate(1 minute)`` and ``rate(1 hour)`` . Specifying ``rate(0 minute)`` or ``rate(0 hour)`` is a special value that causes the canary to run only once when it is started. Use ``cron( *expression* )`` to specify a cron expression. You can't schedule a canary to wait for more than a year before running. For information about the syntax for cron expressions, see `Scheduling canary runs using cron <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_cron.html>`_ .
            :param retry_config: The canary's retry configuration information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
                
                schedule_property = synthetics_mixins.CfnCanaryPropsMixin.ScheduleProperty(
                    duration_in_seconds="durationInSeconds",
                    expression="expression",
                    retry_config=synthetics_mixins.CfnCanaryPropsMixin.RetryConfigProperty(
                        max_retries=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a2ebc1387ac50805a5d502f23cd4a0991078289f562a86667d56d0e3c95efba)
                check_type(argname="argument duration_in_seconds", value=duration_in_seconds, expected_type=type_hints["duration_in_seconds"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument retry_config", value=retry_config, expected_type=type_hints["retry_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds
            if expression is not None:
                self._values["expression"] = expression
            if retry_config is not None:
                self._values["retry_config"] = retry_config

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[builtins.str]:
            '''How long, in seconds, for the canary to continue making regular runs according to the schedule in the ``Expression`` value.

            If you specify 0, the canary continues making runs until you stop it. If you omit this field, the default of 0 is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html#cfn-synthetics-canary-schedule-durationinseconds
            '''
            result = self._values.get("duration_in_seconds")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''A ``rate`` expression or a ``cron`` expression that defines how often the canary is to run.

            For a rate expression, The syntax is ``rate( *number unit* )`` . *unit* can be ``minute`` , ``minutes`` , or ``hour`` .

            For example, ``rate(1 minute)`` runs the canary once a minute, ``rate(10 minutes)`` runs it once every 10 minutes, and ``rate(1 hour)`` runs it once every hour. You can specify a frequency between ``rate(1 minute)`` and ``rate(1 hour)`` .

            Specifying ``rate(0 minute)`` or ``rate(0 hour)`` is a special value that causes the canary to run only once when it is started.

            Use ``cron( *expression* )`` to specify a cron expression. You can't schedule a canary to wait for more than a year before running. For information about the syntax for cron expressions, see `Scheduling canary runs using cron <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_cron.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html#cfn-synthetics-canary-schedule-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retry_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.RetryConfigProperty"]]:
            '''The canary's retry configuration information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html#cfn-synthetics-canary-schedule-retryconfig
            '''
            result = self._values.get("retry_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.RetryConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnCanaryPropsMixin.VPCConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ipv6_allowed_for_dual_stack": "ipv6AllowedForDualStack",
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
            "vpc_id": "vpcId",
        },
    )
    class VPCConfigProperty:
        def __init__(
            self,
            *,
            ipv6_allowed_for_dual_stack: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''If this canary is to test an endpoint in a VPC, this structure contains information about the subnet and security groups of the VPC endpoint.

            For more information, see `Running a Canary in a VPC <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_VPC.html>`_ .

            :param ipv6_allowed_for_dual_stack: Set this to ``true`` to allow outbound IPv6 traffic on VPC canaries that are connected to dual-stack subnets. The default is ``false`` .
            :param security_group_ids: The IDs of the security groups for this canary.
            :param subnet_ids: The IDs of the subnets where this canary is to run.
            :param vpc_id: The ID of the VPC where this canary is to run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
                
                v_pCConfig_property = synthetics_mixins.CfnCanaryPropsMixin.VPCConfigProperty(
                    ipv6_allowed_for_dual_stack=False,
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"],
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a94b89dc6a90d1239b294dfcd5d86ad457f876c18ad2b6b0ba5a4fb93dcb99d0)
                check_type(argname="argument ipv6_allowed_for_dual_stack", value=ipv6_allowed_for_dual_stack, expected_type=type_hints["ipv6_allowed_for_dual_stack"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ipv6_allowed_for_dual_stack is not None:
                self._values["ipv6_allowed_for_dual_stack"] = ipv6_allowed_for_dual_stack
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def ipv6_allowed_for_dual_stack(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this to ``true`` to allow outbound IPv6 traffic on VPC canaries that are connected to dual-stack subnets.

            The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-ipv6allowedfordualstack
            '''
            result = self._values.get("ipv6_allowed_for_dual_stack")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IDs of the security groups for this canary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IDs of the subnets where this canary is to run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the VPC where this canary is to run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VPCConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnCanaryPropsMixin.VisualReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base_canary_run_id": "baseCanaryRunId",
            "base_screenshots": "baseScreenshots",
            "browser_type": "browserType",
        },
    )
    class VisualReferenceProperty:
        def __init__(
            self,
            *,
            base_canary_run_id: typing.Optional[builtins.str] = None,
            base_screenshots: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCanaryPropsMixin.BaseScreenshotProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            browser_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines the screenshots to use as the baseline for comparisons during visual monitoring comparisons during future runs of this canary.

            If you omit this parameter, no changes are made to any baseline screenshots that the canary might be using already.

            Visual monitoring is supported only on canaries running the *syn-puppeteer-node-3.2* runtime or later. For more information, see `Visual monitoring <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_SyntheticsLogger_VisualTesting.html>`_ and `Visual monitoring blueprint <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Blueprints_VisualTesting.html>`_

            :param base_canary_run_id: Specifies which canary run to use the screenshots from as the baseline for future visual monitoring with this canary. Valid values are ``nextrun`` to use the screenshots from the next run after this update is made, ``lastrun`` to use the screenshots from the most recent run before this update was made, or the value of ``Id`` in the `CanaryRun <https://docs.aws.amazon.com/AmazonSynthetics/latest/APIReference/API_CanaryRun.html>`_ from any past run of this canary.
            :param base_screenshots: An array of screenshots that are used as the baseline for comparisons during visual monitoring.
            :param browser_type: The browser type associated with this visual reference configuration. Valid values are ``CHROME`` and ``FIREFOX`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-visualreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
                
                visual_reference_property = synthetics_mixins.CfnCanaryPropsMixin.VisualReferenceProperty(
                    base_canary_run_id="baseCanaryRunId",
                    base_screenshots=[synthetics_mixins.CfnCanaryPropsMixin.BaseScreenshotProperty(
                        ignore_coordinates=["ignoreCoordinates"],
                        screenshot_name="screenshotName"
                    )],
                    browser_type="browserType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e0c859137aab4678dd775814155cfee730a37756215c7f4b3e0d957db57d25e5)
                check_type(argname="argument base_canary_run_id", value=base_canary_run_id, expected_type=type_hints["base_canary_run_id"])
                check_type(argname="argument base_screenshots", value=base_screenshots, expected_type=type_hints["base_screenshots"])
                check_type(argname="argument browser_type", value=browser_type, expected_type=type_hints["browser_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base_canary_run_id is not None:
                self._values["base_canary_run_id"] = base_canary_run_id
            if base_screenshots is not None:
                self._values["base_screenshots"] = base_screenshots
            if browser_type is not None:
                self._values["browser_type"] = browser_type

        @builtins.property
        def base_canary_run_id(self) -> typing.Optional[builtins.str]:
            '''Specifies which canary run to use the screenshots from as the baseline for future visual monitoring with this canary.

            Valid values are ``nextrun`` to use the screenshots from the next run after this update is made, ``lastrun`` to use the screenshots from the most recent run before this update was made, or the value of ``Id`` in the `CanaryRun <https://docs.aws.amazon.com/AmazonSynthetics/latest/APIReference/API_CanaryRun.html>`_ from any past run of this canary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-visualreference.html#cfn-synthetics-canary-visualreference-basecanaryrunid
            '''
            result = self._values.get("base_canary_run_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def base_screenshots(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.BaseScreenshotProperty"]]]]:
            '''An array of screenshots that are used as the baseline for comparisons during visual monitoring.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-visualreference.html#cfn-synthetics-canary-visualreference-basescreenshots
            '''
            result = self._values.get("base_screenshots")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCanaryPropsMixin.BaseScreenshotProperty"]]]], result)

        @builtins.property
        def browser_type(self) -> typing.Optional[builtins.str]:
            '''The browser type associated with this visual reference configuration.

            Valid values are ``CHROME`` and ``FIREFOX`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-visualreference.html#cfn-synthetics-canary-visualreference-browsertype
            '''
            result = self._values.get("browser_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VisualReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "resource_arns": "resourceArns", "tags": "tags"},
)
class CfnGroupMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnGroupPropsMixin.

        :param name: A name for the group. It can include any Unicode characters. The names for all groups in your account, across all Regions, must be unique.
        :param resource_arns: The ARNs of the canaries that you want to associate with this group.
        :param tags: The list of key-value pairs that are associated with the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
            
            cfn_group_mixin_props = synthetics_mixins.CfnGroupMixinProps(
                name="name",
                resource_arns=["resourceArns"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2fd7a450e2055b28604a076989dd5ddd10898ef23f55a652b1ed8bfe36873a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if resource_arns is not None:
            self._values["resource_arns"] = resource_arns
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the group. It can include any Unicode characters.

        The names for all groups in your account, across all Regions, must be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-group.html#cfn-synthetics-group-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs of the canaries that you want to associate with this group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-group.html#cfn-synthetics-group-resourcearns
        '''
        result = self._values.get("resource_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of key-value pairs that are associated with the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-group.html#cfn-synthetics-group-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_synthetics.mixins.CfnGroupPropsMixin",
):
    '''Creates or updates a group which you can use to associate canaries with each other, including cross-Region canaries.

    Using groups can help you with managing and automating your canaries, and you can also view aggregated run results and statistics for all canaries in a group.

    Groups are global resources. When you create a group, it is replicated across all AWS Regions, and you can add canaries from any Region to it, and view it in any Region. Although the group ARN format reflects the Region name where it was created, a group is not constrained to any Region. This means that you can put canaries from multiple Regions into the same group, and then use that group to view and manage all of those canaries in a single view.

    Each group can contain as many as 10 canaries. You can have as many as 20 groups in your account. Any single canary can be a member of up to 10 groups.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-group.html
    :cloudformationResource: AWS::Synthetics::Group
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_synthetics import mixins as synthetics_mixins
        
        cfn_group_props_mixin = synthetics_mixins.CfnGroupPropsMixin(synthetics_mixins.CfnGroupMixinProps(
            name="name",
            resource_arns=["resourceArns"],
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
        props: typing.Union[CfnGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Synthetics::Group``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be23518a60e69749608b17d7f68b044248acf184c5a0b4104f944baeb4002131)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1de0cef3532cdce9e95c6831203d2b13f7e0f2c37038e81aa58b1da5df10a5a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01d95fb99947bd42df6a74dbf54624563e65fd464fb699518dce03f765545159)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGroupMixinProps:
        return typing.cast(CfnGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnCanaryMixinProps",
    "CfnCanaryPropsMixin",
    "CfnGroupMixinProps",
    "CfnGroupPropsMixin",
]

publication.publish()

def _typecheckingstub__ab3e2359ab3e4871bd5a046c76d4c4fd03e4b53c80b90a1cdb06f75afcf36ec6(
    *,
    artifact_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCanaryPropsMixin.ArtifactConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    artifact_s3_location: typing.Optional[builtins.str] = None,
    browser_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCanaryPropsMixin.BrowserConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    code: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCanaryPropsMixin.CodeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    delete_lambda_resources_on_canary_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    dry_run_and_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    failure_retention_period: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    provisioned_resource_cleanup: typing.Optional[builtins.str] = None,
    resources_to_replicate_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    run_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCanaryPropsMixin.RunConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    runtime_version: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCanaryPropsMixin.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    start_canary_after_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    success_retention_period: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    visual_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCanaryPropsMixin.VisualReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    visual_references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCanaryPropsMixin.VisualReferenceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCanaryPropsMixin.VPCConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89848ff58375ae3da523b39bcfcf2f19f8f28d0fe03654bef2706837ddb4e92(
    props: typing.Union[CfnCanaryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2202dff3d20b488596d4d745ffd432a6f90938dba53318ca013cd94e524f85a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721765c759ee37be13763cf115af4efbab6c6ab510a7b98ce1e94fb8c012e099(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd56f9f1e2f6994deecbf333dcd8a1902e973b6dc700558fc26b354c449d930f(
    *,
    s3_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCanaryPropsMixin.S3EncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f85528d7080f9a5186982e840bcc8f32c930778fe6ad8c068e676b29df0c8d(
    *,
    ignore_coordinates: typing.Optional[typing.Sequence[builtins.str]] = None,
    screenshot_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91ff2a49e5ea2236c846f02018e368e8c5f724b3b84677a3379ae6f52f9c6db(
    *,
    browser_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c5aa09e21caa97087afb4b60925f1c69729253167e5eb9f0607c2a69552a6f(
    *,
    blueprint_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    dependencies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCanaryPropsMixin.DependencyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    handler: typing.Optional[builtins.str] = None,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_key: typing.Optional[builtins.str] = None,
    s3_object_version: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
    source_location_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c708ed943796a863f11d2d419470664cdc4209bfe6823c64f7a45ddabebd8327(
    *,
    reference: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3f0b216530311e6a17cbd48757de6dad3a33033c63cfe5ce7f4f0b86563e40(
    *,
    max_retries: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc2dba13ed1744348e3a2f0f973b3ff3dcd132972192813771e9c51273b352b(
    *,
    active_tracing: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    environment_variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    ephemeral_storage: typing.Optional[jsii.Number] = None,
    memory_in_mb: typing.Optional[jsii.Number] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f574b28e0967ac0e21764dbbbc6975aa820f0cab4defa6bf002769928ca89d0a(
    *,
    encryption_mode: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2ebc1387ac50805a5d502f23cd4a0991078289f562a86667d56d0e3c95efba(
    *,
    duration_in_seconds: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    retry_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCanaryPropsMixin.RetryConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94b89dc6a90d1239b294dfcd5d86ad457f876c18ad2b6b0ba5a4fb93dcb99d0(
    *,
    ipv6_allowed_for_dual_stack: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0c859137aab4678dd775814155cfee730a37756215c7f4b3e0d957db57d25e5(
    *,
    base_canary_run_id: typing.Optional[builtins.str] = None,
    base_screenshots: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCanaryPropsMixin.BaseScreenshotProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    browser_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2fd7a450e2055b28604a076989dd5ddd10898ef23f55a652b1ed8bfe36873a(
    *,
    name: typing.Optional[builtins.str] = None,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be23518a60e69749608b17d7f68b044248acf184c5a0b4104f944baeb4002131(
    props: typing.Union[CfnGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1de0cef3532cdce9e95c6831203d2b13f7e0f2c37038e81aa58b1da5df10a5a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01d95fb99947bd42df6a74dbf54624563e65fd464fb699518dce03f765545159(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
