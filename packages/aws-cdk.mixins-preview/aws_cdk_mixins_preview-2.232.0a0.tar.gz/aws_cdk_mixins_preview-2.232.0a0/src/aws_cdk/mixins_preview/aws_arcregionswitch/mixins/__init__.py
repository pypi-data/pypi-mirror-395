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
    jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "associated_alarms": "associatedAlarms",
        "description": "description",
        "execution_role": "executionRole",
        "name": "name",
        "primary_region": "primaryRegion",
        "recovery_approach": "recoveryApproach",
        "recovery_time_objective_minutes": "recoveryTimeObjectiveMinutes",
        "regions": "regions",
        "tags": "tags",
        "triggers": "triggers",
        "workflows": "workflows",
    },
)
class CfnPlanMixinProps:
    def __init__(
        self,
        *,
        associated_alarms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.AssociatedAlarmProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_role: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        primary_region: typing.Optional[builtins.str] = None,
        recovery_approach: typing.Optional[builtins.str] = None,
        recovery_time_objective_minutes: typing.Optional[jsii.Number] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        triggers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.TriggerProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        workflows: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.WorkflowProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnPlanPropsMixin.

        :param associated_alarms: The associated application health alarms for a plan.
        :param description: The description for a plan.
        :param execution_role: The execution role for a plan.
        :param name: The name for a plan.
        :param primary_region: The primary Region for a plan.
        :param recovery_approach: The recovery approach for a Region switch plan, which can be active/active (activeActive) or active/passive (activePassive).
        :param recovery_time_objective_minutes: The recovery time objective for a plan.
        :param regions: The AWS Regions for a plan.
        :param tags: 
        :param triggers: The triggers for a plan.
        :param workflows: The workflows for a plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arcregionswitch-plan.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
            
            # step_property_: arcregionswitch_mixins.CfnPlanPropsMixin.StepProperty
            
            cfn_plan_mixin_props = arcregionswitch_mixins.CfnPlanMixinProps(
                associated_alarms={
                    "associated_alarms_key": arcregionswitch_mixins.CfnPlanPropsMixin.AssociatedAlarmProperty(
                        alarm_type="alarmType",
                        cross_account_role="crossAccountRole",
                        external_id="externalId",
                        resource_identifier="resourceIdentifier"
                    )
                },
                description="description",
                execution_role="executionRole",
                name="name",
                primary_region="primaryRegion",
                recovery_approach="recoveryApproach",
                recovery_time_objective_minutes=123,
                regions=["regions"],
                tags={
                    "tags_key": "tags"
                },
                triggers=[arcregionswitch_mixins.CfnPlanPropsMixin.TriggerProperty(
                    action="action",
                    conditions=[arcregionswitch_mixins.CfnPlanPropsMixin.TriggerConditionProperty(
                        associated_alarm_name="associatedAlarmName",
                        condition="condition"
                    )],
                    description="description",
                    min_delay_minutes_between_executions=123,
                    target_region="targetRegion"
                )],
                workflows=[arcregionswitch_mixins.CfnPlanPropsMixin.WorkflowProperty(
                    steps=[arcregionswitch_mixins.CfnPlanPropsMixin.StepProperty(
                        description="description",
                        execution_block_configuration=arcregionswitch_mixins.CfnPlanPropsMixin.ExecutionBlockConfigurationProperty(
                            arc_routing_control_config=arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlConfigurationProperty(
                                cross_account_role="crossAccountRole",
                                external_id="externalId",
                                region_and_routing_controls={
                                    "region_and_routing_controls_key": [arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlStateProperty(
                                        routing_control_arn="routingControlArn",
                                        state="state"
                                    )]
                                },
                                timeout_minutes=123
                            ),
                            custom_action_lambda_config=arcregionswitch_mixins.CfnPlanPropsMixin.CustomActionLambdaConfigurationProperty(
                                lambdas=[arcregionswitch_mixins.CfnPlanPropsMixin.LambdasProperty(
                                    arn="arn",
                                    cross_account_role="crossAccountRole",
                                    external_id="externalId"
                                )],
                                region_to_run="regionToRun",
                                retry_interval_minutes=123,
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.LambdaUngracefulProperty(
                                    behavior="behavior"
                                )
                            ),
                            ec2_asg_capacity_increase_config=arcregionswitch_mixins.CfnPlanPropsMixin.Ec2AsgCapacityIncreaseConfigurationProperty(
                                asgs=[arcregionswitch_mixins.CfnPlanPropsMixin.AsgProperty(
                                    arn="arn",
                                    cross_account_role="crossAccountRole",
                                    external_id="externalId"
                                )],
                                capacity_monitoring_approach="capacityMonitoringApproach",
                                target_percent=123,
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.Ec2UngracefulProperty(
                                    minimum_success_percentage=123
                                )
                            ),
                            ecs_capacity_increase_config=arcregionswitch_mixins.CfnPlanPropsMixin.EcsCapacityIncreaseConfigurationProperty(
                                capacity_monitoring_approach="capacityMonitoringApproach",
                                services=[arcregionswitch_mixins.CfnPlanPropsMixin.ServiceProperty(
                                    cluster_arn="clusterArn",
                                    cross_account_role="crossAccountRole",
                                    external_id="externalId",
                                    service_arn="serviceArn"
                                )],
                                target_percent=123,
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.EcsUngracefulProperty(
                                    minimum_success_percentage=123
                                )
                            ),
                            eks_resource_scaling_config=arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingConfigurationProperty(
                                capacity_monitoring_approach="capacityMonitoringApproach",
                                eks_clusters=[arcregionswitch_mixins.CfnPlanPropsMixin.EksClusterProperty(
                                    cluster_arn="clusterArn",
                                    cross_account_role="crossAccountRole",
                                    external_id="externalId"
                                )],
                                kubernetes_resource_type=arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesResourceTypeProperty(
                                    api_version="apiVersion",
                                    kind="kind"
                                ),
                                scaling_resources=[{
                                    "scaling_resources_key": {
                                        "scaling_resources_key": arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesScalingResourceProperty(
                                            hpa_name="hpaName",
                                            name="name",
                                            namespace="namespace"
                                        )
                                    }
                                }],
                                target_percent=123,
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingUngracefulProperty(
                                    minimum_success_percentage=123
                                )
                            ),
                            execution_approval_config=arcregionswitch_mixins.CfnPlanPropsMixin.ExecutionApprovalConfigurationProperty(
                                approval_role="approvalRole",
                                timeout_minutes=123
                            ),
                            global_aurora_config=arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraConfigurationProperty(
                                behavior="behavior",
                                cross_account_role="crossAccountRole",
                                database_cluster_arns=["databaseClusterArns"],
                                external_id="externalId",
                                global_cluster_identifier="globalClusterIdentifier",
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraUngracefulProperty(
                                    ungraceful="ungraceful"
                                )
                            ),
                            parallel_config=arcregionswitch_mixins.CfnPlanPropsMixin.ParallelExecutionBlockConfigurationProperty(
                                steps=[step_property_]
                            ),
                            region_switch_plan_config=arcregionswitch_mixins.CfnPlanPropsMixin.RegionSwitchPlanConfigurationProperty(
                                arn="arn",
                                cross_account_role="crossAccountRole",
                                external_id="externalId"
                            ),
                            route53_health_check_config=arcregionswitch_mixins.CfnPlanPropsMixin.Route53HealthCheckConfigurationProperty(
                                cross_account_role="crossAccountRole",
                                external_id="externalId",
                                hosted_zone_id="hostedZoneId",
                                record_name="recordName",
                                record_sets=[arcregionswitch_mixins.CfnPlanPropsMixin.Route53ResourceRecordSetProperty(
                                    record_set_identifier="recordSetIdentifier",
                                    region="region"
                                )],
                                timeout_minutes=123
                            )
                        ),
                        execution_block_type="executionBlockType",
                        name="name"
                    )],
                    workflow_description="workflowDescription",
                    workflow_target_action="workflowTargetAction",
                    workflow_target_region="workflowTargetRegion"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8386d5312f53d51ee1bdd200ee9303f9fe90a07e433c08f6a4386ac40d8f82ad)
            check_type(argname="argument associated_alarms", value=associated_alarms, expected_type=type_hints["associated_alarms"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument primary_region", value=primary_region, expected_type=type_hints["primary_region"])
            check_type(argname="argument recovery_approach", value=recovery_approach, expected_type=type_hints["recovery_approach"])
            check_type(argname="argument recovery_time_objective_minutes", value=recovery_time_objective_minutes, expected_type=type_hints["recovery_time_objective_minutes"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
            check_type(argname="argument workflows", value=workflows, expected_type=type_hints["workflows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if associated_alarms is not None:
            self._values["associated_alarms"] = associated_alarms
        if description is not None:
            self._values["description"] = description
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if name is not None:
            self._values["name"] = name
        if primary_region is not None:
            self._values["primary_region"] = primary_region
        if recovery_approach is not None:
            self._values["recovery_approach"] = recovery_approach
        if recovery_time_objective_minutes is not None:
            self._values["recovery_time_objective_minutes"] = recovery_time_objective_minutes
        if regions is not None:
            self._values["regions"] = regions
        if tags is not None:
            self._values["tags"] = tags
        if triggers is not None:
            self._values["triggers"] = triggers
        if workflows is not None:
            self._values["workflows"] = workflows

    @builtins.property
    def associated_alarms(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.AssociatedAlarmProperty"]]]]:
        '''The associated application health alarms for a plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arcregionswitch-plan.html#cfn-arcregionswitch-plan-associatedalarms
        '''
        result = self._values.get("associated_alarms")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.AssociatedAlarmProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for a plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arcregionswitch-plan.html#cfn-arcregionswitch-plan-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[builtins.str]:
        '''The execution role for a plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arcregionswitch-plan.html#cfn-arcregionswitch-plan-executionrole
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for a plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arcregionswitch-plan.html#cfn-arcregionswitch-plan-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_region(self) -> typing.Optional[builtins.str]:
        '''The primary Region for a plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arcregionswitch-plan.html#cfn-arcregionswitch-plan-primaryregion
        '''
        result = self._values.get("primary_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recovery_approach(self) -> typing.Optional[builtins.str]:
        '''The recovery approach for a Region switch plan, which can be active/active (activeActive) or active/passive (activePassive).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arcregionswitch-plan.html#cfn-arcregionswitch-plan-recoveryapproach
        '''
        result = self._values.get("recovery_approach")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recovery_time_objective_minutes(self) -> typing.Optional[jsii.Number]:
        '''The recovery time objective for a plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arcregionswitch-plan.html#cfn-arcregionswitch-plan-recoverytimeobjectiveminutes
        '''
        result = self._values.get("recovery_time_objective_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The AWS Regions for a plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arcregionswitch-plan.html#cfn-arcregionswitch-plan-regions
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arcregionswitch-plan.html#cfn-arcregionswitch-plan-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def triggers(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.TriggerProperty"]]]]:
        '''The triggers for a plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arcregionswitch-plan.html#cfn-arcregionswitch-plan-triggers
        '''
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.TriggerProperty"]]]], result)

    @builtins.property
    def workflows(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.WorkflowProperty"]]]]:
        '''The workflows for a plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arcregionswitch-plan.html#cfn-arcregionswitch-plan-workflows
        '''
        result = self._values.get("workflows")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.WorkflowProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPlanMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPlanPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin",
):
    '''Represents a Region switch plan.

    A plan defines the steps required to shift traffic from one AWS Region to another.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arcregionswitch-plan.html
    :cloudformationResource: AWS::ARCRegionSwitch::Plan
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
        
        # step_property_: arcregionswitch_mixins.CfnPlanPropsMixin.StepProperty
        
        cfn_plan_props_mixin = arcregionswitch_mixins.CfnPlanPropsMixin(arcregionswitch_mixins.CfnPlanMixinProps(
            associated_alarms={
                "associated_alarms_key": arcregionswitch_mixins.CfnPlanPropsMixin.AssociatedAlarmProperty(
                    alarm_type="alarmType",
                    cross_account_role="crossAccountRole",
                    external_id="externalId",
                    resource_identifier="resourceIdentifier"
                )
            },
            description="description",
            execution_role="executionRole",
            name="name",
            primary_region="primaryRegion",
            recovery_approach="recoveryApproach",
            recovery_time_objective_minutes=123,
            regions=["regions"],
            tags={
                "tags_key": "tags"
            },
            triggers=[arcregionswitch_mixins.CfnPlanPropsMixin.TriggerProperty(
                action="action",
                conditions=[arcregionswitch_mixins.CfnPlanPropsMixin.TriggerConditionProperty(
                    associated_alarm_name="associatedAlarmName",
                    condition="condition"
                )],
                description="description",
                min_delay_minutes_between_executions=123,
                target_region="targetRegion"
            )],
            workflows=[arcregionswitch_mixins.CfnPlanPropsMixin.WorkflowProperty(
                steps=[arcregionswitch_mixins.CfnPlanPropsMixin.StepProperty(
                    description="description",
                    execution_block_configuration=arcregionswitch_mixins.CfnPlanPropsMixin.ExecutionBlockConfigurationProperty(
                        arc_routing_control_config=arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlConfigurationProperty(
                            cross_account_role="crossAccountRole",
                            external_id="externalId",
                            region_and_routing_controls={
                                "region_and_routing_controls_key": [arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlStateProperty(
                                    routing_control_arn="routingControlArn",
                                    state="state"
                                )]
                            },
                            timeout_minutes=123
                        ),
                        custom_action_lambda_config=arcregionswitch_mixins.CfnPlanPropsMixin.CustomActionLambdaConfigurationProperty(
                            lambdas=[arcregionswitch_mixins.CfnPlanPropsMixin.LambdasProperty(
                                arn="arn",
                                cross_account_role="crossAccountRole",
                                external_id="externalId"
                            )],
                            region_to_run="regionToRun",
                            retry_interval_minutes=123,
                            timeout_minutes=123,
                            ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.LambdaUngracefulProperty(
                                behavior="behavior"
                            )
                        ),
                        ec2_asg_capacity_increase_config=arcregionswitch_mixins.CfnPlanPropsMixin.Ec2AsgCapacityIncreaseConfigurationProperty(
                            asgs=[arcregionswitch_mixins.CfnPlanPropsMixin.AsgProperty(
                                arn="arn",
                                cross_account_role="crossAccountRole",
                                external_id="externalId"
                            )],
                            capacity_monitoring_approach="capacityMonitoringApproach",
                            target_percent=123,
                            timeout_minutes=123,
                            ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.Ec2UngracefulProperty(
                                minimum_success_percentage=123
                            )
                        ),
                        ecs_capacity_increase_config=arcregionswitch_mixins.CfnPlanPropsMixin.EcsCapacityIncreaseConfigurationProperty(
                            capacity_monitoring_approach="capacityMonitoringApproach",
                            services=[arcregionswitch_mixins.CfnPlanPropsMixin.ServiceProperty(
                                cluster_arn="clusterArn",
                                cross_account_role="crossAccountRole",
                                external_id="externalId",
                                service_arn="serviceArn"
                            )],
                            target_percent=123,
                            timeout_minutes=123,
                            ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.EcsUngracefulProperty(
                                minimum_success_percentage=123
                            )
                        ),
                        eks_resource_scaling_config=arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingConfigurationProperty(
                            capacity_monitoring_approach="capacityMonitoringApproach",
                            eks_clusters=[arcregionswitch_mixins.CfnPlanPropsMixin.EksClusterProperty(
                                cluster_arn="clusterArn",
                                cross_account_role="crossAccountRole",
                                external_id="externalId"
                            )],
                            kubernetes_resource_type=arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesResourceTypeProperty(
                                api_version="apiVersion",
                                kind="kind"
                            ),
                            scaling_resources=[{
                                "scaling_resources_key": {
                                    "scaling_resources_key": arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesScalingResourceProperty(
                                        hpa_name="hpaName",
                                        name="name",
                                        namespace="namespace"
                                    )
                                }
                            }],
                            target_percent=123,
                            timeout_minutes=123,
                            ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingUngracefulProperty(
                                minimum_success_percentage=123
                            )
                        ),
                        execution_approval_config=arcregionswitch_mixins.CfnPlanPropsMixin.ExecutionApprovalConfigurationProperty(
                            approval_role="approvalRole",
                            timeout_minutes=123
                        ),
                        global_aurora_config=arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraConfigurationProperty(
                            behavior="behavior",
                            cross_account_role="crossAccountRole",
                            database_cluster_arns=["databaseClusterArns"],
                            external_id="externalId",
                            global_cluster_identifier="globalClusterIdentifier",
                            timeout_minutes=123,
                            ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraUngracefulProperty(
                                ungraceful="ungraceful"
                            )
                        ),
                        parallel_config=arcregionswitch_mixins.CfnPlanPropsMixin.ParallelExecutionBlockConfigurationProperty(
                            steps=[step_property_]
                        ),
                        region_switch_plan_config=arcregionswitch_mixins.CfnPlanPropsMixin.RegionSwitchPlanConfigurationProperty(
                            arn="arn",
                            cross_account_role="crossAccountRole",
                            external_id="externalId"
                        ),
                        route53_health_check_config=arcregionswitch_mixins.CfnPlanPropsMixin.Route53HealthCheckConfigurationProperty(
                            cross_account_role="crossAccountRole",
                            external_id="externalId",
                            hosted_zone_id="hostedZoneId",
                            record_name="recordName",
                            record_sets=[arcregionswitch_mixins.CfnPlanPropsMixin.Route53ResourceRecordSetProperty(
                                record_set_identifier="recordSetIdentifier",
                                region="region"
                            )],
                            timeout_minutes=123
                        )
                    ),
                    execution_block_type="executionBlockType",
                    name="name"
                )],
                workflow_description="workflowDescription",
                workflow_target_action="workflowTargetAction",
                workflow_target_region="workflowTargetRegion"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPlanMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ARCRegionSwitch::Plan``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02927817f099aea448dc17179be5908e55fd27c1faff183f516daab6e0e2f173)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c9968ff691ecb114d016d5a3e82c9b414a5fdb955b3135949e36f2fe1311e43)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a91287d75e622a41b3049c7921662670e950efdf9dd7239e56ef17caafedf9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPlanMixinProps:
        return typing.cast(CfnPlanMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.ArcRoutingControlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cross_account_role": "crossAccountRole",
            "external_id": "externalId",
            "region_and_routing_controls": "regionAndRoutingControls",
            "timeout_minutes": "timeoutMinutes",
        },
    )
    class ArcRoutingControlConfigurationProperty:
        def __init__(
            self,
            *,
            cross_account_role: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
            region_and_routing_controls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.ArcRoutingControlStateProperty", typing.Dict[builtins.str, typing.Any]]]]]]]] = None,
            timeout_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configuration for ARC routing controls used in a Region switch plan.

            Routing controls are simple on/off switches that you can use to shift traffic away from an impaired Region.

            :param cross_account_role: The cross account role for the configuration.
            :param external_id: The external ID (secret key) for the configuration.
            :param region_and_routing_controls: The Region and ARC routing controls for the configuration.
            :param timeout_minutes: The timeout value specified for the configuration. Default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-arcroutingcontrolconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                arc_routing_control_configuration_property = arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlConfigurationProperty(
                    cross_account_role="crossAccountRole",
                    external_id="externalId",
                    region_and_routing_controls={
                        "region_and_routing_controls_key": [arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlStateProperty(
                            routing_control_arn="routingControlArn",
                            state="state"
                        )]
                    },
                    timeout_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93b635568571a06e9e55acfa2a3ecf9f0a5b082fe2156aba4e68ca2910361824)
                check_type(argname="argument cross_account_role", value=cross_account_role, expected_type=type_hints["cross_account_role"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
                check_type(argname="argument region_and_routing_controls", value=region_and_routing_controls, expected_type=type_hints["region_and_routing_controls"])
                check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cross_account_role is not None:
                self._values["cross_account_role"] = cross_account_role
            if external_id is not None:
                self._values["external_id"] = external_id
            if region_and_routing_controls is not None:
                self._values["region_and_routing_controls"] = region_and_routing_controls
            if timeout_minutes is not None:
                self._values["timeout_minutes"] = timeout_minutes

        @builtins.property
        def cross_account_role(self) -> typing.Optional[builtins.str]:
            '''The cross account role for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-arcroutingcontrolconfiguration.html#cfn-arcregionswitch-plan-arcroutingcontrolconfiguration-crossaccountrole
            '''
            result = self._values.get("cross_account_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID (secret key) for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-arcroutingcontrolconfiguration.html#cfn-arcregionswitch-plan-arcroutingcontrolconfiguration-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region_and_routing_controls(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ArcRoutingControlStateProperty"]]]]]]:
            '''The Region and ARC routing controls for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-arcroutingcontrolconfiguration.html#cfn-arcregionswitch-plan-arcroutingcontrolconfiguration-regionandroutingcontrols
            '''
            result = self._values.get("region_and_routing_controls")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ArcRoutingControlStateProperty"]]]]]], result)

        @builtins.property
        def timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The timeout value specified for the configuration.

            :default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-arcroutingcontrolconfiguration.html#cfn-arcregionswitch-plan-arcroutingcontrolconfiguration-timeoutminutes
            '''
            result = self._values.get("timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArcRoutingControlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.ArcRoutingControlStateProperty",
        jsii_struct_bases=[],
        name_mapping={"routing_control_arn": "routingControlArn", "state": "state"},
    )
    class ArcRoutingControlStateProperty:
        def __init__(
            self,
            *,
            routing_control_arn: typing.Optional[builtins.str] = None,
            state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param routing_control_arn: 
            :param state: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-arcroutingcontrolstate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                arc_routing_control_state_property = arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlStateProperty(
                    routing_control_arn="routingControlArn",
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f65b2650d0ced2059e4639907ceab60c198bc985ddcbd349ee0c454b6099e261)
                check_type(argname="argument routing_control_arn", value=routing_control_arn, expected_type=type_hints["routing_control_arn"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if routing_control_arn is not None:
                self._values["routing_control_arn"] = routing_control_arn
            if state is not None:
                self._values["state"] = state

        @builtins.property
        def routing_control_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-arcroutingcontrolstate.html#cfn-arcregionswitch-plan-arcroutingcontrolstate-routingcontrolarn
            '''
            result = self._values.get("routing_control_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-arcroutingcontrolstate.html#cfn-arcregionswitch-plan-arcroutingcontrolstate-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArcRoutingControlStateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.AsgProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "cross_account_role": "crossAccountRole",
            "external_id": "externalId",
        },
    )
    class AsgProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            cross_account_role: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for an Amazon EC2 Auto Scaling group used in a Region switch plan.

            :param arn: The Amazon Resource Name (ARN) of the EC2 Auto Scaling group.
            :param cross_account_role: The cross account role for the configuration.
            :param external_id: The external ID (secret key) for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-asg.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                asg_property = arcregionswitch_mixins.CfnPlanPropsMixin.AsgProperty(
                    arn="arn",
                    cross_account_role="crossAccountRole",
                    external_id="externalId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df09f7075961b2ee034bab94576e69d2e2b149eea6ef139d129ed8da0af8b0fe)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument cross_account_role", value=cross_account_role, expected_type=type_hints["cross_account_role"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if cross_account_role is not None:
                self._values["cross_account_role"] = cross_account_role
            if external_id is not None:
                self._values["external_id"] = external_id

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the EC2 Auto Scaling group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-asg.html#cfn-arcregionswitch-plan-asg-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cross_account_role(self) -> typing.Optional[builtins.str]:
            '''The cross account role for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-asg.html#cfn-arcregionswitch-plan-asg-crossaccountrole
            '''
            result = self._values.get("cross_account_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID (secret key) for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-asg.html#cfn-arcregionswitch-plan-asg-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AsgProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.AssociatedAlarmProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alarm_type": "alarmType",
            "cross_account_role": "crossAccountRole",
            "external_id": "externalId",
            "resource_identifier": "resourceIdentifier",
        },
    )
    class AssociatedAlarmProperty:
        def __init__(
            self,
            *,
            alarm_type: typing.Optional[builtins.str] = None,
            cross_account_role: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
            resource_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An Amazon CloudWatch alarm associated with a Region switch plan.

            These alarms can be used to trigger automatic execution of the plan.

            :param alarm_type: The alarm type for an associated alarm. An associated CloudWatch alarm can be an application health alarm or a trigger alarm.
            :param cross_account_role: The cross account role for the configuration.
            :param external_id: The external ID (secret key) for the configuration.
            :param resource_identifier: The resource identifier for alarms that you associate with a plan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-associatedalarm.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                associated_alarm_property = arcregionswitch_mixins.CfnPlanPropsMixin.AssociatedAlarmProperty(
                    alarm_type="alarmType",
                    cross_account_role="crossAccountRole",
                    external_id="externalId",
                    resource_identifier="resourceIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e703a161504358962c74f058528fe8df63184e4a16a7b16937ef6cbd9178471)
                check_type(argname="argument alarm_type", value=alarm_type, expected_type=type_hints["alarm_type"])
                check_type(argname="argument cross_account_role", value=cross_account_role, expected_type=type_hints["cross_account_role"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
                check_type(argname="argument resource_identifier", value=resource_identifier, expected_type=type_hints["resource_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarm_type is not None:
                self._values["alarm_type"] = alarm_type
            if cross_account_role is not None:
                self._values["cross_account_role"] = cross_account_role
            if external_id is not None:
                self._values["external_id"] = external_id
            if resource_identifier is not None:
                self._values["resource_identifier"] = resource_identifier

        @builtins.property
        def alarm_type(self) -> typing.Optional[builtins.str]:
            '''The alarm type for an associated alarm.

            An associated CloudWatch alarm can be an application health alarm or a trigger alarm.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-associatedalarm.html#cfn-arcregionswitch-plan-associatedalarm-alarmtype
            '''
            result = self._values.get("alarm_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cross_account_role(self) -> typing.Optional[builtins.str]:
            '''The cross account role for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-associatedalarm.html#cfn-arcregionswitch-plan-associatedalarm-crossaccountrole
            '''
            result = self._values.get("cross_account_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID (secret key) for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-associatedalarm.html#cfn-arcregionswitch-plan-associatedalarm-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_identifier(self) -> typing.Optional[builtins.str]:
            '''The resource identifier for alarms that you associate with a plan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-associatedalarm.html#cfn-arcregionswitch-plan-associatedalarm-resourceidentifier
            '''
            result = self._values.get("resource_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssociatedAlarmProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.CustomActionLambdaConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambdas": "lambdas",
            "region_to_run": "regionToRun",
            "retry_interval_minutes": "retryIntervalMinutes",
            "timeout_minutes": "timeoutMinutes",
            "ungraceful": "ungraceful",
        },
    )
    class CustomActionLambdaConfigurationProperty:
        def __init__(
            self,
            *,
            lambdas: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.LambdasProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            region_to_run: typing.Optional[builtins.str] = None,
            retry_interval_minutes: typing.Optional[jsii.Number] = None,
            timeout_minutes: typing.Optional[jsii.Number] = None,
            ungraceful: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.LambdaUngracefulProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration for AWS Lambda functions that perform custom actions during a Region switch.

            :param lambdas: The AWS Lambda functions for the execution block.
            :param region_to_run: The AWS Region for the function to run in.
            :param retry_interval_minutes: The retry interval specified.
            :param timeout_minutes: The timeout value specified for the configuration. Default: - 60
            :param ungraceful: The settings for ungraceful execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-customactionlambdaconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                custom_action_lambda_configuration_property = arcregionswitch_mixins.CfnPlanPropsMixin.CustomActionLambdaConfigurationProperty(
                    lambdas=[arcregionswitch_mixins.CfnPlanPropsMixin.LambdasProperty(
                        arn="arn",
                        cross_account_role="crossAccountRole",
                        external_id="externalId"
                    )],
                    region_to_run="regionToRun",
                    retry_interval_minutes=123,
                    timeout_minutes=123,
                    ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.LambdaUngracefulProperty(
                        behavior="behavior"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a25614feef2e72b714dfb8d6034fe976618e3f19e9d55b2ccfb54ed002d75d5c)
                check_type(argname="argument lambdas", value=lambdas, expected_type=type_hints["lambdas"])
                check_type(argname="argument region_to_run", value=region_to_run, expected_type=type_hints["region_to_run"])
                check_type(argname="argument retry_interval_minutes", value=retry_interval_minutes, expected_type=type_hints["retry_interval_minutes"])
                check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
                check_type(argname="argument ungraceful", value=ungraceful, expected_type=type_hints["ungraceful"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambdas is not None:
                self._values["lambdas"] = lambdas
            if region_to_run is not None:
                self._values["region_to_run"] = region_to_run
            if retry_interval_minutes is not None:
                self._values["retry_interval_minutes"] = retry_interval_minutes
            if timeout_minutes is not None:
                self._values["timeout_minutes"] = timeout_minutes
            if ungraceful is not None:
                self._values["ungraceful"] = ungraceful

        @builtins.property
        def lambdas(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.LambdasProperty"]]]]:
            '''The AWS Lambda functions for the execution block.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-customactionlambdaconfiguration.html#cfn-arcregionswitch-plan-customactionlambdaconfiguration-lambdas
            '''
            result = self._values.get("lambdas")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.LambdasProperty"]]]], result)

        @builtins.property
        def region_to_run(self) -> typing.Optional[builtins.str]:
            '''The AWS Region for the function to run in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-customactionlambdaconfiguration.html#cfn-arcregionswitch-plan-customactionlambdaconfiguration-regiontorun
            '''
            result = self._values.get("region_to_run")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retry_interval_minutes(self) -> typing.Optional[jsii.Number]:
            '''The retry interval specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-customactionlambdaconfiguration.html#cfn-arcregionswitch-plan-customactionlambdaconfiguration-retryintervalminutes
            '''
            result = self._values.get("retry_interval_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The timeout value specified for the configuration.

            :default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-customactionlambdaconfiguration.html#cfn-arcregionswitch-plan-customactionlambdaconfiguration-timeoutminutes
            '''
            result = self._values.get("timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ungraceful(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.LambdaUngracefulProperty"]]:
            '''The settings for ungraceful execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-customactionlambdaconfiguration.html#cfn-arcregionswitch-plan-customactionlambdaconfiguration-ungraceful
            '''
            result = self._values.get("ungraceful")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.LambdaUngracefulProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomActionLambdaConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.Ec2AsgCapacityIncreaseConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "asgs": "asgs",
            "capacity_monitoring_approach": "capacityMonitoringApproach",
            "target_percent": "targetPercent",
            "timeout_minutes": "timeoutMinutes",
            "ungraceful": "ungraceful",
        },
    )
    class Ec2AsgCapacityIncreaseConfigurationProperty:
        def __init__(
            self,
            *,
            asgs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.AsgProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            capacity_monitoring_approach: typing.Optional[builtins.str] = None,
            target_percent: typing.Optional[jsii.Number] = None,
            timeout_minutes: typing.Optional[jsii.Number] = None,
            ungraceful: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.Ec2UngracefulProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration for increasing the capacity of Amazon EC2 Auto Scaling groups during a Region switch.

            :param asgs: The EC2 Auto Scaling groups for the configuration.
            :param capacity_monitoring_approach: The monitoring approach that you specify EC2 Auto Scaling groups for the configuration.
            :param target_percent: The target percentage that you specify for EC2 Auto Scaling groups. Default: - 100
            :param timeout_minutes: The timeout value specified for the configuration. Default: - 60
            :param ungraceful: The settings for ungraceful execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ec2asgcapacityincreaseconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                ec2_asg_capacity_increase_configuration_property = arcregionswitch_mixins.CfnPlanPropsMixin.Ec2AsgCapacityIncreaseConfigurationProperty(
                    asgs=[arcregionswitch_mixins.CfnPlanPropsMixin.AsgProperty(
                        arn="arn",
                        cross_account_role="crossAccountRole",
                        external_id="externalId"
                    )],
                    capacity_monitoring_approach="capacityMonitoringApproach",
                    target_percent=123,
                    timeout_minutes=123,
                    ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.Ec2UngracefulProperty(
                        minimum_success_percentage=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__743860ca02471133ca1b320b1553f1a9cad96c501cd50dd4faa020b47721d554)
                check_type(argname="argument asgs", value=asgs, expected_type=type_hints["asgs"])
                check_type(argname="argument capacity_monitoring_approach", value=capacity_monitoring_approach, expected_type=type_hints["capacity_monitoring_approach"])
                check_type(argname="argument target_percent", value=target_percent, expected_type=type_hints["target_percent"])
                check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
                check_type(argname="argument ungraceful", value=ungraceful, expected_type=type_hints["ungraceful"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if asgs is not None:
                self._values["asgs"] = asgs
            if capacity_monitoring_approach is not None:
                self._values["capacity_monitoring_approach"] = capacity_monitoring_approach
            if target_percent is not None:
                self._values["target_percent"] = target_percent
            if timeout_minutes is not None:
                self._values["timeout_minutes"] = timeout_minutes
            if ungraceful is not None:
                self._values["ungraceful"] = ungraceful

        @builtins.property
        def asgs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.AsgProperty"]]]]:
            '''The EC2 Auto Scaling groups for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ec2asgcapacityincreaseconfiguration.html#cfn-arcregionswitch-plan-ec2asgcapacityincreaseconfiguration-asgs
            '''
            result = self._values.get("asgs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.AsgProperty"]]]], result)

        @builtins.property
        def capacity_monitoring_approach(self) -> typing.Optional[builtins.str]:
            '''The monitoring approach that you specify EC2 Auto Scaling groups for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ec2asgcapacityincreaseconfiguration.html#cfn-arcregionswitch-plan-ec2asgcapacityincreaseconfiguration-capacitymonitoringapproach
            '''
            result = self._values.get("capacity_monitoring_approach")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_percent(self) -> typing.Optional[jsii.Number]:
            '''The target percentage that you specify for EC2 Auto Scaling groups.

            :default: - 100

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ec2asgcapacityincreaseconfiguration.html#cfn-arcregionswitch-plan-ec2asgcapacityincreaseconfiguration-targetpercent
            '''
            result = self._values.get("target_percent")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The timeout value specified for the configuration.

            :default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ec2asgcapacityincreaseconfiguration.html#cfn-arcregionswitch-plan-ec2asgcapacityincreaseconfiguration-timeoutminutes
            '''
            result = self._values.get("timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ungraceful(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.Ec2UngracefulProperty"]]:
            '''The settings for ungraceful execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ec2asgcapacityincreaseconfiguration.html#cfn-arcregionswitch-plan-ec2asgcapacityincreaseconfiguration-ungraceful
            '''
            result = self._values.get("ungraceful")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.Ec2UngracefulProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Ec2AsgCapacityIncreaseConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.Ec2UngracefulProperty",
        jsii_struct_bases=[],
        name_mapping={"minimum_success_percentage": "minimumSuccessPercentage"},
    )
    class Ec2UngracefulProperty:
        def __init__(
            self,
            *,
            minimum_success_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configuration for handling failures when performing operations on EC2 resources.

            :param minimum_success_percentage: The minimum success percentage that you specify for EC2 Auto Scaling groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ec2ungraceful.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                ec2_ungraceful_property = arcregionswitch_mixins.CfnPlanPropsMixin.Ec2UngracefulProperty(
                    minimum_success_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__977dd12f7fe108c1722a5001d534514222f029e6b548a731576a58e2709cebea)
                check_type(argname="argument minimum_success_percentage", value=minimum_success_percentage, expected_type=type_hints["minimum_success_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if minimum_success_percentage is not None:
                self._values["minimum_success_percentage"] = minimum_success_percentage

        @builtins.property
        def minimum_success_percentage(self) -> typing.Optional[jsii.Number]:
            '''The minimum success percentage that you specify for EC2 Auto Scaling groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ec2ungraceful.html#cfn-arcregionswitch-plan-ec2ungraceful-minimumsuccesspercentage
            '''
            result = self._values.get("minimum_success_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Ec2UngracefulProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.EcsCapacityIncreaseConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_monitoring_approach": "capacityMonitoringApproach",
            "services": "services",
            "target_percent": "targetPercent",
            "timeout_minutes": "timeoutMinutes",
            "ungraceful": "ungraceful",
        },
    )
    class EcsCapacityIncreaseConfigurationProperty:
        def __init__(
            self,
            *,
            capacity_monitoring_approach: typing.Optional[builtins.str] = None,
            services: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.ServiceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            target_percent: typing.Optional[jsii.Number] = None,
            timeout_minutes: typing.Optional[jsii.Number] = None,
            ungraceful: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.EcsUngracefulProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for an AWS ECS capacity increase.

            :param capacity_monitoring_approach: The monitoring approach specified for the configuration, for example, ``Most_Recent`` .
            :param services: The services specified for the configuration.
            :param target_percent: The target percentage specified for the configuration. Default: - 100
            :param timeout_minutes: The timeout value specified for the configuration. Default: - 60
            :param ungraceful: The settings for ungraceful execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ecscapacityincreaseconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                ecs_capacity_increase_configuration_property = arcregionswitch_mixins.CfnPlanPropsMixin.EcsCapacityIncreaseConfigurationProperty(
                    capacity_monitoring_approach="capacityMonitoringApproach",
                    services=[arcregionswitch_mixins.CfnPlanPropsMixin.ServiceProperty(
                        cluster_arn="clusterArn",
                        cross_account_role="crossAccountRole",
                        external_id="externalId",
                        service_arn="serviceArn"
                    )],
                    target_percent=123,
                    timeout_minutes=123,
                    ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.EcsUngracefulProperty(
                        minimum_success_percentage=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__91d979b81def65c94faa51fc046006b6dbe7331afbd1164c89b2014bcf89ad18)
                check_type(argname="argument capacity_monitoring_approach", value=capacity_monitoring_approach, expected_type=type_hints["capacity_monitoring_approach"])
                check_type(argname="argument services", value=services, expected_type=type_hints["services"])
                check_type(argname="argument target_percent", value=target_percent, expected_type=type_hints["target_percent"])
                check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
                check_type(argname="argument ungraceful", value=ungraceful, expected_type=type_hints["ungraceful"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_monitoring_approach is not None:
                self._values["capacity_monitoring_approach"] = capacity_monitoring_approach
            if services is not None:
                self._values["services"] = services
            if target_percent is not None:
                self._values["target_percent"] = target_percent
            if timeout_minutes is not None:
                self._values["timeout_minutes"] = timeout_minutes
            if ungraceful is not None:
                self._values["ungraceful"] = ungraceful

        @builtins.property
        def capacity_monitoring_approach(self) -> typing.Optional[builtins.str]:
            '''The monitoring approach specified for the configuration, for example, ``Most_Recent`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ecscapacityincreaseconfiguration.html#cfn-arcregionswitch-plan-ecscapacityincreaseconfiguration-capacitymonitoringapproach
            '''
            result = self._values.get("capacity_monitoring_approach")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def services(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ServiceProperty"]]]]:
            '''The services specified for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ecscapacityincreaseconfiguration.html#cfn-arcregionswitch-plan-ecscapacityincreaseconfiguration-services
            '''
            result = self._values.get("services")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ServiceProperty"]]]], result)

        @builtins.property
        def target_percent(self) -> typing.Optional[jsii.Number]:
            '''The target percentage specified for the configuration.

            :default: - 100

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ecscapacityincreaseconfiguration.html#cfn-arcregionswitch-plan-ecscapacityincreaseconfiguration-targetpercent
            '''
            result = self._values.get("target_percent")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The timeout value specified for the configuration.

            :default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ecscapacityincreaseconfiguration.html#cfn-arcregionswitch-plan-ecscapacityincreaseconfiguration-timeoutminutes
            '''
            result = self._values.get("timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ungraceful(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.EcsUngracefulProperty"]]:
            '''The settings for ungraceful execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ecscapacityincreaseconfiguration.html#cfn-arcregionswitch-plan-ecscapacityincreaseconfiguration-ungraceful
            '''
            result = self._values.get("ungraceful")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.EcsUngracefulProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsCapacityIncreaseConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.EcsUngracefulProperty",
        jsii_struct_bases=[],
        name_mapping={"minimum_success_percentage": "minimumSuccessPercentage"},
    )
    class EcsUngracefulProperty:
        def __init__(
            self,
            *,
            minimum_success_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The settings for ungraceful execution.

            :param minimum_success_percentage: The minimum success percentage specified for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ecsungraceful.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                ecs_ungraceful_property = arcregionswitch_mixins.CfnPlanPropsMixin.EcsUngracefulProperty(
                    minimum_success_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__527e26acda0abc4e0b1bd0d382e0a736f25049c22c4e99997c2bb13ba812c64b)
                check_type(argname="argument minimum_success_percentage", value=minimum_success_percentage, expected_type=type_hints["minimum_success_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if minimum_success_percentage is not None:
                self._values["minimum_success_percentage"] = minimum_success_percentage

        @builtins.property
        def minimum_success_percentage(self) -> typing.Optional[jsii.Number]:
            '''The minimum success percentage specified for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ecsungraceful.html#cfn-arcregionswitch-plan-ecsungraceful-minimumsuccesspercentage
            '''
            result = self._values.get("minimum_success_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsUngracefulProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.EksClusterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cluster_arn": "clusterArn",
            "cross_account_role": "crossAccountRole",
            "external_id": "externalId",
        },
    )
    class EksClusterProperty:
        def __init__(
            self,
            *,
            cluster_arn: typing.Optional[builtins.str] = None,
            cross_account_role: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The AWS EKS cluster execution block configuration.

            :param cluster_arn: The Amazon Resource Name (ARN) of an AWS EKS cluster.
            :param cross_account_role: The cross account role for the configuration.
            :param external_id: The external ID (secret key) for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ekscluster.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                eks_cluster_property = arcregionswitch_mixins.CfnPlanPropsMixin.EksClusterProperty(
                    cluster_arn="clusterArn",
                    cross_account_role="crossAccountRole",
                    external_id="externalId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b2299808b1f9fd2f7a402045e006d5fadd21039619c15ccfba5fe9d976aa608)
                check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
                check_type(argname="argument cross_account_role", value=cross_account_role, expected_type=type_hints["cross_account_role"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cluster_arn is not None:
                self._values["cluster_arn"] = cluster_arn
            if cross_account_role is not None:
                self._values["cross_account_role"] = cross_account_role
            if external_id is not None:
                self._values["external_id"] = external_id

        @builtins.property
        def cluster_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an AWS EKS cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ekscluster.html#cfn-arcregionswitch-plan-ekscluster-clusterarn
            '''
            result = self._values.get("cluster_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cross_account_role(self) -> typing.Optional[builtins.str]:
            '''The cross account role for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ekscluster.html#cfn-arcregionswitch-plan-ekscluster-crossaccountrole
            '''
            result = self._values.get("cross_account_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID (secret key) for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-ekscluster.html#cfn-arcregionswitch-plan-ekscluster-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksClusterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.EksResourceScalingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_monitoring_approach": "capacityMonitoringApproach",
            "eks_clusters": "eksClusters",
            "kubernetes_resource_type": "kubernetesResourceType",
            "scaling_resources": "scalingResources",
            "target_percent": "targetPercent",
            "timeout_minutes": "timeoutMinutes",
            "ungraceful": "ungraceful",
        },
    )
    class EksResourceScalingConfigurationProperty:
        def __init__(
            self,
            *,
            capacity_monitoring_approach: typing.Optional[builtins.str] = None,
            eks_clusters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.EksClusterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            kubernetes_resource_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.KubernetesResourceTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            scaling_resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.KubernetesScalingResourceProperty", typing.Dict[builtins.str, typing.Any]]]]]]]]]] = None,
            target_percent: typing.Optional[jsii.Number] = None,
            timeout_minutes: typing.Optional[jsii.Number] = None,
            ungraceful: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.EksResourceScalingUngracefulProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The AWS EKS resource scaling configuration.

            :param capacity_monitoring_approach: The monitoring approach for the configuration, that is, whether it was sampled in the last 24 hours or autoscaled in the last 24 hours.
            :param eks_clusters: The clusters for the configuration.
            :param kubernetes_resource_type: The Kubernetes resource type for the configuration.
            :param scaling_resources: The scaling resources for the configuration.
            :param target_percent: The target percentage for the configuration. Default: - 100
            :param timeout_minutes: The timeout value specified for the configuration. Default: - 60
            :param ungraceful: The settings for ungraceful execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-eksresourcescalingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                eks_resource_scaling_configuration_property = arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingConfigurationProperty(
                    capacity_monitoring_approach="capacityMonitoringApproach",
                    eks_clusters=[arcregionswitch_mixins.CfnPlanPropsMixin.EksClusterProperty(
                        cluster_arn="clusterArn",
                        cross_account_role="crossAccountRole",
                        external_id="externalId"
                    )],
                    kubernetes_resource_type=arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesResourceTypeProperty(
                        api_version="apiVersion",
                        kind="kind"
                    ),
                    scaling_resources=[{
                        "scaling_resources_key": {
                            "scaling_resources_key": arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesScalingResourceProperty(
                                hpa_name="hpaName",
                                name="name",
                                namespace="namespace"
                            )
                        }
                    }],
                    target_percent=123,
                    timeout_minutes=123,
                    ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingUngracefulProperty(
                        minimum_success_percentage=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fdf3327986585c65e94599224a24d86b83df635addf78632d39e771e04ad8e95)
                check_type(argname="argument capacity_monitoring_approach", value=capacity_monitoring_approach, expected_type=type_hints["capacity_monitoring_approach"])
                check_type(argname="argument eks_clusters", value=eks_clusters, expected_type=type_hints["eks_clusters"])
                check_type(argname="argument kubernetes_resource_type", value=kubernetes_resource_type, expected_type=type_hints["kubernetes_resource_type"])
                check_type(argname="argument scaling_resources", value=scaling_resources, expected_type=type_hints["scaling_resources"])
                check_type(argname="argument target_percent", value=target_percent, expected_type=type_hints["target_percent"])
                check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
                check_type(argname="argument ungraceful", value=ungraceful, expected_type=type_hints["ungraceful"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_monitoring_approach is not None:
                self._values["capacity_monitoring_approach"] = capacity_monitoring_approach
            if eks_clusters is not None:
                self._values["eks_clusters"] = eks_clusters
            if kubernetes_resource_type is not None:
                self._values["kubernetes_resource_type"] = kubernetes_resource_type
            if scaling_resources is not None:
                self._values["scaling_resources"] = scaling_resources
            if target_percent is not None:
                self._values["target_percent"] = target_percent
            if timeout_minutes is not None:
                self._values["timeout_minutes"] = timeout_minutes
            if ungraceful is not None:
                self._values["ungraceful"] = ungraceful

        @builtins.property
        def capacity_monitoring_approach(self) -> typing.Optional[builtins.str]:
            '''The monitoring approach for the configuration, that is, whether it was sampled in the last 24 hours or autoscaled in the last 24 hours.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-eksresourcescalingconfiguration.html#cfn-arcregionswitch-plan-eksresourcescalingconfiguration-capacitymonitoringapproach
            '''
            result = self._values.get("capacity_monitoring_approach")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def eks_clusters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.EksClusterProperty"]]]]:
            '''The clusters for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-eksresourcescalingconfiguration.html#cfn-arcregionswitch-plan-eksresourcescalingconfiguration-eksclusters
            '''
            result = self._values.get("eks_clusters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.EksClusterProperty"]]]], result)

        @builtins.property
        def kubernetes_resource_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.KubernetesResourceTypeProperty"]]:
            '''The Kubernetes resource type for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-eksresourcescalingconfiguration.html#cfn-arcregionswitch-plan-eksresourcescalingconfiguration-kubernetesresourcetype
            '''
            result = self._values.get("kubernetes_resource_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.KubernetesResourceTypeProperty"]], result)

        @builtins.property
        def scaling_resources(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.KubernetesScalingResourceProperty"]]]]]]]]:
            '''The scaling resources for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-eksresourcescalingconfiguration.html#cfn-arcregionswitch-plan-eksresourcescalingconfiguration-scalingresources
            '''
            result = self._values.get("scaling_resources")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.KubernetesScalingResourceProperty"]]]]]]]], result)

        @builtins.property
        def target_percent(self) -> typing.Optional[jsii.Number]:
            '''The target percentage for the configuration.

            :default: - 100

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-eksresourcescalingconfiguration.html#cfn-arcregionswitch-plan-eksresourcescalingconfiguration-targetpercent
            '''
            result = self._values.get("target_percent")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The timeout value specified for the configuration.

            :default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-eksresourcescalingconfiguration.html#cfn-arcregionswitch-plan-eksresourcescalingconfiguration-timeoutminutes
            '''
            result = self._values.get("timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ungraceful(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.EksResourceScalingUngracefulProperty"]]:
            '''The settings for ungraceful execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-eksresourcescalingconfiguration.html#cfn-arcregionswitch-plan-eksresourcescalingconfiguration-ungraceful
            '''
            result = self._values.get("ungraceful")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.EksResourceScalingUngracefulProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksResourceScalingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.EksResourceScalingUngracefulProperty",
        jsii_struct_bases=[],
        name_mapping={"minimum_success_percentage": "minimumSuccessPercentage"},
    )
    class EksResourceScalingUngracefulProperty:
        def __init__(
            self,
            *,
            minimum_success_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ungraceful settings for AWS EKS resource scaling.

            :param minimum_success_percentage: The minimum success percentage for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-eksresourcescalingungraceful.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                eks_resource_scaling_ungraceful_property = arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingUngracefulProperty(
                    minimum_success_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f52e2311a13e18f78cd07cfff90054b3f07a236b58cf44d15ed61dd23dbda32e)
                check_type(argname="argument minimum_success_percentage", value=minimum_success_percentage, expected_type=type_hints["minimum_success_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if minimum_success_percentage is not None:
                self._values["minimum_success_percentage"] = minimum_success_percentage

        @builtins.property
        def minimum_success_percentage(self) -> typing.Optional[jsii.Number]:
            '''The minimum success percentage for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-eksresourcescalingungraceful.html#cfn-arcregionswitch-plan-eksresourcescalingungraceful-minimumsuccesspercentage
            '''
            result = self._values.get("minimum_success_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksResourceScalingUngracefulProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.ExecutionApprovalConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "approval_role": "approvalRole",
            "timeout_minutes": "timeoutMinutes",
        },
    )
    class ExecutionApprovalConfigurationProperty:
        def __init__(
            self,
            *,
            approval_role: typing.Optional[builtins.str] = None,
            timeout_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configuration for approval steps in a Region switch plan execution.

            Approval steps require manual intervention before the execution can proceed.

            :param approval_role: The IAM approval role for the configuration.
            :param timeout_minutes: The timeout value specified for the configuration. Default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-executionapprovalconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                execution_approval_configuration_property = arcregionswitch_mixins.CfnPlanPropsMixin.ExecutionApprovalConfigurationProperty(
                    approval_role="approvalRole",
                    timeout_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__025fce55820542914cd108e554f5af60e6b8ce8d4395c2ff2640af9a1682aa11)
                check_type(argname="argument approval_role", value=approval_role, expected_type=type_hints["approval_role"])
                check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if approval_role is not None:
                self._values["approval_role"] = approval_role
            if timeout_minutes is not None:
                self._values["timeout_minutes"] = timeout_minutes

        @builtins.property
        def approval_role(self) -> typing.Optional[builtins.str]:
            '''The IAM approval role for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-executionapprovalconfiguration.html#cfn-arcregionswitch-plan-executionapprovalconfiguration-approvalrole
            '''
            result = self._values.get("approval_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The timeout value specified for the configuration.

            :default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-executionapprovalconfiguration.html#cfn-arcregionswitch-plan-executionapprovalconfiguration-timeoutminutes
            '''
            result = self._values.get("timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExecutionApprovalConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.ExecutionBlockConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arc_routing_control_config": "arcRoutingControlConfig",
            "custom_action_lambda_config": "customActionLambdaConfig",
            "ec2_asg_capacity_increase_config": "ec2AsgCapacityIncreaseConfig",
            "ecs_capacity_increase_config": "ecsCapacityIncreaseConfig",
            "eks_resource_scaling_config": "eksResourceScalingConfig",
            "execution_approval_config": "executionApprovalConfig",
            "global_aurora_config": "globalAuroraConfig",
            "parallel_config": "parallelConfig",
            "region_switch_plan_config": "regionSwitchPlanConfig",
            "route53_health_check_config": "route53HealthCheckConfig",
        },
    )
    class ExecutionBlockConfigurationProperty:
        def __init__(
            self,
            *,
            arc_routing_control_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.ArcRoutingControlConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            custom_action_lambda_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.CustomActionLambdaConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ec2_asg_capacity_increase_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.Ec2AsgCapacityIncreaseConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ecs_capacity_increase_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.EcsCapacityIncreaseConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            eks_resource_scaling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.EksResourceScalingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            execution_approval_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.ExecutionApprovalConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            global_aurora_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.GlobalAuroraConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parallel_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.ParallelExecutionBlockConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            region_switch_plan_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.RegionSwitchPlanConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            route53_health_check_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.Route53HealthCheckConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Execution block configurations for a workflow in a Region switch plan.

            An execution block represents a specific type of action to perform during a Region switch.

            :param arc_routing_control_config: An ARC routing control execution block.
            :param custom_action_lambda_config: An AWS Lambda execution block.
            :param ec2_asg_capacity_increase_config: An EC2 Auto Scaling group execution block.
            :param ecs_capacity_increase_config: The capacity increase specified for the configuration.
            :param eks_resource_scaling_config: An AWS EKS resource scaling execution block.
            :param execution_approval_config: A manual approval execution block.
            :param global_aurora_config: An Aurora Global Database execution block.
            :param parallel_config: A parallel configuration execution block.
            :param region_switch_plan_config: A Region switch plan execution block.
            :param route53_health_check_config: The Amazon Route 53 health check configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-executionblockconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                # execution_block_configuration_property_: arcregionswitch_mixins.CfnPlanPropsMixin.ExecutionBlockConfigurationProperty
                
                execution_block_configuration_property = arcregionswitch_mixins.CfnPlanPropsMixin.ExecutionBlockConfigurationProperty(
                    arc_routing_control_config=arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlConfigurationProperty(
                        cross_account_role="crossAccountRole",
                        external_id="externalId",
                        region_and_routing_controls={
                            "region_and_routing_controls_key": [arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlStateProperty(
                                routing_control_arn="routingControlArn",
                                state="state"
                            )]
                        },
                        timeout_minutes=123
                    ),
                    custom_action_lambda_config=arcregionswitch_mixins.CfnPlanPropsMixin.CustomActionLambdaConfigurationProperty(
                        lambdas=[arcregionswitch_mixins.CfnPlanPropsMixin.LambdasProperty(
                            arn="arn",
                            cross_account_role="crossAccountRole",
                            external_id="externalId"
                        )],
                        region_to_run="regionToRun",
                        retry_interval_minutes=123,
                        timeout_minutes=123,
                        ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.LambdaUngracefulProperty(
                            behavior="behavior"
                        )
                    ),
                    ec2_asg_capacity_increase_config=arcregionswitch_mixins.CfnPlanPropsMixin.Ec2AsgCapacityIncreaseConfigurationProperty(
                        asgs=[arcregionswitch_mixins.CfnPlanPropsMixin.AsgProperty(
                            arn="arn",
                            cross_account_role="crossAccountRole",
                            external_id="externalId"
                        )],
                        capacity_monitoring_approach="capacityMonitoringApproach",
                        target_percent=123,
                        timeout_minutes=123,
                        ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.Ec2UngracefulProperty(
                            minimum_success_percentage=123
                        )
                    ),
                    ecs_capacity_increase_config=arcregionswitch_mixins.CfnPlanPropsMixin.EcsCapacityIncreaseConfigurationProperty(
                        capacity_monitoring_approach="capacityMonitoringApproach",
                        services=[arcregionswitch_mixins.CfnPlanPropsMixin.ServiceProperty(
                            cluster_arn="clusterArn",
                            cross_account_role="crossAccountRole",
                            external_id="externalId",
                            service_arn="serviceArn"
                        )],
                        target_percent=123,
                        timeout_minutes=123,
                        ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.EcsUngracefulProperty(
                            minimum_success_percentage=123
                        )
                    ),
                    eks_resource_scaling_config=arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingConfigurationProperty(
                        capacity_monitoring_approach="capacityMonitoringApproach",
                        eks_clusters=[arcregionswitch_mixins.CfnPlanPropsMixin.EksClusterProperty(
                            cluster_arn="clusterArn",
                            cross_account_role="crossAccountRole",
                            external_id="externalId"
                        )],
                        kubernetes_resource_type=arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesResourceTypeProperty(
                            api_version="apiVersion",
                            kind="kind"
                        ),
                        scaling_resources=[{
                            "scaling_resources_key": {
                                "scaling_resources_key": arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesScalingResourceProperty(
                                    hpa_name="hpaName",
                                    name="name",
                                    namespace="namespace"
                                )
                            }
                        }],
                        target_percent=123,
                        timeout_minutes=123,
                        ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingUngracefulProperty(
                            minimum_success_percentage=123
                        )
                    ),
                    execution_approval_config=arcregionswitch_mixins.CfnPlanPropsMixin.ExecutionApprovalConfigurationProperty(
                        approval_role="approvalRole",
                        timeout_minutes=123
                    ),
                    global_aurora_config=arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraConfigurationProperty(
                        behavior="behavior",
                        cross_account_role="crossAccountRole",
                        database_cluster_arns=["databaseClusterArns"],
                        external_id="externalId",
                        global_cluster_identifier="globalClusterIdentifier",
                        timeout_minutes=123,
                        ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraUngracefulProperty(
                            ungraceful="ungraceful"
                        )
                    ),
                    parallel_config=arcregionswitch_mixins.CfnPlanPropsMixin.ParallelExecutionBlockConfigurationProperty(
                        steps=[arcregionswitch_mixins.CfnPlanPropsMixin.StepProperty(
                            description="description",
                            execution_block_configuration=execution_block_configuration_property_,
                            execution_block_type="executionBlockType",
                            name="name"
                        )]
                    ),
                    region_switch_plan_config=arcregionswitch_mixins.CfnPlanPropsMixin.RegionSwitchPlanConfigurationProperty(
                        arn="arn",
                        cross_account_role="crossAccountRole",
                        external_id="externalId"
                    ),
                    route53_health_check_config=arcregionswitch_mixins.CfnPlanPropsMixin.Route53HealthCheckConfigurationProperty(
                        cross_account_role="crossAccountRole",
                        external_id="externalId",
                        hosted_zone_id="hostedZoneId",
                        record_name="recordName",
                        record_sets=[arcregionswitch_mixins.CfnPlanPropsMixin.Route53ResourceRecordSetProperty(
                            record_set_identifier="recordSetIdentifier",
                            region="region"
                        )],
                        timeout_minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8989f9b403c30f6241dbc5de359dda594041df9692c3c78e1019a14c90705fe4)
                check_type(argname="argument arc_routing_control_config", value=arc_routing_control_config, expected_type=type_hints["arc_routing_control_config"])
                check_type(argname="argument custom_action_lambda_config", value=custom_action_lambda_config, expected_type=type_hints["custom_action_lambda_config"])
                check_type(argname="argument ec2_asg_capacity_increase_config", value=ec2_asg_capacity_increase_config, expected_type=type_hints["ec2_asg_capacity_increase_config"])
                check_type(argname="argument ecs_capacity_increase_config", value=ecs_capacity_increase_config, expected_type=type_hints["ecs_capacity_increase_config"])
                check_type(argname="argument eks_resource_scaling_config", value=eks_resource_scaling_config, expected_type=type_hints["eks_resource_scaling_config"])
                check_type(argname="argument execution_approval_config", value=execution_approval_config, expected_type=type_hints["execution_approval_config"])
                check_type(argname="argument global_aurora_config", value=global_aurora_config, expected_type=type_hints["global_aurora_config"])
                check_type(argname="argument parallel_config", value=parallel_config, expected_type=type_hints["parallel_config"])
                check_type(argname="argument region_switch_plan_config", value=region_switch_plan_config, expected_type=type_hints["region_switch_plan_config"])
                check_type(argname="argument route53_health_check_config", value=route53_health_check_config, expected_type=type_hints["route53_health_check_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arc_routing_control_config is not None:
                self._values["arc_routing_control_config"] = arc_routing_control_config
            if custom_action_lambda_config is not None:
                self._values["custom_action_lambda_config"] = custom_action_lambda_config
            if ec2_asg_capacity_increase_config is not None:
                self._values["ec2_asg_capacity_increase_config"] = ec2_asg_capacity_increase_config
            if ecs_capacity_increase_config is not None:
                self._values["ecs_capacity_increase_config"] = ecs_capacity_increase_config
            if eks_resource_scaling_config is not None:
                self._values["eks_resource_scaling_config"] = eks_resource_scaling_config
            if execution_approval_config is not None:
                self._values["execution_approval_config"] = execution_approval_config
            if global_aurora_config is not None:
                self._values["global_aurora_config"] = global_aurora_config
            if parallel_config is not None:
                self._values["parallel_config"] = parallel_config
            if region_switch_plan_config is not None:
                self._values["region_switch_plan_config"] = region_switch_plan_config
            if route53_health_check_config is not None:
                self._values["route53_health_check_config"] = route53_health_check_config

        @builtins.property
        def arc_routing_control_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ArcRoutingControlConfigurationProperty"]]:
            '''An ARC routing control execution block.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-executionblockconfiguration.html#cfn-arcregionswitch-plan-executionblockconfiguration-arcroutingcontrolconfig
            '''
            result = self._values.get("arc_routing_control_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ArcRoutingControlConfigurationProperty"]], result)

        @builtins.property
        def custom_action_lambda_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.CustomActionLambdaConfigurationProperty"]]:
            '''An AWS Lambda execution block.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-executionblockconfiguration.html#cfn-arcregionswitch-plan-executionblockconfiguration-customactionlambdaconfig
            '''
            result = self._values.get("custom_action_lambda_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.CustomActionLambdaConfigurationProperty"]], result)

        @builtins.property
        def ec2_asg_capacity_increase_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.Ec2AsgCapacityIncreaseConfigurationProperty"]]:
            '''An EC2 Auto Scaling group execution block.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-executionblockconfiguration.html#cfn-arcregionswitch-plan-executionblockconfiguration-ec2asgcapacityincreaseconfig
            '''
            result = self._values.get("ec2_asg_capacity_increase_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.Ec2AsgCapacityIncreaseConfigurationProperty"]], result)

        @builtins.property
        def ecs_capacity_increase_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.EcsCapacityIncreaseConfigurationProperty"]]:
            '''The capacity increase specified for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-executionblockconfiguration.html#cfn-arcregionswitch-plan-executionblockconfiguration-ecscapacityincreaseconfig
            '''
            result = self._values.get("ecs_capacity_increase_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.EcsCapacityIncreaseConfigurationProperty"]], result)

        @builtins.property
        def eks_resource_scaling_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.EksResourceScalingConfigurationProperty"]]:
            '''An AWS EKS resource scaling execution block.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-executionblockconfiguration.html#cfn-arcregionswitch-plan-executionblockconfiguration-eksresourcescalingconfig
            '''
            result = self._values.get("eks_resource_scaling_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.EksResourceScalingConfigurationProperty"]], result)

        @builtins.property
        def execution_approval_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ExecutionApprovalConfigurationProperty"]]:
            '''A manual approval execution block.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-executionblockconfiguration.html#cfn-arcregionswitch-plan-executionblockconfiguration-executionapprovalconfig
            '''
            result = self._values.get("execution_approval_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ExecutionApprovalConfigurationProperty"]], result)

        @builtins.property
        def global_aurora_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.GlobalAuroraConfigurationProperty"]]:
            '''An Aurora Global Database execution block.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-executionblockconfiguration.html#cfn-arcregionswitch-plan-executionblockconfiguration-globalauroraconfig
            '''
            result = self._values.get("global_aurora_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.GlobalAuroraConfigurationProperty"]], result)

        @builtins.property
        def parallel_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ParallelExecutionBlockConfigurationProperty"]]:
            '''A parallel configuration execution block.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-executionblockconfiguration.html#cfn-arcregionswitch-plan-executionblockconfiguration-parallelconfig
            '''
            result = self._values.get("parallel_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ParallelExecutionBlockConfigurationProperty"]], result)

        @builtins.property
        def region_switch_plan_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.RegionSwitchPlanConfigurationProperty"]]:
            '''A Region switch plan execution block.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-executionblockconfiguration.html#cfn-arcregionswitch-plan-executionblockconfiguration-regionswitchplanconfig
            '''
            result = self._values.get("region_switch_plan_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.RegionSwitchPlanConfigurationProperty"]], result)

        @builtins.property
        def route53_health_check_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.Route53HealthCheckConfigurationProperty"]]:
            '''The Amazon Route 53 health check configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-executionblockconfiguration.html#cfn-arcregionswitch-plan-executionblockconfiguration-route53healthcheckconfig
            '''
            result = self._values.get("route53_health_check_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.Route53HealthCheckConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExecutionBlockConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.GlobalAuroraConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "behavior": "behavior",
            "cross_account_role": "crossAccountRole",
            "database_cluster_arns": "databaseClusterArns",
            "external_id": "externalId",
            "global_cluster_identifier": "globalClusterIdentifier",
            "timeout_minutes": "timeoutMinutes",
            "ungraceful": "ungraceful",
        },
    )
    class GlobalAuroraConfigurationProperty:
        def __init__(
            self,
            *,
            behavior: typing.Optional[builtins.str] = None,
            cross_account_role: typing.Optional[builtins.str] = None,
            database_cluster_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            external_id: typing.Optional[builtins.str] = None,
            global_cluster_identifier: typing.Optional[builtins.str] = None,
            timeout_minutes: typing.Optional[jsii.Number] = None,
            ungraceful: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.GlobalAuroraUngracefulProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration for Amazon Aurora global databases used in a Region switch plan.

            :param behavior: The behavior for a global database, that is, only allow switchover or also allow failover.
            :param cross_account_role: The cross account role for the configuration.
            :param database_cluster_arns: The database cluster Amazon Resource Names (ARNs) for a global database.
            :param external_id: The external ID (secret key) for the configuration.
            :param global_cluster_identifier: The global cluster identifier for a global database.
            :param timeout_minutes: The timeout value specified for the configuration. Default: - 60
            :param ungraceful: The settings for ungraceful execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-globalauroraconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                global_aurora_configuration_property = arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraConfigurationProperty(
                    behavior="behavior",
                    cross_account_role="crossAccountRole",
                    database_cluster_arns=["databaseClusterArns"],
                    external_id="externalId",
                    global_cluster_identifier="globalClusterIdentifier",
                    timeout_minutes=123,
                    ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraUngracefulProperty(
                        ungraceful="ungraceful"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a0678138de6f8fa0b660fc14588aa094cf9f1c0c7d25f66b3b3c7d6f3d4cc81)
                check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
                check_type(argname="argument cross_account_role", value=cross_account_role, expected_type=type_hints["cross_account_role"])
                check_type(argname="argument database_cluster_arns", value=database_cluster_arns, expected_type=type_hints["database_cluster_arns"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
                check_type(argname="argument global_cluster_identifier", value=global_cluster_identifier, expected_type=type_hints["global_cluster_identifier"])
                check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
                check_type(argname="argument ungraceful", value=ungraceful, expected_type=type_hints["ungraceful"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if behavior is not None:
                self._values["behavior"] = behavior
            if cross_account_role is not None:
                self._values["cross_account_role"] = cross_account_role
            if database_cluster_arns is not None:
                self._values["database_cluster_arns"] = database_cluster_arns
            if external_id is not None:
                self._values["external_id"] = external_id
            if global_cluster_identifier is not None:
                self._values["global_cluster_identifier"] = global_cluster_identifier
            if timeout_minutes is not None:
                self._values["timeout_minutes"] = timeout_minutes
            if ungraceful is not None:
                self._values["ungraceful"] = ungraceful

        @builtins.property
        def behavior(self) -> typing.Optional[builtins.str]:
            '''The behavior for a global database, that is, only allow switchover or also allow failover.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-globalauroraconfiguration.html#cfn-arcregionswitch-plan-globalauroraconfiguration-behavior
            '''
            result = self._values.get("behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cross_account_role(self) -> typing.Optional[builtins.str]:
            '''The cross account role for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-globalauroraconfiguration.html#cfn-arcregionswitch-plan-globalauroraconfiguration-crossaccountrole
            '''
            result = self._values.get("cross_account_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_cluster_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The database cluster Amazon Resource Names (ARNs) for a global database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-globalauroraconfiguration.html#cfn-arcregionswitch-plan-globalauroraconfiguration-databaseclusterarns
            '''
            result = self._values.get("database_cluster_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID (secret key) for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-globalauroraconfiguration.html#cfn-arcregionswitch-plan-globalauroraconfiguration-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def global_cluster_identifier(self) -> typing.Optional[builtins.str]:
            '''The global cluster identifier for a global database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-globalauroraconfiguration.html#cfn-arcregionswitch-plan-globalauroraconfiguration-globalclusteridentifier
            '''
            result = self._values.get("global_cluster_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The timeout value specified for the configuration.

            :default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-globalauroraconfiguration.html#cfn-arcregionswitch-plan-globalauroraconfiguration-timeoutminutes
            '''
            result = self._values.get("timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ungraceful(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.GlobalAuroraUngracefulProperty"]]:
            '''The settings for ungraceful execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-globalauroraconfiguration.html#cfn-arcregionswitch-plan-globalauroraconfiguration-ungraceful
            '''
            result = self._values.get("ungraceful")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.GlobalAuroraUngracefulProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlobalAuroraConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.GlobalAuroraUngracefulProperty",
        jsii_struct_bases=[],
        name_mapping={"ungraceful": "ungraceful"},
    )
    class GlobalAuroraUngracefulProperty:
        def __init__(self, *, ungraceful: typing.Optional[builtins.str] = None) -> None:
            '''Configuration for handling failures when performing operations on Aurora global databases.

            :param ungraceful: The settings for ungraceful execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-globalauroraungraceful.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                global_aurora_ungraceful_property = arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraUngracefulProperty(
                    ungraceful="ungraceful"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__958a756e61db04b3321e0873649231bac2d60063746f5c90d58527f64c0fefc0)
                check_type(argname="argument ungraceful", value=ungraceful, expected_type=type_hints["ungraceful"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ungraceful is not None:
                self._values["ungraceful"] = ungraceful

        @builtins.property
        def ungraceful(self) -> typing.Optional[builtins.str]:
            '''The settings for ungraceful execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-globalauroraungraceful.html#cfn-arcregionswitch-plan-globalauroraungraceful-ungraceful
            '''
            result = self._values.get("ungraceful")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlobalAuroraUngracefulProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.HealthCheckStateProperty",
        jsii_struct_bases=[],
        name_mapping={"health_check_id": "healthCheckId", "region": "region"},
    )
    class HealthCheckStateProperty:
        def __init__(
            self,
            *,
            health_check_id: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param health_check_id: 
            :param region: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-healthcheckstate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                health_check_state_property = arcregionswitch_mixins.CfnPlanPropsMixin.HealthCheckStateProperty(
                    health_check_id="healthCheckId",
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9fd2c712de3e0d1f5813ee1cc5b56a79d5e487fa7283e1bb2c3f3b7db7c85aa5)
                check_type(argname="argument health_check_id", value=health_check_id, expected_type=type_hints["health_check_id"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if health_check_id is not None:
                self._values["health_check_id"] = health_check_id
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def health_check_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-healthcheckstate.html#cfn-arcregionswitch-plan-healthcheckstate-healthcheckid
            '''
            result = self._values.get("health_check_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-healthcheckstate.html#cfn-arcregionswitch-plan-healthcheckstate-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckStateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.KubernetesResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"api_version": "apiVersion", "kind": "kind"},
    )
    class KubernetesResourceTypeProperty:
        def __init__(
            self,
            *,
            api_version: typing.Optional[builtins.str] = None,
            kind: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines the type of Kubernetes resource to scale in an Amazon EKS cluster.

            :param api_version: The API version type for the Kubernetes resource.
            :param kind: The kind for the Kubernetes resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-kubernetesresourcetype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                kubernetes_resource_type_property = arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesResourceTypeProperty(
                    api_version="apiVersion",
                    kind="kind"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea34de91796f73baca849a2ad4f8514039657ad1efb37d00b9a8edf5f4c66142)
                check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
                check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_version is not None:
                self._values["api_version"] = api_version
            if kind is not None:
                self._values["kind"] = kind

        @builtins.property
        def api_version(self) -> typing.Optional[builtins.str]:
            '''The API version type for the Kubernetes resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-kubernetesresourcetype.html#cfn-arcregionswitch-plan-kubernetesresourcetype-apiversion
            '''
            result = self._values.get("api_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kind(self) -> typing.Optional[builtins.str]:
            '''The kind for the Kubernetes resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-kubernetesresourcetype.html#cfn-arcregionswitch-plan-kubernetesresourcetype-kind
            '''
            result = self._values.get("kind")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KubernetesResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.KubernetesScalingResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"hpa_name": "hpaName", "name": "name", "namespace": "namespace"},
    )
    class KubernetesScalingResourceProperty:
        def __init__(
            self,
            *,
            hpa_name: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a Kubernetes resource to scale in an Amazon EKS cluster.

            :param hpa_name: The hpaname for the Kubernetes resource.
            :param name: The name for the Kubernetes resource.
            :param namespace: The namespace for the Kubernetes resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-kubernetesscalingresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                kubernetes_scaling_resource_property = arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesScalingResourceProperty(
                    hpa_name="hpaName",
                    name="name",
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a270b7ad157aa546ec5e3ba9d159a6cdae7ea69fc8cf748d5c3f526695029c6e)
                check_type(argname="argument hpa_name", value=hpa_name, expected_type=type_hints["hpa_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hpa_name is not None:
                self._values["hpa_name"] = hpa_name
            if name is not None:
                self._values["name"] = name
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def hpa_name(self) -> typing.Optional[builtins.str]:
            '''The hpaname for the Kubernetes resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-kubernetesscalingresource.html#cfn-arcregionswitch-plan-kubernetesscalingresource-hpaname
            '''
            result = self._values.get("hpa_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name for the Kubernetes resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-kubernetesscalingresource.html#cfn-arcregionswitch-plan-kubernetesscalingresource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace for the Kubernetes resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-kubernetesscalingresource.html#cfn-arcregionswitch-plan-kubernetesscalingresource-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KubernetesScalingResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.LambdaUngracefulProperty",
        jsii_struct_bases=[],
        name_mapping={"behavior": "behavior"},
    )
    class LambdaUngracefulProperty:
        def __init__(self, *, behavior: typing.Optional[builtins.str] = None) -> None:
            '''Configuration for handling failures when invoking Lambda functions.

            :param behavior: The ungraceful behavior for a Lambda function, which must be set to ``skip`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-lambdaungraceful.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                lambda_ungraceful_property = arcregionswitch_mixins.CfnPlanPropsMixin.LambdaUngracefulProperty(
                    behavior="behavior"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92820c03e1bb57fe84e7ec00966797cf630418c1a97d303187253b27627d7657)
                check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if behavior is not None:
                self._values["behavior"] = behavior

        @builtins.property
        def behavior(self) -> typing.Optional[builtins.str]:
            '''The ungraceful behavior for a Lambda function, which must be set to ``skip`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-lambdaungraceful.html#cfn-arcregionswitch-plan-lambdaungraceful-behavior
            '''
            result = self._values.get("behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaUngracefulProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.LambdasProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "cross_account_role": "crossAccountRole",
            "external_id": "externalId",
        },
    )
    class LambdasProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            cross_account_role: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for AWS Lambda functions used in a Region switch plan.

            :param arn: The Amazon Resource Name (ARN) of the Lambda function.
            :param cross_account_role: The cross account role for the configuration.
            :param external_id: The external ID (secret key) for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-lambdas.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                lambdas_property = arcregionswitch_mixins.CfnPlanPropsMixin.LambdasProperty(
                    arn="arn",
                    cross_account_role="crossAccountRole",
                    external_id="externalId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__08e2bdff8aa03672d5075553dd249cb17c6227ea6f05dca6be6d736bbaa8019b)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument cross_account_role", value=cross_account_role, expected_type=type_hints["cross_account_role"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if cross_account_role is not None:
                self._values["cross_account_role"] = cross_account_role
            if external_id is not None:
                self._values["external_id"] = external_id

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-lambdas.html#cfn-arcregionswitch-plan-lambdas-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cross_account_role(self) -> typing.Optional[builtins.str]:
            '''The cross account role for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-lambdas.html#cfn-arcregionswitch-plan-lambdas-crossaccountrole
            '''
            result = self._values.get("cross_account_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID (secret key) for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-lambdas.html#cfn-arcregionswitch-plan-lambdas-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdasProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.ParallelExecutionBlockConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"steps": "steps"},
    )
    class ParallelExecutionBlockConfigurationProperty:
        def __init__(
            self,
            *,
            steps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.StepProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configuration for steps that should be executed in parallel during a Region switch.

            :param steps: The steps for a parallel execution block.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-parallelexecutionblockconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                # parallel_execution_block_configuration_property_: arcregionswitch_mixins.CfnPlanPropsMixin.ParallelExecutionBlockConfigurationProperty
                
                parallel_execution_block_configuration_property = arcregionswitch_mixins.CfnPlanPropsMixin.ParallelExecutionBlockConfigurationProperty(
                    steps=[arcregionswitch_mixins.CfnPlanPropsMixin.StepProperty(
                        description="description",
                        execution_block_configuration=arcregionswitch_mixins.CfnPlanPropsMixin.ExecutionBlockConfigurationProperty(
                            arc_routing_control_config=arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlConfigurationProperty(
                                cross_account_role="crossAccountRole",
                                external_id="externalId",
                                region_and_routing_controls={
                                    "region_and_routing_controls_key": [arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlStateProperty(
                                        routing_control_arn="routingControlArn",
                                        state="state"
                                    )]
                                },
                                timeout_minutes=123
                            ),
                            custom_action_lambda_config=arcregionswitch_mixins.CfnPlanPropsMixin.CustomActionLambdaConfigurationProperty(
                                lambdas=[arcregionswitch_mixins.CfnPlanPropsMixin.LambdasProperty(
                                    arn="arn",
                                    cross_account_role="crossAccountRole",
                                    external_id="externalId"
                                )],
                                region_to_run="regionToRun",
                                retry_interval_minutes=123,
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.LambdaUngracefulProperty(
                                    behavior="behavior"
                                )
                            ),
                            ec2_asg_capacity_increase_config=arcregionswitch_mixins.CfnPlanPropsMixin.Ec2AsgCapacityIncreaseConfigurationProperty(
                                asgs=[arcregionswitch_mixins.CfnPlanPropsMixin.AsgProperty(
                                    arn="arn",
                                    cross_account_role="crossAccountRole",
                                    external_id="externalId"
                                )],
                                capacity_monitoring_approach="capacityMonitoringApproach",
                                target_percent=123,
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.Ec2UngracefulProperty(
                                    minimum_success_percentage=123
                                )
                            ),
                            ecs_capacity_increase_config=arcregionswitch_mixins.CfnPlanPropsMixin.EcsCapacityIncreaseConfigurationProperty(
                                capacity_monitoring_approach="capacityMonitoringApproach",
                                services=[arcregionswitch_mixins.CfnPlanPropsMixin.ServiceProperty(
                                    cluster_arn="clusterArn",
                                    cross_account_role="crossAccountRole",
                                    external_id="externalId",
                                    service_arn="serviceArn"
                                )],
                                target_percent=123,
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.EcsUngracefulProperty(
                                    minimum_success_percentage=123
                                )
                            ),
                            eks_resource_scaling_config=arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingConfigurationProperty(
                                capacity_monitoring_approach="capacityMonitoringApproach",
                                eks_clusters=[arcregionswitch_mixins.CfnPlanPropsMixin.EksClusterProperty(
                                    cluster_arn="clusterArn",
                                    cross_account_role="crossAccountRole",
                                    external_id="externalId"
                                )],
                                kubernetes_resource_type=arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesResourceTypeProperty(
                                    api_version="apiVersion",
                                    kind="kind"
                                ),
                                scaling_resources=[{
                                    "scaling_resources_key": {
                                        "scaling_resources_key": arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesScalingResourceProperty(
                                            hpa_name="hpaName",
                                            name="name",
                                            namespace="namespace"
                                        )
                                    }
                                }],
                                target_percent=123,
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingUngracefulProperty(
                                    minimum_success_percentage=123
                                )
                            ),
                            execution_approval_config=arcregionswitch_mixins.CfnPlanPropsMixin.ExecutionApprovalConfigurationProperty(
                                approval_role="approvalRole",
                                timeout_minutes=123
                            ),
                            global_aurora_config=arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraConfigurationProperty(
                                behavior="behavior",
                                cross_account_role="crossAccountRole",
                                database_cluster_arns=["databaseClusterArns"],
                                external_id="externalId",
                                global_cluster_identifier="globalClusterIdentifier",
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraUngracefulProperty(
                                    ungraceful="ungraceful"
                                )
                            ),
                            parallel_config=parallel_execution_block_configuration_property_,
                            region_switch_plan_config=arcregionswitch_mixins.CfnPlanPropsMixin.RegionSwitchPlanConfigurationProperty(
                                arn="arn",
                                cross_account_role="crossAccountRole",
                                external_id="externalId"
                            ),
                            route53_health_check_config=arcregionswitch_mixins.CfnPlanPropsMixin.Route53HealthCheckConfigurationProperty(
                                cross_account_role="crossAccountRole",
                                external_id="externalId",
                                hosted_zone_id="hostedZoneId",
                                record_name="recordName",
                                record_sets=[arcregionswitch_mixins.CfnPlanPropsMixin.Route53ResourceRecordSetProperty(
                                    record_set_identifier="recordSetIdentifier",
                                    region="region"
                                )],
                                timeout_minutes=123
                            )
                        ),
                        execution_block_type="executionBlockType",
                        name="name"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c4738a388cfb9222789b9ac4991db830c2db33b5fedf64becbdfb1e645a1ffd5)
                check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if steps is not None:
                self._values["steps"] = steps

        @builtins.property
        def steps(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.StepProperty"]]]]:
            '''The steps for a parallel execution block.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-parallelexecutionblockconfiguration.html#cfn-arcregionswitch-plan-parallelexecutionblockconfiguration-steps
            '''
            result = self._values.get("steps")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.StepProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParallelExecutionBlockConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.RegionSwitchPlanConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "cross_account_role": "crossAccountRole",
            "external_id": "externalId",
        },
    )
    class RegionSwitchPlanConfigurationProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            cross_account_role: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for nested Region switch plans.

            This allows one Region switch plan to trigger another plan as part of its execution.

            :param arn: The Amazon Resource Name (ARN) of the plan configuration.
            :param cross_account_role: The cross account role for the configuration.
            :param external_id: The external ID (secret key) for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-regionswitchplanconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                region_switch_plan_configuration_property = arcregionswitch_mixins.CfnPlanPropsMixin.RegionSwitchPlanConfigurationProperty(
                    arn="arn",
                    cross_account_role="crossAccountRole",
                    external_id="externalId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c7eecd526d1046c817a8297da3102d065b2e0ee8f5d8c5567bdb3be5c7eca2c)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument cross_account_role", value=cross_account_role, expected_type=type_hints["cross_account_role"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if cross_account_role is not None:
                self._values["cross_account_role"] = cross_account_role
            if external_id is not None:
                self._values["external_id"] = external_id

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the plan configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-regionswitchplanconfiguration.html#cfn-arcregionswitch-plan-regionswitchplanconfiguration-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cross_account_role(self) -> typing.Optional[builtins.str]:
            '''The cross account role for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-regionswitchplanconfiguration.html#cfn-arcregionswitch-plan-regionswitchplanconfiguration-crossaccountrole
            '''
            result = self._values.get("cross_account_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID (secret key) for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-regionswitchplanconfiguration.html#cfn-arcregionswitch-plan-regionswitchplanconfiguration-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegionSwitchPlanConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.Route53HealthCheckConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cross_account_role": "crossAccountRole",
            "external_id": "externalId",
            "hosted_zone_id": "hostedZoneId",
            "record_name": "recordName",
            "record_sets": "recordSets",
            "timeout_minutes": "timeoutMinutes",
        },
    )
    class Route53HealthCheckConfigurationProperty:
        def __init__(
            self,
            *,
            cross_account_role: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
            record_name: typing.Optional[builtins.str] = None,
            record_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.Route53ResourceRecordSetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            timeout_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The Amazon Route 53 health check configuration.

            :param cross_account_role: The cross account role for the configuration.
            :param external_id: The external ID (secret key) for the configuration.
            :param hosted_zone_id: The Amazon Route 53 health check configuration hosted zone ID.
            :param record_name: The Amazon Route 53 health check configuration record name.
            :param record_sets: The Amazon Route 53 health check configuration record sets.
            :param timeout_minutes: The Amazon Route 53 health check configuration time out (in minutes). Default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53healthcheckconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                route53_health_check_configuration_property = arcregionswitch_mixins.CfnPlanPropsMixin.Route53HealthCheckConfigurationProperty(
                    cross_account_role="crossAccountRole",
                    external_id="externalId",
                    hosted_zone_id="hostedZoneId",
                    record_name="recordName",
                    record_sets=[arcregionswitch_mixins.CfnPlanPropsMixin.Route53ResourceRecordSetProperty(
                        record_set_identifier="recordSetIdentifier",
                        region="region"
                    )],
                    timeout_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1d375d86de6d706e2f1ccca366d53a4833bfd533775512025bbad2a975c01910)
                check_type(argname="argument cross_account_role", value=cross_account_role, expected_type=type_hints["cross_account_role"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
                check_type(argname="argument record_name", value=record_name, expected_type=type_hints["record_name"])
                check_type(argname="argument record_sets", value=record_sets, expected_type=type_hints["record_sets"])
                check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cross_account_role is not None:
                self._values["cross_account_role"] = cross_account_role
            if external_id is not None:
                self._values["external_id"] = external_id
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id
            if record_name is not None:
                self._values["record_name"] = record_name
            if record_sets is not None:
                self._values["record_sets"] = record_sets
            if timeout_minutes is not None:
                self._values["timeout_minutes"] = timeout_minutes

        @builtins.property
        def cross_account_role(self) -> typing.Optional[builtins.str]:
            '''The cross account role for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53healthcheckconfiguration.html#cfn-arcregionswitch-plan-route53healthcheckconfiguration-crossaccountrole
            '''
            result = self._values.get("cross_account_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID (secret key) for the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53healthcheckconfiguration.html#cfn-arcregionswitch-plan-route53healthcheckconfiguration-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Route 53 health check configuration hosted zone ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53healthcheckconfiguration.html#cfn-arcregionswitch-plan-route53healthcheckconfiguration-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon Route 53 health check configuration record name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53healthcheckconfiguration.html#cfn-arcregionswitch-plan-route53healthcheckconfiguration-recordname
            '''
            result = self._values.get("record_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_sets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.Route53ResourceRecordSetProperty"]]]]:
            '''The Amazon Route 53 health check configuration record sets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53healthcheckconfiguration.html#cfn-arcregionswitch-plan-route53healthcheckconfiguration-recordsets
            '''
            result = self._values.get("record_sets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.Route53ResourceRecordSetProperty"]]]], result)

        @builtins.property
        def timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The Amazon Route 53 health check configuration time out (in minutes).

            :default: - 60

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53healthcheckconfiguration.html#cfn-arcregionswitch-plan-route53healthcheckconfiguration-timeoutminutes
            '''
            result = self._values.get("timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Route53HealthCheckConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.Route53HealthChecksProperty",
        jsii_struct_bases=[],
        name_mapping={
            "health_check_ids": "healthCheckIds",
            "hosted_zone_ids": "hostedZoneIds",
            "record_names": "recordNames",
            "regions": "regions",
        },
    )
    class Route53HealthChecksProperty:
        def __init__(
            self,
            *,
            health_check_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            hosted_zone_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            record_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param health_check_ids: 
            :param hosted_zone_ids: 
            :param record_names: 
            :param regions: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53healthchecks.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                route53_health_checks_property = arcregionswitch_mixins.CfnPlanPropsMixin.Route53HealthChecksProperty(
                    health_check_ids=["healthCheckIds"],
                    hosted_zone_ids=["hostedZoneIds"],
                    record_names=["recordNames"],
                    regions=["regions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de3814f60c9eeed56e551224f39b2ffc2962d58f6783435ca14fc902fa59e564)
                check_type(argname="argument health_check_ids", value=health_check_ids, expected_type=type_hints["health_check_ids"])
                check_type(argname="argument hosted_zone_ids", value=hosted_zone_ids, expected_type=type_hints["hosted_zone_ids"])
                check_type(argname="argument record_names", value=record_names, expected_type=type_hints["record_names"])
                check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if health_check_ids is not None:
                self._values["health_check_ids"] = health_check_ids
            if hosted_zone_ids is not None:
                self._values["hosted_zone_ids"] = hosted_zone_ids
            if record_names is not None:
                self._values["record_names"] = record_names
            if regions is not None:
                self._values["regions"] = regions

        @builtins.property
        def health_check_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53healthchecks.html#cfn-arcregionswitch-plan-route53healthchecks-healthcheckids
            '''
            result = self._values.get("health_check_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def hosted_zone_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53healthchecks.html#cfn-arcregionswitch-plan-route53healthchecks-hostedzoneids
            '''
            result = self._values.get("hosted_zone_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def record_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53healthchecks.html#cfn-arcregionswitch-plan-route53healthchecks-recordnames
            '''
            result = self._values.get("record_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53healthchecks.html#cfn-arcregionswitch-plan-route53healthchecks-regions
            '''
            result = self._values.get("regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Route53HealthChecksProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.Route53ResourceRecordSetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_set_identifier": "recordSetIdentifier",
            "region": "region",
        },
    )
    class Route53ResourceRecordSetProperty:
        def __init__(
            self,
            *,
            record_set_identifier: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon Route 53 record set.

            :param record_set_identifier: The Amazon Route 53 record set identifier.
            :param region: The Amazon Route 53 record set Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53resourcerecordset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                route53_resource_record_set_property = arcregionswitch_mixins.CfnPlanPropsMixin.Route53ResourceRecordSetProperty(
                    record_set_identifier="recordSetIdentifier",
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dd9ef0b7a1f04d25033e7b6d8aa93ff59042cdd94bf0708c65a70ba1531e5015)
                check_type(argname="argument record_set_identifier", value=record_set_identifier, expected_type=type_hints["record_set_identifier"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if record_set_identifier is not None:
                self._values["record_set_identifier"] = record_set_identifier
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def record_set_identifier(self) -> typing.Optional[builtins.str]:
            '''The Amazon Route 53 record set identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53resourcerecordset.html#cfn-arcregionswitch-plan-route53resourcerecordset-recordsetidentifier
            '''
            result = self._values.get("record_set_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The Amazon Route 53 record set Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-route53resourcerecordset.html#cfn-arcregionswitch-plan-route53resourcerecordset-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Route53ResourceRecordSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.ServiceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cluster_arn": "clusterArn",
            "cross_account_role": "crossAccountRole",
            "external_id": "externalId",
            "service_arn": "serviceArn",
        },
    )
    class ServiceProperty:
        def __init__(
            self,
            *,
            cluster_arn: typing.Optional[builtins.str] = None,
            cross_account_role: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
            service_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The service for a cross account role.

            :param cluster_arn: The cluster Amazon Resource Name (ARN) for a service.
            :param cross_account_role: The cross account role for a service.
            :param external_id: The external ID (secret key) for the service.
            :param service_arn: The Amazon Resource Name (ARN) for a service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-service.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                service_property = arcregionswitch_mixins.CfnPlanPropsMixin.ServiceProperty(
                    cluster_arn="clusterArn",
                    cross_account_role="crossAccountRole",
                    external_id="externalId",
                    service_arn="serviceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9036c40d0207a1d32cf1a5876890c3665f34b79e9dd4c8d2b6d6994bc385aeeb)
                check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
                check_type(argname="argument cross_account_role", value=cross_account_role, expected_type=type_hints["cross_account_role"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
                check_type(argname="argument service_arn", value=service_arn, expected_type=type_hints["service_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cluster_arn is not None:
                self._values["cluster_arn"] = cluster_arn
            if cross_account_role is not None:
                self._values["cross_account_role"] = cross_account_role
            if external_id is not None:
                self._values["external_id"] = external_id
            if service_arn is not None:
                self._values["service_arn"] = service_arn

        @builtins.property
        def cluster_arn(self) -> typing.Optional[builtins.str]:
            '''The cluster Amazon Resource Name (ARN) for a service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-service.html#cfn-arcregionswitch-plan-service-clusterarn
            '''
            result = self._values.get("cluster_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cross_account_role(self) -> typing.Optional[builtins.str]:
            '''The cross account role for a service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-service.html#cfn-arcregionswitch-plan-service-crossaccountrole
            '''
            result = self._values.get("cross_account_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID (secret key) for the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-service.html#cfn-arcregionswitch-plan-service-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for a service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-service.html#cfn-arcregionswitch-plan-service-servicearn
            '''
            result = self._values.get("service_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.StepProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "execution_block_configuration": "executionBlockConfiguration",
            "execution_block_type": "executionBlockType",
            "name": "name",
        },
    )
    class StepProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            execution_block_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.ExecutionBlockConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            execution_block_type: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a step in a Region switch plan workflow.

            Each step performs a specific action during the Region switch process.

            :param description: The description of a step in a workflow.
            :param execution_block_configuration: The configuration for an execution block in a workflow.
            :param execution_block_type: The type of an execution block in a workflow.
            :param name: The name of a step in a workflow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-step.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                # step_property_: arcregionswitch_mixins.CfnPlanPropsMixin.StepProperty
                
                step_property = arcregionswitch_mixins.CfnPlanPropsMixin.StepProperty(
                    description="description",
                    execution_block_configuration=arcregionswitch_mixins.CfnPlanPropsMixin.ExecutionBlockConfigurationProperty(
                        arc_routing_control_config=arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlConfigurationProperty(
                            cross_account_role="crossAccountRole",
                            external_id="externalId",
                            region_and_routing_controls={
                                "region_and_routing_controls_key": [arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlStateProperty(
                                    routing_control_arn="routingControlArn",
                                    state="state"
                                )]
                            },
                            timeout_minutes=123
                        ),
                        custom_action_lambda_config=arcregionswitch_mixins.CfnPlanPropsMixin.CustomActionLambdaConfigurationProperty(
                            lambdas=[arcregionswitch_mixins.CfnPlanPropsMixin.LambdasProperty(
                                arn="arn",
                                cross_account_role="crossAccountRole",
                                external_id="externalId"
                            )],
                            region_to_run="regionToRun",
                            retry_interval_minutes=123,
                            timeout_minutes=123,
                            ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.LambdaUngracefulProperty(
                                behavior="behavior"
                            )
                        ),
                        ec2_asg_capacity_increase_config=arcregionswitch_mixins.CfnPlanPropsMixin.Ec2AsgCapacityIncreaseConfigurationProperty(
                            asgs=[arcregionswitch_mixins.CfnPlanPropsMixin.AsgProperty(
                                arn="arn",
                                cross_account_role="crossAccountRole",
                                external_id="externalId"
                            )],
                            capacity_monitoring_approach="capacityMonitoringApproach",
                            target_percent=123,
                            timeout_minutes=123,
                            ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.Ec2UngracefulProperty(
                                minimum_success_percentage=123
                            )
                        ),
                        ecs_capacity_increase_config=arcregionswitch_mixins.CfnPlanPropsMixin.EcsCapacityIncreaseConfigurationProperty(
                            capacity_monitoring_approach="capacityMonitoringApproach",
                            services=[arcregionswitch_mixins.CfnPlanPropsMixin.ServiceProperty(
                                cluster_arn="clusterArn",
                                cross_account_role="crossAccountRole",
                                external_id="externalId",
                                service_arn="serviceArn"
                            )],
                            target_percent=123,
                            timeout_minutes=123,
                            ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.EcsUngracefulProperty(
                                minimum_success_percentage=123
                            )
                        ),
                        eks_resource_scaling_config=arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingConfigurationProperty(
                            capacity_monitoring_approach="capacityMonitoringApproach",
                            eks_clusters=[arcregionswitch_mixins.CfnPlanPropsMixin.EksClusterProperty(
                                cluster_arn="clusterArn",
                                cross_account_role="crossAccountRole",
                                external_id="externalId"
                            )],
                            kubernetes_resource_type=arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesResourceTypeProperty(
                                api_version="apiVersion",
                                kind="kind"
                            ),
                            scaling_resources=[{
                                "scaling_resources_key": {
                                    "scaling_resources_key": arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesScalingResourceProperty(
                                        hpa_name="hpaName",
                                        name="name",
                                        namespace="namespace"
                                    )
                                }
                            }],
                            target_percent=123,
                            timeout_minutes=123,
                            ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingUngracefulProperty(
                                minimum_success_percentage=123
                            )
                        ),
                        execution_approval_config=arcregionswitch_mixins.CfnPlanPropsMixin.ExecutionApprovalConfigurationProperty(
                            approval_role="approvalRole",
                            timeout_minutes=123
                        ),
                        global_aurora_config=arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraConfigurationProperty(
                            behavior="behavior",
                            cross_account_role="crossAccountRole",
                            database_cluster_arns=["databaseClusterArns"],
                            external_id="externalId",
                            global_cluster_identifier="globalClusterIdentifier",
                            timeout_minutes=123,
                            ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraUngracefulProperty(
                                ungraceful="ungraceful"
                            )
                        ),
                        parallel_config=arcregionswitch_mixins.CfnPlanPropsMixin.ParallelExecutionBlockConfigurationProperty(
                            steps=[step_property_]
                        ),
                        region_switch_plan_config=arcregionswitch_mixins.CfnPlanPropsMixin.RegionSwitchPlanConfigurationProperty(
                            arn="arn",
                            cross_account_role="crossAccountRole",
                            external_id="externalId"
                        ),
                        route53_health_check_config=arcregionswitch_mixins.CfnPlanPropsMixin.Route53HealthCheckConfigurationProperty(
                            cross_account_role="crossAccountRole",
                            external_id="externalId",
                            hosted_zone_id="hostedZoneId",
                            record_name="recordName",
                            record_sets=[arcregionswitch_mixins.CfnPlanPropsMixin.Route53ResourceRecordSetProperty(
                                record_set_identifier="recordSetIdentifier",
                                region="region"
                            )],
                            timeout_minutes=123
                        )
                    ),
                    execution_block_type="executionBlockType",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7d4b1dbd42b7beada9a7eefc48e9d37e7a7686aecf1bdf54eb80cf2e36dd8df)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument execution_block_configuration", value=execution_block_configuration, expected_type=type_hints["execution_block_configuration"])
                check_type(argname="argument execution_block_type", value=execution_block_type, expected_type=type_hints["execution_block_type"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if execution_block_configuration is not None:
                self._values["execution_block_configuration"] = execution_block_configuration
            if execution_block_type is not None:
                self._values["execution_block_type"] = execution_block_type
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of a step in a workflow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-step.html#cfn-arcregionswitch-plan-step-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def execution_block_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ExecutionBlockConfigurationProperty"]]:
            '''The configuration for an execution block in a workflow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-step.html#cfn-arcregionswitch-plan-step-executionblockconfiguration
            '''
            result = self._values.get("execution_block_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ExecutionBlockConfigurationProperty"]], result)

        @builtins.property
        def execution_block_type(self) -> typing.Optional[builtins.str]:
            '''The type of an execution block in a workflow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-step.html#cfn-arcregionswitch-plan-step-executionblocktype
            '''
            result = self._values.get("execution_block_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of a step in a workflow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-step.html#cfn-arcregionswitch-plan-step-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StepProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.TriggerConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "associated_alarm_name": "associatedAlarmName",
            "condition": "condition",
        },
    )
    class TriggerConditionProperty:
        def __init__(
            self,
            *,
            associated_alarm_name: typing.Optional[builtins.str] = None,
            condition: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a condition that must be met for a trigger to fire.

            :param associated_alarm_name: The name of the CloudWatch alarm associated with the condition.
            :param condition: The condition that must be met. Valid values include ALARM and OK.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-triggercondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                trigger_condition_property = arcregionswitch_mixins.CfnPlanPropsMixin.TriggerConditionProperty(
                    associated_alarm_name="associatedAlarmName",
                    condition="condition"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8fece57b504e78dabffa0ebaefc748ec720150f87abb43adba3bed28512d1ce)
                check_type(argname="argument associated_alarm_name", value=associated_alarm_name, expected_type=type_hints["associated_alarm_name"])
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if associated_alarm_name is not None:
                self._values["associated_alarm_name"] = associated_alarm_name
            if condition is not None:
                self._values["condition"] = condition

        @builtins.property
        def associated_alarm_name(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch alarm associated with the condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-triggercondition.html#cfn-arcregionswitch-plan-triggercondition-associatedalarmname
            '''
            result = self._values.get("associated_alarm_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def condition(self) -> typing.Optional[builtins.str]:
            '''The condition that must be met.

            Valid values include ALARM and OK.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-triggercondition.html#cfn-arcregionswitch-plan-triggercondition-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggerConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.TriggerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "conditions": "conditions",
            "description": "description",
            "min_delay_minutes_between_executions": "minDelayMinutesBetweenExecutions",
            "target_region": "targetRegion",
        },
    )
    class TriggerProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.TriggerConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            description: typing.Optional[builtins.str] = None,
            min_delay_minutes_between_executions: typing.Optional[jsii.Number] = None,
            target_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a condition that can automatically trigger the execution of a Region switch plan.

            :param action: The action to perform when the trigger fires. Valid values include ACTIVATE and DEACTIVATE.
            :param conditions: The conditions that must be met for the trigger to fire.
            :param description: The description for a trigger.
            :param min_delay_minutes_between_executions: The minimum time, in minutes, that must elapse between automatic executions of the plan.
            :param target_region: The AWS Region for a trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-trigger.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                trigger_property = arcregionswitch_mixins.CfnPlanPropsMixin.TriggerProperty(
                    action="action",
                    conditions=[arcregionswitch_mixins.CfnPlanPropsMixin.TriggerConditionProperty(
                        associated_alarm_name="associatedAlarmName",
                        condition="condition"
                    )],
                    description="description",
                    min_delay_minutes_between_executions=123,
                    target_region="targetRegion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd3e21d530597dfceac1545d7fea064029759c2866f807b324fa507f506b0dec)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument min_delay_minutes_between_executions", value=min_delay_minutes_between_executions, expected_type=type_hints["min_delay_minutes_between_executions"])
                check_type(argname="argument target_region", value=target_region, expected_type=type_hints["target_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if conditions is not None:
                self._values["conditions"] = conditions
            if description is not None:
                self._values["description"] = description
            if min_delay_minutes_between_executions is not None:
                self._values["min_delay_minutes_between_executions"] = min_delay_minutes_between_executions
            if target_region is not None:
                self._values["target_region"] = target_region

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to perform when the trigger fires.

            Valid values include ACTIVATE and DEACTIVATE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-trigger.html#cfn-arcregionswitch-plan-trigger-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def conditions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.TriggerConditionProperty"]]]]:
            '''The conditions that must be met for the trigger to fire.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-trigger.html#cfn-arcregionswitch-plan-trigger-conditions
            '''
            result = self._values.get("conditions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.TriggerConditionProperty"]]]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description for a trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-trigger.html#cfn-arcregionswitch-plan-trigger-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def min_delay_minutes_between_executions(self) -> typing.Optional[jsii.Number]:
            '''The minimum time, in minutes, that must elapse between automatic executions of the plan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-trigger.html#cfn-arcregionswitch-plan-trigger-mindelayminutesbetweenexecutions
            '''
            result = self._values.get("min_delay_minutes_between_executions")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def target_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region for a trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-trigger.html#cfn-arcregionswitch-plan-trigger-targetregion
            '''
            result = self._values.get("target_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arcregionswitch.mixins.CfnPlanPropsMixin.WorkflowProperty",
        jsii_struct_bases=[],
        name_mapping={
            "steps": "steps",
            "workflow_description": "workflowDescription",
            "workflow_target_action": "workflowTargetAction",
            "workflow_target_region": "workflowTargetRegion",
        },
    )
    class WorkflowProperty:
        def __init__(
            self,
            *,
            steps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.StepProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            workflow_description: typing.Optional[builtins.str] = None,
            workflow_target_action: typing.Optional[builtins.str] = None,
            workflow_target_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a workflow in a Region switch plan.

            A workflow defines a sequence of steps to execute during a Region switch.

            :param steps: The steps that make up the workflow.
            :param workflow_description: The description of the workflow.
            :param workflow_target_action: The action that the workflow performs. Valid values include ACTIVATE and DEACTIVATE.
            :param workflow_target_region: The AWS Region that the workflow targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-workflow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arcregionswitch import mixins as arcregionswitch_mixins
                
                # step_property_: arcregionswitch_mixins.CfnPlanPropsMixin.StepProperty
                
                workflow_property = arcregionswitch_mixins.CfnPlanPropsMixin.WorkflowProperty(
                    steps=[arcregionswitch_mixins.CfnPlanPropsMixin.StepProperty(
                        description="description",
                        execution_block_configuration=arcregionswitch_mixins.CfnPlanPropsMixin.ExecutionBlockConfigurationProperty(
                            arc_routing_control_config=arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlConfigurationProperty(
                                cross_account_role="crossAccountRole",
                                external_id="externalId",
                                region_and_routing_controls={
                                    "region_and_routing_controls_key": [arcregionswitch_mixins.CfnPlanPropsMixin.ArcRoutingControlStateProperty(
                                        routing_control_arn="routingControlArn",
                                        state="state"
                                    )]
                                },
                                timeout_minutes=123
                            ),
                            custom_action_lambda_config=arcregionswitch_mixins.CfnPlanPropsMixin.CustomActionLambdaConfigurationProperty(
                                lambdas=[arcregionswitch_mixins.CfnPlanPropsMixin.LambdasProperty(
                                    arn="arn",
                                    cross_account_role="crossAccountRole",
                                    external_id="externalId"
                                )],
                                region_to_run="regionToRun",
                                retry_interval_minutes=123,
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.LambdaUngracefulProperty(
                                    behavior="behavior"
                                )
                            ),
                            ec2_asg_capacity_increase_config=arcregionswitch_mixins.CfnPlanPropsMixin.Ec2AsgCapacityIncreaseConfigurationProperty(
                                asgs=[arcregionswitch_mixins.CfnPlanPropsMixin.AsgProperty(
                                    arn="arn",
                                    cross_account_role="crossAccountRole",
                                    external_id="externalId"
                                )],
                                capacity_monitoring_approach="capacityMonitoringApproach",
                                target_percent=123,
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.Ec2UngracefulProperty(
                                    minimum_success_percentage=123
                                )
                            ),
                            ecs_capacity_increase_config=arcregionswitch_mixins.CfnPlanPropsMixin.EcsCapacityIncreaseConfigurationProperty(
                                capacity_monitoring_approach="capacityMonitoringApproach",
                                services=[arcregionswitch_mixins.CfnPlanPropsMixin.ServiceProperty(
                                    cluster_arn="clusterArn",
                                    cross_account_role="crossAccountRole",
                                    external_id="externalId",
                                    service_arn="serviceArn"
                                )],
                                target_percent=123,
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.EcsUngracefulProperty(
                                    minimum_success_percentage=123
                                )
                            ),
                            eks_resource_scaling_config=arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingConfigurationProperty(
                                capacity_monitoring_approach="capacityMonitoringApproach",
                                eks_clusters=[arcregionswitch_mixins.CfnPlanPropsMixin.EksClusterProperty(
                                    cluster_arn="clusterArn",
                                    cross_account_role="crossAccountRole",
                                    external_id="externalId"
                                )],
                                kubernetes_resource_type=arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesResourceTypeProperty(
                                    api_version="apiVersion",
                                    kind="kind"
                                ),
                                scaling_resources=[{
                                    "scaling_resources_key": {
                                        "scaling_resources_key": arcregionswitch_mixins.CfnPlanPropsMixin.KubernetesScalingResourceProperty(
                                            hpa_name="hpaName",
                                            name="name",
                                            namespace="namespace"
                                        )
                                    }
                                }],
                                target_percent=123,
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.EksResourceScalingUngracefulProperty(
                                    minimum_success_percentage=123
                                )
                            ),
                            execution_approval_config=arcregionswitch_mixins.CfnPlanPropsMixin.ExecutionApprovalConfigurationProperty(
                                approval_role="approvalRole",
                                timeout_minutes=123
                            ),
                            global_aurora_config=arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraConfigurationProperty(
                                behavior="behavior",
                                cross_account_role="crossAccountRole",
                                database_cluster_arns=["databaseClusterArns"],
                                external_id="externalId",
                                global_cluster_identifier="globalClusterIdentifier",
                                timeout_minutes=123,
                                ungraceful=arcregionswitch_mixins.CfnPlanPropsMixin.GlobalAuroraUngracefulProperty(
                                    ungraceful="ungraceful"
                                )
                            ),
                            parallel_config=arcregionswitch_mixins.CfnPlanPropsMixin.ParallelExecutionBlockConfigurationProperty(
                                steps=[step_property_]
                            ),
                            region_switch_plan_config=arcregionswitch_mixins.CfnPlanPropsMixin.RegionSwitchPlanConfigurationProperty(
                                arn="arn",
                                cross_account_role="crossAccountRole",
                                external_id="externalId"
                            ),
                            route53_health_check_config=arcregionswitch_mixins.CfnPlanPropsMixin.Route53HealthCheckConfigurationProperty(
                                cross_account_role="crossAccountRole",
                                external_id="externalId",
                                hosted_zone_id="hostedZoneId",
                                record_name="recordName",
                                record_sets=[arcregionswitch_mixins.CfnPlanPropsMixin.Route53ResourceRecordSetProperty(
                                    record_set_identifier="recordSetIdentifier",
                                    region="region"
                                )],
                                timeout_minutes=123
                            )
                        ),
                        execution_block_type="executionBlockType",
                        name="name"
                    )],
                    workflow_description="workflowDescription",
                    workflow_target_action="workflowTargetAction",
                    workflow_target_region="workflowTargetRegion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c331a8ef156c4fb8bc0cb5cf9d04bbdbee9c622e75ae87231431b742cc32063c)
                check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
                check_type(argname="argument workflow_description", value=workflow_description, expected_type=type_hints["workflow_description"])
                check_type(argname="argument workflow_target_action", value=workflow_target_action, expected_type=type_hints["workflow_target_action"])
                check_type(argname="argument workflow_target_region", value=workflow_target_region, expected_type=type_hints["workflow_target_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if steps is not None:
                self._values["steps"] = steps
            if workflow_description is not None:
                self._values["workflow_description"] = workflow_description
            if workflow_target_action is not None:
                self._values["workflow_target_action"] = workflow_target_action
            if workflow_target_region is not None:
                self._values["workflow_target_region"] = workflow_target_region

        @builtins.property
        def steps(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.StepProperty"]]]]:
            '''The steps that make up the workflow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-workflow.html#cfn-arcregionswitch-plan-workflow-steps
            '''
            result = self._values.get("steps")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.StepProperty"]]]], result)

        @builtins.property
        def workflow_description(self) -> typing.Optional[builtins.str]:
            '''The description of the workflow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-workflow.html#cfn-arcregionswitch-plan-workflow-workflowdescription
            '''
            result = self._values.get("workflow_description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def workflow_target_action(self) -> typing.Optional[builtins.str]:
            '''The action that the workflow performs.

            Valid values include ACTIVATE and DEACTIVATE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-workflow.html#cfn-arcregionswitch-plan-workflow-workflowtargetaction
            '''
            result = self._values.get("workflow_target_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def workflow_target_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region that the workflow targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arcregionswitch-plan-workflow.html#cfn-arcregionswitch-plan-workflow-workflowtargetregion
            '''
            result = self._values.get("workflow_target_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnPlanMixinProps",
    "CfnPlanPropsMixin",
]

publication.publish()

def _typecheckingstub__8386d5312f53d51ee1bdd200ee9303f9fe90a07e433c08f6a4386ac40d8f82ad(
    *,
    associated_alarms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.AssociatedAlarmProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    execution_role: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    primary_region: typing.Optional[builtins.str] = None,
    recovery_approach: typing.Optional[builtins.str] = None,
    recovery_time_objective_minutes: typing.Optional[jsii.Number] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    triggers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.TriggerProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    workflows: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.WorkflowProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02927817f099aea448dc17179be5908e55fd27c1faff183f516daab6e0e2f173(
    props: typing.Union[CfnPlanMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9968ff691ecb114d016d5a3e82c9b414a5fdb955b3135949e36f2fe1311e43(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a91287d75e622a41b3049c7921662670e950efdf9dd7239e56ef17caafedf9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b635568571a06e9e55acfa2a3ecf9f0a5b082fe2156aba4e68ca2910361824(
    *,
    cross_account_role: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    region_and_routing_controls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.ArcRoutingControlStateProperty, typing.Dict[builtins.str, typing.Any]]]]]]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65b2650d0ced2059e4639907ceab60c198bc985ddcbd349ee0c454b6099e261(
    *,
    routing_control_arn: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df09f7075961b2ee034bab94576e69d2e2b149eea6ef139d129ed8da0af8b0fe(
    *,
    arn: typing.Optional[builtins.str] = None,
    cross_account_role: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e703a161504358962c74f058528fe8df63184e4a16a7b16937ef6cbd9178471(
    *,
    alarm_type: typing.Optional[builtins.str] = None,
    cross_account_role: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    resource_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25614feef2e72b714dfb8d6034fe976618e3f19e9d55b2ccfb54ed002d75d5c(
    *,
    lambdas: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.LambdasProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    region_to_run: typing.Optional[builtins.str] = None,
    retry_interval_minutes: typing.Optional[jsii.Number] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    ungraceful: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.LambdaUngracefulProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743860ca02471133ca1b320b1553f1a9cad96c501cd50dd4faa020b47721d554(
    *,
    asgs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.AsgProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    capacity_monitoring_approach: typing.Optional[builtins.str] = None,
    target_percent: typing.Optional[jsii.Number] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    ungraceful: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.Ec2UngracefulProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__977dd12f7fe108c1722a5001d534514222f029e6b548a731576a58e2709cebea(
    *,
    minimum_success_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d979b81def65c94faa51fc046006b6dbe7331afbd1164c89b2014bcf89ad18(
    *,
    capacity_monitoring_approach: typing.Optional[builtins.str] = None,
    services: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.ServiceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    target_percent: typing.Optional[jsii.Number] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    ungraceful: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.EcsUngracefulProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527e26acda0abc4e0b1bd0d382e0a736f25049c22c4e99997c2bb13ba812c64b(
    *,
    minimum_success_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b2299808b1f9fd2f7a402045e006d5fadd21039619c15ccfba5fe9d976aa608(
    *,
    cluster_arn: typing.Optional[builtins.str] = None,
    cross_account_role: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf3327986585c65e94599224a24d86b83df635addf78632d39e771e04ad8e95(
    *,
    capacity_monitoring_approach: typing.Optional[builtins.str] = None,
    eks_clusters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.EksClusterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    kubernetes_resource_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.KubernetesResourceTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scaling_resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.KubernetesScalingResourceProperty, typing.Dict[builtins.str, typing.Any]]]]]]]]]] = None,
    target_percent: typing.Optional[jsii.Number] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    ungraceful: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.EksResourceScalingUngracefulProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52e2311a13e18f78cd07cfff90054b3f07a236b58cf44d15ed61dd23dbda32e(
    *,
    minimum_success_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025fce55820542914cd108e554f5af60e6b8ce8d4395c2ff2640af9a1682aa11(
    *,
    approval_role: typing.Optional[builtins.str] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8989f9b403c30f6241dbc5de359dda594041df9692c3c78e1019a14c90705fe4(
    *,
    arc_routing_control_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.ArcRoutingControlConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_action_lambda_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.CustomActionLambdaConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ec2_asg_capacity_increase_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.Ec2AsgCapacityIncreaseConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ecs_capacity_increase_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.EcsCapacityIncreaseConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    eks_resource_scaling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.EksResourceScalingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    execution_approval_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.ExecutionApprovalConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    global_aurora_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.GlobalAuroraConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parallel_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.ParallelExecutionBlockConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    region_switch_plan_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.RegionSwitchPlanConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    route53_health_check_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.Route53HealthCheckConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0678138de6f8fa0b660fc14588aa094cf9f1c0c7d25f66b3b3c7d6f3d4cc81(
    *,
    behavior: typing.Optional[builtins.str] = None,
    cross_account_role: typing.Optional[builtins.str] = None,
    database_cluster_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_id: typing.Optional[builtins.str] = None,
    global_cluster_identifier: typing.Optional[builtins.str] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    ungraceful: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.GlobalAuroraUngracefulProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958a756e61db04b3321e0873649231bac2d60063746f5c90d58527f64c0fefc0(
    *,
    ungraceful: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd2c712de3e0d1f5813ee1cc5b56a79d5e487fa7283e1bb2c3f3b7db7c85aa5(
    *,
    health_check_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea34de91796f73baca849a2ad4f8514039657ad1efb37d00b9a8edf5f4c66142(
    *,
    api_version: typing.Optional[builtins.str] = None,
    kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a270b7ad157aa546ec5e3ba9d159a6cdae7ea69fc8cf748d5c3f526695029c6e(
    *,
    hpa_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92820c03e1bb57fe84e7ec00966797cf630418c1a97d303187253b27627d7657(
    *,
    behavior: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e2bdff8aa03672d5075553dd249cb17c6227ea6f05dca6be6d736bbaa8019b(
    *,
    arn: typing.Optional[builtins.str] = None,
    cross_account_role: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4738a388cfb9222789b9ac4991db830c2db33b5fedf64becbdfb1e645a1ffd5(
    *,
    steps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.StepProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7eecd526d1046c817a8297da3102d065b2e0ee8f5d8c5567bdb3be5c7eca2c(
    *,
    arn: typing.Optional[builtins.str] = None,
    cross_account_role: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d375d86de6d706e2f1ccca366d53a4833bfd533775512025bbad2a975c01910(
    *,
    cross_account_role: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    record_name: typing.Optional[builtins.str] = None,
    record_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.Route53ResourceRecordSetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3814f60c9eeed56e551224f39b2ffc2962d58f6783435ca14fc902fa59e564(
    *,
    health_check_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    hosted_zone_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    record_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9ef0b7a1f04d25033e7b6d8aa93ff59042cdd94bf0708c65a70ba1531e5015(
    *,
    record_set_identifier: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9036c40d0207a1d32cf1a5876890c3665f34b79e9dd4c8d2b6d6994bc385aeeb(
    *,
    cluster_arn: typing.Optional[builtins.str] = None,
    cross_account_role: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    service_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d4b1dbd42b7beada9a7eefc48e9d37e7a7686aecf1bdf54eb80cf2e36dd8df(
    *,
    description: typing.Optional[builtins.str] = None,
    execution_block_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.ExecutionBlockConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    execution_block_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8fece57b504e78dabffa0ebaefc748ec720150f87abb43adba3bed28512d1ce(
    *,
    associated_alarm_name: typing.Optional[builtins.str] = None,
    condition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd3e21d530597dfceac1545d7fea064029759c2866f807b324fa507f506b0dec(
    *,
    action: typing.Optional[builtins.str] = None,
    conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.TriggerConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    min_delay_minutes_between_executions: typing.Optional[jsii.Number] = None,
    target_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c331a8ef156c4fb8bc0cb5cf9d04bbdbee9c622e75ae87231431b742cc32063c(
    *,
    steps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.StepProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    workflow_description: typing.Optional[builtins.str] = None,
    workflow_target_action: typing.Optional[builtins.str] = None,
    workflow_target_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
