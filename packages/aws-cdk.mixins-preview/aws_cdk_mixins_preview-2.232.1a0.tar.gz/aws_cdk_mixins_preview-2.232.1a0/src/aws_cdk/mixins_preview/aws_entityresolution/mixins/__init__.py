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
class CfnIdMappingWorkflowLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdMappingWorkflowLogsMixin",
):
    '''Creates an ``IdMappingWorkflow`` object which stores the configuration of the data processing job to be run.

    Each ``IdMappingWorkflow`` must have a unique workflow name. To modify an existing workflow, use the UpdateIdMappingWorkflow API.
    .. epigraph::

       Incremental processing is not supported for ID mapping workflows.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idmappingworkflow.html
    :cloudformationResource: AWS::EntityResolution::IdMappingWorkflow
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_id_mapping_workflow_logs_mixin = entityresolution_mixins.CfnIdMappingWorkflowLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::EntityResolution::IdMappingWorkflow``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8319c797870fa92349f44077970fe8648468e2795b9542d5ca9411c4ed149e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d87cdbf6f8b09b8206a9ba5b3013799b7cf869f2fa739acaf9ee868341cf8c4)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e558b8ce6c2ccef5e30fb2c16ebf9979785916fa1ff01f6dcec2603fb764fba8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WORKFLOW_LOGS")
    def WORKFLOW_LOGS(cls) -> "CfnIdMappingWorkflowWorkflowLogs":
        return typing.cast("CfnIdMappingWorkflowWorkflowLogs", jsii.sget(cls, "WORKFLOW_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdMappingWorkflowMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "id_mapping_incremental_run_config": "idMappingIncrementalRunConfig",
        "id_mapping_techniques": "idMappingTechniques",
        "input_source_config": "inputSourceConfig",
        "output_source_config": "outputSourceConfig",
        "role_arn": "roleArn",
        "tags": "tags",
        "workflow_name": "workflowName",
    },
)
class CfnIdMappingWorkflowMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        id_mapping_incremental_run_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdMappingWorkflowPropsMixin.IdMappingIncrementalRunConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        id_mapping_techniques: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdMappingWorkflowPropsMixin.IdMappingTechniquesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        input_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowInputSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        output_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowOutputSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnIdMappingWorkflowPropsMixin.

        :param description: A description of the workflow.
        :param id_mapping_incremental_run_config: 
        :param id_mapping_techniques: An object which defines the ID mapping technique and any additional configurations.
        :param input_source_config: A list of ``InputSource`` objects, which have the fields ``InputSourceARN`` and ``SchemaName`` .
        :param output_source_config: A list of ``IdMappingWorkflowOutputSource`` objects, each of which contains fields ``outputS3Path`` and ``KMSArn`` .
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role. AWS Entity Resolution assumes this role to create resources on your behalf as part of workflow execution.
        :param tags: The tags used to organize, track, or control access for this resource.
        :param workflow_name: The name of the workflow. There can't be multiple ``IdMappingWorkflows`` with the same name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idmappingworkflow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
            
            cfn_id_mapping_workflow_mixin_props = entityresolution_mixins.CfnIdMappingWorkflowMixinProps(
                description="description",
                id_mapping_incremental_run_config=entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingIncrementalRunConfigProperty(
                    incremental_run_type="incrementalRunType"
                ),
                id_mapping_techniques=entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingTechniquesProperty(
                    id_mapping_type="idMappingType",
                    normalization_version="normalizationVersion",
                    provider_properties=entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.ProviderPropertiesProperty(
                        intermediate_source_configuration=entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IntermediateSourceConfigurationProperty(
                            intermediate_s3_path="intermediateS3Path"
                        ),
                        provider_configuration={
                            "provider_configuration_key": "providerConfiguration"
                        },
                        provider_service_arn="providerServiceArn"
                    ),
                    rule_based_properties=entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingRuleBasedPropertiesProperty(
                        attribute_matching_model="attributeMatchingModel",
                        record_matching_model="recordMatchingModel",
                        rule_definition_type="ruleDefinitionType",
                        rules=[entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.RuleProperty(
                            matching_keys=["matchingKeys"],
                            rule_name="ruleName"
                        )]
                    )
                ),
                input_source_config=[entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowInputSourceProperty(
                    input_source_arn="inputSourceArn",
                    schema_arn="schemaArn",
                    type="type"
                )],
                output_source_config=[entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowOutputSourceProperty(
                    kms_arn="kmsArn",
                    output_s3_path="outputS3Path"
                )],
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                workflow_name="workflowName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872ed9683a8c0f8dfb03136eed0491f63b743e00a9a2867b87c763d0ae9d28da)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id_mapping_incremental_run_config", value=id_mapping_incremental_run_config, expected_type=type_hints["id_mapping_incremental_run_config"])
            check_type(argname="argument id_mapping_techniques", value=id_mapping_techniques, expected_type=type_hints["id_mapping_techniques"])
            check_type(argname="argument input_source_config", value=input_source_config, expected_type=type_hints["input_source_config"])
            check_type(argname="argument output_source_config", value=output_source_config, expected_type=type_hints["output_source_config"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workflow_name", value=workflow_name, expected_type=type_hints["workflow_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if id_mapping_incremental_run_config is not None:
            self._values["id_mapping_incremental_run_config"] = id_mapping_incremental_run_config
        if id_mapping_techniques is not None:
            self._values["id_mapping_techniques"] = id_mapping_techniques
        if input_source_config is not None:
            self._values["input_source_config"] = input_source_config
        if output_source_config is not None:
            self._values["output_source_config"] = output_source_config
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags
        if workflow_name is not None:
            self._values["workflow_name"] = workflow_name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idmappingworkflow.html#cfn-entityresolution-idmappingworkflow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id_mapping_incremental_run_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.IdMappingIncrementalRunConfigProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idmappingworkflow.html#cfn-entityresolution-idmappingworkflow-idmappingincrementalrunconfig
        '''
        result = self._values.get("id_mapping_incremental_run_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.IdMappingIncrementalRunConfigProperty"]], result)

    @builtins.property
    def id_mapping_techniques(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.IdMappingTechniquesProperty"]]:
        '''An object which defines the ID mapping technique and any additional configurations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idmappingworkflow.html#cfn-entityresolution-idmappingworkflow-idmappingtechniques
        '''
        result = self._values.get("id_mapping_techniques")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.IdMappingTechniquesProperty"]], result)

    @builtins.property
    def input_source_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowInputSourceProperty"]]]]:
        '''A list of ``InputSource`` objects, which have the fields ``InputSourceARN`` and ``SchemaName`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idmappingworkflow.html#cfn-entityresolution-idmappingworkflow-inputsourceconfig
        '''
        result = self._values.get("input_source_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowInputSourceProperty"]]]], result)

    @builtins.property
    def output_source_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowOutputSourceProperty"]]]]:
        '''A list of ``IdMappingWorkflowOutputSource`` objects, each of which contains fields ``outputS3Path`` and ``KMSArn`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idmappingworkflow.html#cfn-entityresolution-idmappingworkflow-outputsourceconfig
        '''
        result = self._values.get("output_source_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowOutputSourceProperty"]]]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role.

        AWS Entity Resolution assumes this role to create resources on your behalf as part of workflow execution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idmappingworkflow.html#cfn-entityresolution-idmappingworkflow-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idmappingworkflow.html#cfn-entityresolution-idmappingworkflow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def workflow_name(self) -> typing.Optional[builtins.str]:
        '''The name of the workflow.

        There can't be multiple ``IdMappingWorkflows`` with the same name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idmappingworkflow.html#cfn-entityresolution-idmappingworkflow-workflowname
        '''
        result = self._values.get("workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIdMappingWorkflowMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIdMappingWorkflowPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdMappingWorkflowPropsMixin",
):
    '''Creates an ``IdMappingWorkflow`` object which stores the configuration of the data processing job to be run.

    Each ``IdMappingWorkflow`` must have a unique workflow name. To modify an existing workflow, use the UpdateIdMappingWorkflow API.
    .. epigraph::

       Incremental processing is not supported for ID mapping workflows.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idmappingworkflow.html
    :cloudformationResource: AWS::EntityResolution::IdMappingWorkflow
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
        
        cfn_id_mapping_workflow_props_mixin = entityresolution_mixins.CfnIdMappingWorkflowPropsMixin(entityresolution_mixins.CfnIdMappingWorkflowMixinProps(
            description="description",
            id_mapping_incremental_run_config=entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingIncrementalRunConfigProperty(
                incremental_run_type="incrementalRunType"
            ),
            id_mapping_techniques=entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingTechniquesProperty(
                id_mapping_type="idMappingType",
                normalization_version="normalizationVersion",
                provider_properties=entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.ProviderPropertiesProperty(
                    intermediate_source_configuration=entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IntermediateSourceConfigurationProperty(
                        intermediate_s3_path="intermediateS3Path"
                    ),
                    provider_configuration={
                        "provider_configuration_key": "providerConfiguration"
                    },
                    provider_service_arn="providerServiceArn"
                ),
                rule_based_properties=entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingRuleBasedPropertiesProperty(
                    attribute_matching_model="attributeMatchingModel",
                    record_matching_model="recordMatchingModel",
                    rule_definition_type="ruleDefinitionType",
                    rules=[entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.RuleProperty(
                        matching_keys=["matchingKeys"],
                        rule_name="ruleName"
                    )]
                )
            ),
            input_source_config=[entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowInputSourceProperty(
                input_source_arn="inputSourceArn",
                schema_arn="schemaArn",
                type="type"
            )],
            output_source_config=[entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowOutputSourceProperty(
                kms_arn="kmsArn",
                output_s3_path="outputS3Path"
            )],
            role_arn="roleArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            workflow_name="workflowName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIdMappingWorkflowMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EntityResolution::IdMappingWorkflow``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92fc2fd00dfb7dad77ea27b98e6573256f20953223aa1e8fa8b47fa16ee03b22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e78a282d047c939676e0eb7a1f9a0377c7cac23ec5311f3294a483df2dfb786)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62b286c89e09ad929ae34cfc5c5b319b58f4b2f395e64678141d86df3777c67)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIdMappingWorkflowMixinProps:
        return typing.cast(CfnIdMappingWorkflowMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdMappingWorkflowPropsMixin.IdMappingIncrementalRunConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"incremental_run_type": "incrementalRunType"},
    )
    class IdMappingIncrementalRunConfigProperty:
        def __init__(
            self,
            *,
            incremental_run_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param incremental_run_type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingincrementalrunconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                id_mapping_incremental_run_config_property = entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingIncrementalRunConfigProperty(
                    incremental_run_type="incrementalRunType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6f60850a287041aeea15ce3a5492dfd44c4934c5036750a4efa25e4946d38002)
                check_type(argname="argument incremental_run_type", value=incremental_run_type, expected_type=type_hints["incremental_run_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if incremental_run_type is not None:
                self._values["incremental_run_type"] = incremental_run_type

        @builtins.property
        def incremental_run_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingincrementalrunconfig.html#cfn-entityresolution-idmappingworkflow-idmappingincrementalrunconfig-incrementalruntype
            '''
            result = self._values.get("incremental_run_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdMappingIncrementalRunConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdMappingWorkflowPropsMixin.IdMappingRuleBasedPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_matching_model": "attributeMatchingModel",
            "record_matching_model": "recordMatchingModel",
            "rule_definition_type": "ruleDefinitionType",
            "rules": "rules",
        },
    )
    class IdMappingRuleBasedPropertiesProperty:
        def __init__(
            self,
            *,
            attribute_matching_model: typing.Optional[builtins.str] = None,
            record_matching_model: typing.Optional[builtins.str] = None,
            rule_definition_type: typing.Optional[builtins.str] = None,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdMappingWorkflowPropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An object that defines the list of matching rules to run in an ID mapping workflow.

            :param attribute_matching_model: The comparison type. You can either choose ``ONE_TO_ONE`` or ``MANY_TO_MANY`` as the ``attributeMatchingModel`` . If you choose ``ONE_TO_ONE`` , the system can only match attributes if the sub-types are an exact match. For example, for the ``Email`` attribute type, the system will only consider it a match if the value of the ``Email`` field of Profile A matches the value of the ``Email`` field of Profile B. If you choose ``MANY_TO_MANY`` , the system can match attributes across the sub-types of an attribute type. For example, if the value of the ``Email`` field of Profile A matches the value of the ``BusinessEmail`` field of Profile B, the two profiles are matched on the ``Email`` attribute type.
            :param record_matching_model: The type of matching record that is allowed to be used in an ID mapping workflow. If the value is set to ``ONE_SOURCE_TO_ONE_TARGET`` , only one record in the source can be matched to the same record in the target. If the value is set to ``MANY_SOURCE_TO_ONE_TARGET`` , multiple records in the source can be matched to one record in the target.
            :param rule_definition_type: The set of rules you can use in an ID mapping workflow. The limitations specified for the source or target to define the match rules must be compatible.
            :param rules: The rules that can be used for ID mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingrulebasedproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                id_mapping_rule_based_properties_property = entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingRuleBasedPropertiesProperty(
                    attribute_matching_model="attributeMatchingModel",
                    record_matching_model="recordMatchingModel",
                    rule_definition_type="ruleDefinitionType",
                    rules=[entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.RuleProperty(
                        matching_keys=["matchingKeys"],
                        rule_name="ruleName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0086ada6ae07164de9c0264b0d94bad50ebf16f356a841bcd825f0f67d774630)
                check_type(argname="argument attribute_matching_model", value=attribute_matching_model, expected_type=type_hints["attribute_matching_model"])
                check_type(argname="argument record_matching_model", value=record_matching_model, expected_type=type_hints["record_matching_model"])
                check_type(argname="argument rule_definition_type", value=rule_definition_type, expected_type=type_hints["rule_definition_type"])
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_matching_model is not None:
                self._values["attribute_matching_model"] = attribute_matching_model
            if record_matching_model is not None:
                self._values["record_matching_model"] = record_matching_model
            if rule_definition_type is not None:
                self._values["rule_definition_type"] = rule_definition_type
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def attribute_matching_model(self) -> typing.Optional[builtins.str]:
            '''The comparison type. You can either choose ``ONE_TO_ONE`` or ``MANY_TO_MANY`` as the ``attributeMatchingModel`` .

            If you choose ``ONE_TO_ONE`` , the system can only match attributes if the sub-types are an exact match. For example, for the ``Email`` attribute type, the system will only consider it a match if the value of the ``Email`` field of Profile A matches the value of the ``Email`` field of Profile B.

            If you choose ``MANY_TO_MANY`` , the system can match attributes across the sub-types of an attribute type. For example, if the value of the ``Email`` field of Profile A matches the value of the ``BusinessEmail`` field of Profile B, the two profiles are matched on the ``Email`` attribute type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingrulebasedproperties.html#cfn-entityresolution-idmappingworkflow-idmappingrulebasedproperties-attributematchingmodel
            '''
            result = self._values.get("attribute_matching_model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_matching_model(self) -> typing.Optional[builtins.str]:
            '''The type of matching record that is allowed to be used in an ID mapping workflow.

            If the value is set to ``ONE_SOURCE_TO_ONE_TARGET`` , only one record in the source can be matched to the same record in the target.

            If the value is set to ``MANY_SOURCE_TO_ONE_TARGET`` , multiple records in the source can be matched to one record in the target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingrulebasedproperties.html#cfn-entityresolution-idmappingworkflow-idmappingrulebasedproperties-recordmatchingmodel
            '''
            result = self._values.get("record_matching_model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_definition_type(self) -> typing.Optional[builtins.str]:
            '''The set of rules you can use in an ID mapping workflow.

            The limitations specified for the source or target to define the match rules must be compatible.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingrulebasedproperties.html#cfn-entityresolution-idmappingworkflow-idmappingrulebasedproperties-ruledefinitiontype
            '''
            result = self._values.get("rule_definition_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.RuleProperty"]]]]:
            '''The rules that can be used for ID mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingrulebasedproperties.html#cfn-entityresolution-idmappingworkflow-idmappingrulebasedproperties-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.RuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdMappingRuleBasedPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdMappingWorkflowPropsMixin.IdMappingTechniquesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id_mapping_type": "idMappingType",
            "normalization_version": "normalizationVersion",
            "provider_properties": "providerProperties",
            "rule_based_properties": "ruleBasedProperties",
        },
    )
    class IdMappingTechniquesProperty:
        def __init__(
            self,
            *,
            id_mapping_type: typing.Optional[builtins.str] = None,
            normalization_version: typing.Optional[builtins.str] = None,
            provider_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdMappingWorkflowPropsMixin.ProviderPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rule_based_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdMappingWorkflowPropsMixin.IdMappingRuleBasedPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object which defines the ID mapping technique and any additional configurations.

            :param id_mapping_type: The type of ID mapping.
            :param normalization_version: 
            :param provider_properties: An object which defines any additional configurations required by the provider service.
            :param rule_based_properties: An object which defines any additional configurations required by rule-based matching.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingtechniques.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                id_mapping_techniques_property = entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingTechniquesProperty(
                    id_mapping_type="idMappingType",
                    normalization_version="normalizationVersion",
                    provider_properties=entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.ProviderPropertiesProperty(
                        intermediate_source_configuration=entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IntermediateSourceConfigurationProperty(
                            intermediate_s3_path="intermediateS3Path"
                        ),
                        provider_configuration={
                            "provider_configuration_key": "providerConfiguration"
                        },
                        provider_service_arn="providerServiceArn"
                    ),
                    rule_based_properties=entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingRuleBasedPropertiesProperty(
                        attribute_matching_model="attributeMatchingModel",
                        record_matching_model="recordMatchingModel",
                        rule_definition_type="ruleDefinitionType",
                        rules=[entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.RuleProperty(
                            matching_keys=["matchingKeys"],
                            rule_name="ruleName"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e07fe89f0b2e9629c9c824133c96582687b0ceaa77728a260410923f0fa188fd)
                check_type(argname="argument id_mapping_type", value=id_mapping_type, expected_type=type_hints["id_mapping_type"])
                check_type(argname="argument normalization_version", value=normalization_version, expected_type=type_hints["normalization_version"])
                check_type(argname="argument provider_properties", value=provider_properties, expected_type=type_hints["provider_properties"])
                check_type(argname="argument rule_based_properties", value=rule_based_properties, expected_type=type_hints["rule_based_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id_mapping_type is not None:
                self._values["id_mapping_type"] = id_mapping_type
            if normalization_version is not None:
                self._values["normalization_version"] = normalization_version
            if provider_properties is not None:
                self._values["provider_properties"] = provider_properties
            if rule_based_properties is not None:
                self._values["rule_based_properties"] = rule_based_properties

        @builtins.property
        def id_mapping_type(self) -> typing.Optional[builtins.str]:
            '''The type of ID mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingtechniques.html#cfn-entityresolution-idmappingworkflow-idmappingtechniques-idmappingtype
            '''
            result = self._values.get("id_mapping_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def normalization_version(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingtechniques.html#cfn-entityresolution-idmappingworkflow-idmappingtechniques-normalizationversion
            '''
            result = self._values.get("normalization_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def provider_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.ProviderPropertiesProperty"]]:
            '''An object which defines any additional configurations required by the provider service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingtechniques.html#cfn-entityresolution-idmappingworkflow-idmappingtechniques-providerproperties
            '''
            result = self._values.get("provider_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.ProviderPropertiesProperty"]], result)

        @builtins.property
        def rule_based_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.IdMappingRuleBasedPropertiesProperty"]]:
            '''An object which defines any additional configurations required by rule-based matching.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingtechniques.html#cfn-entityresolution-idmappingworkflow-idmappingtechniques-rulebasedproperties
            '''
            result = self._values.get("rule_based_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.IdMappingRuleBasedPropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdMappingTechniquesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowInputSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input_source_arn": "inputSourceArn",
            "schema_arn": "schemaArn",
            "type": "type",
        },
    )
    class IdMappingWorkflowInputSourceProperty:
        def __init__(
            self,
            *,
            input_source_arn: typing.Optional[builtins.str] = None,
            schema_arn: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object containing ``inputSourceARN`` , ``schemaName`` , and ``type`` .

            :param input_source_arn: An AWS Glue table Amazon Resource Name (ARN) or a matching workflow ARN for the input source table.
            :param schema_arn: The ARN (Amazon Resource Name) that AWS Entity Resolution generated for the ``SchemaMapping`` .
            :param type: The type of ID namespace. There are two types: ``SOURCE`` and ``TARGET`` . The ``SOURCE`` contains configurations for ``sourceId`` data that will be processed in an ID mapping workflow. The ``TARGET`` contains a configuration of ``targetId`` which all ``sourceIds`` will resolve to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingworkflowinputsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                id_mapping_workflow_input_source_property = entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowInputSourceProperty(
                    input_source_arn="inputSourceArn",
                    schema_arn="schemaArn",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f03475da1b07f3106a4a5471fd83f87889a822ee744480b83a7e593ae7da9ca4)
                check_type(argname="argument input_source_arn", value=input_source_arn, expected_type=type_hints["input_source_arn"])
                check_type(argname="argument schema_arn", value=schema_arn, expected_type=type_hints["schema_arn"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_source_arn is not None:
                self._values["input_source_arn"] = input_source_arn
            if schema_arn is not None:
                self._values["schema_arn"] = schema_arn
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def input_source_arn(self) -> typing.Optional[builtins.str]:
            '''An AWS Glue table Amazon Resource Name (ARN) or a matching workflow ARN for the input source table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingworkflowinputsource.html#cfn-entityresolution-idmappingworkflow-idmappingworkflowinputsource-inputsourcearn
            '''
            result = self._values.get("input_source_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN (Amazon Resource Name) that AWS Entity Resolution generated for the ``SchemaMapping`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingworkflowinputsource.html#cfn-entityresolution-idmappingworkflow-idmappingworkflowinputsource-schemaarn
            '''
            result = self._values.get("schema_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of ID namespace. There are two types: ``SOURCE`` and ``TARGET`` .

            The ``SOURCE`` contains configurations for ``sourceId`` data that will be processed in an ID mapping workflow.

            The ``TARGET`` contains a configuration of ``targetId`` which all ``sourceIds`` will resolve to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingworkflowinputsource.html#cfn-entityresolution-idmappingworkflow-idmappingworkflowinputsource-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdMappingWorkflowInputSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowOutputSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_arn": "kmsArn", "output_s3_path": "outputS3Path"},
    )
    class IdMappingWorkflowOutputSourceProperty:
        def __init__(
            self,
            *,
            kms_arn: typing.Optional[builtins.str] = None,
            output_s3_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of ``IdMappingWorkflowOutputSource`` objects, each of which contains fields ``outputS3Path`` and ``KMSArn`` .

            :param kms_arn: Customer AWS ARN for encryption at rest. If not provided, system will use an AWS Entity Resolution managed KMS key.
            :param output_s3_path: The S3 path to which AWS Entity Resolution will write the output table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingworkflowoutputsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                id_mapping_workflow_output_source_property = entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowOutputSourceProperty(
                    kms_arn="kmsArn",
                    output_s3_path="outputS3Path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fe74982bfa6737143f1df4ac6bc06356d755b62e82e1cf043d11dc742183c870)
                check_type(argname="argument kms_arn", value=kms_arn, expected_type=type_hints["kms_arn"])
                check_type(argname="argument output_s3_path", value=output_s3_path, expected_type=type_hints["output_s3_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_arn is not None:
                self._values["kms_arn"] = kms_arn
            if output_s3_path is not None:
                self._values["output_s3_path"] = output_s3_path

        @builtins.property
        def kms_arn(self) -> typing.Optional[builtins.str]:
            '''Customer AWS  ARN for encryption at rest.

            If not provided, system will use an AWS Entity Resolution managed KMS key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingworkflowoutputsource.html#cfn-entityresolution-idmappingworkflow-idmappingworkflowoutputsource-kmsarn
            '''
            result = self._values.get("kms_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_s3_path(self) -> typing.Optional[builtins.str]:
            '''The S3 path to which AWS Entity Resolution will write the output table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-idmappingworkflowoutputsource.html#cfn-entityresolution-idmappingworkflow-idmappingworkflowoutputsource-outputs3path
            '''
            result = self._values.get("output_s3_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdMappingWorkflowOutputSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdMappingWorkflowPropsMixin.IntermediateSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"intermediate_s3_path": "intermediateS3Path"},
    )
    class IntermediateSourceConfigurationProperty:
        def __init__(
            self,
            *,
            intermediate_s3_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon S3 location that temporarily stores your data while it processes.

            Your information won't be saved permanently.

            :param intermediate_s3_path: The Amazon S3 location (bucket and prefix). For example: ``s3://provider_bucket/DOC-EXAMPLE-BUCKET``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-intermediatesourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                intermediate_source_configuration_property = entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IntermediateSourceConfigurationProperty(
                    intermediate_s3_path="intermediateS3Path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c6eea13c22074734c9f2599c1197d57a30d7647f1aa5bda94d5f84c6384cc8e)
                check_type(argname="argument intermediate_s3_path", value=intermediate_s3_path, expected_type=type_hints["intermediate_s3_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if intermediate_s3_path is not None:
                self._values["intermediate_s3_path"] = intermediate_s3_path

        @builtins.property
        def intermediate_s3_path(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 location (bucket and prefix).

            For example: ``s3://provider_bucket/DOC-EXAMPLE-BUCKET``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-intermediatesourceconfiguration.html#cfn-entityresolution-idmappingworkflow-intermediatesourceconfiguration-intermediates3path
            '''
            result = self._values.get("intermediate_s3_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntermediateSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdMappingWorkflowPropsMixin.ProviderPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "intermediate_source_configuration": "intermediateSourceConfiguration",
            "provider_configuration": "providerConfiguration",
            "provider_service_arn": "providerServiceArn",
        },
    )
    class ProviderPropertiesProperty:
        def __init__(
            self,
            *,
            intermediate_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdMappingWorkflowPropsMixin.IntermediateSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            provider_configuration: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            provider_service_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object containing the ``providerServiceARN`` , ``intermediateSourceConfiguration`` , and ``providerConfiguration`` .

            :param intermediate_source_configuration: The Amazon S3 location that temporarily stores your data while it processes. Your information won't be saved permanently.
            :param provider_configuration: The required configuration fields to use with the provider service.
            :param provider_service_arn: The ARN of the provider service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-providerproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                provider_properties_property = entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.ProviderPropertiesProperty(
                    intermediate_source_configuration=entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.IntermediateSourceConfigurationProperty(
                        intermediate_s3_path="intermediateS3Path"
                    ),
                    provider_configuration={
                        "provider_configuration_key": "providerConfiguration"
                    },
                    provider_service_arn="providerServiceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7833b17b3fb027301e18d8113e4706598bb03e030b9128e378979983d7e11799)
                check_type(argname="argument intermediate_source_configuration", value=intermediate_source_configuration, expected_type=type_hints["intermediate_source_configuration"])
                check_type(argname="argument provider_configuration", value=provider_configuration, expected_type=type_hints["provider_configuration"])
                check_type(argname="argument provider_service_arn", value=provider_service_arn, expected_type=type_hints["provider_service_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if intermediate_source_configuration is not None:
                self._values["intermediate_source_configuration"] = intermediate_source_configuration
            if provider_configuration is not None:
                self._values["provider_configuration"] = provider_configuration
            if provider_service_arn is not None:
                self._values["provider_service_arn"] = provider_service_arn

        @builtins.property
        def intermediate_source_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.IntermediateSourceConfigurationProperty"]]:
            '''The Amazon S3 location that temporarily stores your data while it processes.

            Your information won't be saved permanently.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-providerproperties.html#cfn-entityresolution-idmappingworkflow-providerproperties-intermediatesourceconfiguration
            '''
            result = self._values.get("intermediate_source_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdMappingWorkflowPropsMixin.IntermediateSourceConfigurationProperty"]], result)

        @builtins.property
        def provider_configuration(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The required configuration fields to use with the provider service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-providerproperties.html#cfn-entityresolution-idmappingworkflow-providerproperties-providerconfiguration
            '''
            result = self._values.get("provider_configuration")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def provider_service_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the provider service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-providerproperties.html#cfn-entityresolution-idmappingworkflow-providerproperties-providerservicearn
            '''
            result = self._values.get("provider_service_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProviderPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdMappingWorkflowPropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={"matching_keys": "matchingKeys", "rule_name": "ruleName"},
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            matching_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
            rule_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object containing the ``ruleName`` and ``matchingKeys`` .

            :param matching_keys: A list of ``MatchingKeys`` . The ``MatchingKeys`` must have been defined in the ``SchemaMapping`` . Two records are considered to match according to this rule if all of the ``MatchingKeys`` match.
            :param rule_name: A name for the matching rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                rule_property = entityresolution_mixins.CfnIdMappingWorkflowPropsMixin.RuleProperty(
                    matching_keys=["matchingKeys"],
                    rule_name="ruleName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f871ae72e0f47a9dc90cbd55f6ebab18a602dd0b0e7721fae9e266a1cec6b53)
                check_type(argname="argument matching_keys", value=matching_keys, expected_type=type_hints["matching_keys"])
                check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if matching_keys is not None:
                self._values["matching_keys"] = matching_keys
            if rule_name is not None:
                self._values["rule_name"] = rule_name

        @builtins.property
        def matching_keys(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of ``MatchingKeys`` .

            The ``MatchingKeys`` must have been defined in the ``SchemaMapping`` . Two records are considered to match according to this rule if all of the ``MatchingKeys`` match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-rule.html#cfn-entityresolution-idmappingworkflow-rule-matchingkeys
            '''
            result = self._values.get("matching_keys")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def rule_name(self) -> typing.Optional[builtins.str]:
            '''A name for the matching rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idmappingworkflow-rule.html#cfn-entityresolution-idmappingworkflow-rule-rulename
            '''
            result = self._values.get("rule_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnIdMappingWorkflowWorkflowLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdMappingWorkflowWorkflowLogs",
):
    '''Builder for CfnIdMappingWorkflowLogsMixin to generate WORKFLOW_LOGS for CfnIdMappingWorkflow.

    :cloudformationResource: AWS::EntityResolution::IdMappingWorkflow
    :logType: WORKFLOW_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
        
        cfn_id_mapping_workflow_workflow_logs = entityresolution_mixins.CfnIdMappingWorkflowWorkflowLogs()
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
    ) -> CfnIdMappingWorkflowLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3efe0cff0ff4600833c55d1c985fc32b7d8dcad347cda41b6079e3485e5e6e2c)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnIdMappingWorkflowLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnIdMappingWorkflowLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ab79b7040061e1d0b085b12c2f3432fc871a7d4338f602047fec39483a97cba)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnIdMappingWorkflowLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnIdMappingWorkflowLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c221bcb56c45f3dbd005ebee24ed401a32efcfff33a39a56e20c1442bc844e)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnIdMappingWorkflowLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdNamespaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "id_mapping_workflow_properties": "idMappingWorkflowProperties",
        "id_namespace_name": "idNamespaceName",
        "input_source_config": "inputSourceConfig",
        "role_arn": "roleArn",
        "tags": "tags",
        "type": "type",
    },
)
class CfnIdNamespaceMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        id_mapping_workflow_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdNamespacePropsMixin.IdNamespaceIdMappingWorkflowPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        id_namespace_name: typing.Optional[builtins.str] = None,
        input_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdNamespacePropsMixin.IdNamespaceInputSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnIdNamespacePropsMixin.

        :param description: The description of the ID namespace.
        :param id_mapping_workflow_properties: Determines the properties of ``IdMappingWorflow`` where this ``IdNamespace`` can be used as a ``Source`` or a ``Target`` .
        :param id_namespace_name: The name of the ID namespace.
        :param input_source_config: A list of ``InputSource`` objects, which have the fields ``InputSourceARN`` and ``SchemaName`` .
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role. AWS Entity Resolution assumes this role to access the resources defined in this ``IdNamespace`` on your behalf as part of the workflow run.
        :param tags: The tags used to organize, track, or control access for this resource.
        :param type: The type of ID namespace. There are two types: ``SOURCE`` and ``TARGET`` . The ``SOURCE`` contains configurations for ``sourceId`` data that will be processed in an ID mapping workflow. The ``TARGET`` contains a configuration of ``targetId`` which all ``sourceIds`` will resolve to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idnamespace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
            
            cfn_id_namespace_mixin_props = entityresolution_mixins.CfnIdNamespaceMixinProps(
                description="description",
                id_mapping_workflow_properties=[entityresolution_mixins.CfnIdNamespacePropsMixin.IdNamespaceIdMappingWorkflowPropertiesProperty(
                    id_mapping_type="idMappingType",
                    provider_properties=entityresolution_mixins.CfnIdNamespacePropsMixin.NamespaceProviderPropertiesProperty(
                        provider_configuration={
                            "provider_configuration_key": "providerConfiguration"
                        },
                        provider_service_arn="providerServiceArn"
                    ),
                    rule_based_properties=entityresolution_mixins.CfnIdNamespacePropsMixin.NamespaceRuleBasedPropertiesProperty(
                        attribute_matching_model="attributeMatchingModel",
                        record_matching_models=["recordMatchingModels"],
                        rule_definition_types=["ruleDefinitionTypes"],
                        rules=[entityresolution_mixins.CfnIdNamespacePropsMixin.RuleProperty(
                            matching_keys=["matchingKeys"],
                            rule_name="ruleName"
                        )]
                    )
                )],
                id_namespace_name="idNamespaceName",
                input_source_config=[entityresolution_mixins.CfnIdNamespacePropsMixin.IdNamespaceInputSourceProperty(
                    input_source_arn="inputSourceArn",
                    schema_name="schemaName"
                )],
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92918df5d58e1f792127627b9d8a4549cc4e1b43655d5bc09acb645e24501565)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id_mapping_workflow_properties", value=id_mapping_workflow_properties, expected_type=type_hints["id_mapping_workflow_properties"])
            check_type(argname="argument id_namespace_name", value=id_namespace_name, expected_type=type_hints["id_namespace_name"])
            check_type(argname="argument input_source_config", value=input_source_config, expected_type=type_hints["input_source_config"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if id_mapping_workflow_properties is not None:
            self._values["id_mapping_workflow_properties"] = id_mapping_workflow_properties
        if id_namespace_name is not None:
            self._values["id_namespace_name"] = id_namespace_name
        if input_source_config is not None:
            self._values["input_source_config"] = input_source_config
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the ID namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idnamespace.html#cfn-entityresolution-idnamespace-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id_mapping_workflow_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdNamespacePropsMixin.IdNamespaceIdMappingWorkflowPropertiesProperty"]]]]:
        '''Determines the properties of ``IdMappingWorflow`` where this ``IdNamespace`` can be used as a ``Source`` or a ``Target`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idnamespace.html#cfn-entityresolution-idnamespace-idmappingworkflowproperties
        '''
        result = self._values.get("id_mapping_workflow_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdNamespacePropsMixin.IdNamespaceIdMappingWorkflowPropertiesProperty"]]]], result)

    @builtins.property
    def id_namespace_name(self) -> typing.Optional[builtins.str]:
        '''The name of the ID namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idnamespace.html#cfn-entityresolution-idnamespace-idnamespacename
        '''
        result = self._values.get("id_namespace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_source_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdNamespacePropsMixin.IdNamespaceInputSourceProperty"]]]]:
        '''A list of ``InputSource`` objects, which have the fields ``InputSourceARN`` and ``SchemaName`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idnamespace.html#cfn-entityresolution-idnamespace-inputsourceconfig
        '''
        result = self._values.get("input_source_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdNamespacePropsMixin.IdNamespaceInputSourceProperty"]]]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role.

        AWS Entity Resolution assumes this role to access the resources defined in this ``IdNamespace`` on your behalf as part of the workflow run.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idnamespace.html#cfn-entityresolution-idnamespace-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idnamespace.html#cfn-entityresolution-idnamespace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of ID namespace. There are two types: ``SOURCE`` and ``TARGET`` .

        The ``SOURCE`` contains configurations for ``sourceId`` data that will be processed in an ID mapping workflow.

        The ``TARGET`` contains a configuration of ``targetId`` which all ``sourceIds`` will resolve to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idnamespace.html#cfn-entityresolution-idnamespace-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIdNamespaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIdNamespacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdNamespacePropsMixin",
):
    '''Creates an ID namespace object which will help customers provide metadata explaining their dataset and how to use it.

    Each ID namespace must have a unique name. To modify an existing ID namespace, use the UpdateIdNamespace API.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-idnamespace.html
    :cloudformationResource: AWS::EntityResolution::IdNamespace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
        
        cfn_id_namespace_props_mixin = entityresolution_mixins.CfnIdNamespacePropsMixin(entityresolution_mixins.CfnIdNamespaceMixinProps(
            description="description",
            id_mapping_workflow_properties=[entityresolution_mixins.CfnIdNamespacePropsMixin.IdNamespaceIdMappingWorkflowPropertiesProperty(
                id_mapping_type="idMappingType",
                provider_properties=entityresolution_mixins.CfnIdNamespacePropsMixin.NamespaceProviderPropertiesProperty(
                    provider_configuration={
                        "provider_configuration_key": "providerConfiguration"
                    },
                    provider_service_arn="providerServiceArn"
                ),
                rule_based_properties=entityresolution_mixins.CfnIdNamespacePropsMixin.NamespaceRuleBasedPropertiesProperty(
                    attribute_matching_model="attributeMatchingModel",
                    record_matching_models=["recordMatchingModels"],
                    rule_definition_types=["ruleDefinitionTypes"],
                    rules=[entityresolution_mixins.CfnIdNamespacePropsMixin.RuleProperty(
                        matching_keys=["matchingKeys"],
                        rule_name="ruleName"
                    )]
                )
            )],
            id_namespace_name="idNamespaceName",
            input_source_config=[entityresolution_mixins.CfnIdNamespacePropsMixin.IdNamespaceInputSourceProperty(
                input_source_arn="inputSourceArn",
                schema_name="schemaName"
            )],
            role_arn="roleArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIdNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EntityResolution::IdNamespace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d155158cf121a939f6590b382d22cd641b7299801a6d1137eb274f3d52002e9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b74ec1f5cd5bdd613ecbc31fa48c0cf82dfa3a3ad9f4eef5e9a813efb3ae293b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825df660df3db33ec1f10eda0c641b3fa857157a13dbe4509ec9ab5daace22ea)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIdNamespaceMixinProps:
        return typing.cast(CfnIdNamespaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdNamespacePropsMixin.IdNamespaceIdMappingWorkflowPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id_mapping_type": "idMappingType",
            "provider_properties": "providerProperties",
            "rule_based_properties": "ruleBasedProperties",
        },
    )
    class IdNamespaceIdMappingWorkflowPropertiesProperty:
        def __init__(
            self,
            *,
            id_mapping_type: typing.Optional[builtins.str] = None,
            provider_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdNamespacePropsMixin.NamespaceProviderPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rule_based_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdNamespacePropsMixin.NamespaceRuleBasedPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object containing ``idMappingType`` , ``providerProperties`` , and ``ruleBasedProperties`` .

            :param id_mapping_type: The type of ID mapping.
            :param provider_properties: An object which defines any additional configurations required by the provider service.
            :param rule_based_properties: An object which defines any additional configurations required by rule-based matching.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-idnamespaceidmappingworkflowproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                id_namespace_id_mapping_workflow_properties_property = entityresolution_mixins.CfnIdNamespacePropsMixin.IdNamespaceIdMappingWorkflowPropertiesProperty(
                    id_mapping_type="idMappingType",
                    provider_properties=entityresolution_mixins.CfnIdNamespacePropsMixin.NamespaceProviderPropertiesProperty(
                        provider_configuration={
                            "provider_configuration_key": "providerConfiguration"
                        },
                        provider_service_arn="providerServiceArn"
                    ),
                    rule_based_properties=entityresolution_mixins.CfnIdNamespacePropsMixin.NamespaceRuleBasedPropertiesProperty(
                        attribute_matching_model="attributeMatchingModel",
                        record_matching_models=["recordMatchingModels"],
                        rule_definition_types=["ruleDefinitionTypes"],
                        rules=[entityresolution_mixins.CfnIdNamespacePropsMixin.RuleProperty(
                            matching_keys=["matchingKeys"],
                            rule_name="ruleName"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dfc3ea07e64905084a9ef9c333f31ad705397c84181663cad487dafc13cc0442)
                check_type(argname="argument id_mapping_type", value=id_mapping_type, expected_type=type_hints["id_mapping_type"])
                check_type(argname="argument provider_properties", value=provider_properties, expected_type=type_hints["provider_properties"])
                check_type(argname="argument rule_based_properties", value=rule_based_properties, expected_type=type_hints["rule_based_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id_mapping_type is not None:
                self._values["id_mapping_type"] = id_mapping_type
            if provider_properties is not None:
                self._values["provider_properties"] = provider_properties
            if rule_based_properties is not None:
                self._values["rule_based_properties"] = rule_based_properties

        @builtins.property
        def id_mapping_type(self) -> typing.Optional[builtins.str]:
            '''The type of ID mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-idnamespaceidmappingworkflowproperties.html#cfn-entityresolution-idnamespace-idnamespaceidmappingworkflowproperties-idmappingtype
            '''
            result = self._values.get("id_mapping_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def provider_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdNamespacePropsMixin.NamespaceProviderPropertiesProperty"]]:
            '''An object which defines any additional configurations required by the provider service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-idnamespaceidmappingworkflowproperties.html#cfn-entityresolution-idnamespace-idnamespaceidmappingworkflowproperties-providerproperties
            '''
            result = self._values.get("provider_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdNamespacePropsMixin.NamespaceProviderPropertiesProperty"]], result)

        @builtins.property
        def rule_based_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdNamespacePropsMixin.NamespaceRuleBasedPropertiesProperty"]]:
            '''An object which defines any additional configurations required by rule-based matching.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-idnamespaceidmappingworkflowproperties.html#cfn-entityresolution-idnamespace-idnamespaceidmappingworkflowproperties-rulebasedproperties
            '''
            result = self._values.get("rule_based_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdNamespacePropsMixin.NamespaceRuleBasedPropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdNamespaceIdMappingWorkflowPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdNamespacePropsMixin.IdNamespaceInputSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input_source_arn": "inputSourceArn",
            "schema_name": "schemaName",
        },
    )
    class IdNamespaceInputSourceProperty:
        def __init__(
            self,
            *,
            input_source_arn: typing.Optional[builtins.str] = None,
            schema_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object containing ``inputSourceARN`` and ``schemaName`` .

            :param input_source_arn: An AWS Glue table Amazon Resource Name (ARN) or a matching workflow ARN for the input source table.
            :param schema_name: The name of the schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-idnamespaceinputsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                id_namespace_input_source_property = entityresolution_mixins.CfnIdNamespacePropsMixin.IdNamespaceInputSourceProperty(
                    input_source_arn="inputSourceArn",
                    schema_name="schemaName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c519617e4e36ea6093e1483848c7044aaecdcf22149ec43f97d51617c712fa0f)
                check_type(argname="argument input_source_arn", value=input_source_arn, expected_type=type_hints["input_source_arn"])
                check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_source_arn is not None:
                self._values["input_source_arn"] = input_source_arn
            if schema_name is not None:
                self._values["schema_name"] = schema_name

        @builtins.property
        def input_source_arn(self) -> typing.Optional[builtins.str]:
            '''An AWS Glue table Amazon Resource Name (ARN) or a matching workflow ARN for the input source table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-idnamespaceinputsource.html#cfn-entityresolution-idnamespace-idnamespaceinputsource-inputsourcearn
            '''
            result = self._values.get("input_source_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_name(self) -> typing.Optional[builtins.str]:
            '''The name of the schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-idnamespaceinputsource.html#cfn-entityresolution-idnamespace-idnamespaceinputsource-schemaname
            '''
            result = self._values.get("schema_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdNamespaceInputSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdNamespacePropsMixin.NamespaceProviderPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "provider_configuration": "providerConfiguration",
            "provider_service_arn": "providerServiceArn",
        },
    )
    class NamespaceProviderPropertiesProperty:
        def __init__(
            self,
            *,
            provider_configuration: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            provider_service_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object containing ``providerConfiguration`` and ``providerServiceArn`` .

            :param provider_configuration: An object which defines any additional configurations required by the provider service.
            :param provider_service_arn: The Amazon Resource Name (ARN) of the provider service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-namespaceproviderproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                namespace_provider_properties_property = entityresolution_mixins.CfnIdNamespacePropsMixin.NamespaceProviderPropertiesProperty(
                    provider_configuration={
                        "provider_configuration_key": "providerConfiguration"
                    },
                    provider_service_arn="providerServiceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a2ffb05cba7610bf4b90dbe0ac58e3ef6c5963465f08792c91f016db4dcda82)
                check_type(argname="argument provider_configuration", value=provider_configuration, expected_type=type_hints["provider_configuration"])
                check_type(argname="argument provider_service_arn", value=provider_service_arn, expected_type=type_hints["provider_service_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if provider_configuration is not None:
                self._values["provider_configuration"] = provider_configuration
            if provider_service_arn is not None:
                self._values["provider_service_arn"] = provider_service_arn

        @builtins.property
        def provider_configuration(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''An object which defines any additional configurations required by the provider service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-namespaceproviderproperties.html#cfn-entityresolution-idnamespace-namespaceproviderproperties-providerconfiguration
            '''
            result = self._values.get("provider_configuration")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def provider_service_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the provider service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-namespaceproviderproperties.html#cfn-entityresolution-idnamespace-namespaceproviderproperties-providerservicearn
            '''
            result = self._values.get("provider_service_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NamespaceProviderPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdNamespacePropsMixin.NamespaceRuleBasedPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_matching_model": "attributeMatchingModel",
            "record_matching_models": "recordMatchingModels",
            "rule_definition_types": "ruleDefinitionTypes",
            "rules": "rules",
        },
    )
    class NamespaceRuleBasedPropertiesProperty:
        def __init__(
            self,
            *,
            attribute_matching_model: typing.Optional[builtins.str] = None,
            record_matching_models: typing.Optional[typing.Sequence[builtins.str]] = None,
            rule_definition_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdNamespacePropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The rule-based properties of an ID namespace.

            These properties define how the ID namespace can be used in an ID mapping workflow.

            :param attribute_matching_model: The comparison type. You can either choose ``ONE_TO_ONE`` or ``MANY_TO_MANY`` as the ``attributeMatchingModel`` . If you choose ``ONE_TO_ONE`` , the system can only match attributes if the sub-types are an exact match. For example, for the ``Email`` attribute type, the system will only consider it a match if the value of the ``Email`` field of Profile A matches the value of the ``Email`` field of Profile B. If you choose ``MANY_TO_MANY`` , the system can match attributes across the sub-types of an attribute type. For example, if the value of the ``Email`` field of Profile A matches the value of ``BusinessEmail`` field of Profile B, the two profiles are matched on the ``Email`` attribute type.
            :param record_matching_models: The type of matching record that is allowed to be used in an ID mapping workflow. If the value is set to ``ONE_SOURCE_TO_ONE_TARGET`` , only one record in the source is matched to one record in the target. If the value is set to ``MANY_SOURCE_TO_ONE_TARGET`` , all matching records in the source are matched to one record in the target.
            :param rule_definition_types: The sets of rules you can use in an ID mapping workflow. The limitations specified for the source and target must be compatible.
            :param rules: The rules for the ID namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-namespacerulebasedproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                namespace_rule_based_properties_property = entityresolution_mixins.CfnIdNamespacePropsMixin.NamespaceRuleBasedPropertiesProperty(
                    attribute_matching_model="attributeMatchingModel",
                    record_matching_models=["recordMatchingModels"],
                    rule_definition_types=["ruleDefinitionTypes"],
                    rules=[entityresolution_mixins.CfnIdNamespacePropsMixin.RuleProperty(
                        matching_keys=["matchingKeys"],
                        rule_name="ruleName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__458fd11728fefbd547681c825c04ded5aea1af8a40485418cadfbf72cd2bb64e)
                check_type(argname="argument attribute_matching_model", value=attribute_matching_model, expected_type=type_hints["attribute_matching_model"])
                check_type(argname="argument record_matching_models", value=record_matching_models, expected_type=type_hints["record_matching_models"])
                check_type(argname="argument rule_definition_types", value=rule_definition_types, expected_type=type_hints["rule_definition_types"])
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_matching_model is not None:
                self._values["attribute_matching_model"] = attribute_matching_model
            if record_matching_models is not None:
                self._values["record_matching_models"] = record_matching_models
            if rule_definition_types is not None:
                self._values["rule_definition_types"] = rule_definition_types
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def attribute_matching_model(self) -> typing.Optional[builtins.str]:
            '''The comparison type. You can either choose ``ONE_TO_ONE`` or ``MANY_TO_MANY`` as the ``attributeMatchingModel`` .

            If you choose ``ONE_TO_ONE`` , the system can only match attributes if the sub-types are an exact match. For example, for the ``Email`` attribute type, the system will only consider it a match if the value of the ``Email`` field of Profile A matches the value of the ``Email`` field of Profile B.

            If you choose ``MANY_TO_MANY`` , the system can match attributes across the sub-types of an attribute type. For example, if the value of the ``Email`` field of Profile A matches the value of ``BusinessEmail`` field of Profile B, the two profiles are matched on the ``Email`` attribute type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-namespacerulebasedproperties.html#cfn-entityresolution-idnamespace-namespacerulebasedproperties-attributematchingmodel
            '''
            result = self._values.get("attribute_matching_model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_matching_models(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The type of matching record that is allowed to be used in an ID mapping workflow.

            If the value is set to ``ONE_SOURCE_TO_ONE_TARGET`` , only one record in the source is matched to one record in the target.

            If the value is set to ``MANY_SOURCE_TO_ONE_TARGET`` , all matching records in the source are matched to one record in the target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-namespacerulebasedproperties.html#cfn-entityresolution-idnamespace-namespacerulebasedproperties-recordmatchingmodels
            '''
            result = self._values.get("record_matching_models")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def rule_definition_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The sets of rules you can use in an ID mapping workflow.

            The limitations specified for the source and target must be compatible.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-namespacerulebasedproperties.html#cfn-entityresolution-idnamespace-namespacerulebasedproperties-ruledefinitiontypes
            '''
            result = self._values.get("rule_definition_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdNamespacePropsMixin.RuleProperty"]]]]:
            '''The rules for the ID namespace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-namespacerulebasedproperties.html#cfn-entityresolution-idnamespace-namespacerulebasedproperties-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdNamespacePropsMixin.RuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NamespaceRuleBasedPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnIdNamespacePropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={"matching_keys": "matchingKeys", "rule_name": "ruleName"},
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            matching_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
            rule_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object containing the ``ruleName`` and ``matchingKeys`` .

            :param matching_keys: A list of ``MatchingKeys`` . The ``MatchingKeys`` must have been defined in the ``SchemaMapping`` . Two records are considered to match according to this rule if all of the ``MatchingKeys`` match.
            :param rule_name: A name for the matching rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                rule_property = entityresolution_mixins.CfnIdNamespacePropsMixin.RuleProperty(
                    matching_keys=["matchingKeys"],
                    rule_name="ruleName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__71c3dfff14d95c2b780d6a677f9ef854948f39e634c2a2949bcaf774d7b32cc2)
                check_type(argname="argument matching_keys", value=matching_keys, expected_type=type_hints["matching_keys"])
                check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if matching_keys is not None:
                self._values["matching_keys"] = matching_keys
            if rule_name is not None:
                self._values["rule_name"] = rule_name

        @builtins.property
        def matching_keys(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of ``MatchingKeys`` .

            The ``MatchingKeys`` must have been defined in the ``SchemaMapping`` . Two records are considered to match according to this rule if all of the ``MatchingKeys`` match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-rule.html#cfn-entityresolution-idnamespace-rule-matchingkeys
            '''
            result = self._values.get("matching_keys")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def rule_name(self) -> typing.Optional[builtins.str]:
            '''A name for the matching rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-idnamespace-rule.html#cfn-entityresolution-idnamespace-rule-rulename
            '''
            result = self._values.get("rule_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnMatchingWorkflowLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowLogsMixin",
):
    '''Creates a matching workflow that defines the configuration for a data processing job.

    The workflow name must be unique. To modify an existing workflow, use ``UpdateMatchingWorkflow`` .
    .. epigraph::

       For workflows where ``resolutionType`` is ``ML_MATCHING`` or ``PROVIDER`` , incremental processing is not supported.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-matchingworkflow.html
    :cloudformationResource: AWS::EntityResolution::MatchingWorkflow
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_matching_workflow_logs_mixin = entityresolution_mixins.CfnMatchingWorkflowLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::EntityResolution::MatchingWorkflow``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2a2f8f41e56803947feeac063141099a92bd03d48742c1294fd888e5c86f3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32fe9df30012d7ee5ff8ad68526b3ca56aa553a067d710540e6da25435985e55)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f0125aaab9fb5c7fe239c86824ba8eb20303f55113b06eb498ed52aeef2cca)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WORKFLOW_LOGS")
    def WORKFLOW_LOGS(cls) -> "CfnMatchingWorkflowWorkflowLogs":
        return typing.cast("CfnMatchingWorkflowWorkflowLogs", jsii.sget(cls, "WORKFLOW_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "incremental_run_config": "incrementalRunConfig",
        "input_source_config": "inputSourceConfig",
        "output_source_config": "outputSourceConfig",
        "resolution_techniques": "resolutionTechniques",
        "role_arn": "roleArn",
        "tags": "tags",
        "workflow_name": "workflowName",
    },
)
class CfnMatchingWorkflowMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        incremental_run_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMatchingWorkflowPropsMixin.IncrementalRunConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        input_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMatchingWorkflowPropsMixin.InputSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        output_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMatchingWorkflowPropsMixin.OutputSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        resolution_techniques: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMatchingWorkflowPropsMixin.ResolutionTechniquesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMatchingWorkflowPropsMixin.

        :param description: A description of the workflow.
        :param incremental_run_config: Optional. An object that defines the incremental run type. This object contains only the ``incrementalRunType`` field, which appears as "Automatic" in the console. .. epigraph:: For workflows where ``resolutionType`` is ``ML_MATCHING`` or ``PROVIDER`` , incremental processing is not supported.
        :param input_source_config: A list of ``InputSource`` objects, which have the fields ``InputSourceARN`` and ``SchemaName`` .
        :param output_source_config: A list of ``OutputSource`` objects, each of which contains fields ``outputS3Path`` , ``applyNormalization`` , ``KMSArn`` , and ``output`` .
        :param resolution_techniques: An object which defines the ``resolutionType`` and the ``ruleBasedProperties`` .
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role. AWS Entity Resolution assumes this role to create resources on your behalf as part of workflow execution.
        :param tags: The tags used to organize, track, or control access for this resource.
        :param workflow_name: The name of the workflow. There can't be multiple ``MatchingWorkflows`` with the same name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-matchingworkflow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
            
            cfn_matching_workflow_mixin_props = entityresolution_mixins.CfnMatchingWorkflowMixinProps(
                description="description",
                incremental_run_config=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.IncrementalRunConfigProperty(
                    incremental_run_type="incrementalRunType"
                ),
                input_source_config=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.InputSourceProperty(
                    apply_normalization=False,
                    input_source_arn="inputSourceArn",
                    schema_arn="schemaArn"
                )],
                output_source_config=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.OutputSourceProperty(
                    apply_normalization=False,
                    kms_arn="kmsArn",
                    output=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.OutputAttributeProperty(
                        hashed=False,
                        name="name"
                    )],
                    output_s3_path="outputS3Path"
                )],
                resolution_techniques=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.ResolutionTechniquesProperty(
                    provider_properties=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.ProviderPropertiesProperty(
                        intermediate_source_configuration=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.IntermediateSourceConfigurationProperty(
                            intermediate_s3_path="intermediateS3Path"
                        ),
                        provider_configuration={
                            "provider_configuration_key": "providerConfiguration"
                        },
                        provider_service_arn="providerServiceArn"
                    ),
                    resolution_type="resolutionType",
                    rule_based_properties=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleBasedPropertiesProperty(
                        attribute_matching_model="attributeMatchingModel",
                        match_purpose="matchPurpose",
                        rules=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleProperty(
                            matching_keys=["matchingKeys"],
                            rule_name="ruleName"
                        )]
                    ),
                    rule_condition_properties=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleConditionPropertiesProperty(
                        rules=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleConditionProperty(
                            condition="condition",
                            rule_name="ruleName"
                        )]
                    )
                ),
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                workflow_name="workflowName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f24aa8b48e66db77e27e4f7115bb80b5b27f6a17a962cb140c19898694371ed)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument incremental_run_config", value=incremental_run_config, expected_type=type_hints["incremental_run_config"])
            check_type(argname="argument input_source_config", value=input_source_config, expected_type=type_hints["input_source_config"])
            check_type(argname="argument output_source_config", value=output_source_config, expected_type=type_hints["output_source_config"])
            check_type(argname="argument resolution_techniques", value=resolution_techniques, expected_type=type_hints["resolution_techniques"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workflow_name", value=workflow_name, expected_type=type_hints["workflow_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if incremental_run_config is not None:
            self._values["incremental_run_config"] = incremental_run_config
        if input_source_config is not None:
            self._values["input_source_config"] = input_source_config
        if output_source_config is not None:
            self._values["output_source_config"] = output_source_config
        if resolution_techniques is not None:
            self._values["resolution_techniques"] = resolution_techniques
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags
        if workflow_name is not None:
            self._values["workflow_name"] = workflow_name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-matchingworkflow.html#cfn-entityresolution-matchingworkflow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def incremental_run_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.IncrementalRunConfigProperty"]]:
        '''Optional.

        An object that defines the incremental run type. This object contains only the ``incrementalRunType`` field, which appears as "Automatic" in the console.
        .. epigraph::

           For workflows where ``resolutionType`` is ``ML_MATCHING`` or ``PROVIDER`` , incremental processing is not supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-matchingworkflow.html#cfn-entityresolution-matchingworkflow-incrementalrunconfig
        '''
        result = self._values.get("incremental_run_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.IncrementalRunConfigProperty"]], result)

    @builtins.property
    def input_source_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.InputSourceProperty"]]]]:
        '''A list of ``InputSource`` objects, which have the fields ``InputSourceARN`` and ``SchemaName`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-matchingworkflow.html#cfn-entityresolution-matchingworkflow-inputsourceconfig
        '''
        result = self._values.get("input_source_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.InputSourceProperty"]]]], result)

    @builtins.property
    def output_source_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.OutputSourceProperty"]]]]:
        '''A list of ``OutputSource`` objects, each of which contains fields ``outputS3Path`` , ``applyNormalization`` , ``KMSArn`` , and ``output`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-matchingworkflow.html#cfn-entityresolution-matchingworkflow-outputsourceconfig
        '''
        result = self._values.get("output_source_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.OutputSourceProperty"]]]], result)

    @builtins.property
    def resolution_techniques(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.ResolutionTechniquesProperty"]]:
        '''An object which defines the ``resolutionType`` and the ``ruleBasedProperties`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-matchingworkflow.html#cfn-entityresolution-matchingworkflow-resolutiontechniques
        '''
        result = self._values.get("resolution_techniques")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.ResolutionTechniquesProperty"]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role.

        AWS Entity Resolution assumes this role to create resources on your behalf as part of workflow execution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-matchingworkflow.html#cfn-entityresolution-matchingworkflow-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-matchingworkflow.html#cfn-entityresolution-matchingworkflow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def workflow_name(self) -> typing.Optional[builtins.str]:
        '''The name of the workflow.

        There can't be multiple ``MatchingWorkflows`` with the same name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-matchingworkflow.html#cfn-entityresolution-matchingworkflow-workflowname
        '''
        result = self._values.get("workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMatchingWorkflowMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMatchingWorkflowPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowPropsMixin",
):
    '''Creates a matching workflow that defines the configuration for a data processing job.

    The workflow name must be unique. To modify an existing workflow, use ``UpdateMatchingWorkflow`` .
    .. epigraph::

       For workflows where ``resolutionType`` is ``ML_MATCHING`` or ``PROVIDER`` , incremental processing is not supported.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-matchingworkflow.html
    :cloudformationResource: AWS::EntityResolution::MatchingWorkflow
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
        
        cfn_matching_workflow_props_mixin = entityresolution_mixins.CfnMatchingWorkflowPropsMixin(entityresolution_mixins.CfnMatchingWorkflowMixinProps(
            description="description",
            incremental_run_config=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.IncrementalRunConfigProperty(
                incremental_run_type="incrementalRunType"
            ),
            input_source_config=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.InputSourceProperty(
                apply_normalization=False,
                input_source_arn="inputSourceArn",
                schema_arn="schemaArn"
            )],
            output_source_config=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.OutputSourceProperty(
                apply_normalization=False,
                kms_arn="kmsArn",
                output=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.OutputAttributeProperty(
                    hashed=False,
                    name="name"
                )],
                output_s3_path="outputS3Path"
            )],
            resolution_techniques=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.ResolutionTechniquesProperty(
                provider_properties=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.ProviderPropertiesProperty(
                    intermediate_source_configuration=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.IntermediateSourceConfigurationProperty(
                        intermediate_s3_path="intermediateS3Path"
                    ),
                    provider_configuration={
                        "provider_configuration_key": "providerConfiguration"
                    },
                    provider_service_arn="providerServiceArn"
                ),
                resolution_type="resolutionType",
                rule_based_properties=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleBasedPropertiesProperty(
                    attribute_matching_model="attributeMatchingModel",
                    match_purpose="matchPurpose",
                    rules=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleProperty(
                        matching_keys=["matchingKeys"],
                        rule_name="ruleName"
                    )]
                ),
                rule_condition_properties=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleConditionPropertiesProperty(
                    rules=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleConditionProperty(
                        condition="condition",
                        rule_name="ruleName"
                    )]
                )
            ),
            role_arn="roleArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            workflow_name="workflowName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMatchingWorkflowMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EntityResolution::MatchingWorkflow``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f449b46dec1c6dfa62a7a669c6bc327a1568c7d6286f1641a9cd5c20bad861c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ae9930f751d4e311361b198b824c26790a1b183b0ceb3b03012554cb7aad44c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ba61f6dbff2ed563ad16b6a3db5f183f75d4ebee70dbbf72b13c10763fe4305)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMatchingWorkflowMixinProps:
        return typing.cast(CfnMatchingWorkflowMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowPropsMixin.IncrementalRunConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"incremental_run_type": "incrementalRunType"},
    )
    class IncrementalRunConfigProperty:
        def __init__(
            self,
            *,
            incremental_run_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Optional.

            An object that defines the incremental run type. This object contains only the ``incrementalRunType`` field, which appears as "Automatic" in the console.
            .. epigraph::

               For workflows where ``resolutionType`` is ``ML_MATCHING`` or ``PROVIDER`` , incremental processing is not supported.

            :param incremental_run_type: The type of incremental run. The only valid value is ``IMMEDIATE`` . This appears as "Automatic" in the console. .. epigraph:: For workflows where ``resolutionType`` is ``ML_MATCHING`` or ``PROVIDER`` , incremental processing is not supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-incrementalrunconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                incremental_run_config_property = entityresolution_mixins.CfnMatchingWorkflowPropsMixin.IncrementalRunConfigProperty(
                    incremental_run_type="incrementalRunType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f20dd2505489de2bacc4a3e0b5eda8bd6f5a9c355c250de4a988442fd882d86a)
                check_type(argname="argument incremental_run_type", value=incremental_run_type, expected_type=type_hints["incremental_run_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if incremental_run_type is not None:
                self._values["incremental_run_type"] = incremental_run_type

        @builtins.property
        def incremental_run_type(self) -> typing.Optional[builtins.str]:
            '''The type of incremental run. The only valid value is ``IMMEDIATE`` . This appears as "Automatic" in the console.

            .. epigraph::

               For workflows where ``resolutionType`` is ``ML_MATCHING`` or ``PROVIDER`` , incremental processing is not supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-incrementalrunconfig.html#cfn-entityresolution-matchingworkflow-incrementalrunconfig-incrementalruntype
            '''
            result = self._values.get("incremental_run_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IncrementalRunConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowPropsMixin.InputSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "apply_normalization": "applyNormalization",
            "input_source_arn": "inputSourceArn",
            "schema_arn": "schemaArn",
        },
    )
    class InputSourceProperty:
        def __init__(
            self,
            *,
            apply_normalization: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            input_source_arn: typing.Optional[builtins.str] = None,
            schema_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object containing ``inputSourceARN`` , ``schemaName`` , and ``applyNormalization`` .

            :param apply_normalization: Normalizes the attributes defined in the schema in the input data. For example, if an attribute has an ``AttributeType`` of ``PHONE_NUMBER`` , and the data in the input table is in a format of 1234567890, AWS Entity Resolution will normalize this field in the output to (123)-456-7890.
            :param input_source_arn: An object containing ``inputSourceARN`` , ``schemaName`` , and ``applyNormalization`` .
            :param schema_arn: The name of the schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-inputsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                input_source_property = entityresolution_mixins.CfnMatchingWorkflowPropsMixin.InputSourceProperty(
                    apply_normalization=False,
                    input_source_arn="inputSourceArn",
                    schema_arn="schemaArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__09059cd81838eeef0bf03b9d702fc94bdf0ddb41c47d85c667029dbe9c754d9b)
                check_type(argname="argument apply_normalization", value=apply_normalization, expected_type=type_hints["apply_normalization"])
                check_type(argname="argument input_source_arn", value=input_source_arn, expected_type=type_hints["input_source_arn"])
                check_type(argname="argument schema_arn", value=schema_arn, expected_type=type_hints["schema_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if apply_normalization is not None:
                self._values["apply_normalization"] = apply_normalization
            if input_source_arn is not None:
                self._values["input_source_arn"] = input_source_arn
            if schema_arn is not None:
                self._values["schema_arn"] = schema_arn

        @builtins.property
        def apply_normalization(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Normalizes the attributes defined in the schema in the input data.

            For example, if an attribute has an ``AttributeType`` of ``PHONE_NUMBER`` , and the data in the input table is in a format of 1234567890, AWS Entity Resolution will normalize this field in the output to (123)-456-7890.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-inputsource.html#cfn-entityresolution-matchingworkflow-inputsource-applynormalization
            '''
            result = self._values.get("apply_normalization")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def input_source_arn(self) -> typing.Optional[builtins.str]:
            '''An object containing ``inputSourceARN`` , ``schemaName`` , and ``applyNormalization`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-inputsource.html#cfn-entityresolution-matchingworkflow-inputsource-inputsourcearn
            '''
            result = self._values.get("input_source_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_arn(self) -> typing.Optional[builtins.str]:
            '''The name of the schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-inputsource.html#cfn-entityresolution-matchingworkflow-inputsource-schemaarn
            '''
            result = self._values.get("schema_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowPropsMixin.IntermediateSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"intermediate_s3_path": "intermediateS3Path"},
    )
    class IntermediateSourceConfigurationProperty:
        def __init__(
            self,
            *,
            intermediate_s3_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon S3 location that temporarily stores your data while it processes.

            Your information won't be saved permanently.

            :param intermediate_s3_path: The Amazon S3 location (bucket and prefix). For example: ``s3://provider_bucket/DOC-EXAMPLE-BUCKET``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-intermediatesourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                intermediate_source_configuration_property = entityresolution_mixins.CfnMatchingWorkflowPropsMixin.IntermediateSourceConfigurationProperty(
                    intermediate_s3_path="intermediateS3Path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__531709d47b71d4503e8735a2c5d63d276a0956fa10f6fe00eb3c83ac490b5821)
                check_type(argname="argument intermediate_s3_path", value=intermediate_s3_path, expected_type=type_hints["intermediate_s3_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if intermediate_s3_path is not None:
                self._values["intermediate_s3_path"] = intermediate_s3_path

        @builtins.property
        def intermediate_s3_path(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 location (bucket and prefix).

            For example: ``s3://provider_bucket/DOC-EXAMPLE-BUCKET``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-intermediatesourceconfiguration.html#cfn-entityresolution-matchingworkflow-intermediatesourceconfiguration-intermediates3path
            '''
            result = self._values.get("intermediate_s3_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntermediateSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowPropsMixin.OutputAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"hashed": "hashed", "name": "name"},
    )
    class OutputAttributeProperty:
        def __init__(
            self,
            *,
            hashed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of ``OutputAttribute`` objects, each of which have the fields ``Name`` and ``Hashed`` .

            Each of these objects selects a column to be included in the output table, and whether the values of the column should be hashed.

            :param hashed: Enables the ability to hash the column values in the output.
            :param name: A name of a column to be written to the output. This must be an ``InputField`` name in the schema mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-outputattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                output_attribute_property = entityresolution_mixins.CfnMatchingWorkflowPropsMixin.OutputAttributeProperty(
                    hashed=False,
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1699c9f415fc9759a56c2227c29343071594a40719e14e7e1cc442ac1878f0d9)
                check_type(argname="argument hashed", value=hashed, expected_type=type_hints["hashed"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hashed is not None:
                self._values["hashed"] = hashed
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def hashed(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables the ability to hash the column values in the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-outputattribute.html#cfn-entityresolution-matchingworkflow-outputattribute-hashed
            '''
            result = self._values.get("hashed")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''A name of a column to be written to the output.

            This must be an ``InputField`` name in the schema mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-outputattribute.html#cfn-entityresolution-matchingworkflow-outputattribute-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowPropsMixin.OutputSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "apply_normalization": "applyNormalization",
            "kms_arn": "kmsArn",
            "output": "output",
            "output_s3_path": "outputS3Path",
        },
    )
    class OutputSourceProperty:
        def __init__(
            self,
            *,
            apply_normalization: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            kms_arn: typing.Optional[builtins.str] = None,
            output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMatchingWorkflowPropsMixin.OutputAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            output_s3_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of ``OutputAttribute`` objects, each of which have the fields ``Name`` and ``Hashed`` .

            Each of these objects selects a column to be included in the output table, and whether the values of the column should be hashed.

            :param apply_normalization: Normalizes the attributes defined in the schema in the input data. For example, if an attribute has an ``AttributeType`` of ``PHONE_NUMBER`` , and the data in the input table is in a format of 1234567890, AWS Entity Resolution will normalize this field in the output to (123)-456-7890.
            :param kms_arn: Customer KMS ARN for encryption at rest. If not provided, system will use an AWS Entity Resolution managed KMS key.
            :param output: A list of ``OutputAttribute`` objects, each of which have the fields ``Name`` and ``Hashed`` . Each of these objects selects a column to be included in the output table, and whether the values of the column should be hashed.
            :param output_s3_path: The S3 path to which AWS Entity Resolution will write the output table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-outputsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                output_source_property = entityresolution_mixins.CfnMatchingWorkflowPropsMixin.OutputSourceProperty(
                    apply_normalization=False,
                    kms_arn="kmsArn",
                    output=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.OutputAttributeProperty(
                        hashed=False,
                        name="name"
                    )],
                    output_s3_path="outputS3Path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__18a70b30ce5b5ccffa3185350937bf9746d5621d6165510d2fc2f1bc3318645f)
                check_type(argname="argument apply_normalization", value=apply_normalization, expected_type=type_hints["apply_normalization"])
                check_type(argname="argument kms_arn", value=kms_arn, expected_type=type_hints["kms_arn"])
                check_type(argname="argument output", value=output, expected_type=type_hints["output"])
                check_type(argname="argument output_s3_path", value=output_s3_path, expected_type=type_hints["output_s3_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if apply_normalization is not None:
                self._values["apply_normalization"] = apply_normalization
            if kms_arn is not None:
                self._values["kms_arn"] = kms_arn
            if output is not None:
                self._values["output"] = output
            if output_s3_path is not None:
                self._values["output_s3_path"] = output_s3_path

        @builtins.property
        def apply_normalization(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Normalizes the attributes defined in the schema in the input data.

            For example, if an attribute has an ``AttributeType`` of ``PHONE_NUMBER`` , and the data in the input table is in a format of 1234567890, AWS Entity Resolution will normalize this field in the output to (123)-456-7890.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-outputsource.html#cfn-entityresolution-matchingworkflow-outputsource-applynormalization
            '''
            result = self._values.get("apply_normalization")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def kms_arn(self) -> typing.Optional[builtins.str]:
            '''Customer KMS ARN for encryption at rest.

            If not provided, system will use an AWS Entity Resolution managed KMS key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-outputsource.html#cfn-entityresolution-matchingworkflow-outputsource-kmsarn
            '''
            result = self._values.get("kms_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.OutputAttributeProperty"]]]]:
            '''A list of ``OutputAttribute`` objects, each of which have the fields ``Name`` and ``Hashed`` .

            Each of these objects selects a column to be included in the output table, and whether the values of the column should be hashed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-outputsource.html#cfn-entityresolution-matchingworkflow-outputsource-output
            '''
            result = self._values.get("output")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.OutputAttributeProperty"]]]], result)

        @builtins.property
        def output_s3_path(self) -> typing.Optional[builtins.str]:
            '''The S3 path to which AWS Entity Resolution will write the output table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-outputsource.html#cfn-entityresolution-matchingworkflow-outputsource-outputs3path
            '''
            result = self._values.get("output_s3_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowPropsMixin.ProviderPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "intermediate_source_configuration": "intermediateSourceConfiguration",
            "provider_configuration": "providerConfiguration",
            "provider_service_arn": "providerServiceArn",
        },
    )
    class ProviderPropertiesProperty:
        def __init__(
            self,
            *,
            intermediate_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMatchingWorkflowPropsMixin.IntermediateSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            provider_configuration: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            provider_service_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object containing the ``providerServiceARN`` , ``intermediateSourceConfiguration`` , and ``providerConfiguration`` .

            :param intermediate_source_configuration: The Amazon S3 location that temporarily stores your data while it processes. Your information won't be saved permanently.
            :param provider_configuration: The required configuration fields to use with the provider service.
            :param provider_service_arn: The ARN of the provider service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-providerproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                provider_properties_property = entityresolution_mixins.CfnMatchingWorkflowPropsMixin.ProviderPropertiesProperty(
                    intermediate_source_configuration=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.IntermediateSourceConfigurationProperty(
                        intermediate_s3_path="intermediateS3Path"
                    ),
                    provider_configuration={
                        "provider_configuration_key": "providerConfiguration"
                    },
                    provider_service_arn="providerServiceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a18a80242336ee811f0445ac0530befbdfd7eaf96c8a539009bf2c3c0dd12829)
                check_type(argname="argument intermediate_source_configuration", value=intermediate_source_configuration, expected_type=type_hints["intermediate_source_configuration"])
                check_type(argname="argument provider_configuration", value=provider_configuration, expected_type=type_hints["provider_configuration"])
                check_type(argname="argument provider_service_arn", value=provider_service_arn, expected_type=type_hints["provider_service_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if intermediate_source_configuration is not None:
                self._values["intermediate_source_configuration"] = intermediate_source_configuration
            if provider_configuration is not None:
                self._values["provider_configuration"] = provider_configuration
            if provider_service_arn is not None:
                self._values["provider_service_arn"] = provider_service_arn

        @builtins.property
        def intermediate_source_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.IntermediateSourceConfigurationProperty"]]:
            '''The Amazon S3 location that temporarily stores your data while it processes.

            Your information won't be saved permanently.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-providerproperties.html#cfn-entityresolution-matchingworkflow-providerproperties-intermediatesourceconfiguration
            '''
            result = self._values.get("intermediate_source_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.IntermediateSourceConfigurationProperty"]], result)

        @builtins.property
        def provider_configuration(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The required configuration fields to use with the provider service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-providerproperties.html#cfn-entityresolution-matchingworkflow-providerproperties-providerconfiguration
            '''
            result = self._values.get("provider_configuration")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def provider_service_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the provider service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-providerproperties.html#cfn-entityresolution-matchingworkflow-providerproperties-providerservicearn
            '''
            result = self._values.get("provider_service_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProviderPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowPropsMixin.ResolutionTechniquesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "provider_properties": "providerProperties",
            "resolution_type": "resolutionType",
            "rule_based_properties": "ruleBasedProperties",
            "rule_condition_properties": "ruleConditionProperties",
        },
    )
    class ResolutionTechniquesProperty:
        def __init__(
            self,
            *,
            provider_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMatchingWorkflowPropsMixin.ProviderPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resolution_type: typing.Optional[builtins.str] = None,
            rule_based_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMatchingWorkflowPropsMixin.RuleBasedPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rule_condition_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMatchingWorkflowPropsMixin.RuleConditionPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object which defines the ``resolutionType`` and the ``ruleBasedProperties`` .

            :param provider_properties: The properties of the provider service.
            :param resolution_type: The type of matching workflow to create. Specify one of the following types:. - ``RULE_MATCHING`` : Match records using configurable rule-based criteria - ``ML_MATCHING`` : Match records using machine learning models - ``PROVIDER`` : Match records using a third-party matching provider
            :param rule_based_properties: An object which defines the list of matching rules to run and has a field ``rules`` , which is a list of rule objects.
            :param rule_condition_properties: An object containing the ``rules`` for a matching workflow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-resolutiontechniques.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                resolution_techniques_property = entityresolution_mixins.CfnMatchingWorkflowPropsMixin.ResolutionTechniquesProperty(
                    provider_properties=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.ProviderPropertiesProperty(
                        intermediate_source_configuration=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.IntermediateSourceConfigurationProperty(
                            intermediate_s3_path="intermediateS3Path"
                        ),
                        provider_configuration={
                            "provider_configuration_key": "providerConfiguration"
                        },
                        provider_service_arn="providerServiceArn"
                    ),
                    resolution_type="resolutionType",
                    rule_based_properties=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleBasedPropertiesProperty(
                        attribute_matching_model="attributeMatchingModel",
                        match_purpose="matchPurpose",
                        rules=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleProperty(
                            matching_keys=["matchingKeys"],
                            rule_name="ruleName"
                        )]
                    ),
                    rule_condition_properties=entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleConditionPropertiesProperty(
                        rules=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleConditionProperty(
                            condition="condition",
                            rule_name="ruleName"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e40fd68d9d4bf08cdc4faf15c32386377fd240668045c4a5b489b1f3b929d474)
                check_type(argname="argument provider_properties", value=provider_properties, expected_type=type_hints["provider_properties"])
                check_type(argname="argument resolution_type", value=resolution_type, expected_type=type_hints["resolution_type"])
                check_type(argname="argument rule_based_properties", value=rule_based_properties, expected_type=type_hints["rule_based_properties"])
                check_type(argname="argument rule_condition_properties", value=rule_condition_properties, expected_type=type_hints["rule_condition_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if provider_properties is not None:
                self._values["provider_properties"] = provider_properties
            if resolution_type is not None:
                self._values["resolution_type"] = resolution_type
            if rule_based_properties is not None:
                self._values["rule_based_properties"] = rule_based_properties
            if rule_condition_properties is not None:
                self._values["rule_condition_properties"] = rule_condition_properties

        @builtins.property
        def provider_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.ProviderPropertiesProperty"]]:
            '''The properties of the provider service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-resolutiontechniques.html#cfn-entityresolution-matchingworkflow-resolutiontechniques-providerproperties
            '''
            result = self._values.get("provider_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.ProviderPropertiesProperty"]], result)

        @builtins.property
        def resolution_type(self) -> typing.Optional[builtins.str]:
            '''The type of matching workflow to create. Specify one of the following types:.

            - ``RULE_MATCHING`` : Match records using configurable rule-based criteria
            - ``ML_MATCHING`` : Match records using machine learning models
            - ``PROVIDER`` : Match records using a third-party matching provider

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-resolutiontechniques.html#cfn-entityresolution-matchingworkflow-resolutiontechniques-resolutiontype
            '''
            result = self._values.get("resolution_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_based_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.RuleBasedPropertiesProperty"]]:
            '''An object which defines the list of matching rules to run and has a field ``rules`` , which is a list of rule objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-resolutiontechniques.html#cfn-entityresolution-matchingworkflow-resolutiontechniques-rulebasedproperties
            '''
            result = self._values.get("rule_based_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.RuleBasedPropertiesProperty"]], result)

        @builtins.property
        def rule_condition_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.RuleConditionPropertiesProperty"]]:
            '''An object containing the ``rules`` for a matching workflow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-resolutiontechniques.html#cfn-entityresolution-matchingworkflow-resolutiontechniques-ruleconditionproperties
            '''
            result = self._values.get("rule_condition_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.RuleConditionPropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResolutionTechniquesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowPropsMixin.RuleBasedPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_matching_model": "attributeMatchingModel",
            "match_purpose": "matchPurpose",
            "rules": "rules",
        },
    )
    class RuleBasedPropertiesProperty:
        def __init__(
            self,
            *,
            attribute_matching_model: typing.Optional[builtins.str] = None,
            match_purpose: typing.Optional[builtins.str] = None,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMatchingWorkflowPropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An object which defines the list of matching rules to run in a matching workflow.

            :param attribute_matching_model: The comparison type. You can choose ``ONE_TO_ONE`` or ``MANY_TO_MANY`` as the ``attributeMatchingModel`` . If you choose ``ONE_TO_ONE`` , the system can only match attributes if the sub-types are an exact match. For example, for the ``Email`` attribute type, the system will only consider it a match if the value of the ``Email`` field of Profile A matches the value of the ``Email`` field of Profile B. If you choose ``MANY_TO_MANY`` , the system can match attributes across the sub-types of an attribute type. For example, if the value of the ``Email`` field of Profile A and the value of ``BusinessEmail`` field of Profile B matches, the two profiles are matched on the ``Email`` attribute type.
            :param match_purpose: An indicator of whether to generate IDs and index the data or not. If you choose ``IDENTIFIER_GENERATION`` , the process generates IDs and indexes the data. If you choose ``INDEXING`` , the process indexes the data without generating IDs.
            :param rules: A list of ``Rule`` objects, each of which have fields ``RuleName`` and ``MatchingKeys`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-rulebasedproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                rule_based_properties_property = entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleBasedPropertiesProperty(
                    attribute_matching_model="attributeMatchingModel",
                    match_purpose="matchPurpose",
                    rules=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleProperty(
                        matching_keys=["matchingKeys"],
                        rule_name="ruleName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__875b34aed58ef1b93bad2c3e75e2d6167795b78777b701ec861e5b1f1345aede)
                check_type(argname="argument attribute_matching_model", value=attribute_matching_model, expected_type=type_hints["attribute_matching_model"])
                check_type(argname="argument match_purpose", value=match_purpose, expected_type=type_hints["match_purpose"])
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_matching_model is not None:
                self._values["attribute_matching_model"] = attribute_matching_model
            if match_purpose is not None:
                self._values["match_purpose"] = match_purpose
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def attribute_matching_model(self) -> typing.Optional[builtins.str]:
            '''The comparison type. You can choose ``ONE_TO_ONE`` or ``MANY_TO_MANY`` as the ``attributeMatchingModel`` .

            If you choose ``ONE_TO_ONE`` , the system can only match attributes if the sub-types are an exact match. For example, for the ``Email`` attribute type, the system will only consider it a match if the value of the ``Email`` field of Profile A matches the value of the ``Email`` field of Profile B.

            If you choose ``MANY_TO_MANY`` , the system can match attributes across the sub-types of an attribute type. For example, if the value of the ``Email`` field of Profile A and the value of ``BusinessEmail`` field of Profile B matches, the two profiles are matched on the ``Email`` attribute type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-rulebasedproperties.html#cfn-entityresolution-matchingworkflow-rulebasedproperties-attributematchingmodel
            '''
            result = self._values.get("attribute_matching_model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def match_purpose(self) -> typing.Optional[builtins.str]:
            '''An indicator of whether to generate IDs and index the data or not.

            If you choose ``IDENTIFIER_GENERATION`` , the process generates IDs and indexes the data.

            If you choose ``INDEXING`` , the process indexes the data without generating IDs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-rulebasedproperties.html#cfn-entityresolution-matchingworkflow-rulebasedproperties-matchpurpose
            '''
            result = self._values.get("match_purpose")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.RuleProperty"]]]]:
            '''A list of ``Rule`` objects, each of which have fields ``RuleName`` and ``MatchingKeys`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-rulebasedproperties.html#cfn-entityresolution-matchingworkflow-rulebasedproperties-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.RuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleBasedPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowPropsMixin.RuleConditionPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class RuleConditionPropertiesProperty:
        def __init__(
            self,
            *,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMatchingWorkflowPropsMixin.RuleConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The properties of a rule condition that provides the ability to use more complex syntax.

            :param rules: A list of rule objects, each of which have fields ``ruleName`` and ``condition`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-ruleconditionproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                rule_condition_properties_property = entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleConditionPropertiesProperty(
                    rules=[entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleConditionProperty(
                        condition="condition",
                        rule_name="ruleName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dc7a8de7aef83b6877b4fbe07bc1eff6e273abc8ae82fe8c598a9e6af8d998b2)
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.RuleConditionProperty"]]]]:
            '''A list of rule objects, each of which have fields ``ruleName`` and ``condition`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-ruleconditionproperties.html#cfn-entityresolution-matchingworkflow-ruleconditionproperties-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchingWorkflowPropsMixin.RuleConditionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleConditionPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowPropsMixin.RuleConditionProperty",
        jsii_struct_bases=[],
        name_mapping={"condition": "condition", "rule_name": "ruleName"},
    )
    class RuleConditionProperty:
        def __init__(
            self,
            *,
            condition: typing.Optional[builtins.str] = None,
            rule_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that defines the ``ruleCondition`` and the ``ruleName`` to use in a matching workflow.

            :param condition: A statement that specifies the conditions for a matching rule. If your data is accurate, use an Exact matching function: ``Exact`` or ``ExactManyToMany`` . If your data has variations in spelling or pronunciation, use a Fuzzy matching function: ``Cosine`` , ``Levenshtein`` , or ``Soundex`` . Use operators if you want to combine ( ``AND`` ), separate ( ``OR`` ), or group matching functions ``(...)`` . For example: ``(Cosine(a, 10) AND Exact(b, true)) OR ExactManyToMany(c, d)``
            :param rule_name: A name for the matching rule. For example: ``Rule1``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-rulecondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                rule_condition_property = entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleConditionProperty(
                    condition="condition",
                    rule_name="ruleName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93abefea5dfd05e8f6a358ac9dff06ee05c7c9e1f66e779bd08c91e036012405)
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition is not None:
                self._values["condition"] = condition
            if rule_name is not None:
                self._values["rule_name"] = rule_name

        @builtins.property
        def condition(self) -> typing.Optional[builtins.str]:
            '''A statement that specifies the conditions for a matching rule.

            If your data is accurate, use an Exact matching function: ``Exact`` or ``ExactManyToMany`` .

            If your data has variations in spelling or pronunciation, use a Fuzzy matching function: ``Cosine`` , ``Levenshtein`` , or ``Soundex`` .

            Use operators if you want to combine ( ``AND`` ), separate ( ``OR`` ), or group matching functions ``(...)`` .

            For example: ``(Cosine(a, 10) AND Exact(b, true)) OR ExactManyToMany(c, d)``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-rulecondition.html#cfn-entityresolution-matchingworkflow-rulecondition-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_name(self) -> typing.Optional[builtins.str]:
            '''A name for the matching rule.

            For example: ``Rule1``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-rulecondition.html#cfn-entityresolution-matchingworkflow-rulecondition-rulename
            '''
            result = self._values.get("rule_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowPropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={"matching_keys": "matchingKeys", "rule_name": "ruleName"},
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            matching_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
            rule_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object containing the ``ruleName`` and ``matchingKeys`` .

            :param matching_keys: A list of ``MatchingKeys`` . The ``MatchingKeys`` must have been defined in the ``SchemaMapping`` . Two records are considered to match according to this rule if all of the ``MatchingKeys`` match.
            :param rule_name: A name for the matching rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                rule_property = entityresolution_mixins.CfnMatchingWorkflowPropsMixin.RuleProperty(
                    matching_keys=["matchingKeys"],
                    rule_name="ruleName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f67424b379c494cdf0f52783c145263587e8aff22af6d61d332ad7b11c0376ea)
                check_type(argname="argument matching_keys", value=matching_keys, expected_type=type_hints["matching_keys"])
                check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if matching_keys is not None:
                self._values["matching_keys"] = matching_keys
            if rule_name is not None:
                self._values["rule_name"] = rule_name

        @builtins.property
        def matching_keys(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of ``MatchingKeys`` .

            The ``MatchingKeys`` must have been defined in the ``SchemaMapping`` . Two records are considered to match according to this rule if all of the ``MatchingKeys`` match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-rule.html#cfn-entityresolution-matchingworkflow-rule-matchingkeys
            '''
            result = self._values.get("matching_keys")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def rule_name(self) -> typing.Optional[builtins.str]:
            '''A name for the matching rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-matchingworkflow-rule.html#cfn-entityresolution-matchingworkflow-rule-rulename
            '''
            result = self._values.get("rule_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnMatchingWorkflowWorkflowLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnMatchingWorkflowWorkflowLogs",
):
    '''Builder for CfnMatchingWorkflowLogsMixin to generate WORKFLOW_LOGS for CfnMatchingWorkflow.

    :cloudformationResource: AWS::EntityResolution::MatchingWorkflow
    :logType: WORKFLOW_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
        
        cfn_matching_workflow_workflow_logs = entityresolution_mixins.CfnMatchingWorkflowWorkflowLogs()
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
    ) -> CfnMatchingWorkflowLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2257f60341f3ac0ce4bb5c2d9279eff2a4cf56696f4e3747e11be5ba9717ea2f)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnMatchingWorkflowLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnMatchingWorkflowLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62f4c04076cf2ec5388c7ed48d97ed740d99f753b91b46a39a157d76af5d3144)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnMatchingWorkflowLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnMatchingWorkflowLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a646188826501c408843de84a3831e589b86d9928f3ac9573807567fc8e379)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnMatchingWorkflowLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnPolicyStatementMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "arn": "arn",
        "condition": "condition",
        "effect": "effect",
        "principal": "principal",
        "statement_id": "statementId",
    },
)
class CfnPolicyStatementMixinProps:
    def __init__(
        self,
        *,
        action: typing.Optional[typing.Sequence[builtins.str]] = None,
        arn: typing.Optional[builtins.str] = None,
        condition: typing.Optional[builtins.str] = None,
        effect: typing.Optional[builtins.str] = None,
        principal: typing.Optional[typing.Sequence[builtins.str]] = None,
        statement_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPolicyStatementPropsMixin.

        :param action: The action that the principal can use on the resource. For example, ``entityresolution:GetIdMappingJob`` , ``entityresolution:GetMatchingJob`` .
        :param arn: The Amazon Resource Name (ARN) of the resource that will be accessed by the principal.
        :param condition: A set of condition keys that you can use in key policies.
        :param effect: Determines whether the permissions specified in the policy are to be allowed ( ``Allow`` ) or denied ( ``Deny`` ). .. epigraph:: If you set the value of the ``effect`` parameter to ``Deny`` for the ``AddPolicyStatement`` operation, you must also set the value of the ``effect`` parameter in the ``policy`` to ``Deny`` for the ``PutPolicy`` operation.
        :param principal: The AWS service or AWS account that can access the resource defined as ARN.
        :param statement_id: A statement identifier that differentiates the statement from others in the same policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-policystatement.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
            
            cfn_policy_statement_mixin_props = entityresolution_mixins.CfnPolicyStatementMixinProps(
                action=["action"],
                arn="arn",
                condition="condition",
                effect="effect",
                principal=["principal"],
                statement_id="statementId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce2e2110c9c3ead5c9c8af4c6f56fa3b9b54fa990c1f961b9ef9db30d969707)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument statement_id", value=statement_id, expected_type=type_hints["statement_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if arn is not None:
            self._values["arn"] = arn
        if condition is not None:
            self._values["condition"] = condition
        if effect is not None:
            self._values["effect"] = effect
        if principal is not None:
            self._values["principal"] = principal
        if statement_id is not None:
            self._values["statement_id"] = statement_id

    @builtins.property
    def action(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The action that the principal can use on the resource.

        For example, ``entityresolution:GetIdMappingJob`` , ``entityresolution:GetMatchingJob`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-policystatement.html#cfn-entityresolution-policystatement-action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the resource that will be accessed by the principal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-policystatement.html#cfn-entityresolution-policystatement-arn
        '''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''A set of condition keys that you can use in key policies.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-policystatement.html#cfn-entityresolution-policystatement-condition
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def effect(self) -> typing.Optional[builtins.str]:
        '''Determines whether the permissions specified in the policy are to be allowed ( ``Allow`` ) or denied ( ``Deny`` ).

        .. epigraph::

           If you set the value of the ``effect`` parameter to ``Deny`` for the ``AddPolicyStatement`` operation, you must also set the value of the ``effect`` parameter in the ``policy`` to ``Deny`` for the ``PutPolicy`` operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-policystatement.html#cfn-entityresolution-policystatement-effect
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The AWS service or AWS account that can access the resource defined as ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-policystatement.html#cfn-entityresolution-policystatement-principal
        '''
        result = self._values.get("principal")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def statement_id(self) -> typing.Optional[builtins.str]:
        '''A statement identifier that differentiates the statement from others in the same policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-policystatement.html#cfn-entityresolution-policystatement-statementid
        '''
        result = self._values.get("statement_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyStatementMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPolicyStatementPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnPolicyStatementPropsMixin",
):
    '''Adds a policy statement object.

    To retrieve a list of existing policy statements, use the ``GetPolicy`` API.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-policystatement.html
    :cloudformationResource: AWS::EntityResolution::PolicyStatement
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
        
        cfn_policy_statement_props_mixin = entityresolution_mixins.CfnPolicyStatementPropsMixin(entityresolution_mixins.CfnPolicyStatementMixinProps(
            action=["action"],
            arn="arn",
            condition="condition",
            effect="effect",
            principal=["principal"],
            statement_id="statementId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPolicyStatementMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EntityResolution::PolicyStatement``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39920205d53fba8783ba1d6da459550a25c3dfd38b6d61a84acd0a1ac429e3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f770dc61c00c8afefe16dc69cec5781e76dc38041fb78db75402863d3ffa341)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bad98df7d11e837a234646aeeeee789978cb9f25459ed313adc5a69fd4eb844)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPolicyStatementMixinProps:
        return typing.cast(CfnPolicyStatementMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnSchemaMappingMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "mapped_input_fields": "mappedInputFields",
        "schema_name": "schemaName",
        "tags": "tags",
    },
)
class CfnSchemaMappingMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        mapped_input_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchemaMappingPropsMixin.SchemaInputAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        schema_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSchemaMappingPropsMixin.

        :param description: A description of the schema.
        :param mapped_input_fields: A list of ``MappedInputFields`` . Each ``MappedInputField`` corresponds to a column the source data table, and contains column name plus additional information that AWS Entity Resolution uses for matching.
        :param schema_name: The name of the schema. There can't be multiple ``SchemaMappings`` with the same name.
        :param tags: The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-schemamapping.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
            
            cfn_schema_mapping_mixin_props = entityresolution_mixins.CfnSchemaMappingMixinProps(
                description="description",
                mapped_input_fields=[entityresolution_mixins.CfnSchemaMappingPropsMixin.SchemaInputAttributeProperty(
                    field_name="fieldName",
                    group_name="groupName",
                    hashed=False,
                    match_key="matchKey",
                    sub_type="subType",
                    type="type"
                )],
                schema_name="schemaName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f7171f5577d10e2e18c4a5f8728ea8ee28ea1c7960f9ade75e06d0f7beb7757)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument mapped_input_fields", value=mapped_input_fields, expected_type=type_hints["mapped_input_fields"])
            check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if mapped_input_fields is not None:
            self._values["mapped_input_fields"] = mapped_input_fields
        if schema_name is not None:
            self._values["schema_name"] = schema_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the schema.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-schemamapping.html#cfn-entityresolution-schemamapping-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mapped_input_fields(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchemaMappingPropsMixin.SchemaInputAttributeProperty"]]]]:
        '''A list of ``MappedInputFields`` .

        Each ``MappedInputField`` corresponds to a column the source data table, and contains column name plus additional information that AWS Entity Resolution uses for matching.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-schemamapping.html#cfn-entityresolution-schemamapping-mappedinputfields
        '''
        result = self._values.get("mapped_input_fields")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchemaMappingPropsMixin.SchemaInputAttributeProperty"]]]], result)

    @builtins.property
    def schema_name(self) -> typing.Optional[builtins.str]:
        '''The name of the schema.

        There can't be multiple ``SchemaMappings`` with the same name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-schemamapping.html#cfn-entityresolution-schemamapping-schemaname
        '''
        result = self._values.get("schema_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-schemamapping.html#cfn-entityresolution-schemamapping-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSchemaMappingMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSchemaMappingPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnSchemaMappingPropsMixin",
):
    '''Creates a schema mapping, which defines the schema of the input customer records table.

    The ``SchemaMapping`` also provides AWS Entity Resolution with some metadata about the table, such as the attribute types of the columns and which columns to match on.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-entityresolution-schemamapping.html
    :cloudformationResource: AWS::EntityResolution::SchemaMapping
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
        
        cfn_schema_mapping_props_mixin = entityresolution_mixins.CfnSchemaMappingPropsMixin(entityresolution_mixins.CfnSchemaMappingMixinProps(
            description="description",
            mapped_input_fields=[entityresolution_mixins.CfnSchemaMappingPropsMixin.SchemaInputAttributeProperty(
                field_name="fieldName",
                group_name="groupName",
                hashed=False,
                match_key="matchKey",
                sub_type="subType",
                type="type"
            )],
            schema_name="schemaName",
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
        props: typing.Union[CfnSchemaMappingMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EntityResolution::SchemaMapping``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9384b30f69c51cb7a6e52106c8f4026909dbad6d9249e4f222bcdeaf88689b00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__872e0615a52ee9b0e0b4557f906eda3470b976744ab3cd2236657b674220bd82)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1c22733f349d20a71d1eefd1b1e811a2d0c37606792934ea51bf4a430862e5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSchemaMappingMixinProps:
        return typing.cast(CfnSchemaMappingMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_entityresolution.mixins.CfnSchemaMappingPropsMixin.SchemaInputAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field_name": "fieldName",
            "group_name": "groupName",
            "hashed": "hashed",
            "match_key": "matchKey",
            "sub_type": "subType",
            "type": "type",
        },
    )
    class SchemaInputAttributeProperty:
        def __init__(
            self,
            *,
            field_name: typing.Optional[builtins.str] = None,
            group_name: typing.Optional[builtins.str] = None,
            hashed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            match_key: typing.Optional[builtins.str] = None,
            sub_type: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A configuration object for defining input data fields in AWS Entity Resolution .

            The ``SchemaInputAttribute`` specifies how individual fields in your input data should be processed and matched.

            :param field_name: A string containing the field name.
            :param group_name: A string that instructs AWS Entity Resolution to combine several columns into a unified column with the identical attribute type. For example, when working with columns such as ``NAME_FIRST`` , ``NAME_MIDDLE`` , and ``NAME_LAST`` , assigning them a common ``groupName`` will prompt AWS Entity Resolution to concatenate them into a single value.
            :param hashed: Indicates if the column values are hashed in the schema input. If the value is set to ``TRUE`` , the column values are hashed. If the value is set to ``FALSE`` , the column values are cleartext.
            :param match_key: A key that allows grouping of multiple input attributes into a unified matching group. For example, consider a scenario where the source table contains various addresses, such as ``business_address`` and ``shipping_address`` . By assigning a ``matchKey`` called ``address`` to both attributes, AWS Entity Resolution will match records across these fields to create a consolidated matching group. If no ``matchKey`` is specified for a column, it won't be utilized for matching purposes but will still be included in the output table.
            :param sub_type: The subtype of the attribute, selected from a list of values.
            :param type: The type of the attribute, selected from a list of values. LiveRamp supports: ``NAME`` | ``NAME_FIRST`` | ``NAME_MIDDLE`` | ``NAME_LAST`` | ``ADDRESS`` | ``ADDRESS_STREET1`` | ``ADDRESS_STREET2`` | ``ADDRESS_STREET3`` | ``ADDRESS_CITY`` | ``ADDRESS_STATE`` | ``ADDRESS_COUNTRY`` | ``ADDRESS_POSTALCODE`` | ``PHONE`` | ``PHONE_NUMBER`` | ``EMAIL_ADDRESS`` | ``UNIQUE_ID`` | ``PROVIDER_ID`` TransUnion supports: ``NAME`` | ``NAME_FIRST`` | ``NAME_LAST`` | ``ADDRESS`` | ``ADDRESS_CITY`` | ``ADDRESS_STATE`` | ``ADDRESS_COUNTRY`` | ``ADDRESS_POSTALCODE`` | ``PHONE_NUMBER`` | ``EMAIL_ADDRESS`` | ``UNIQUE_ID`` | ``IPV4`` | ``IPV6`` | ``MAID`` Unified ID 2.0 supports: ``PHONE_NUMBER`` | ``EMAIL_ADDRESS`` | ``UNIQUE_ID`` .. epigraph:: Normalization is only supported for ``NAME`` , ``ADDRESS`` , ``PHONE`` , and ``EMAIL_ADDRESS`` . If you want to normalize ``NAME_FIRST`` , ``NAME_MIDDLE`` , and ``NAME_LAST`` , you must group them by assigning them to the ``NAME`` ``groupName`` . If you want to normalize ``ADDRESS_STREET1`` , ``ADDRESS_STREET2`` , ``ADDRESS_STREET3`` , ``ADDRESS_CITY`` , ``ADDRESS_STATE`` , ``ADDRESS_COUNTRY`` , and ``ADDRESS_POSTALCODE`` , you must group them by assigning them to the ``ADDRESS`` ``groupName`` . If you want to normalize ``PHONE_NUMBER`` and ``PHONE_COUNTRYCODE`` , you must group them by assigning them to the ``PHONE`` ``groupName`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-schemamapping-schemainputattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_entityresolution import mixins as entityresolution_mixins
                
                schema_input_attribute_property = entityresolution_mixins.CfnSchemaMappingPropsMixin.SchemaInputAttributeProperty(
                    field_name="fieldName",
                    group_name="groupName",
                    hashed=False,
                    match_key="matchKey",
                    sub_type="subType",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b284b3b70325aa4d40005a7f30b0d92678f36275e80e09db4e44edf73f209dd4)
                check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
                check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
                check_type(argname="argument hashed", value=hashed, expected_type=type_hints["hashed"])
                check_type(argname="argument match_key", value=match_key, expected_type=type_hints["match_key"])
                check_type(argname="argument sub_type", value=sub_type, expected_type=type_hints["sub_type"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field_name is not None:
                self._values["field_name"] = field_name
            if group_name is not None:
                self._values["group_name"] = group_name
            if hashed is not None:
                self._values["hashed"] = hashed
            if match_key is not None:
                self._values["match_key"] = match_key
            if sub_type is not None:
                self._values["sub_type"] = sub_type
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def field_name(self) -> typing.Optional[builtins.str]:
            '''A string containing the field name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-schemamapping-schemainputattribute.html#cfn-entityresolution-schemamapping-schemainputattribute-fieldname
            '''
            result = self._values.get("field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_name(self) -> typing.Optional[builtins.str]:
            '''A string that instructs AWS Entity Resolution to combine several columns into a unified column with the identical attribute type.

            For example, when working with columns such as ``NAME_FIRST`` , ``NAME_MIDDLE`` , and ``NAME_LAST`` , assigning them a common ``groupName`` will prompt AWS Entity Resolution to concatenate them into a single value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-schemamapping-schemainputattribute.html#cfn-entityresolution-schemamapping-schemainputattribute-groupname
            '''
            result = self._values.get("group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hashed(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates if the column values are hashed in the schema input.

            If the value is set to ``TRUE`` , the column values are hashed.

            If the value is set to ``FALSE`` , the column values are cleartext.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-schemamapping-schemainputattribute.html#cfn-entityresolution-schemamapping-schemainputattribute-hashed
            '''
            result = self._values.get("hashed")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def match_key(self) -> typing.Optional[builtins.str]:
            '''A key that allows grouping of multiple input attributes into a unified matching group.

            For example, consider a scenario where the source table contains various addresses, such as ``business_address`` and ``shipping_address`` . By assigning a ``matchKey`` called ``address`` to both attributes, AWS Entity Resolution will match records across these fields to create a consolidated matching group.

            If no ``matchKey`` is specified for a column, it won't be utilized for matching purposes but will still be included in the output table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-schemamapping-schemainputattribute.html#cfn-entityresolution-schemamapping-schemainputattribute-matchkey
            '''
            result = self._values.get("match_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sub_type(self) -> typing.Optional[builtins.str]:
            '''The subtype of the attribute, selected from a list of values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-schemamapping-schemainputattribute.html#cfn-entityresolution-schemamapping-schemainputattribute-subtype
            '''
            result = self._values.get("sub_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the attribute, selected from a list of values.

            LiveRamp supports: ``NAME`` | ``NAME_FIRST`` | ``NAME_MIDDLE`` | ``NAME_LAST`` | ``ADDRESS`` | ``ADDRESS_STREET1`` | ``ADDRESS_STREET2`` | ``ADDRESS_STREET3`` | ``ADDRESS_CITY`` | ``ADDRESS_STATE`` | ``ADDRESS_COUNTRY`` | ``ADDRESS_POSTALCODE`` | ``PHONE`` | ``PHONE_NUMBER`` | ``EMAIL_ADDRESS`` | ``UNIQUE_ID`` | ``PROVIDER_ID``

            TransUnion supports: ``NAME`` | ``NAME_FIRST`` | ``NAME_LAST`` | ``ADDRESS`` | ``ADDRESS_CITY`` | ``ADDRESS_STATE`` | ``ADDRESS_COUNTRY`` | ``ADDRESS_POSTALCODE`` | ``PHONE_NUMBER`` | ``EMAIL_ADDRESS`` | ``UNIQUE_ID`` | ``IPV4`` | ``IPV6`` | ``MAID``

            Unified ID 2.0 supports: ``PHONE_NUMBER`` | ``EMAIL_ADDRESS`` | ``UNIQUE_ID``
            .. epigraph::

               Normalization is only supported for ``NAME`` , ``ADDRESS`` , ``PHONE`` , and ``EMAIL_ADDRESS`` .

               If you want to normalize ``NAME_FIRST`` , ``NAME_MIDDLE`` , and ``NAME_LAST`` , you must group them by assigning them to the ``NAME`` ``groupName`` .

               If you want to normalize ``ADDRESS_STREET1`` , ``ADDRESS_STREET2`` , ``ADDRESS_STREET3`` , ``ADDRESS_CITY`` , ``ADDRESS_STATE`` , ``ADDRESS_COUNTRY`` , and ``ADDRESS_POSTALCODE`` , you must group them by assigning them to the ``ADDRESS`` ``groupName`` .

               If you want to normalize ``PHONE_NUMBER`` and ``PHONE_COUNTRYCODE`` , you must group them by assigning them to the ``PHONE`` ``groupName`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-entityresolution-schemamapping-schemainputattribute.html#cfn-entityresolution-schemamapping-schemainputattribute-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaInputAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnIdMappingWorkflowLogsMixin",
    "CfnIdMappingWorkflowMixinProps",
    "CfnIdMappingWorkflowPropsMixin",
    "CfnIdMappingWorkflowWorkflowLogs",
    "CfnIdNamespaceMixinProps",
    "CfnIdNamespacePropsMixin",
    "CfnMatchingWorkflowLogsMixin",
    "CfnMatchingWorkflowMixinProps",
    "CfnMatchingWorkflowPropsMixin",
    "CfnMatchingWorkflowWorkflowLogs",
    "CfnPolicyStatementMixinProps",
    "CfnPolicyStatementPropsMixin",
    "CfnSchemaMappingMixinProps",
    "CfnSchemaMappingPropsMixin",
]

publication.publish()

def _typecheckingstub__f8319c797870fa92349f44077970fe8648468e2795b9542d5ca9411c4ed149e9(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d87cdbf6f8b09b8206a9ba5b3013799b7cf869f2fa739acaf9ee868341cf8c4(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e558b8ce6c2ccef5e30fb2c16ebf9979785916fa1ff01f6dcec2603fb764fba8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872ed9683a8c0f8dfb03136eed0491f63b743e00a9a2867b87c763d0ae9d28da(
    *,
    description: typing.Optional[builtins.str] = None,
    id_mapping_incremental_run_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdMappingWorkflowPropsMixin.IdMappingIncrementalRunConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    id_mapping_techniques: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdMappingWorkflowPropsMixin.IdMappingTechniquesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    input_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowInputSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    output_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdMappingWorkflowPropsMixin.IdMappingWorkflowOutputSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    workflow_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92fc2fd00dfb7dad77ea27b98e6573256f20953223aa1e8fa8b47fa16ee03b22(
    props: typing.Union[CfnIdMappingWorkflowMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e78a282d047c939676e0eb7a1f9a0377c7cac23ec5311f3294a483df2dfb786(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62b286c89e09ad929ae34cfc5c5b319b58f4b2f395e64678141d86df3777c67(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f60850a287041aeea15ce3a5492dfd44c4934c5036750a4efa25e4946d38002(
    *,
    incremental_run_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0086ada6ae07164de9c0264b0d94bad50ebf16f356a841bcd825f0f67d774630(
    *,
    attribute_matching_model: typing.Optional[builtins.str] = None,
    record_matching_model: typing.Optional[builtins.str] = None,
    rule_definition_type: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdMappingWorkflowPropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07fe89f0b2e9629c9c824133c96582687b0ceaa77728a260410923f0fa188fd(
    *,
    id_mapping_type: typing.Optional[builtins.str] = None,
    normalization_version: typing.Optional[builtins.str] = None,
    provider_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdMappingWorkflowPropsMixin.ProviderPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_based_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdMappingWorkflowPropsMixin.IdMappingRuleBasedPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03475da1b07f3106a4a5471fd83f87889a822ee744480b83a7e593ae7da9ca4(
    *,
    input_source_arn: typing.Optional[builtins.str] = None,
    schema_arn: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe74982bfa6737143f1df4ac6bc06356d755b62e82e1cf043d11dc742183c870(
    *,
    kms_arn: typing.Optional[builtins.str] = None,
    output_s3_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6eea13c22074734c9f2599c1197d57a30d7647f1aa5bda94d5f84c6384cc8e(
    *,
    intermediate_s3_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7833b17b3fb027301e18d8113e4706598bb03e030b9128e378979983d7e11799(
    *,
    intermediate_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdMappingWorkflowPropsMixin.IntermediateSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    provider_configuration: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    provider_service_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f871ae72e0f47a9dc90cbd55f6ebab18a602dd0b0e7721fae9e266a1cec6b53(
    *,
    matching_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3efe0cff0ff4600833c55d1c985fc32b7d8dcad347cda41b6079e3485e5e6e2c(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab79b7040061e1d0b085b12c2f3432fc871a7d4338f602047fec39483a97cba(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c221bcb56c45f3dbd005ebee24ed401a32efcfff33a39a56e20c1442bc844e(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92918df5d58e1f792127627b9d8a4549cc4e1b43655d5bc09acb645e24501565(
    *,
    description: typing.Optional[builtins.str] = None,
    id_mapping_workflow_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdNamespacePropsMixin.IdNamespaceIdMappingWorkflowPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    id_namespace_name: typing.Optional[builtins.str] = None,
    input_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdNamespacePropsMixin.IdNamespaceInputSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d155158cf121a939f6590b382d22cd641b7299801a6d1137eb274f3d52002e9e(
    props: typing.Union[CfnIdNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74ec1f5cd5bdd613ecbc31fa48c0cf82dfa3a3ad9f4eef5e9a813efb3ae293b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825df660df3db33ec1f10eda0c641b3fa857157a13dbe4509ec9ab5daace22ea(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc3ea07e64905084a9ef9c333f31ad705397c84181663cad487dafc13cc0442(
    *,
    id_mapping_type: typing.Optional[builtins.str] = None,
    provider_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdNamespacePropsMixin.NamespaceProviderPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_based_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdNamespacePropsMixin.NamespaceRuleBasedPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c519617e4e36ea6093e1483848c7044aaecdcf22149ec43f97d51617c712fa0f(
    *,
    input_source_arn: typing.Optional[builtins.str] = None,
    schema_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2ffb05cba7610bf4b90dbe0ac58e3ef6c5963465f08792c91f016db4dcda82(
    *,
    provider_configuration: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    provider_service_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458fd11728fefbd547681c825c04ded5aea1af8a40485418cadfbf72cd2bb64e(
    *,
    attribute_matching_model: typing.Optional[builtins.str] = None,
    record_matching_models: typing.Optional[typing.Sequence[builtins.str]] = None,
    rule_definition_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdNamespacePropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c3dfff14d95c2b780d6a677f9ef854948f39e634c2a2949bcaf774d7b32cc2(
    *,
    matching_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2a2f8f41e56803947feeac063141099a92bd03d48742c1294fd888e5c86f3f(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32fe9df30012d7ee5ff8ad68526b3ca56aa553a067d710540e6da25435985e55(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f0125aaab9fb5c7fe239c86824ba8eb20303f55113b06eb498ed52aeef2cca(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f24aa8b48e66db77e27e4f7115bb80b5b27f6a17a962cb140c19898694371ed(
    *,
    description: typing.Optional[builtins.str] = None,
    incremental_run_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMatchingWorkflowPropsMixin.IncrementalRunConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    input_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMatchingWorkflowPropsMixin.InputSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    output_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMatchingWorkflowPropsMixin.OutputSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resolution_techniques: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMatchingWorkflowPropsMixin.ResolutionTechniquesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    workflow_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f449b46dec1c6dfa62a7a669c6bc327a1568c7d6286f1641a9cd5c20bad861c(
    props: typing.Union[CfnMatchingWorkflowMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae9930f751d4e311361b198b824c26790a1b183b0ceb3b03012554cb7aad44c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba61f6dbff2ed563ad16b6a3db5f183f75d4ebee70dbbf72b13c10763fe4305(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20dd2505489de2bacc4a3e0b5eda8bd6f5a9c355c250de4a988442fd882d86a(
    *,
    incremental_run_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09059cd81838eeef0bf03b9d702fc94bdf0ddb41c47d85c667029dbe9c754d9b(
    *,
    apply_normalization: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    input_source_arn: typing.Optional[builtins.str] = None,
    schema_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531709d47b71d4503e8735a2c5d63d276a0956fa10f6fe00eb3c83ac490b5821(
    *,
    intermediate_s3_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1699c9f415fc9759a56c2227c29343071594a40719e14e7e1cc442ac1878f0d9(
    *,
    hashed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a70b30ce5b5ccffa3185350937bf9746d5621d6165510d2fc2f1bc3318645f(
    *,
    apply_normalization: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    kms_arn: typing.Optional[builtins.str] = None,
    output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMatchingWorkflowPropsMixin.OutputAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    output_s3_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18a80242336ee811f0445ac0530befbdfd7eaf96c8a539009bf2c3c0dd12829(
    *,
    intermediate_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMatchingWorkflowPropsMixin.IntermediateSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    provider_configuration: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    provider_service_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40fd68d9d4bf08cdc4faf15c32386377fd240668045c4a5b489b1f3b929d474(
    *,
    provider_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMatchingWorkflowPropsMixin.ProviderPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resolution_type: typing.Optional[builtins.str] = None,
    rule_based_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMatchingWorkflowPropsMixin.RuleBasedPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_condition_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMatchingWorkflowPropsMixin.RuleConditionPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875b34aed58ef1b93bad2c3e75e2d6167795b78777b701ec861e5b1f1345aede(
    *,
    attribute_matching_model: typing.Optional[builtins.str] = None,
    match_purpose: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMatchingWorkflowPropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7a8de7aef83b6877b4fbe07bc1eff6e273abc8ae82fe8c598a9e6af8d998b2(
    *,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMatchingWorkflowPropsMixin.RuleConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93abefea5dfd05e8f6a358ac9dff06ee05c7c9e1f66e779bd08c91e036012405(
    *,
    condition: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67424b379c494cdf0f52783c145263587e8aff22af6d61d332ad7b11c0376ea(
    *,
    matching_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2257f60341f3ac0ce4bb5c2d9279eff2a4cf56696f4e3747e11be5ba9717ea2f(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f4c04076cf2ec5388c7ed48d97ed740d99f753b91b46a39a157d76af5d3144(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a646188826501c408843de84a3831e589b86d9928f3ac9573807567fc8e379(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce2e2110c9c3ead5c9c8af4c6f56fa3b9b54fa990c1f961b9ef9db30d969707(
    *,
    action: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[builtins.str] = None,
    condition: typing.Optional[builtins.str] = None,
    effect: typing.Optional[builtins.str] = None,
    principal: typing.Optional[typing.Sequence[builtins.str]] = None,
    statement_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39920205d53fba8783ba1d6da459550a25c3dfd38b6d61a84acd0a1ac429e3a(
    props: typing.Union[CfnPolicyStatementMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f770dc61c00c8afefe16dc69cec5781e76dc38041fb78db75402863d3ffa341(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bad98df7d11e837a234646aeeeee789978cb9f25459ed313adc5a69fd4eb844(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7171f5577d10e2e18c4a5f8728ea8ee28ea1c7960f9ade75e06d0f7beb7757(
    *,
    description: typing.Optional[builtins.str] = None,
    mapped_input_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchemaMappingPropsMixin.SchemaInputAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    schema_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9384b30f69c51cb7a6e52106c8f4026909dbad6d9249e4f222bcdeaf88689b00(
    props: typing.Union[CfnSchemaMappingMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872e0615a52ee9b0e0b4557f906eda3470b976744ab3cd2236657b674220bd82(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1c22733f349d20a71d1eefd1b1e811a2d0c37606792934ea51bf4a430862e5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b284b3b70325aa4d40005a7f30b0d92678f36275e80e09db4e44edf73f209dd4(
    *,
    field_name: typing.Optional[builtins.str] = None,
    group_name: typing.Optional[builtins.str] = None,
    hashed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    match_key: typing.Optional[builtins.str] = None,
    sub_type: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
