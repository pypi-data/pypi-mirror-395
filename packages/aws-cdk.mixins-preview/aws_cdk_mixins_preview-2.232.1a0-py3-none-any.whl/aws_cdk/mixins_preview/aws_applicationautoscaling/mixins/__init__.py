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
    jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalableTargetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "max_capacity": "maxCapacity",
        "min_capacity": "minCapacity",
        "resource_id": "resourceId",
        "role_arn": "roleArn",
        "scalable_dimension": "scalableDimension",
        "scheduled_actions": "scheduledActions",
        "service_namespace": "serviceNamespace",
        "suspended_state": "suspendedState",
    },
)
class CfnScalableTargetMixinProps:
    def __init__(
        self,
        *,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        resource_id: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        scalable_dimension: typing.Optional[builtins.str] = None,
        scheduled_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalableTargetPropsMixin.ScheduledActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        service_namespace: typing.Optional[builtins.str] = None,
        suspended_state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalableTargetPropsMixin.SuspendedStateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnScalableTargetPropsMixin.

        :param max_capacity: The maximum value that you plan to scale out to. When a scaling policy is in effect, Application Auto Scaling can scale out (expand) as needed to the maximum capacity limit in response to changing demand.
        :param min_capacity: The minimum value that you plan to scale in to. When a scaling policy is in effect, Application Auto Scaling can scale in (contract) as needed to the minimum capacity limit in response to changing demand.
        :param resource_id: The identifier of the resource associated with the scalable target. This string consists of the resource type and unique identifier. - ECS service - The resource type is ``service`` and the unique identifier is the cluster name and service name. Example: ``service/my-cluster/my-service`` . - Spot Fleet - The resource type is ``spot-fleet-request`` and the unique identifier is the Spot Fleet request ID. Example: ``spot-fleet-request/sfr-73fbd2ce-aa30-494c-8788-1cee4EXAMPLE`` . - EMR cluster - The resource type is ``instancegroup`` and the unique identifier is the cluster ID and instance group ID. Example: ``instancegroup/j-2EEZNYKUA1NTV/ig-1791Y4E1L8YI0`` . - AppStream 2.0 fleet - The resource type is ``fleet`` and the unique identifier is the fleet name. Example: ``fleet/sample-fleet`` . - DynamoDB table - The resource type is ``table`` and the unique identifier is the table name. Example: ``table/my-table`` . - DynamoDB global secondary index - The resource type is ``index`` and the unique identifier is the index name. Example: ``table/my-table/index/my-table-index`` . - Aurora DB cluster - The resource type is ``cluster`` and the unique identifier is the cluster name. Example: ``cluster:my-db-cluster`` . - SageMaker endpoint variant - The resource type is ``variant`` and the unique identifier is the resource ID. Example: ``endpoint/my-end-point/variant/KMeansClustering`` . - Custom resources are not supported with a resource type. This parameter must specify the ``OutputValue`` from the CloudFormation template stack used to access the resources. The unique identifier is defined by the service provider. More information is available in our `GitHub repository <https://docs.aws.amazon.com/https://github.com/aws/aws-auto-scaling-custom-resource>`_ . - Amazon Comprehend document classification endpoint - The resource type and unique identifier are specified using the endpoint ARN. Example: ``arn:aws:comprehend:us-west-2:123456789012:document-classifier-endpoint/EXAMPLE`` . - Amazon Comprehend entity recognizer endpoint - The resource type and unique identifier are specified using the endpoint ARN. Example: ``arn:aws:comprehend:us-west-2:123456789012:entity-recognizer-endpoint/EXAMPLE`` . - Lambda provisioned concurrency - The resource type is ``function`` and the unique identifier is the function name with a function version or alias name suffix that is not ``$LATEST`` . Example: ``function:my-function:prod`` or ``function:my-function:1`` . - Amazon Keyspaces table - The resource type is ``table`` and the unique identifier is the table name. Example: ``keyspace/mykeyspace/table/mytable`` . - Amazon MSK cluster - The resource type and unique identifier are specified using the cluster ARN. Example: ``arn:aws:kafka:us-east-1:123456789012:cluster/demo-cluster-1/6357e0b2-0e6a-4b86-a0b4-70df934c2e31-5`` . - Amazon ElastiCache replication group - The resource type is ``replication-group`` and the unique identifier is the replication group name. Example: ``replication-group/mycluster`` . - Amazon ElastiCache cache cluster - The resource type is ``cache-cluster`` and the unique identifier is the cache cluster name. Example: ``cache-cluster/mycluster`` . - Neptune cluster - The resource type is ``cluster`` and the unique identifier is the cluster name. Example: ``cluster:mycluster`` . - SageMaker serverless endpoint - The resource type is ``variant`` and the unique identifier is the resource ID. Example: ``endpoint/my-end-point/variant/KMeansClustering`` . - SageMaker inference component - The resource type is ``inference-component`` and the unique identifier is the resource ID. Example: ``inference-component/my-inference-component`` . - Pool of WorkSpaces - The resource type is ``workspacespool`` and the unique identifier is the pool ID. Example: ``workspacespool/wspool-123456`` .
        :param role_arn: Specify the Amazon Resource Name (ARN) of an Identity and Access Management (IAM) role that allows Application Auto Scaling to modify the scalable target on your behalf. This can be either an IAM service role that Application Auto Scaling can assume to make calls to other AWS resources on your behalf, or a service-linked role for the specified service. For more information, see `How Application Auto Scaling works with IAM <https://docs.aws.amazon.com/autoscaling/application/userguide/security_iam_service-with-iam.html>`_ in the *Application Auto Scaling User Guide* . To automatically create a service-linked role (recommended), specify the full ARN of the service-linked role in your stack template. To find the exact ARN of the service-linked role for your AWS or custom resource, see the `Service-linked roles <https://docs.aws.amazon.com/autoscaling/application/userguide/application-auto-scaling-service-linked-roles.html>`_ topic in the *Application Auto Scaling User Guide* . Look for the ARN in the table at the bottom of the page.
        :param scalable_dimension: The scalable dimension associated with the scalable target. This string consists of the service namespace, resource type, and scaling property. - ``ecs:service:DesiredCount`` - The task count of an ECS service. - ``elasticmapreduce:instancegroup:InstanceCount`` - The instance count of an EMR Instance Group. - ``ec2:spot-fleet-request:TargetCapacity`` - The target capacity of a Spot Fleet. - ``appstream:fleet:DesiredCapacity`` - The capacity of an AppStream 2.0 fleet. - ``dynamodb:table:ReadCapacityUnits`` - The provisioned read capacity for a DynamoDB table. - ``dynamodb:table:WriteCapacityUnits`` - The provisioned write capacity for a DynamoDB table. - ``dynamodb:index:ReadCapacityUnits`` - The provisioned read capacity for a DynamoDB global secondary index. - ``dynamodb:index:WriteCapacityUnits`` - The provisioned write capacity for a DynamoDB global secondary index. - ``rds:cluster:ReadReplicaCount`` - The count of Aurora Replicas in an Aurora DB cluster. Available for Aurora MySQL-compatible edition and Aurora PostgreSQL-compatible edition. - ``sagemaker:variant:DesiredInstanceCount`` - The number of EC2 instances for a SageMaker model endpoint variant. - ``custom-resource:ResourceType:Property`` - The scalable dimension for a custom resource provided by your own application or service. - ``comprehend:document-classifier-endpoint:DesiredInferenceUnits`` - The number of inference units for an Amazon Comprehend document classification endpoint. - ``comprehend:entity-recognizer-endpoint:DesiredInferenceUnits`` - The number of inference units for an Amazon Comprehend entity recognizer endpoint. - ``lambda:function:ProvisionedConcurrency`` - The provisioned concurrency for a Lambda function. - ``cassandra:table:ReadCapacityUnits`` - The provisioned read capacity for an Amazon Keyspaces table. - ``cassandra:table:WriteCapacityUnits`` - The provisioned write capacity for an Amazon Keyspaces table. - ``kafka:broker-storage:VolumeSize`` - The provisioned volume size (in GiB) for brokers in an Amazon MSK cluster. - ``elasticache:cache-cluster:Nodes`` - The number of nodes for an Amazon ElastiCache cache cluster. - ``elasticache:replication-group:NodeGroups`` - The number of node groups for an Amazon ElastiCache replication group. - ``elasticache:replication-group:Replicas`` - The number of replicas per node group for an Amazon ElastiCache replication group. - ``neptune:cluster:ReadReplicaCount`` - The count of read replicas in an Amazon Neptune DB cluster. - ``sagemaker:variant:DesiredProvisionedConcurrency`` - The provisioned concurrency for a SageMaker serverless endpoint. - ``sagemaker:inference-component:DesiredCopyCount`` - The number of copies across an endpoint for a SageMaker inference component. - ``workspaces:workspacespool:DesiredUserSessions`` - The number of user sessions for the WorkSpaces in the pool.
        :param scheduled_actions: The scheduled actions for the scalable target. Duplicates aren't allowed.
        :param service_namespace: The namespace of the AWS service that provides the resource, or a ``custom-resource`` .
        :param suspended_state: An embedded object that contains attributes and attribute values that are used to suspend and resume automatic scaling. Setting the value of an attribute to ``true`` suspends the specified scaling activities. Setting it to ``false`` (default) resumes the specified scaling activities. *Suspension Outcomes* - For ``DynamicScalingInSuspended`` , while a suspension is in effect, all scale-in activities that are triggered by a scaling policy are suspended. - For ``DynamicScalingOutSuspended`` , while a suspension is in effect, all scale-out activities that are triggered by a scaling policy are suspended. - For ``ScheduledScalingSuspended`` , while a suspension is in effect, all scaling activities that involve scheduled actions are suspended.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
            
            cfn_scalable_target_mixin_props = applicationautoscaling_mixins.CfnScalableTargetMixinProps(
                max_capacity=123,
                min_capacity=123,
                resource_id="resourceId",
                role_arn="roleArn",
                scalable_dimension="scalableDimension",
                scheduled_actions=[applicationautoscaling_mixins.CfnScalableTargetPropsMixin.ScheduledActionProperty(
                    end_time=Date(),
                    scalable_target_action=applicationautoscaling_mixins.CfnScalableTargetPropsMixin.ScalableTargetActionProperty(
                        max_capacity=123,
                        min_capacity=123
                    ),
                    schedule="schedule",
                    scheduled_action_name="scheduledActionName",
                    start_time=Date(),
                    timezone="timezone"
                )],
                service_namespace="serviceNamespace",
                suspended_state=applicationautoscaling_mixins.CfnScalableTargetPropsMixin.SuspendedStateProperty(
                    dynamic_scaling_in_suspended=False,
                    dynamic_scaling_out_suspended=False,
                    scheduled_scaling_suspended=False
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d746e165b1787f1a21596bb9cfffd2fc4be923c05fc7ef2091b9f08d12792fd3)
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument scalable_dimension", value=scalable_dimension, expected_type=type_hints["scalable_dimension"])
            check_type(argname="argument scheduled_actions", value=scheduled_actions, expected_type=type_hints["scheduled_actions"])
            check_type(argname="argument service_namespace", value=service_namespace, expected_type=type_hints["service_namespace"])
            check_type(argname="argument suspended_state", value=suspended_state, expected_type=type_hints["suspended_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if min_capacity is not None:
            self._values["min_capacity"] = min_capacity
        if resource_id is not None:
            self._values["resource_id"] = resource_id
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if scalable_dimension is not None:
            self._values["scalable_dimension"] = scalable_dimension
        if scheduled_actions is not None:
            self._values["scheduled_actions"] = scheduled_actions
        if service_namespace is not None:
            self._values["service_namespace"] = service_namespace
        if suspended_state is not None:
            self._values["suspended_state"] = suspended_state

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''The maximum value that you plan to scale out to.

        When a scaling policy is in effect, Application Auto Scaling can scale out (expand) as needed to the maximum capacity limit in response to changing demand.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-maxcapacity
        '''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        '''The minimum value that you plan to scale in to.

        When a scaling policy is in effect, Application Auto Scaling can scale in (contract) as needed to the minimum capacity limit in response to changing demand.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-mincapacity
        '''
        result = self._values.get("min_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the resource associated with the scalable target.

        This string consists of the resource type and unique identifier.

        - ECS service - The resource type is ``service`` and the unique identifier is the cluster name and service name. Example: ``service/my-cluster/my-service`` .
        - Spot Fleet - The resource type is ``spot-fleet-request`` and the unique identifier is the Spot Fleet request ID. Example: ``spot-fleet-request/sfr-73fbd2ce-aa30-494c-8788-1cee4EXAMPLE`` .
        - EMR cluster - The resource type is ``instancegroup`` and the unique identifier is the cluster ID and instance group ID. Example: ``instancegroup/j-2EEZNYKUA1NTV/ig-1791Y4E1L8YI0`` .
        - AppStream 2.0 fleet - The resource type is ``fleet`` and the unique identifier is the fleet name. Example: ``fleet/sample-fleet`` .
        - DynamoDB table - The resource type is ``table`` and the unique identifier is the table name. Example: ``table/my-table`` .
        - DynamoDB global secondary index - The resource type is ``index`` and the unique identifier is the index name. Example: ``table/my-table/index/my-table-index`` .
        - Aurora DB cluster - The resource type is ``cluster`` and the unique identifier is the cluster name. Example: ``cluster:my-db-cluster`` .
        - SageMaker endpoint variant - The resource type is ``variant`` and the unique identifier is the resource ID. Example: ``endpoint/my-end-point/variant/KMeansClustering`` .
        - Custom resources are not supported with a resource type. This parameter must specify the ``OutputValue`` from the CloudFormation template stack used to access the resources. The unique identifier is defined by the service provider. More information is available in our `GitHub repository <https://docs.aws.amazon.com/https://github.com/aws/aws-auto-scaling-custom-resource>`_ .
        - Amazon Comprehend document classification endpoint - The resource type and unique identifier are specified using the endpoint ARN. Example: ``arn:aws:comprehend:us-west-2:123456789012:document-classifier-endpoint/EXAMPLE`` .
        - Amazon Comprehend entity recognizer endpoint - The resource type and unique identifier are specified using the endpoint ARN. Example: ``arn:aws:comprehend:us-west-2:123456789012:entity-recognizer-endpoint/EXAMPLE`` .
        - Lambda provisioned concurrency - The resource type is ``function`` and the unique identifier is the function name with a function version or alias name suffix that is not ``$LATEST`` . Example: ``function:my-function:prod`` or ``function:my-function:1`` .
        - Amazon Keyspaces table - The resource type is ``table`` and the unique identifier is the table name. Example: ``keyspace/mykeyspace/table/mytable`` .
        - Amazon MSK cluster - The resource type and unique identifier are specified using the cluster ARN. Example: ``arn:aws:kafka:us-east-1:123456789012:cluster/demo-cluster-1/6357e0b2-0e6a-4b86-a0b4-70df934c2e31-5`` .
        - Amazon ElastiCache replication group - The resource type is ``replication-group`` and the unique identifier is the replication group name. Example: ``replication-group/mycluster`` .
        - Amazon ElastiCache cache cluster - The resource type is ``cache-cluster`` and the unique identifier is the cache cluster name. Example: ``cache-cluster/mycluster`` .
        - Neptune cluster - The resource type is ``cluster`` and the unique identifier is the cluster name. Example: ``cluster:mycluster`` .
        - SageMaker serverless endpoint - The resource type is ``variant`` and the unique identifier is the resource ID. Example: ``endpoint/my-end-point/variant/KMeansClustering`` .
        - SageMaker inference component - The resource type is ``inference-component`` and the unique identifier is the resource ID. Example: ``inference-component/my-inference-component`` .
        - Pool of WorkSpaces - The resource type is ``workspacespool`` and the unique identifier is the pool ID. Example: ``workspacespool/wspool-123456`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-resourceid
        '''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Specify the Amazon Resource Name (ARN) of an Identity and Access Management (IAM) role that allows Application Auto Scaling to modify the scalable target on your behalf.

        This can be either an IAM service role that Application Auto Scaling can assume to make calls to other AWS resources on your behalf, or a service-linked role for the specified service. For more information, see `How Application Auto Scaling works with IAM <https://docs.aws.amazon.com/autoscaling/application/userguide/security_iam_service-with-iam.html>`_ in the *Application Auto Scaling User Guide* .

        To automatically create a service-linked role (recommended), specify the full ARN of the service-linked role in your stack template. To find the exact ARN of the service-linked role for your AWS or custom resource, see the `Service-linked roles <https://docs.aws.amazon.com/autoscaling/application/userguide/application-auto-scaling-service-linked-roles.html>`_ topic in the *Application Auto Scaling User Guide* . Look for the ARN in the table at the bottom of the page.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scalable_dimension(self) -> typing.Optional[builtins.str]:
        '''The scalable dimension associated with the scalable target.

        This string consists of the service namespace, resource type, and scaling property.

        - ``ecs:service:DesiredCount`` - The task count of an ECS service.
        - ``elasticmapreduce:instancegroup:InstanceCount`` - The instance count of an EMR Instance Group.
        - ``ec2:spot-fleet-request:TargetCapacity`` - The target capacity of a Spot Fleet.
        - ``appstream:fleet:DesiredCapacity`` - The capacity of an AppStream 2.0 fleet.
        - ``dynamodb:table:ReadCapacityUnits`` - The provisioned read capacity for a DynamoDB table.
        - ``dynamodb:table:WriteCapacityUnits`` - The provisioned write capacity for a DynamoDB table.
        - ``dynamodb:index:ReadCapacityUnits`` - The provisioned read capacity for a DynamoDB global secondary index.
        - ``dynamodb:index:WriteCapacityUnits`` - The provisioned write capacity for a DynamoDB global secondary index.
        - ``rds:cluster:ReadReplicaCount`` - The count of Aurora Replicas in an Aurora DB cluster. Available for Aurora MySQL-compatible edition and Aurora PostgreSQL-compatible edition.
        - ``sagemaker:variant:DesiredInstanceCount`` - The number of EC2 instances for a SageMaker model endpoint variant.
        - ``custom-resource:ResourceType:Property`` - The scalable dimension for a custom resource provided by your own application or service.
        - ``comprehend:document-classifier-endpoint:DesiredInferenceUnits`` - The number of inference units for an Amazon Comprehend document classification endpoint.
        - ``comprehend:entity-recognizer-endpoint:DesiredInferenceUnits`` - The number of inference units for an Amazon Comprehend entity recognizer endpoint.
        - ``lambda:function:ProvisionedConcurrency`` - The provisioned concurrency for a Lambda function.
        - ``cassandra:table:ReadCapacityUnits`` - The provisioned read capacity for an Amazon Keyspaces table.
        - ``cassandra:table:WriteCapacityUnits`` - The provisioned write capacity for an Amazon Keyspaces table.
        - ``kafka:broker-storage:VolumeSize`` - The provisioned volume size (in GiB) for brokers in an Amazon MSK cluster.
        - ``elasticache:cache-cluster:Nodes`` - The number of nodes for an Amazon ElastiCache cache cluster.
        - ``elasticache:replication-group:NodeGroups`` - The number of node groups for an Amazon ElastiCache replication group.
        - ``elasticache:replication-group:Replicas`` - The number of replicas per node group for an Amazon ElastiCache replication group.
        - ``neptune:cluster:ReadReplicaCount`` - The count of read replicas in an Amazon Neptune DB cluster.
        - ``sagemaker:variant:DesiredProvisionedConcurrency`` - The provisioned concurrency for a SageMaker serverless endpoint.
        - ``sagemaker:inference-component:DesiredCopyCount`` - The number of copies across an endpoint for a SageMaker inference component.
        - ``workspaces:workspacespool:DesiredUserSessions`` - The number of user sessions for the WorkSpaces in the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-scalabledimension
        '''
        result = self._values.get("scalable_dimension")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduled_actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalableTargetPropsMixin.ScheduledActionProperty"]]]]:
        '''The scheduled actions for the scalable target.

        Duplicates aren't allowed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-scheduledactions
        '''
        result = self._values.get("scheduled_actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalableTargetPropsMixin.ScheduledActionProperty"]]]], result)

    @builtins.property
    def service_namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the AWS service that provides the resource, or a ``custom-resource`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-servicenamespace
        '''
        result = self._values.get("service_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspended_state(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalableTargetPropsMixin.SuspendedStateProperty"]]:
        '''An embedded object that contains attributes and attribute values that are used to suspend and resume automatic scaling.

        Setting the value of an attribute to ``true`` suspends the specified scaling activities. Setting it to ``false`` (default) resumes the specified scaling activities.

        *Suspension Outcomes*

        - For ``DynamicScalingInSuspended`` , while a suspension is in effect, all scale-in activities that are triggered by a scaling policy are suspended.
        - For ``DynamicScalingOutSuspended`` , while a suspension is in effect, all scale-out activities that are triggered by a scaling policy are suspended.
        - For ``ScheduledScalingSuspended`` , while a suspension is in effect, all scaling activities that involve scheduled actions are suspended.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-suspendedstate
        '''
        result = self._values.get("suspended_state")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalableTargetPropsMixin.SuspendedStateProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScalableTargetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnScalableTargetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalableTargetPropsMixin",
):
    '''The ``AWS::ApplicationAutoScaling::ScalableTarget`` resource specifies a resource that Application Auto Scaling can scale, such as an AWS::DynamoDB::Table or AWS::ECS::Service resource.

    For more information, see `Getting started <https://docs.aws.amazon.com/autoscaling/application/userguide/getting-started.html>`_ in the *Application Auto Scaling User Guide* .
    .. epigraph::

       If the resource that you want Application Auto Scaling to scale is not yet created in your account, add a dependency on the resource when registering it as a scalable target using the `DependsOn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ attribute.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html
    :cloudformationResource: AWS::ApplicationAutoScaling::ScalableTarget
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
        
        cfn_scalable_target_props_mixin = applicationautoscaling_mixins.CfnScalableTargetPropsMixin(applicationautoscaling_mixins.CfnScalableTargetMixinProps(
            max_capacity=123,
            min_capacity=123,
            resource_id="resourceId",
            role_arn="roleArn",
            scalable_dimension="scalableDimension",
            scheduled_actions=[applicationautoscaling_mixins.CfnScalableTargetPropsMixin.ScheduledActionProperty(
                end_time=Date(),
                scalable_target_action=applicationautoscaling_mixins.CfnScalableTargetPropsMixin.ScalableTargetActionProperty(
                    max_capacity=123,
                    min_capacity=123
                ),
                schedule="schedule",
                scheduled_action_name="scheduledActionName",
                start_time=Date(),
                timezone="timezone"
            )],
            service_namespace="serviceNamespace",
            suspended_state=applicationautoscaling_mixins.CfnScalableTargetPropsMixin.SuspendedStateProperty(
                dynamic_scaling_in_suspended=False,
                dynamic_scaling_out_suspended=False,
                scheduled_scaling_suspended=False
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnScalableTargetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApplicationAutoScaling::ScalableTarget``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41f085b5f1c60e69e9c1d91bf3507ce41fe0062eded98bf81e88918be39f8f73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71090bdc436b331d4568c9b8cade7e5dd4daef3a393b273a8990c7f9ff667225)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda8098b784e0402e60ddb0e2a21cbacd69a18f21ef7980a1929c53c43898aa4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnScalableTargetMixinProps:
        return typing.cast(CfnScalableTargetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalableTargetPropsMixin.ScalableTargetActionProperty",
        jsii_struct_bases=[],
        name_mapping={"max_capacity": "maxCapacity", "min_capacity": "minCapacity"},
    )
    class ScalableTargetActionProperty:
        def __init__(
            self,
            *,
            max_capacity: typing.Optional[jsii.Number] = None,
            min_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``ScalableTargetAction`` specifies the minimum and maximum capacity for the ``ScalableTargetAction`` property of the `AWS::ApplicationAutoScaling::ScalableTarget ScheduledAction <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html>`_ property type.

            :param max_capacity: The maximum capacity.
            :param min_capacity: The minimum capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scalabletargetaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                scalable_target_action_property = applicationautoscaling_mixins.CfnScalableTargetPropsMixin.ScalableTargetActionProperty(
                    max_capacity=123,
                    min_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9e7cac209d2bec1b6d64365f4efcfdca02f0eaf5277d690770d24c9da4d5260)
                check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
                check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_capacity is not None:
                self._values["max_capacity"] = max_capacity
            if min_capacity is not None:
                self._values["min_capacity"] = min_capacity

        @builtins.property
        def max_capacity(self) -> typing.Optional[jsii.Number]:
            '''The maximum capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scalabletargetaction.html#cfn-applicationautoscaling-scalabletarget-scalabletargetaction-maxcapacity
            '''
            result = self._values.get("max_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_capacity(self) -> typing.Optional[jsii.Number]:
            '''The minimum capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scalabletargetaction.html#cfn-applicationautoscaling-scalabletarget-scalabletargetaction-mincapacity
            '''
            result = self._values.get("min_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalableTargetActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalableTargetPropsMixin.ScheduledActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "end_time": "endTime",
            "scalable_target_action": "scalableTargetAction",
            "schedule": "schedule",
            "scheduled_action_name": "scheduledActionName",
            "start_time": "startTime",
            "timezone": "timezone",
        },
    )
    class ScheduledActionProperty:
        def __init__(
            self,
            *,
            end_time: typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]] = None,
            scalable_target_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalableTargetPropsMixin.ScalableTargetActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            schedule: typing.Optional[builtins.str] = None,
            scheduled_action_name: typing.Optional[builtins.str] = None,
            start_time: typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]] = None,
            timezone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``ScheduledAction`` is a property of the `AWS::ApplicationAutoScaling::ScalableTarget <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html>`_ resource that specifies a scheduled action for a scalable target.

            For more information, see `Scheduled scaling <https://docs.aws.amazon.com/autoscaling/application/userguide/application-auto-scaling-scheduled-scaling.html>`_ in the *Application Auto Scaling User Guide* .

            :param end_time: The date and time that the action is scheduled to end, in UTC.
            :param scalable_target_action: The new minimum and maximum capacity. You can set both values or just one. At the scheduled time, if the current capacity is below the minimum capacity, Application Auto Scaling scales out to the minimum capacity. If the current capacity is above the maximum capacity, Application Auto Scaling scales in to the maximum capacity.
            :param schedule: The schedule for this action. The following formats are supported:. - At expressions - " ``at( *yyyy* - *mm* - *dd* T *hh* : *mm* : *ss* )`` " - Rate expressions - " ``rate( *value* *unit* )`` " - Cron expressions - " ``cron( *fields* )`` " At expressions are useful for one-time schedules. Cron expressions are useful for scheduled actions that run periodically at a specified date and time, and rate expressions are useful for scheduled actions that run at a regular interval. At and cron expressions use Universal Coordinated Time (UTC) by default. The cron format consists of six fields separated by white spaces: [Minutes] [Hours] [Day_of_Month] [Month] [Day_of_Week] [Year]. For rate expressions, *value* is a positive integer and *unit* is ``minute`` | ``minutes`` | ``hour`` | ``hours`` | ``day`` | ``days`` .
            :param scheduled_action_name: The name of the scheduled action. This name must be unique among all other scheduled actions on the specified scalable target.
            :param start_time: The date and time that the action is scheduled to begin, in UTC.
            :param timezone: The time zone used when referring to the date and time of a scheduled action, when the scheduled action uses an at or cron expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                scheduled_action_property = applicationautoscaling_mixins.CfnScalableTargetPropsMixin.ScheduledActionProperty(
                    end_time=Date(),
                    scalable_target_action=applicationautoscaling_mixins.CfnScalableTargetPropsMixin.ScalableTargetActionProperty(
                        max_capacity=123,
                        min_capacity=123
                    ),
                    schedule="schedule",
                    scheduled_action_name="scheduledActionName",
                    start_time=Date(),
                    timezone="timezone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e92abc186e22f43180acb28d793193ba0a7b128da992695e2899e60b6fb1acd)
                check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                check_type(argname="argument scalable_target_action", value=scalable_target_action, expected_type=type_hints["scalable_target_action"])
                check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
                check_type(argname="argument scheduled_action_name", value=scheduled_action_name, expected_type=type_hints["scheduled_action_name"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
                check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end_time is not None:
                self._values["end_time"] = end_time
            if scalable_target_action is not None:
                self._values["scalable_target_action"] = scalable_target_action
            if schedule is not None:
                self._values["schedule"] = schedule
            if scheduled_action_name is not None:
                self._values["scheduled_action_name"] = scheduled_action_name
            if start_time is not None:
                self._values["start_time"] = start_time
            if timezone is not None:
                self._values["timezone"] = timezone

        @builtins.property
        def end_time(
            self,
        ) -> typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]]:
            '''The date and time that the action is scheduled to end, in UTC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-endtime
            '''
            result = self._values.get("end_time")
            return typing.cast(typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def scalable_target_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalableTargetPropsMixin.ScalableTargetActionProperty"]]:
            '''The new minimum and maximum capacity.

            You can set both values or just one. At the scheduled time, if the current capacity is below the minimum capacity, Application Auto Scaling scales out to the minimum capacity. If the current capacity is above the maximum capacity, Application Auto Scaling scales in to the maximum capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-scalabletargetaction
            '''
            result = self._values.get("scalable_target_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalableTargetPropsMixin.ScalableTargetActionProperty"]], result)

        @builtins.property
        def schedule(self) -> typing.Optional[builtins.str]:
            '''The schedule for this action. The following formats are supported:.

            - At expressions - " ``at( *yyyy* - *mm* - *dd* T *hh* : *mm* : *ss* )`` "
            - Rate expressions - " ``rate( *value* *unit* )`` "
            - Cron expressions - " ``cron( *fields* )`` "

            At expressions are useful for one-time schedules. Cron expressions are useful for scheduled actions that run periodically at a specified date and time, and rate expressions are useful for scheduled actions that run at a regular interval.

            At and cron expressions use Universal Coordinated Time (UTC) by default.

            The cron format consists of six fields separated by white spaces: [Minutes] [Hours] [Day_of_Month] [Month] [Day_of_Week] [Year].

            For rate expressions, *value* is a positive integer and *unit* is ``minute`` | ``minutes`` | ``hour`` | ``hours`` | ``day`` | ``days`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-schedule
            '''
            result = self._values.get("schedule")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scheduled_action_name(self) -> typing.Optional[builtins.str]:
            '''The name of the scheduled action.

            This name must be unique among all other scheduled actions on the specified scalable target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-scheduledactionname
            '''
            result = self._values.get("scheduled_action_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_time(
            self,
        ) -> typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]]:
            '''The date and time that the action is scheduled to begin, in UTC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def timezone(self) -> typing.Optional[builtins.str]:
            '''The time zone used when referring to the date and time of a scheduled action, when the scheduled action uses an at or cron expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-timezone
            '''
            result = self._values.get("timezone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduledActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalableTargetPropsMixin.SuspendedStateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dynamic_scaling_in_suspended": "dynamicScalingInSuspended",
            "dynamic_scaling_out_suspended": "dynamicScalingOutSuspended",
            "scheduled_scaling_suspended": "scheduledScalingSuspended",
        },
    )
    class SuspendedStateProperty:
        def __init__(
            self,
            *,
            dynamic_scaling_in_suspended: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            dynamic_scaling_out_suspended: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            scheduled_scaling_suspended: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''``SuspendedState`` is a property of the `AWS::ApplicationAutoScaling::ScalableTarget <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html>`_ resource that specifies whether the scaling activities for a scalable target are in a suspended state.

            For more information, see `Suspending and resuming scaling <https://docs.aws.amazon.com/autoscaling/application/userguide/application-auto-scaling-suspend-resume-scaling.html>`_ in the *Application Auto Scaling User Guide* .

            :param dynamic_scaling_in_suspended: Whether scale in by a target tracking scaling policy or a step scaling policy is suspended. Set the value to ``true`` if you don't want Application Auto Scaling to remove capacity when a scaling policy is triggered. The default is ``false`` .
            :param dynamic_scaling_out_suspended: Whether scale out by a target tracking scaling policy or a step scaling policy is suspended. Set the value to ``true`` if you don't want Application Auto Scaling to add capacity when a scaling policy is triggered. The default is ``false`` .
            :param scheduled_scaling_suspended: Whether scheduled scaling is suspended. Set the value to ``true`` if you don't want Application Auto Scaling to add or remove capacity by initiating scheduled actions. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-suspendedstate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                suspended_state_property = applicationautoscaling_mixins.CfnScalableTargetPropsMixin.SuspendedStateProperty(
                    dynamic_scaling_in_suspended=False,
                    dynamic_scaling_out_suspended=False,
                    scheduled_scaling_suspended=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fdbde4a25286dd05c8c77ebd67e7334a6d3609c97fdfb5a4e49d1fd7bda2aed1)
                check_type(argname="argument dynamic_scaling_in_suspended", value=dynamic_scaling_in_suspended, expected_type=type_hints["dynamic_scaling_in_suspended"])
                check_type(argname="argument dynamic_scaling_out_suspended", value=dynamic_scaling_out_suspended, expected_type=type_hints["dynamic_scaling_out_suspended"])
                check_type(argname="argument scheduled_scaling_suspended", value=scheduled_scaling_suspended, expected_type=type_hints["scheduled_scaling_suspended"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dynamic_scaling_in_suspended is not None:
                self._values["dynamic_scaling_in_suspended"] = dynamic_scaling_in_suspended
            if dynamic_scaling_out_suspended is not None:
                self._values["dynamic_scaling_out_suspended"] = dynamic_scaling_out_suspended
            if scheduled_scaling_suspended is not None:
                self._values["scheduled_scaling_suspended"] = scheduled_scaling_suspended

        @builtins.property
        def dynamic_scaling_in_suspended(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether scale in by a target tracking scaling policy or a step scaling policy is suspended.

            Set the value to ``true`` if you don't want Application Auto Scaling to remove capacity when a scaling policy is triggered. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-suspendedstate.html#cfn-applicationautoscaling-scalabletarget-suspendedstate-dynamicscalinginsuspended
            '''
            result = self._values.get("dynamic_scaling_in_suspended")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def dynamic_scaling_out_suspended(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether scale out by a target tracking scaling policy or a step scaling policy is suspended.

            Set the value to ``true`` if you don't want Application Auto Scaling to add capacity when a scaling policy is triggered. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-suspendedstate.html#cfn-applicationautoscaling-scalabletarget-suspendedstate-dynamicscalingoutsuspended
            '''
            result = self._values.get("dynamic_scaling_out_suspended")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def scheduled_scaling_suspended(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether scheduled scaling is suspended.

            Set the value to ``true`` if you don't want Application Auto Scaling to add or remove capacity by initiating scheduled actions. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-suspendedstate.html#cfn-applicationautoscaling-scalabletarget-suspendedstate-scheduledscalingsuspended
            '''
            result = self._values.get("scheduled_scaling_suspended")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SuspendedStateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy_name": "policyName",
        "policy_type": "policyType",
        "predictive_scaling_policy_configuration": "predictiveScalingPolicyConfiguration",
        "resource_id": "resourceId",
        "scalable_dimension": "scalableDimension",
        "scaling_target_id": "scalingTargetId",
        "service_namespace": "serviceNamespace",
        "step_scaling_policy_configuration": "stepScalingPolicyConfiguration",
        "target_tracking_scaling_policy_configuration": "targetTrackingScalingPolicyConfiguration",
    },
)
class CfnScalingPolicyMixinProps:
    def __init__(
        self,
        *,
        policy_name: typing.Optional[builtins.str] = None,
        policy_type: typing.Optional[builtins.str] = None,
        predictive_scaling_policy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingPolicyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_id: typing.Optional[builtins.str] = None,
        scalable_dimension: typing.Optional[builtins.str] = None,
        scaling_target_id: typing.Optional[builtins.str] = None,
        service_namespace: typing.Optional[builtins.str] = None,
        step_scaling_policy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.StepScalingPolicyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        target_tracking_scaling_policy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.TargetTrackingScalingPolicyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnScalingPolicyPropsMixin.

        :param policy_name: The name of the scaling policy. Updates to the name of a target tracking scaling policy are not supported, unless you also update the metric used for scaling. To change only a target tracking scaling policy's name, first delete the policy by removing the existing ``AWS::ApplicationAutoScaling::ScalingPolicy`` resource from the template and updating the stack. Then, recreate the resource with the same settings and a different name.
        :param policy_type: The scaling policy type. The following policy types are supported: ``TargetTrackingScaling`` —Not supported for Amazon EMR ``StepScaling`` —Not supported for DynamoDB, Amazon Comprehend, Lambda, Amazon Keyspaces, Amazon MSK, Amazon ElastiCache, or Neptune. ``PredictiveScaling`` —Only supported for Amazon ECS
        :param predictive_scaling_policy_configuration: The predictive scaling policy configuration.
        :param resource_id: The identifier of the resource associated with the scaling policy. This string consists of the resource type and unique identifier. - ECS service - The resource type is ``service`` and the unique identifier is the cluster name and service name. Example: ``service/my-cluster/my-service`` . - Spot Fleet - The resource type is ``spot-fleet-request`` and the unique identifier is the Spot Fleet request ID. Example: ``spot-fleet-request/sfr-73fbd2ce-aa30-494c-8788-1cee4EXAMPLE`` . - EMR cluster - The resource type is ``instancegroup`` and the unique identifier is the cluster ID and instance group ID. Example: ``instancegroup/j-2EEZNYKUA1NTV/ig-1791Y4E1L8YI0`` . - AppStream 2.0 fleet - The resource type is ``fleet`` and the unique identifier is the fleet name. Example: ``fleet/sample-fleet`` . - DynamoDB table - The resource type is ``table`` and the unique identifier is the table name. Example: ``table/my-table`` . - DynamoDB global secondary index - The resource type is ``index`` and the unique identifier is the index name. Example: ``table/my-table/index/my-table-index`` . - Aurora DB cluster - The resource type is ``cluster`` and the unique identifier is the cluster name. Example: ``cluster:my-db-cluster`` . - SageMaker endpoint variant - The resource type is ``variant`` and the unique identifier is the resource ID. Example: ``endpoint/my-end-point/variant/KMeansClustering`` . - Custom resources are not supported with a resource type. This parameter must specify the ``OutputValue`` from the CloudFormation template stack used to access the resources. The unique identifier is defined by the service provider. More information is available in our `GitHub repository <https://docs.aws.amazon.com/https://github.com/aws/aws-auto-scaling-custom-resource>`_ . - Amazon Comprehend document classification endpoint - The resource type and unique identifier are specified using the endpoint ARN. Example: ``arn:aws:comprehend:us-west-2:123456789012:document-classifier-endpoint/EXAMPLE`` . - Amazon Comprehend entity recognizer endpoint - The resource type and unique identifier are specified using the endpoint ARN. Example: ``arn:aws:comprehend:us-west-2:123456789012:entity-recognizer-endpoint/EXAMPLE`` . - Lambda provisioned concurrency - The resource type is ``function`` and the unique identifier is the function name with a function version or alias name suffix that is not ``$LATEST`` . Example: ``function:my-function:prod`` or ``function:my-function:1`` . - Amazon Keyspaces table - The resource type is ``table`` and the unique identifier is the table name. Example: ``keyspace/mykeyspace/table/mytable`` . - Amazon MSK cluster - The resource type and unique identifier are specified using the cluster ARN. Example: ``arn:aws:kafka:us-east-1:123456789012:cluster/demo-cluster-1/6357e0b2-0e6a-4b86-a0b4-70df934c2e31-5`` . - Amazon ElastiCache replication group - The resource type is ``replication-group`` and the unique identifier is the replication group name. Example: ``replication-group/mycluster`` . - Amazon ElastiCache cache cluster - The resource type is ``cache-cluster`` and the unique identifier is the cache cluster name. Example: ``cache-cluster/mycluster`` . - Neptune cluster - The resource type is ``cluster`` and the unique identifier is the cluster name. Example: ``cluster:mycluster`` . - SageMaker serverless endpoint - The resource type is ``variant`` and the unique identifier is the resource ID. Example: ``endpoint/my-end-point/variant/KMeansClustering`` . - SageMaker inference component - The resource type is ``inference-component`` and the unique identifier is the resource ID. Example: ``inference-component/my-inference-component`` . - Pool of WorkSpaces - The resource type is ``workspacespool`` and the unique identifier is the pool ID. Example: ``workspacespool/wspool-123456`` .
        :param scalable_dimension: The scalable dimension. This string consists of the service namespace, resource type, and scaling property. - ``ecs:service:DesiredCount`` - The task count of an ECS service. - ``elasticmapreduce:instancegroup:InstanceCount`` - The instance count of an EMR Instance Group. - ``ec2:spot-fleet-request:TargetCapacity`` - The target capacity of a Spot Fleet. - ``appstream:fleet:DesiredCapacity`` - The capacity of an AppStream 2.0 fleet. - ``dynamodb:table:ReadCapacityUnits`` - The provisioned read capacity for a DynamoDB table. - ``dynamodb:table:WriteCapacityUnits`` - The provisioned write capacity for a DynamoDB table. - ``dynamodb:index:ReadCapacityUnits`` - The provisioned read capacity for a DynamoDB global secondary index. - ``dynamodb:index:WriteCapacityUnits`` - The provisioned write capacity for a DynamoDB global secondary index. - ``rds:cluster:ReadReplicaCount`` - The count of Aurora Replicas in an Aurora DB cluster. Available for Aurora MySQL-compatible edition and Aurora PostgreSQL-compatible edition. - ``sagemaker:variant:DesiredInstanceCount`` - The number of EC2 instances for a SageMaker model endpoint variant. - ``custom-resource:ResourceType:Property`` - The scalable dimension for a custom resource provided by your own application or service. - ``comprehend:document-classifier-endpoint:DesiredInferenceUnits`` - The number of inference units for an Amazon Comprehend document classification endpoint. - ``comprehend:entity-recognizer-endpoint:DesiredInferenceUnits`` - The number of inference units for an Amazon Comprehend entity recognizer endpoint. - ``lambda:function:ProvisionedConcurrency`` - The provisioned concurrency for a Lambda function. - ``cassandra:table:ReadCapacityUnits`` - The provisioned read capacity for an Amazon Keyspaces table. - ``cassandra:table:WriteCapacityUnits`` - The provisioned write capacity for an Amazon Keyspaces table. - ``kafka:broker-storage:VolumeSize`` - The provisioned volume size (in GiB) for brokers in an Amazon MSK cluster. - ``elasticache:cache-cluster:Nodes`` - The number of nodes for an Amazon ElastiCache cache cluster. - ``elasticache:replication-group:NodeGroups`` - The number of node groups for an Amazon ElastiCache replication group. - ``elasticache:replication-group:Replicas`` - The number of replicas per node group for an Amazon ElastiCache replication group. - ``neptune:cluster:ReadReplicaCount`` - The count of read replicas in an Amazon Neptune DB cluster. - ``sagemaker:variant:DesiredProvisionedConcurrency`` - The provisioned concurrency for a SageMaker serverless endpoint. - ``sagemaker:inference-component:DesiredCopyCount`` - The number of copies across an endpoint for a SageMaker inference component. - ``workspaces:workspacespool:DesiredUserSessions`` - The number of user sessions for the WorkSpaces in the pool.
        :param scaling_target_id: The CloudFormation-generated ID of an Application Auto Scaling scalable target. For more information about the ID, see the Return Value section of the ``AWS::ApplicationAutoScaling::ScalableTarget`` resource. .. epigraph:: You must specify either the ``ScalingTargetId`` property, or the ``ResourceId`` , ``ScalableDimension`` , and ``ServiceNamespace`` properties, but not both.
        :param service_namespace: The namespace of the AWS service that provides the resource, or a ``custom-resource`` .
        :param step_scaling_policy_configuration: A step scaling policy.
        :param target_tracking_scaling_policy_configuration: A target tracking scaling policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
            
            cfn_scaling_policy_mixin_props = applicationautoscaling_mixins.CfnScalingPolicyMixinProps(
                policy_name="policyName",
                policy_type="policyType",
                predictive_scaling_policy_configuration=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPolicyConfigurationProperty(
                    max_capacity_breach_behavior="maxCapacityBreachBehavior",
                    max_capacity_buffer=123,
                    metric_specifications=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty(
                        customized_capacity_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty(
                            metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                                expression="expression",
                                id="id",
                                label="label",
                                metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                                    metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                        dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )]
                        ),
                        customized_load_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty(
                            metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                                expression="expression",
                                id="id",
                                label="label",
                                metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                                    metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                        dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )]
                        ),
                        customized_scaling_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty(
                            metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                                expression="expression",
                                id="id",
                                label="label",
                                metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                                    metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                        dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )]
                        ),
                        predefined_load_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty(
                            predefined_metric_type="predefinedMetricType",
                            resource_label="resourceLabel"
                        ),
                        predefined_metric_pair_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty(
                            predefined_metric_type="predefinedMetricType",
                            resource_label="resourceLabel"
                        ),
                        predefined_scaling_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty(
                            predefined_metric_type="predefinedMetricType",
                            resource_label="resourceLabel"
                        ),
                        target_value=123
                    )],
                    mode="mode",
                    scheduling_buffer_time=123
                ),
                resource_id="resourceId",
                scalable_dimension="scalableDimension",
                scaling_target_id="scalingTargetId",
                service_namespace="serviceNamespace",
                step_scaling_policy_configuration=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.StepScalingPolicyConfigurationProperty(
                    adjustment_type="adjustmentType",
                    cooldown=123,
                    metric_aggregation_type="metricAggregationType",
                    min_adjustment_magnitude=123,
                    step_adjustments=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.StepAdjustmentProperty(
                        metric_interval_lower_bound=123,
                        metric_interval_upper_bound=123,
                        scaling_adjustment=123
                    )]
                ),
                target_tracking_scaling_policy_configuration=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                    customized_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty(
                        dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                            name="name",
                            value="value"
                        )],
                        metric_name="metricName",
                        metrics=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty(
                                metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricProperty(
                                    dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )],
                        namespace="namespace",
                        statistic="statistic",
                        unit="unit"
                    ),
                    disable_scale_in=False,
                    predefined_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    scale_in_cooldown=123,
                    scale_out_cooldown=123,
                    target_value=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c34e67301ee8d0c479a05f580c20b4f4e18061059c69e51ee6f199c21cdc629)
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
            check_type(argname="argument predictive_scaling_policy_configuration", value=predictive_scaling_policy_configuration, expected_type=type_hints["predictive_scaling_policy_configuration"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument scalable_dimension", value=scalable_dimension, expected_type=type_hints["scalable_dimension"])
            check_type(argname="argument scaling_target_id", value=scaling_target_id, expected_type=type_hints["scaling_target_id"])
            check_type(argname="argument service_namespace", value=service_namespace, expected_type=type_hints["service_namespace"])
            check_type(argname="argument step_scaling_policy_configuration", value=step_scaling_policy_configuration, expected_type=type_hints["step_scaling_policy_configuration"])
            check_type(argname="argument target_tracking_scaling_policy_configuration", value=target_tracking_scaling_policy_configuration, expected_type=type_hints["target_tracking_scaling_policy_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if policy_type is not None:
            self._values["policy_type"] = policy_type
        if predictive_scaling_policy_configuration is not None:
            self._values["predictive_scaling_policy_configuration"] = predictive_scaling_policy_configuration
        if resource_id is not None:
            self._values["resource_id"] = resource_id
        if scalable_dimension is not None:
            self._values["scalable_dimension"] = scalable_dimension
        if scaling_target_id is not None:
            self._values["scaling_target_id"] = scaling_target_id
        if service_namespace is not None:
            self._values["service_namespace"] = service_namespace
        if step_scaling_policy_configuration is not None:
            self._values["step_scaling_policy_configuration"] = step_scaling_policy_configuration
        if target_tracking_scaling_policy_configuration is not None:
            self._values["target_tracking_scaling_policy_configuration"] = target_tracking_scaling_policy_configuration

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the scaling policy.

        Updates to the name of a target tracking scaling policy are not supported, unless you also update the metric used for scaling. To change only a target tracking scaling policy's name, first delete the policy by removing the existing ``AWS::ApplicationAutoScaling::ScalingPolicy`` resource from the template and updating the stack. Then, recreate the resource with the same settings and a different name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-policyname
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_type(self) -> typing.Optional[builtins.str]:
        '''The scaling policy type.

        The following policy types are supported:

        ``TargetTrackingScaling`` —Not supported for Amazon EMR

        ``StepScaling`` —Not supported for DynamoDB, Amazon Comprehend, Lambda, Amazon Keyspaces, Amazon MSK, Amazon ElastiCache, or Neptune.

        ``PredictiveScaling`` —Only supported for Amazon ECS

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-policytype
        '''
        result = self._values.get("policy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def predictive_scaling_policy_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingPolicyConfigurationProperty"]]:
        '''The predictive scaling policy configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingpolicyconfiguration
        '''
        result = self._values.get("predictive_scaling_policy_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingPolicyConfigurationProperty"]], result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the resource associated with the scaling policy.

        This string consists of the resource type and unique identifier.

        - ECS service - The resource type is ``service`` and the unique identifier is the cluster name and service name. Example: ``service/my-cluster/my-service`` .
        - Spot Fleet - The resource type is ``spot-fleet-request`` and the unique identifier is the Spot Fleet request ID. Example: ``spot-fleet-request/sfr-73fbd2ce-aa30-494c-8788-1cee4EXAMPLE`` .
        - EMR cluster - The resource type is ``instancegroup`` and the unique identifier is the cluster ID and instance group ID. Example: ``instancegroup/j-2EEZNYKUA1NTV/ig-1791Y4E1L8YI0`` .
        - AppStream 2.0 fleet - The resource type is ``fleet`` and the unique identifier is the fleet name. Example: ``fleet/sample-fleet`` .
        - DynamoDB table - The resource type is ``table`` and the unique identifier is the table name. Example: ``table/my-table`` .
        - DynamoDB global secondary index - The resource type is ``index`` and the unique identifier is the index name. Example: ``table/my-table/index/my-table-index`` .
        - Aurora DB cluster - The resource type is ``cluster`` and the unique identifier is the cluster name. Example: ``cluster:my-db-cluster`` .
        - SageMaker endpoint variant - The resource type is ``variant`` and the unique identifier is the resource ID. Example: ``endpoint/my-end-point/variant/KMeansClustering`` .
        - Custom resources are not supported with a resource type. This parameter must specify the ``OutputValue`` from the CloudFormation template stack used to access the resources. The unique identifier is defined by the service provider. More information is available in our `GitHub repository <https://docs.aws.amazon.com/https://github.com/aws/aws-auto-scaling-custom-resource>`_ .
        - Amazon Comprehend document classification endpoint - The resource type and unique identifier are specified using the endpoint ARN. Example: ``arn:aws:comprehend:us-west-2:123456789012:document-classifier-endpoint/EXAMPLE`` .
        - Amazon Comprehend entity recognizer endpoint - The resource type and unique identifier are specified using the endpoint ARN. Example: ``arn:aws:comprehend:us-west-2:123456789012:entity-recognizer-endpoint/EXAMPLE`` .
        - Lambda provisioned concurrency - The resource type is ``function`` and the unique identifier is the function name with a function version or alias name suffix that is not ``$LATEST`` . Example: ``function:my-function:prod`` or ``function:my-function:1`` .
        - Amazon Keyspaces table - The resource type is ``table`` and the unique identifier is the table name. Example: ``keyspace/mykeyspace/table/mytable`` .
        - Amazon MSK cluster - The resource type and unique identifier are specified using the cluster ARN. Example: ``arn:aws:kafka:us-east-1:123456789012:cluster/demo-cluster-1/6357e0b2-0e6a-4b86-a0b4-70df934c2e31-5`` .
        - Amazon ElastiCache replication group - The resource type is ``replication-group`` and the unique identifier is the replication group name. Example: ``replication-group/mycluster`` .
        - Amazon ElastiCache cache cluster - The resource type is ``cache-cluster`` and the unique identifier is the cache cluster name. Example: ``cache-cluster/mycluster`` .
        - Neptune cluster - The resource type is ``cluster`` and the unique identifier is the cluster name. Example: ``cluster:mycluster`` .
        - SageMaker serverless endpoint - The resource type is ``variant`` and the unique identifier is the resource ID. Example: ``endpoint/my-end-point/variant/KMeansClustering`` .
        - SageMaker inference component - The resource type is ``inference-component`` and the unique identifier is the resource ID. Example: ``inference-component/my-inference-component`` .
        - Pool of WorkSpaces - The resource type is ``workspacespool`` and the unique identifier is the pool ID. Example: ``workspacespool/wspool-123456`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-resourceid
        '''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scalable_dimension(self) -> typing.Optional[builtins.str]:
        '''The scalable dimension. This string consists of the service namespace, resource type, and scaling property.

        - ``ecs:service:DesiredCount`` - The task count of an ECS service.
        - ``elasticmapreduce:instancegroup:InstanceCount`` - The instance count of an EMR Instance Group.
        - ``ec2:spot-fleet-request:TargetCapacity`` - The target capacity of a Spot Fleet.
        - ``appstream:fleet:DesiredCapacity`` - The capacity of an AppStream 2.0 fleet.
        - ``dynamodb:table:ReadCapacityUnits`` - The provisioned read capacity for a DynamoDB table.
        - ``dynamodb:table:WriteCapacityUnits`` - The provisioned write capacity for a DynamoDB table.
        - ``dynamodb:index:ReadCapacityUnits`` - The provisioned read capacity for a DynamoDB global secondary index.
        - ``dynamodb:index:WriteCapacityUnits`` - The provisioned write capacity for a DynamoDB global secondary index.
        - ``rds:cluster:ReadReplicaCount`` - The count of Aurora Replicas in an Aurora DB cluster. Available for Aurora MySQL-compatible edition and Aurora PostgreSQL-compatible edition.
        - ``sagemaker:variant:DesiredInstanceCount`` - The number of EC2 instances for a SageMaker model endpoint variant.
        - ``custom-resource:ResourceType:Property`` - The scalable dimension for a custom resource provided by your own application or service.
        - ``comprehend:document-classifier-endpoint:DesiredInferenceUnits`` - The number of inference units for an Amazon Comprehend document classification endpoint.
        - ``comprehend:entity-recognizer-endpoint:DesiredInferenceUnits`` - The number of inference units for an Amazon Comprehend entity recognizer endpoint.
        - ``lambda:function:ProvisionedConcurrency`` - The provisioned concurrency for a Lambda function.
        - ``cassandra:table:ReadCapacityUnits`` - The provisioned read capacity for an Amazon Keyspaces table.
        - ``cassandra:table:WriteCapacityUnits`` - The provisioned write capacity for an Amazon Keyspaces table.
        - ``kafka:broker-storage:VolumeSize`` - The provisioned volume size (in GiB) for brokers in an Amazon MSK cluster.
        - ``elasticache:cache-cluster:Nodes`` - The number of nodes for an Amazon ElastiCache cache cluster.
        - ``elasticache:replication-group:NodeGroups`` - The number of node groups for an Amazon ElastiCache replication group.
        - ``elasticache:replication-group:Replicas`` - The number of replicas per node group for an Amazon ElastiCache replication group.
        - ``neptune:cluster:ReadReplicaCount`` - The count of read replicas in an Amazon Neptune DB cluster.
        - ``sagemaker:variant:DesiredProvisionedConcurrency`` - The provisioned concurrency for a SageMaker serverless endpoint.
        - ``sagemaker:inference-component:DesiredCopyCount`` - The number of copies across an endpoint for a SageMaker inference component.
        - ``workspaces:workspacespool:DesiredUserSessions`` - The number of user sessions for the WorkSpaces in the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-scalabledimension
        '''
        result = self._values.get("scalable_dimension")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_target_id(self) -> typing.Optional[builtins.str]:
        '''The CloudFormation-generated ID of an Application Auto Scaling scalable target.

        For more information about the ID, see the Return Value section of the ``AWS::ApplicationAutoScaling::ScalableTarget`` resource.
        .. epigraph::

           You must specify either the ``ScalingTargetId`` property, or the ``ResourceId`` , ``ScalableDimension`` , and ``ServiceNamespace`` properties, but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-scalingtargetid
        '''
        result = self._values.get("scaling_target_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the AWS service that provides the resource, or a ``custom-resource`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-servicenamespace
        '''
        result = self._values.get("service_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def step_scaling_policy_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.StepScalingPolicyConfigurationProperty"]]:
        '''A step scaling policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration
        '''
        result = self._values.get("step_scaling_policy_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.StepScalingPolicyConfigurationProperty"]], result)

    @builtins.property
    def target_tracking_scaling_policy_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingScalingPolicyConfigurationProperty"]]:
        '''A target tracking scaling policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration
        '''
        result = self._values.get("target_tracking_scaling_policy_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingScalingPolicyConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScalingPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnScalingPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin",
):
    '''The ``AWS::ApplicationAutoScaling::ScalingPolicy`` resource defines a scaling policy that Application Auto Scaling uses to adjust the capacity of a scalable target.

    For more information, see `Target tracking scaling policies <https://docs.aws.amazon.com/autoscaling/application/userguide/application-auto-scaling-target-tracking.html>`_ and `Step scaling policies <https://docs.aws.amazon.com/autoscaling/application/userguide/application-auto-scaling-step-scaling-policies.html>`_ in the *Application Auto Scaling User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html
    :cloudformationResource: AWS::ApplicationAutoScaling::ScalingPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
        
        cfn_scaling_policy_props_mixin = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin(applicationautoscaling_mixins.CfnScalingPolicyMixinProps(
            policy_name="policyName",
            policy_type="policyType",
            predictive_scaling_policy_configuration=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPolicyConfigurationProperty(
                max_capacity_breach_behavior="maxCapacityBreachBehavior",
                max_capacity_buffer=123,
                metric_specifications=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty(
                    customized_capacity_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty(
                        metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                                metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                    dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    ),
                    customized_load_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty(
                        metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                                metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                    dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    ),
                    customized_scaling_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty(
                        metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                                metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                    dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    ),
                    predefined_load_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    predefined_metric_pair_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    predefined_scaling_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    target_value=123
                )],
                mode="mode",
                scheduling_buffer_time=123
            ),
            resource_id="resourceId",
            scalable_dimension="scalableDimension",
            scaling_target_id="scalingTargetId",
            service_namespace="serviceNamespace",
            step_scaling_policy_configuration=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.StepScalingPolicyConfigurationProperty(
                adjustment_type="adjustmentType",
                cooldown=123,
                metric_aggregation_type="metricAggregationType",
                min_adjustment_magnitude=123,
                step_adjustments=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.StepAdjustmentProperty(
                    metric_interval_lower_bound=123,
                    metric_interval_upper_bound=123,
                    scaling_adjustment=123
                )]
            ),
            target_tracking_scaling_policy_configuration=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                customized_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty(
                    dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    metrics=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty(
                        expression="expression",
                        id="id",
                        label="label",
                        metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty(
                            metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricProperty(
                                dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            stat="stat",
                            unit="unit"
                        ),
                        return_data=False
                    )],
                    namespace="namespace",
                    statistic="statistic",
                    unit="unit"
                ),
                disable_scale_in=False,
                predefined_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty(
                    predefined_metric_type="predefinedMetricType",
                    resource_label="resourceLabel"
                ),
                scale_in_cooldown=123,
                scale_out_cooldown=123,
                target_value=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnScalingPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApplicationAutoScaling::ScalingPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__932aaf740a6a1435196f066ae3dc479dbca49da6054590006760ad6c7005c62c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a954b3da6b57ef86b01e364f80d119cfdc1cb74c7f16c8483c476a56cb483fe)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d511615d56de3a2964111baad16cdc5f74f428db935868d03b404935e4f358b6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnScalingPolicyMixinProps:
        return typing.cast(CfnScalingPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "metric_name": "metricName",
            "metrics": "metrics",
            "namespace": "namespace",
            "statistic": "statistic",
            "unit": "unit",
        },
    )
    class CustomizedMetricSpecificationProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.MetricDimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metric_name: typing.Optional[builtins.str] = None,
            metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            namespace: typing.Optional[builtins.str] = None,
            statistic: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains customized metric specification information for a target tracking scaling policy for Application Auto Scaling.

            For information about the available metrics for a service, see `AWS services that publish CloudWatch metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_ in the *Amazon CloudWatch User Guide* .

            To create your customized metric specification:

            - Add values for each required parameter from CloudWatch. You can use an existing metric, or a new metric that you create. To use your own metric, you must first publish the metric to CloudWatch. For more information, see `Publish custom metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html>`_ in the *Amazon CloudWatch User Guide* .
            - Choose a metric that changes proportionally with capacity. The value of the metric should increase or decrease in inverse proportion to the number of capacity units. That is, the value of the metric should decrease when capacity increases, and increase when capacity decreases.

            For an example of how creating new metrics can be useful, see `Scaling based on Amazon SQS <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-using-sqs-queue.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . This topic mentions Auto Scaling groups, but the same scenario for Amazon SQS can apply to the target tracking scaling policies that you create for a Spot Fleet by using Application Auto Scaling.

            For more information about the CloudWatch terminology below, see `Amazon CloudWatch concepts <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html>`_ .

            ``CustomizedMetricSpecification`` is a property of the `AWS::ApplicationAutoScaling::ScalingPolicy TargetTrackingScalingPolicyConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html>`_ property type.

            :param dimensions: The dimensions of the metric. Conditional: If you published your metric with dimensions, you must specify the same dimensions in your scaling policy.
            :param metric_name: The name of the metric. To get the exact metric name, namespace, and dimensions, inspect the `Metric <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_Metric.html>`_ object that's returned by a call to `ListMetrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_ListMetrics.html>`_ .
            :param metrics: The metrics to include in the target tracking scaling policy, as a metric data query. This can include both raw metric and metric math expressions.
            :param namespace: The namespace of the metric.
            :param statistic: The statistic of the metric.
            :param unit: The unit of the metric. For a complete list of the units that CloudWatch supports, see the `MetricDatum <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html>`_ data type in the *Amazon CloudWatch API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                customized_metric_specification_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty(
                    dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    metrics=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty(
                        expression="expression",
                        id="id",
                        label="label",
                        metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty(
                            metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricProperty(
                                dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            stat="stat",
                            unit="unit"
                        ),
                        return_data=False
                    )],
                    namespace="namespace",
                    statistic="statistic",
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8afbcda4ad27d0c22ee099b805507b12bad062007f5bd7fe823f35e366d3de62)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if metrics is not None:
                self._values["metrics"] = metrics
            if namespace is not None:
                self._values["namespace"] = namespace
            if statistic is not None:
                self._values["statistic"] = statistic
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricDimensionProperty"]]]]:
            '''The dimensions of the metric.

            Conditional: If you published your metric with dimensions, you must specify the same dimensions in your scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricDimensionProperty"]]]], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric.

            To get the exact metric name, namespace, and dimensions, inspect the `Metric <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_Metric.html>`_ object that's returned by a call to `ListMetrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_ListMetrics.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty"]]]]:
            '''The metrics to include in the target tracking scaling policy, as a metric data query.

            This can include both raw metric and metric math expressions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-metrics
            '''
            result = self._values.get("metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty"]]]], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def statistic(self) -> typing.Optional[builtins.str]:
            '''The statistic of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-statistic
            '''
            result = self._values.get("statistic")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit of the metric.

            For a complete list of the units that CloudWatch supports, see the `MetricDatum <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html>`_ data type in the *Amazon CloudWatch API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomizedMetricSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class MetricDimensionProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``MetricDimension`` specifies a name/value pair that is part of the identity of a CloudWatch metric for the ``Dimensions`` property of the `AWS::ApplicationAutoScaling::ScalingPolicy CustomizedMetricSpecification <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html>`_ property type. Duplicate dimensions are not allowed.

            :param name: The name of the dimension.
            :param value: The value of the dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-metricdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                metric_dimension_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__056aa8eb80fa82904b9a738d22b8ebe5a4ac45679ffe2856ae3a05fd18b15016)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-metricdimension.html#cfn-applicationautoscaling-scalingpolicy-metricdimension-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-metricdimension.html#cfn-applicationautoscaling-scalingpolicy-metricdimension-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "predefined_metric_type": "predefinedMetricType",
            "resource_label": "resourceLabel",
        },
    )
    class PredefinedMetricSpecificationProperty:
        def __init__(
            self,
            *,
            predefined_metric_type: typing.Optional[builtins.str] = None,
            resource_label: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains predefined metric specification information for a target tracking scaling policy for Application Auto Scaling.

            ``PredefinedMetricSpecification`` is a property of the `AWS::ApplicationAutoScaling::ScalingPolicy TargetTrackingScalingPolicyConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html>`_ property type.

            :param predefined_metric_type: The metric type. The ``ALBRequestCountPerTarget`` metric type applies only to Spot fleet requests and ECS services.
            :param resource_label: Identifies the resource associated with the metric type. You can't specify a resource label unless the metric type is ``ALBRequestCountPerTarget`` and there is a target group attached to the Spot Fleet or ECS service. You create the resource label by appending the final portion of the load balancer ARN and the final portion of the target group ARN into a single value, separated by a forward slash (/). The format of the resource label is: ``app/my-alb/778d41231b141a0f/targetgroup/my-alb-target-group/943f017f100becff`` . Where: - app// is the final portion of the load balancer ARN - targetgroup// is the final portion of the target group ARN. To find the ARN for an Application Load Balancer, use the `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ API operation. To find the ARN for the target group, use the `DescribeTargetGroups <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeTargetGroups.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predefinedmetricspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                predefined_metric_specification_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty(
                    predefined_metric_type="predefinedMetricType",
                    resource_label="resourceLabel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b28b44359760e1302f08f5faf8ce5bd7c7a656bd34e0fe26e2f2d769daa5acb2)
                check_type(argname="argument predefined_metric_type", value=predefined_metric_type, expected_type=type_hints["predefined_metric_type"])
                check_type(argname="argument resource_label", value=resource_label, expected_type=type_hints["resource_label"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if predefined_metric_type is not None:
                self._values["predefined_metric_type"] = predefined_metric_type
            if resource_label is not None:
                self._values["resource_label"] = resource_label

        @builtins.property
        def predefined_metric_type(self) -> typing.Optional[builtins.str]:
            '''The metric type.

            The ``ALBRequestCountPerTarget`` metric type applies only to Spot fleet requests and ECS services.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predefinedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-predefinedmetricspecification-predefinedmetrictype
            '''
            result = self._values.get("predefined_metric_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_label(self) -> typing.Optional[builtins.str]:
            '''Identifies the resource associated with the metric type.

            You can't specify a resource label unless the metric type is ``ALBRequestCountPerTarget`` and there is a target group attached to the Spot Fleet or ECS service.

            You create the resource label by appending the final portion of the load balancer ARN and the final portion of the target group ARN into a single value, separated by a forward slash (/). The format of the resource label is:

            ``app/my-alb/778d41231b141a0f/targetgroup/my-alb-target-group/943f017f100becff`` .

            Where:

            - app// is the final portion of the load balancer ARN
            - targetgroup// is the final portion of the target group ARN.

            To find the ARN for an Application Load Balancer, use the `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ API operation. To find the ARN for the target group, use the `DescribeTargetGroups <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeTargetGroups.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predefinedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-predefinedmetricspecification-resourcelabel
            '''
            result = self._values.get("resource_label")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredefinedMetricSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty",
        jsii_struct_bases=[],
        name_mapping={"metric_data_queries": "metricDataQueries"},
    )
    class PredictiveScalingCustomizedCapacityMetricProperty:
        def __init__(
            self,
            *,
            metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Represents a CloudWatch metric of your choosing for a predictive scaling policy.

            :param metric_data_queries: One or more metric data queries to provide data points for a metric specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingcustomizedcapacitymetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                predictive_scaling_customized_capacity_metric_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty(
                    metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                        expression="expression",
                        id="id",
                        label="label",
                        metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                            metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            stat="stat",
                            unit="unit"
                        ),
                        return_data=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ffb0cbdae4ecc2f4b18c128f667105620d63ab6d046ac33dbd1b808b535416e)
                check_type(argname="argument metric_data_queries", value=metric_data_queries, expected_type=type_hints["metric_data_queries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_data_queries is not None:
                self._values["metric_data_queries"] = metric_data_queries

        @builtins.property
        def metric_data_queries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty"]]]]:
            '''One or more metric data queries to provide data points for a metric specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingcustomizedcapacitymetric.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingcustomizedcapacitymetric-metricdataqueries
            '''
            result = self._values.get("metric_data_queries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingCustomizedCapacityMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty",
        jsii_struct_bases=[],
        name_mapping={"metric_data_queries": "metricDataQueries"},
    )
    class PredictiveScalingCustomizedLoadMetricProperty:
        def __init__(
            self,
            *,
            metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The customized load metric specification.

            :param metric_data_queries: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingcustomizedloadmetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                predictive_scaling_customized_load_metric_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty(
                    metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                        expression="expression",
                        id="id",
                        label="label",
                        metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                            metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            stat="stat",
                            unit="unit"
                        ),
                        return_data=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b4c5eed138acad76bc740a8213cf25674ec254f07044f087d7eb9b7a53550e2f)
                check_type(argname="argument metric_data_queries", value=metric_data_queries, expected_type=type_hints["metric_data_queries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_data_queries is not None:
                self._values["metric_data_queries"] = metric_data_queries

        @builtins.property
        def metric_data_queries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingcustomizedloadmetric.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingcustomizedloadmetric-metricdataqueries
            '''
            result = self._values.get("metric_data_queries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingCustomizedLoadMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty",
        jsii_struct_bases=[],
        name_mapping={"metric_data_queries": "metricDataQueries"},
    )
    class PredictiveScalingCustomizedScalingMetricProperty:
        def __init__(
            self,
            *,
            metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''One or more metric data queries to provide data points for a metric specification.

            :param metric_data_queries: One or more metric data queries to provide data points for a metric specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingcustomizedscalingmetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                predictive_scaling_customized_scaling_metric_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty(
                    metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                        expression="expression",
                        id="id",
                        label="label",
                        metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                            metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            stat="stat",
                            unit="unit"
                        ),
                        return_data=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6271c324ecb0ebb213294e8f41c66ce2fd0e3712e2f03c9b3b3443d150ba2fe)
                check_type(argname="argument metric_data_queries", value=metric_data_queries, expected_type=type_hints["metric_data_queries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_data_queries is not None:
                self._values["metric_data_queries"] = metric_data_queries

        @builtins.property
        def metric_data_queries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty"]]]]:
            '''One or more metric data queries to provide data points for a metric specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingcustomizedscalingmetric.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingcustomizedscalingmetric-metricdataqueries
            '''
            result = self._values.get("metric_data_queries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingCustomizedScalingMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "expression": "expression",
            "id": "id",
            "label": "label",
            "metric_stat": "metricStat",
            "return_data": "returnData",
        },
    )
    class PredictiveScalingMetricDataQueryProperty:
        def __init__(
            self,
            *,
            expression: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            label: typing.Optional[builtins.str] = None,
            metric_stat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            return_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The metric data to return.

            Also defines whether this call is returning data for one metric only, or whether it is performing a math expression on the values of returned metric statistics to create a new time series. A time series is a series of data points, each of which is associated with a timestamp.

            :param expression: The math expression to perform on the returned data, if this object is performing a math expression. This expression can use the ``Id`` of the other metrics to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions. Conditional: Within each ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.
            :param id: A short name that identifies the object's results in the response. This name must be unique among all ``MetricDataQuery`` objects specified for a single scaling policy. If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscores. The first character must be a lowercase letter.
            :param label: A human-readable label for this metric or expression. This is especially useful if this is a math expression, so that you know what the value represents.
            :param metric_stat: Information about the metric data to return. Conditional: Within each ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.
            :param return_data: Indicates whether to return the timestamps and raw data values of this metric. If you use any math expressions, specify ``true`` for this value for only the final math expression that the metric specification is based on. You must specify ``false`` for ``ReturnData`` for all the other metrics and expressions used in the metric specification. If you are only retrieving metrics and not performing any math expressions, do not specify anything for ``ReturnData`` . This sets it to its default ( ``true`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricdataquery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                predictive_scaling_metric_data_query_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                    expression="expression",
                    id="id",
                    label="label",
                    metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                        metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                            dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                name="name",
                                value="value"
                            )],
                            metric_name="metricName",
                            namespace="namespace"
                        ),
                        stat="stat",
                        unit="unit"
                    ),
                    return_data=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1cd71bcb12d8818c4ee665cf114e6a8d6e29210a0027ebcb92b87f2ba46c11c)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument label", value=label, expected_type=type_hints["label"])
                check_type(argname="argument metric_stat", value=metric_stat, expected_type=type_hints["metric_stat"])
                check_type(argname="argument return_data", value=return_data, expected_type=type_hints["return_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression
            if id is not None:
                self._values["id"] = id
            if label is not None:
                self._values["label"] = label
            if metric_stat is not None:
                self._values["metric_stat"] = metric_stat
            if return_data is not None:
                self._values["return_data"] = return_data

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The math expression to perform on the returned data, if this object is performing a math expression.

            This expression can use the ``Id`` of the other metrics to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions.

            Conditional: Within each ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricdataquery.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricdataquery-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A short name that identifies the object's results in the response.

            This name must be unique among all ``MetricDataQuery`` objects specified for a single scaling policy. If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscores. The first character must be a lowercase letter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricdataquery.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricdataquery-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def label(self) -> typing.Optional[builtins.str]:
            '''A human-readable label for this metric or expression.

            This is especially useful if this is a math expression, so that you know what the value represents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricdataquery.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricdataquery-label
            '''
            result = self._values.get("label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_stat(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty"]]:
            '''Information about the metric data to return.

            Conditional: Within each ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricdataquery.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricdataquery-metricstat
            '''
            result = self._values.get("metric_stat")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty"]], result)

        @builtins.property
        def return_data(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to return the timestamps and raw data values of this metric.

            If you use any math expressions, specify ``true`` for this value for only the final math expression that the metric specification is based on. You must specify ``false`` for ``ReturnData`` for all the other metrics and expressions used in the metric specification.

            If you are only retrieving metrics and not performing any math expressions, do not specify anything for ``ReturnData`` . This sets it to its default ( ``true`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricdataquery.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricdataquery-returndata
            '''
            result = self._values.get("return_data")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingMetricDataQueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class PredictiveScalingMetricDimensionProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the dimension of a metric.

            :param name: The name of the dimension.
            :param value: The value of the dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                predictive_scaling_metric_dimension_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c8070f3ef92724e83279e91c46e1b5ec49aa73a2bfd343011e8c14b6ce12767)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricdimension.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricdimension-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricdimension.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricdimension-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingMetricDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "metric_name": "metricName",
            "namespace": "namespace",
        },
    )
    class PredictiveScalingMetricProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metric_name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the scaling metric.

            :param dimensions: Describes the dimensions of the metric.
            :param metric_name: The name of the metric.
            :param namespace: The namespace of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                predictive_scaling_metric_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                    dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__077664a9309c3b45e697083a49221eea10faf26443a91ad4375eed712f1c00f5)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty"]]]]:
            '''Describes the dimensions of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetric.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetric-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty"]]]], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetric.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetric-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetric.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetric-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customized_capacity_metric_specification": "customizedCapacityMetricSpecification",
            "customized_load_metric_specification": "customizedLoadMetricSpecification",
            "customized_scaling_metric_specification": "customizedScalingMetricSpecification",
            "predefined_load_metric_specification": "predefinedLoadMetricSpecification",
            "predefined_metric_pair_specification": "predefinedMetricPairSpecification",
            "predefined_scaling_metric_specification": "predefinedScalingMetricSpecification",
            "target_value": "targetValue",
        },
    )
    class PredictiveScalingMetricSpecificationProperty:
        def __init__(
            self,
            *,
            customized_capacity_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            customized_load_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            customized_scaling_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            predefined_load_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            predefined_metric_pair_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            predefined_scaling_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''This structure specifies the metrics and target utilization settings for a predictive scaling policy.

            You must specify either a metric pair, or a load metric and a scaling metric individually. Specifying a metric pair instead of individual metrics provides a simpler way to configure metrics for a scaling policy. You choose the metric pair, and the policy automatically knows the correct sum and average statistics to use for the load metric and the scaling metric.

            :param customized_capacity_metric_specification: The customized capacity metric specification.
            :param customized_load_metric_specification: The customized load metric specification.
            :param customized_scaling_metric_specification: The customized scaling metric specification.
            :param predefined_load_metric_specification: The predefined load metric specification.
            :param predefined_metric_pair_specification: The predefined metric pair specification that determines the appropriate scaling metric and load metric to use.
            :param predefined_scaling_metric_specification: The predefined scaling metric specification.
            :param target_value: Specifies the target utilization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                predictive_scaling_metric_specification_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty(
                    customized_capacity_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty(
                        metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                                metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                    dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    ),
                    customized_load_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty(
                        metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                                metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                    dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    ),
                    customized_scaling_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty(
                        metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                                metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                    dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    ),
                    predefined_load_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    predefined_metric_pair_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    predefined_scaling_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    target_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca18e6910fd0fb22f9473e97f8ecbc4133469cf68b559ac45f2de253b5f91ec0)
                check_type(argname="argument customized_capacity_metric_specification", value=customized_capacity_metric_specification, expected_type=type_hints["customized_capacity_metric_specification"])
                check_type(argname="argument customized_load_metric_specification", value=customized_load_metric_specification, expected_type=type_hints["customized_load_metric_specification"])
                check_type(argname="argument customized_scaling_metric_specification", value=customized_scaling_metric_specification, expected_type=type_hints["customized_scaling_metric_specification"])
                check_type(argname="argument predefined_load_metric_specification", value=predefined_load_metric_specification, expected_type=type_hints["predefined_load_metric_specification"])
                check_type(argname="argument predefined_metric_pair_specification", value=predefined_metric_pair_specification, expected_type=type_hints["predefined_metric_pair_specification"])
                check_type(argname="argument predefined_scaling_metric_specification", value=predefined_scaling_metric_specification, expected_type=type_hints["predefined_scaling_metric_specification"])
                check_type(argname="argument target_value", value=target_value, expected_type=type_hints["target_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customized_capacity_metric_specification is not None:
                self._values["customized_capacity_metric_specification"] = customized_capacity_metric_specification
            if customized_load_metric_specification is not None:
                self._values["customized_load_metric_specification"] = customized_load_metric_specification
            if customized_scaling_metric_specification is not None:
                self._values["customized_scaling_metric_specification"] = customized_scaling_metric_specification
            if predefined_load_metric_specification is not None:
                self._values["predefined_load_metric_specification"] = predefined_load_metric_specification
            if predefined_metric_pair_specification is not None:
                self._values["predefined_metric_pair_specification"] = predefined_metric_pair_specification
            if predefined_scaling_metric_specification is not None:
                self._values["predefined_scaling_metric_specification"] = predefined_scaling_metric_specification
            if target_value is not None:
                self._values["target_value"] = target_value

        @builtins.property
        def customized_capacity_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty"]]:
            '''The customized capacity metric specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification-customizedcapacitymetricspecification
            '''
            result = self._values.get("customized_capacity_metric_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty"]], result)

        @builtins.property
        def customized_load_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty"]]:
            '''The customized load metric specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification-customizedloadmetricspecification
            '''
            result = self._values.get("customized_load_metric_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty"]], result)

        @builtins.property
        def customized_scaling_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty"]]:
            '''The customized scaling metric specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification-customizedscalingmetricspecification
            '''
            result = self._values.get("customized_scaling_metric_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty"]], result)

        @builtins.property
        def predefined_load_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty"]]:
            '''The predefined load metric specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification-predefinedloadmetricspecification
            '''
            result = self._values.get("predefined_load_metric_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty"]], result)

        @builtins.property
        def predefined_metric_pair_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty"]]:
            '''The predefined metric pair specification that determines the appropriate scaling metric and load metric to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification-predefinedmetricpairspecification
            '''
            result = self._values.get("predefined_metric_pair_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty"]], result)

        @builtins.property
        def predefined_scaling_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty"]]:
            '''The predefined scaling metric specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification-predefinedscalingmetricspecification
            '''
            result = self._values.get("predefined_scaling_metric_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty"]], result)

        @builtins.property
        def target_value(self) -> typing.Optional[jsii.Number]:
            '''Specifies the target utilization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricspecification-targetvalue
            '''
            result = self._values.get("target_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingMetricSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty",
        jsii_struct_bases=[],
        name_mapping={"metric": "metric", "stat": "stat", "unit": "unit"},
    )
    class PredictiveScalingMetricStatProperty:
        def __init__(
            self,
            *,
            metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stat: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure defines the CloudWatch metric to return, along with the statistic and unit.

            :param metric: The CloudWatch metric to return, including the metric name, namespace, and dimensions. To get the exact metric name, namespace, and dimensions, inspect the `Metric <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_Metric.html>`_ object that is returned by a call to `ListMetrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_ListMetrics.html>`_ .
            :param stat: The statistic to return. It can include any CloudWatch statistic or extended statistic. For a list of valid values, see the table in `Statistics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic>`_ in the *Amazon CloudWatch User Guide* . The most commonly used metrics for predictive scaling are ``Average`` and ``Sum`` .
            :param unit: The unit to use for the returned data points. For a complete list of the units that CloudWatch supports, see the `MetricDatum <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html>`_ data type in the *Amazon CloudWatch API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricstat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                predictive_scaling_metric_stat_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                    metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                        dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                            name="name",
                            value="value"
                        )],
                        metric_name="metricName",
                        namespace="namespace"
                    ),
                    stat="stat",
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__73b1e1d88fe137e14c136a4588d278a7ce6dafda668bb28817f35d9c67e6f918)
                check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
                check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric is not None:
                self._values["metric"] = metric
            if stat is not None:
                self._values["stat"] = stat
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def metric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty"]]:
            '''The CloudWatch metric to return, including the metric name, namespace, and dimensions.

            To get the exact metric name, namespace, and dimensions, inspect the `Metric <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_Metric.html>`_ object that is returned by a call to `ListMetrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_ListMetrics.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricstat.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricstat-metric
            '''
            result = self._values.get("metric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty"]], result)

        @builtins.property
        def stat(self) -> typing.Optional[builtins.str]:
            '''The statistic to return.

            It can include any CloudWatch statistic or extended statistic. For a list of valid values, see the table in `Statistics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic>`_ in the *Amazon CloudWatch User Guide* .

            The most commonly used metrics for predictive scaling are ``Average`` and ``Sum`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricstat.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricstat-stat
            '''
            result = self._values.get("stat")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit to use for the returned data points.

            For a complete list of the units that CloudWatch supports, see the `MetricDatum <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html>`_ data type in the *Amazon CloudWatch API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingmetricstat.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingmetricstat-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingMetricStatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPolicyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_capacity_breach_behavior": "maxCapacityBreachBehavior",
            "max_capacity_buffer": "maxCapacityBuffer",
            "metric_specifications": "metricSpecifications",
            "mode": "mode",
            "scheduling_buffer_time": "schedulingBufferTime",
        },
    )
    class PredictiveScalingPolicyConfigurationProperty:
        def __init__(
            self,
            *,
            max_capacity_breach_behavior: typing.Optional[builtins.str] = None,
            max_capacity_buffer: typing.Optional[jsii.Number] = None,
            metric_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            mode: typing.Optional[builtins.str] = None,
            scheduling_buffer_time: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Represents a predictive scaling policy configuration.

            Predictive scaling is supported on Amazon ECS services.

            :param max_capacity_breach_behavior: Defines the behavior that should be applied if the forecast capacity approaches or exceeds the maximum capacity. Defaults to ``HonorMaxCapacity`` if not specified.
            :param max_capacity_buffer: The size of the capacity buffer to use when the forecast capacity is close to or exceeds the maximum capacity. The value is specified as a percentage relative to the forecast capacity. For example, if the buffer is 10, this means a 10 percent buffer, such that if the forecast capacity is 50, and the maximum capacity is 40, then the effective maximum capacity is 55. Required if the ``MaxCapacityBreachBehavior`` property is set to ``IncreaseMaxCapacity`` , and cannot be used otherwise.
            :param metric_specifications: This structure includes the metrics and target utilization to use for predictive scaling. This is an array, but we currently only support a single metric specification. That is, you can specify a target value and a single metric pair, or a target value and one scaling metric and one load metric.
            :param mode: The predictive scaling mode. Defaults to ``ForecastOnly`` if not specified.
            :param scheduling_buffer_time: The amount of time, in seconds, that the start time can be advanced. The value must be less than the forecast interval duration of 3600 seconds (60 minutes). Defaults to 300 seconds if not specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpolicyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                predictive_scaling_policy_configuration_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPolicyConfigurationProperty(
                    max_capacity_breach_behavior="maxCapacityBreachBehavior",
                    max_capacity_buffer=123,
                    metric_specifications=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty(
                        customized_capacity_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty(
                            metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                                expression="expression",
                                id="id",
                                label="label",
                                metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                                    metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                        dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )]
                        ),
                        customized_load_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty(
                            metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                                expression="expression",
                                id="id",
                                label="label",
                                metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                                    metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                        dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )]
                        ),
                        customized_scaling_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty(
                            metric_data_queries=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty(
                                expression="expression",
                                id="id",
                                label="label",
                                metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty(
                                    metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty(
                                        dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )]
                        ),
                        predefined_load_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty(
                            predefined_metric_type="predefinedMetricType",
                            resource_label="resourceLabel"
                        ),
                        predefined_metric_pair_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty(
                            predefined_metric_type="predefinedMetricType",
                            resource_label="resourceLabel"
                        ),
                        predefined_scaling_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty(
                            predefined_metric_type="predefinedMetricType",
                            resource_label="resourceLabel"
                        ),
                        target_value=123
                    )],
                    mode="mode",
                    scheduling_buffer_time=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed2c9cbdbb3a30239956d38ec8ede1347fa63be40b777472eed09b5ff62a17d5)
                check_type(argname="argument max_capacity_breach_behavior", value=max_capacity_breach_behavior, expected_type=type_hints["max_capacity_breach_behavior"])
                check_type(argname="argument max_capacity_buffer", value=max_capacity_buffer, expected_type=type_hints["max_capacity_buffer"])
                check_type(argname="argument metric_specifications", value=metric_specifications, expected_type=type_hints["metric_specifications"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument scheduling_buffer_time", value=scheduling_buffer_time, expected_type=type_hints["scheduling_buffer_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_capacity_breach_behavior is not None:
                self._values["max_capacity_breach_behavior"] = max_capacity_breach_behavior
            if max_capacity_buffer is not None:
                self._values["max_capacity_buffer"] = max_capacity_buffer
            if metric_specifications is not None:
                self._values["metric_specifications"] = metric_specifications
            if mode is not None:
                self._values["mode"] = mode
            if scheduling_buffer_time is not None:
                self._values["scheduling_buffer_time"] = scheduling_buffer_time

        @builtins.property
        def max_capacity_breach_behavior(self) -> typing.Optional[builtins.str]:
            '''Defines the behavior that should be applied if the forecast capacity approaches or exceeds the maximum capacity.

            Defaults to ``HonorMaxCapacity`` if not specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingpolicyconfiguration-maxcapacitybreachbehavior
            '''
            result = self._values.get("max_capacity_breach_behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_capacity_buffer(self) -> typing.Optional[jsii.Number]:
            '''The size of the capacity buffer to use when the forecast capacity is close to or exceeds the maximum capacity.

            The value is specified as a percentage relative to the forecast capacity. For example, if the buffer is 10, this means a 10 percent buffer, such that if the forecast capacity is 50, and the maximum capacity is 40, then the effective maximum capacity is 55.

            Required if the ``MaxCapacityBreachBehavior`` property is set to ``IncreaseMaxCapacity`` , and cannot be used otherwise.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingpolicyconfiguration-maxcapacitybuffer
            '''
            result = self._values.get("max_capacity_buffer")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def metric_specifications(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty"]]]]:
            '''This structure includes the metrics and target utilization to use for predictive scaling.

            This is an array, but we currently only support a single metric specification. That is, you can specify a target value and a single metric pair, or a target value and one scaling metric and one load metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingpolicyconfiguration-metricspecifications
            '''
            result = self._values.get("metric_specifications")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty"]]]], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The predictive scaling mode.

            Defaults to ``ForecastOnly`` if not specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingpolicyconfiguration-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scheduling_buffer_time(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, that the start time can be advanced.

            The value must be less than the forecast interval duration of 3600 seconds (60 minutes). Defaults to 300 seconds if not specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingpolicyconfiguration-schedulingbuffertime
            '''
            result = self._values.get("scheduling_buffer_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingPolicyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "predefined_metric_type": "predefinedMetricType",
            "resource_label": "resourceLabel",
        },
    )
    class PredictiveScalingPredefinedLoadMetricProperty:
        def __init__(
            self,
            *,
            predefined_metric_type: typing.Optional[builtins.str] = None,
            resource_label: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a load metric for a predictive scaling policy.

            When returned in the output of ``DescribePolicies`` , it indicates that a predictive scaling policy uses individually specified load and scaling metrics instead of a metric pair.

            The following predefined metrics are available for predictive scaling:

            - ``ECSServiceAverageCPUUtilization``
            - ``ECSServiceAverageMemoryUtilization``
            - ``ECSServiceCPUUtilization``
            - ``ECSServiceMemoryUtilization``
            - ``ECSServiceTotalCPUUtilization``
            - ``ECSServiceTotalMemoryUtilization``
            - ``ALBRequestCount``
            - ``ALBRequestCountPerTarget``
            - ``TotalALBRequestCount``

            :param predefined_metric_type: The metric type.
            :param resource_label: A label that uniquely identifies a target group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpredefinedloadmetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                predictive_scaling_predefined_load_metric_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty(
                    predefined_metric_type="predefinedMetricType",
                    resource_label="resourceLabel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4936dca5996bf7399a5aea56aaf77d72e381e6ee1a4143d1d6a2704c6d3946f0)
                check_type(argname="argument predefined_metric_type", value=predefined_metric_type, expected_type=type_hints["predefined_metric_type"])
                check_type(argname="argument resource_label", value=resource_label, expected_type=type_hints["resource_label"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if predefined_metric_type is not None:
                self._values["predefined_metric_type"] = predefined_metric_type
            if resource_label is not None:
                self._values["resource_label"] = resource_label

        @builtins.property
        def predefined_metric_type(self) -> typing.Optional[builtins.str]:
            '''The metric type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpredefinedloadmetric.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingpredefinedloadmetric-predefinedmetrictype
            '''
            result = self._values.get("predefined_metric_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_label(self) -> typing.Optional[builtins.str]:
            '''A label that uniquely identifies a target group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpredefinedloadmetric.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingpredefinedloadmetric-resourcelabel
            '''
            result = self._values.get("resource_label")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingPredefinedLoadMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty",
        jsii_struct_bases=[],
        name_mapping={
            "predefined_metric_type": "predefinedMetricType",
            "resource_label": "resourceLabel",
        },
    )
    class PredictiveScalingPredefinedMetricPairProperty:
        def __init__(
            self,
            *,
            predefined_metric_type: typing.Optional[builtins.str] = None,
            resource_label: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a metric pair for a predictive scaling policy.

            The following predefined metrics are available for predictive scaling:

            - ``ECSServiceAverageCPUUtilization``
            - ``ECSServiceAverageMemoryUtilization``
            - ``ECSServiceCPUUtilization``
            - ``ECSServiceMemoryUtilization``
            - ``ECSServiceTotalCPUUtilization``
            - ``ECSServiceTotalMemoryUtilization``
            - ``ALBRequestCount``
            - ``ALBRequestCountPerTarget``
            - ``TotalALBRequestCount``

            :param predefined_metric_type: Indicates which metrics to use. There are two different types of metrics for each metric type: one is a load metric and one is a scaling metric.
            :param resource_label: A label that uniquely identifies a specific target group from which to determine the total and average request count.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpredefinedmetricpair.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                predictive_scaling_predefined_metric_pair_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty(
                    predefined_metric_type="predefinedMetricType",
                    resource_label="resourceLabel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17ee91ad66f40f633663008094aa047fc5cdd0df7e3df7a2cd4c4012f62e5aa9)
                check_type(argname="argument predefined_metric_type", value=predefined_metric_type, expected_type=type_hints["predefined_metric_type"])
                check_type(argname="argument resource_label", value=resource_label, expected_type=type_hints["resource_label"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if predefined_metric_type is not None:
                self._values["predefined_metric_type"] = predefined_metric_type
            if resource_label is not None:
                self._values["resource_label"] = resource_label

        @builtins.property
        def predefined_metric_type(self) -> typing.Optional[builtins.str]:
            '''Indicates which metrics to use.

            There are two different types of metrics for each metric type: one is a load metric and one is a scaling metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpredefinedmetricpair.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingpredefinedmetricpair-predefinedmetrictype
            '''
            result = self._values.get("predefined_metric_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_label(self) -> typing.Optional[builtins.str]:
            '''A label that uniquely identifies a specific target group from which to determine the total and average request count.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpredefinedmetricpair.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingpredefinedmetricpair-resourcelabel
            '''
            result = self._values.get("resource_label")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingPredefinedMetricPairProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "predefined_metric_type": "predefinedMetricType",
            "resource_label": "resourceLabel",
        },
    )
    class PredictiveScalingPredefinedScalingMetricProperty:
        def __init__(
            self,
            *,
            predefined_metric_type: typing.Optional[builtins.str] = None,
            resource_label: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a scaling metric for a predictive scaling policy.

            When returned in the output of ``DescribePolicies`` , it indicates that a predictive scaling policy uses individually specified load and scaling metrics instead of a metric pair.

            The following predefined metrics are available for predictive scaling:

            - ``ECSServiceAverageCPUUtilization``
            - ``ECSServiceAverageMemoryUtilization``
            - ``ECSServiceCPUUtilization``
            - ``ECSServiceMemoryUtilization``
            - ``ECSServiceTotalCPUUtilization``
            - ``ECSServiceTotalMemoryUtilization``
            - ``ALBRequestCount``
            - ``ALBRequestCountPerTarget``
            - ``TotalALBRequestCount``

            :param predefined_metric_type: The metric type.
            :param resource_label: A label that uniquely identifies a specific target group from which to determine the average request count.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpredefinedscalingmetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                predictive_scaling_predefined_scaling_metric_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty(
                    predefined_metric_type="predefinedMetricType",
                    resource_label="resourceLabel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b62b10c963a9b352358366ce63b5bcd51d54f43326baf1e2bc414ab0d458b3a)
                check_type(argname="argument predefined_metric_type", value=predefined_metric_type, expected_type=type_hints["predefined_metric_type"])
                check_type(argname="argument resource_label", value=resource_label, expected_type=type_hints["resource_label"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if predefined_metric_type is not None:
                self._values["predefined_metric_type"] = predefined_metric_type
            if resource_label is not None:
                self._values["resource_label"] = resource_label

        @builtins.property
        def predefined_metric_type(self) -> typing.Optional[builtins.str]:
            '''The metric type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpredefinedscalingmetric.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingpredefinedscalingmetric-predefinedmetrictype
            '''
            result = self._values.get("predefined_metric_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_label(self) -> typing.Optional[builtins.str]:
            '''A label that uniquely identifies a specific target group from which to determine the average request count.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predictivescalingpredefinedscalingmetric.html#cfn-applicationautoscaling-scalingpolicy-predictivescalingpredefinedscalingmetric-resourcelabel
            '''
            result = self._values.get("resource_label")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingPredefinedScalingMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.StepAdjustmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric_interval_lower_bound": "metricIntervalLowerBound",
            "metric_interval_upper_bound": "metricIntervalUpperBound",
            "scaling_adjustment": "scalingAdjustment",
        },
    )
    class StepAdjustmentProperty:
        def __init__(
            self,
            *,
            metric_interval_lower_bound: typing.Optional[jsii.Number] = None,
            metric_interval_upper_bound: typing.Optional[jsii.Number] = None,
            scaling_adjustment: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``StepAdjustment`` specifies a step adjustment for the ``StepAdjustments`` property of the `AWS::ApplicationAutoScaling::ScalingPolicy StepScalingPolicyConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html>`_ property type.

            For the following examples, suppose that you have an alarm with a breach threshold of 50:

            - To trigger a step adjustment when the metric is greater than or equal to 50 and less than 60, specify a lower bound of 0 and an upper bound of 10.
            - To trigger a step adjustment when the metric is greater than 40 and less than or equal to 50, specify a lower bound of -10 and an upper bound of 0.

            For more information, see `Step adjustments <https://docs.aws.amazon.com/autoscaling/application/userguide/application-auto-scaling-step-scaling-policies.html#as-scaling-steps>`_ in the *Application Auto Scaling User Guide* .

            You can find a sample template snippet in the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#aws-resource-applicationautoscaling-scalingpolicy--examples>`_ section of the ``AWS::ApplicationAutoScaling::ScalingPolicy`` documentation.

            :param metric_interval_lower_bound: The lower bound for the difference between the alarm threshold and the CloudWatch metric. If the metric value is above the breach threshold, the lower bound is inclusive (the metric must be greater than or equal to the threshold plus the lower bound). Otherwise, it is exclusive (the metric must be greater than the threshold plus the lower bound). A null value indicates negative infinity. You must specify at least one upper or lower bound.
            :param metric_interval_upper_bound: The upper bound for the difference between the alarm threshold and the CloudWatch metric. If the metric value is above the breach threshold, the upper bound is exclusive (the metric must be less than the threshold plus the upper bound). Otherwise, it is inclusive (the metric must be less than or equal to the threshold plus the upper bound). A null value indicates positive infinity. You must specify at least one upper or lower bound.
            :param scaling_adjustment: The amount by which to scale. The adjustment is based on the value that you specified in the ``AdjustmentType`` property (either an absolute number or a percentage). A positive value adds to the current capacity and a negative number subtracts from the current capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepadjustment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                step_adjustment_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.StepAdjustmentProperty(
                    metric_interval_lower_bound=123,
                    metric_interval_upper_bound=123,
                    scaling_adjustment=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__13c3e088c87d293dd039f98c21e91691f12147dc4d2aefb0fbe2a6761c28d30e)
                check_type(argname="argument metric_interval_lower_bound", value=metric_interval_lower_bound, expected_type=type_hints["metric_interval_lower_bound"])
                check_type(argname="argument metric_interval_upper_bound", value=metric_interval_upper_bound, expected_type=type_hints["metric_interval_upper_bound"])
                check_type(argname="argument scaling_adjustment", value=scaling_adjustment, expected_type=type_hints["scaling_adjustment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_interval_lower_bound is not None:
                self._values["metric_interval_lower_bound"] = metric_interval_lower_bound
            if metric_interval_upper_bound is not None:
                self._values["metric_interval_upper_bound"] = metric_interval_upper_bound
            if scaling_adjustment is not None:
                self._values["scaling_adjustment"] = scaling_adjustment

        @builtins.property
        def metric_interval_lower_bound(self) -> typing.Optional[jsii.Number]:
            '''The lower bound for the difference between the alarm threshold and the CloudWatch metric.

            If the metric value is above the breach threshold, the lower bound is inclusive (the metric must be greater than or equal to the threshold plus the lower bound). Otherwise, it is exclusive (the metric must be greater than the threshold plus the lower bound). A null value indicates negative infinity.

            You must specify at least one upper or lower bound.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepadjustment.html#cfn-applicationautoscaling-scalingpolicy-stepadjustment-metricintervallowerbound
            '''
            result = self._values.get("metric_interval_lower_bound")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def metric_interval_upper_bound(self) -> typing.Optional[jsii.Number]:
            '''The upper bound for the difference between the alarm threshold and the CloudWatch metric.

            If the metric value is above the breach threshold, the upper bound is exclusive (the metric must be less than the threshold plus the upper bound). Otherwise, it is inclusive (the metric must be less than or equal to the threshold plus the upper bound). A null value indicates positive infinity.

            You must specify at least one upper or lower bound.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepadjustment.html#cfn-applicationautoscaling-scalingpolicy-stepadjustment-metricintervalupperbound
            '''
            result = self._values.get("metric_interval_upper_bound")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scaling_adjustment(self) -> typing.Optional[jsii.Number]:
            '''The amount by which to scale.

            The adjustment is based on the value that you specified in the ``AdjustmentType`` property (either an absolute number or a percentage). A positive value adds to the current capacity and a negative number subtracts from the current capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepadjustment.html#cfn-applicationautoscaling-scalingpolicy-stepadjustment-scalingadjustment
            '''
            result = self._values.get("scaling_adjustment")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StepAdjustmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.StepScalingPolicyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "adjustment_type": "adjustmentType",
            "cooldown": "cooldown",
            "metric_aggregation_type": "metricAggregationType",
            "min_adjustment_magnitude": "minAdjustmentMagnitude",
            "step_adjustments": "stepAdjustments",
        },
    )
    class StepScalingPolicyConfigurationProperty:
        def __init__(
            self,
            *,
            adjustment_type: typing.Optional[builtins.str] = None,
            cooldown: typing.Optional[jsii.Number] = None,
            metric_aggregation_type: typing.Optional[builtins.str] = None,
            min_adjustment_magnitude: typing.Optional[jsii.Number] = None,
            step_adjustments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.StepAdjustmentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''``StepScalingPolicyConfiguration`` is a property of the `AWS::ApplicationAutoScaling::ScalingPolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html>`_ resource that specifies a step scaling policy configuration for Application Auto Scaling.

            For more information, see `Step scaling policies <https://docs.aws.amazon.com/autoscaling/application/userguide/application-auto-scaling-step-scaling-policies.html>`_ in the *Application Auto Scaling User Guide* .

            :param adjustment_type: Specifies whether the ``ScalingAdjustment`` value in the ``StepAdjustment`` property is an absolute number or a percentage of the current capacity.
            :param cooldown: The amount of time, in seconds, to wait for a previous scaling activity to take effect. If not specified, the default value is 300. For more information, see `Cooldown period <https://docs.aws.amazon.com/autoscaling/application/userguide/step-scaling-policy-overview.html#step-scaling-cooldown>`_ in the *Application Auto Scaling User Guide* .
            :param metric_aggregation_type: The aggregation type for the CloudWatch metrics. Valid values are ``Minimum`` , ``Maximum`` , and ``Average`` . If the aggregation type is null, the value is treated as ``Average`` .
            :param min_adjustment_magnitude: The minimum value to scale by when the adjustment type is ``PercentChangeInCapacity`` . For example, suppose that you create a step scaling policy to scale out an Amazon ECS service by 25 percent and you specify a ``MinAdjustmentMagnitude`` of 2. If the service has 4 tasks and the scaling policy is performed, 25 percent of 4 is 1. However, because you specified a ``MinAdjustmentMagnitude`` of 2, Application Auto Scaling scales out the service by 2 tasks.
            :param step_adjustments: A set of adjustments that enable you to scale based on the size of the alarm breach. At least one step adjustment is required if you are adding a new step scaling policy configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                step_scaling_policy_configuration_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.StepScalingPolicyConfigurationProperty(
                    adjustment_type="adjustmentType",
                    cooldown=123,
                    metric_aggregation_type="metricAggregationType",
                    min_adjustment_magnitude=123,
                    step_adjustments=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.StepAdjustmentProperty(
                        metric_interval_lower_bound=123,
                        metric_interval_upper_bound=123,
                        scaling_adjustment=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__70ee881c981103a974efd4fd77fd131e564b7a2a5720000049f207f72d59f46b)
                check_type(argname="argument adjustment_type", value=adjustment_type, expected_type=type_hints["adjustment_type"])
                check_type(argname="argument cooldown", value=cooldown, expected_type=type_hints["cooldown"])
                check_type(argname="argument metric_aggregation_type", value=metric_aggregation_type, expected_type=type_hints["metric_aggregation_type"])
                check_type(argname="argument min_adjustment_magnitude", value=min_adjustment_magnitude, expected_type=type_hints["min_adjustment_magnitude"])
                check_type(argname="argument step_adjustments", value=step_adjustments, expected_type=type_hints["step_adjustments"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if adjustment_type is not None:
                self._values["adjustment_type"] = adjustment_type
            if cooldown is not None:
                self._values["cooldown"] = cooldown
            if metric_aggregation_type is not None:
                self._values["metric_aggregation_type"] = metric_aggregation_type
            if min_adjustment_magnitude is not None:
                self._values["min_adjustment_magnitude"] = min_adjustment_magnitude
            if step_adjustments is not None:
                self._values["step_adjustments"] = step_adjustments

        @builtins.property
        def adjustment_type(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the ``ScalingAdjustment`` value in the ``StepAdjustment`` property is an absolute number or a percentage of the current capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-adjustmenttype
            '''
            result = self._values.get("adjustment_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cooldown(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, to wait for a previous scaling activity to take effect.

            If not specified, the default value is 300. For more information, see `Cooldown period <https://docs.aws.amazon.com/autoscaling/application/userguide/step-scaling-policy-overview.html#step-scaling-cooldown>`_ in the *Application Auto Scaling User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-cooldown
            '''
            result = self._values.get("cooldown")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def metric_aggregation_type(self) -> typing.Optional[builtins.str]:
            '''The aggregation type for the CloudWatch metrics.

            Valid values are ``Minimum`` , ``Maximum`` , and ``Average`` . If the aggregation type is null, the value is treated as ``Average`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-metricaggregationtype
            '''
            result = self._values.get("metric_aggregation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
            '''The minimum value to scale by when the adjustment type is ``PercentChangeInCapacity`` .

            For example, suppose that you create a step scaling policy to scale out an Amazon ECS service by 25 percent and you specify a ``MinAdjustmentMagnitude`` of 2. If the service has 4 tasks and the scaling policy is performed, 25 percent of 4 is 1. However, because you specified a ``MinAdjustmentMagnitude`` of 2, Application Auto Scaling scales out the service by 2 tasks.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-minadjustmentmagnitude
            '''
            result = self._values.get("min_adjustment_magnitude")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def step_adjustments(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.StepAdjustmentProperty"]]]]:
            '''A set of adjustments that enable you to scale based on the size of the alarm breach.

            At least one step adjustment is required if you are adding a new step scaling policy configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustments
            '''
            result = self._values.get("step_adjustments")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.StepAdjustmentProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StepScalingPolicyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "expression": "expression",
            "id": "id",
            "label": "label",
            "metric_stat": "metricStat",
            "return_data": "returnData",
        },
    )
    class TargetTrackingMetricDataQueryProperty:
        def __init__(
            self,
            *,
            expression: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            label: typing.Optional[builtins.str] = None,
            metric_stat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            return_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The metric data to return.

            Also defines whether this call is returning data for one metric only, or whether it is performing a math expression on the values of returned metric statistics to create a new time series. A time series is a series of data points, each of which is associated with a timestamp.

            You can call for a single metric or perform math expressions on multiple metrics. Any expressions used in a metric specification must eventually return a single time series.

            For more information and examples, see `Create a target tracking scaling policy for Application Auto Scaling using metric math <https://docs.aws.amazon.com/autoscaling/application/userguide/application-auto-scaling-target-tracking-metric-math.html>`_ in the *Application Auto Scaling User Guide* .

            ``TargetTrackingMetricDataQuery`` is a property of the `AWS::ApplicationAutoScaling::ScalingPolicy CustomizedMetricSpecification <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html>`_ property type.

            :param expression: The math expression to perform on the returned data, if this object is performing a math expression. This expression can use the ``Id`` of the other metrics to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions. Conditional: Within each ``TargetTrackingMetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.
            :param id: A short name that identifies the object's results in the response. This name must be unique among all ``MetricDataQuery`` objects specified for a single scaling policy. If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscores. The first character must be a lowercase letter.
            :param label: A human-readable label for this metric or expression. This is especially useful if this is a math expression, so that you know what the value represents.
            :param metric_stat: Information about the metric data to return. Conditional: Within each ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.
            :param return_data: Indicates whether to return the timestamps and raw data values of this metric. If you use any math expressions, specify ``true`` for this value for only the final math expression that the metric specification is based on. You must specify ``false`` for ``ReturnData`` for all the other metrics and expressions used in the metric specification. If you are only retrieving metrics and not performing any math expressions, do not specify anything for ``ReturnData`` . This sets it to its default ( ``true`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricdataquery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                target_tracking_metric_data_query_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty(
                    expression="expression",
                    id="id",
                    label="label",
                    metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty(
                        metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricProperty(
                            dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDimensionProperty(
                                name="name",
                                value="value"
                            )],
                            metric_name="metricName",
                            namespace="namespace"
                        ),
                        stat="stat",
                        unit="unit"
                    ),
                    return_data=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3292c6b2f9747b9b82ab07a84997e26c32630618dfc25c83ec4f49b658db9f03)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument label", value=label, expected_type=type_hints["label"])
                check_type(argname="argument metric_stat", value=metric_stat, expected_type=type_hints["metric_stat"])
                check_type(argname="argument return_data", value=return_data, expected_type=type_hints["return_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression
            if id is not None:
                self._values["id"] = id
            if label is not None:
                self._values["label"] = label
            if metric_stat is not None:
                self._values["metric_stat"] = metric_stat
            if return_data is not None:
                self._values["return_data"] = return_data

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The math expression to perform on the returned data, if this object is performing a math expression.

            This expression can use the ``Id`` of the other metrics to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions.

            Conditional: Within each ``TargetTrackingMetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricdataquery.html#cfn-applicationautoscaling-scalingpolicy-targettrackingmetricdataquery-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A short name that identifies the object's results in the response.

            This name must be unique among all ``MetricDataQuery`` objects specified for a single scaling policy. If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscores. The first character must be a lowercase letter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricdataquery.html#cfn-applicationautoscaling-scalingpolicy-targettrackingmetricdataquery-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def label(self) -> typing.Optional[builtins.str]:
            '''A human-readable label for this metric or expression.

            This is especially useful if this is a math expression, so that you know what the value represents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricdataquery.html#cfn-applicationautoscaling-scalingpolicy-targettrackingmetricdataquery-label
            '''
            result = self._values.get("label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_stat(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty"]]:
            '''Information about the metric data to return.

            Conditional: Within each ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricdataquery.html#cfn-applicationautoscaling-scalingpolicy-targettrackingmetricdataquery-metricstat
            '''
            result = self._values.get("metric_stat")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty"]], result)

        @builtins.property
        def return_data(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to return the timestamps and raw data values of this metric.

            If you use any math expressions, specify ``true`` for this value for only the final math expression that the metric specification is based on. You must specify ``false`` for ``ReturnData`` for all the other metrics and expressions used in the metric specification.

            If you are only retrieving metrics and not performing any math expressions, do not specify anything for ``ReturnData`` . This sets it to its default ( ``true`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricdataquery.html#cfn-applicationautoscaling-scalingpolicy-targettrackingmetricdataquery-returndata
            '''
            result = self._values.get("return_data")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingMetricDataQueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class TargetTrackingMetricDimensionProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``TargetTrackingMetricDimension`` specifies a name/value pair that is part of the identity of a CloudWatch metric for the ``Dimensions`` property of the `AWS::ApplicationAutoScaling::ScalingPolicy TargetTrackingMetric <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetric.html>`_ property type. Duplicate dimensions are not allowed.

            :param name: The name of the dimension.
            :param value: The value of the dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                target_tracking_metric_dimension_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDimensionProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89aa8ff507ee7374abf5c3c03fc679e3225d204a4ee477deca84d55e1377bf06)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricdimension.html#cfn-applicationautoscaling-scalingpolicy-targettrackingmetricdimension-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricdimension.html#cfn-applicationautoscaling-scalingpolicy-targettrackingmetricdimension-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingMetricDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "metric_name": "metricName",
            "namespace": "namespace",
        },
    )
    class TargetTrackingMetricProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.TargetTrackingMetricDimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metric_name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a specific metric for a target tracking scaling policy for Application Auto Scaling.

            Metric is a property of the `AWS::ApplicationAutoScaling::ScalingPolicy TargetTrackingMetricStat <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricstat.html>`_ property type.

            :param dimensions: The dimensions for the metric. For the list of available dimensions, see the AWS documentation available from the table in `AWS services that publish CloudWatch metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_ in the *Amazon CloudWatch User Guide* . Conditional: If you published your metric with dimensions, you must specify the same dimensions in your scaling policy.
            :param metric_name: The name of the metric.
            :param namespace: The namespace of the metric. For more information, see the table in `AWS services that publish CloudWatch metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_ in the *Amazon CloudWatch User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                target_tracking_metric_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricProperty(
                    dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42f64bcd95eba6e7fa8732f1b4cb7d5f4b231ffc95e53e126d5454dd72df11e6)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingMetricDimensionProperty"]]]]:
            '''The dimensions for the metric.

            For the list of available dimensions, see the AWS documentation available from the table in `AWS services that publish CloudWatch metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_ in the *Amazon CloudWatch User Guide* .

            Conditional: If you published your metric with dimensions, you must specify the same dimensions in your scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetric.html#cfn-applicationautoscaling-scalingpolicy-targettrackingmetric-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingMetricDimensionProperty"]]]], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetric.html#cfn-applicationautoscaling-scalingpolicy-targettrackingmetric-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the metric.

            For more information, see the table in `AWS services that publish CloudWatch metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_ in the *Amazon CloudWatch User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetric.html#cfn-applicationautoscaling-scalingpolicy-targettrackingmetric-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty",
        jsii_struct_bases=[],
        name_mapping={"metric": "metric", "stat": "stat", "unit": "unit"},
    )
    class TargetTrackingMetricStatProperty:
        def __init__(
            self,
            *,
            metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.TargetTrackingMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stat: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure defines the CloudWatch metric to return, along with the statistic and unit.

            ``TargetTrackingMetricStat`` is a property of the `AWS::ApplicationAutoScaling::ScalingPolicy TargetTrackingMetricDataQuery <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricdataquery.html>`_ property type.

            For more information about the CloudWatch terminology below, see `Amazon CloudWatch concepts <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html>`_ in the *Amazon CloudWatch User Guide* .

            :param metric: The CloudWatch metric to return, including the metric name, namespace, and dimensions. To get the exact metric name, namespace, and dimensions, inspect the `Metric <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_Metric.html>`_ object that is returned by a call to `ListMetrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_ListMetrics.html>`_ .
            :param stat: The statistic to return. It can include any CloudWatch statistic or extended statistic. For a list of valid values, see the table in `Statistics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic>`_ in the *Amazon CloudWatch User Guide* . The most commonly used metric for scaling is ``Average`` .
            :param unit: The unit to use for the returned data points. For a complete list of the units that CloudWatch supports, see the `MetricDatum <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html>`_ data type in the *Amazon CloudWatch API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricstat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                target_tracking_metric_stat_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty(
                    metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricProperty(
                        dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDimensionProperty(
                            name="name",
                            value="value"
                        )],
                        metric_name="metricName",
                        namespace="namespace"
                    ),
                    stat="stat",
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__28f55a7beb9f4de36e94cdbd87609ebd3b1afa7a7d6c8a2be10bbf73ce15bfd8)
                check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
                check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric is not None:
                self._values["metric"] = metric
            if stat is not None:
                self._values["stat"] = stat
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def metric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingMetricProperty"]]:
            '''The CloudWatch metric to return, including the metric name, namespace, and dimensions.

            To get the exact metric name, namespace, and dimensions, inspect the `Metric <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_Metric.html>`_ object that is returned by a call to `ListMetrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_ListMetrics.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricstat.html#cfn-applicationautoscaling-scalingpolicy-targettrackingmetricstat-metric
            '''
            result = self._values.get("metric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingMetricProperty"]], result)

        @builtins.property
        def stat(self) -> typing.Optional[builtins.str]:
            '''The statistic to return.

            It can include any CloudWatch statistic or extended statistic. For a list of valid values, see the table in `Statistics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic>`_ in the *Amazon CloudWatch User Guide* .

            The most commonly used metric for scaling is ``Average`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricstat.html#cfn-applicationautoscaling-scalingpolicy-targettrackingmetricstat-stat
            '''
            result = self._values.get("stat")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit to use for the returned data points.

            For a complete list of the units that CloudWatch supports, see the `MetricDatum <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html>`_ data type in the *Amazon CloudWatch API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingmetricstat.html#cfn-applicationautoscaling-scalingpolicy-targettrackingmetricstat-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingMetricStatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationautoscaling.mixins.CfnScalingPolicyPropsMixin.TargetTrackingScalingPolicyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customized_metric_specification": "customizedMetricSpecification",
            "disable_scale_in": "disableScaleIn",
            "predefined_metric_specification": "predefinedMetricSpecification",
            "scale_in_cooldown": "scaleInCooldown",
            "scale_out_cooldown": "scaleOutCooldown",
            "target_value": "targetValue",
        },
    )
    class TargetTrackingScalingPolicyConfigurationProperty:
        def __init__(
            self,
            *,
            customized_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            disable_scale_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            predefined_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            scale_in_cooldown: typing.Optional[jsii.Number] = None,
            scale_out_cooldown: typing.Optional[jsii.Number] = None,
            target_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``TargetTrackingScalingPolicyConfiguration`` is a property of the `AWS::ApplicationAutoScaling::ScalingPolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html>`_ resource that specifies a target tracking scaling policy configuration for Application Auto Scaling. Use a target tracking scaling policy to adjust the capacity of the specified scalable target in response to actual workloads, so that resource utilization remains at or near the target utilization value.

            For more information, see `Target tracking scaling policies <https://docs.aws.amazon.com/autoscaling/application/userguide/application-auto-scaling-target-tracking.html>`_ in the *Application Auto Scaling User Guide* .

            :param customized_metric_specification: A customized metric. You can specify either a predefined metric or a customized metric.
            :param disable_scale_in: Indicates whether scale in by the target tracking scaling policy is disabled. If the value is ``true`` , scale in is disabled and the target tracking scaling policy won't remove capacity from the scalable target. Otherwise, scale in is enabled and the target tracking scaling policy can remove capacity from the scalable target. The default value is ``false`` .
            :param predefined_metric_specification: A predefined metric. You can specify either a predefined metric or a customized metric.
            :param scale_in_cooldown: The amount of time, in seconds, after a scale-in activity completes before another scale-in activity can start. For more information and for default values, see `Define cooldown periods <https://docs.aws.amazon.com/autoscaling/application/userguide/target-tracking-scaling-policy-overview.html#target-tracking-cooldown>`_ in the *Application Auto Scaling User Guide* .
            :param scale_out_cooldown: The amount of time, in seconds, to wait for a previous scale-out activity to take effect. For more information and for default values, see `Define cooldown periods <https://docs.aws.amazon.com/autoscaling/application/userguide/target-tracking-scaling-policy-overview.html#target-tracking-cooldown>`_ in the *Application Auto Scaling User Guide* .
            :param target_value: The target value for the metric. Although this property accepts numbers of type Double, it won't accept values that are either too small or too large. Values must be in the range of -2^360 to 2^360. The value must be a valid number based on the choice of metric. For example, if the metric is CPU utilization, then the target value is a percent value that represents how much of the CPU can be used before scaling out.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationautoscaling import mixins as applicationautoscaling_mixins
                
                target_tracking_scaling_policy_configuration_property = applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingScalingPolicyConfigurationProperty(
                    customized_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty(
                        dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                            name="name",
                            value="value"
                        )],
                        metric_name="metricName",
                        metrics=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty(
                                metric=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricProperty(
                                    dimensions=[applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )],
                        namespace="namespace",
                        statistic="statistic",
                        unit="unit"
                    ),
                    disable_scale_in=False,
                    predefined_metric_specification=applicationautoscaling_mixins.CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    scale_in_cooldown=123,
                    scale_out_cooldown=123,
                    target_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77d705004db594d44fd193ab0a83e7a54ee48285cf56975b6dd3e01485e4da21)
                check_type(argname="argument customized_metric_specification", value=customized_metric_specification, expected_type=type_hints["customized_metric_specification"])
                check_type(argname="argument disable_scale_in", value=disable_scale_in, expected_type=type_hints["disable_scale_in"])
                check_type(argname="argument predefined_metric_specification", value=predefined_metric_specification, expected_type=type_hints["predefined_metric_specification"])
                check_type(argname="argument scale_in_cooldown", value=scale_in_cooldown, expected_type=type_hints["scale_in_cooldown"])
                check_type(argname="argument scale_out_cooldown", value=scale_out_cooldown, expected_type=type_hints["scale_out_cooldown"])
                check_type(argname="argument target_value", value=target_value, expected_type=type_hints["target_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customized_metric_specification is not None:
                self._values["customized_metric_specification"] = customized_metric_specification
            if disable_scale_in is not None:
                self._values["disable_scale_in"] = disable_scale_in
            if predefined_metric_specification is not None:
                self._values["predefined_metric_specification"] = predefined_metric_specification
            if scale_in_cooldown is not None:
                self._values["scale_in_cooldown"] = scale_in_cooldown
            if scale_out_cooldown is not None:
                self._values["scale_out_cooldown"] = scale_out_cooldown
            if target_value is not None:
                self._values["target_value"] = target_value

        @builtins.property
        def customized_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty"]]:
            '''A customized metric.

            You can specify either a predefined metric or a customized metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-customizedmetricspecification
            '''
            result = self._values.get("customized_metric_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty"]], result)

        @builtins.property
        def disable_scale_in(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether scale in by the target tracking scaling policy is disabled.

            If the value is ``true`` , scale in is disabled and the target tracking scaling policy won't remove capacity from the scalable target. Otherwise, scale in is enabled and the target tracking scaling policy can remove capacity from the scalable target. The default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-disablescalein
            '''
            result = self._values.get("disable_scale_in")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def predefined_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty"]]:
            '''A predefined metric.

            You can specify either a predefined metric or a customized metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-predefinedmetricspecification
            '''
            result = self._values.get("predefined_metric_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty"]], result)

        @builtins.property
        def scale_in_cooldown(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, after a scale-in activity completes before another scale-in activity can start.

            For more information and for default values, see `Define cooldown periods <https://docs.aws.amazon.com/autoscaling/application/userguide/target-tracking-scaling-policy-overview.html#target-tracking-cooldown>`_ in the *Application Auto Scaling User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-scaleincooldown
            '''
            result = self._values.get("scale_in_cooldown")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scale_out_cooldown(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, to wait for a previous scale-out activity to take effect.

            For more information and for default values, see `Define cooldown periods <https://docs.aws.amazon.com/autoscaling/application/userguide/target-tracking-scaling-policy-overview.html#target-tracking-cooldown>`_ in the *Application Auto Scaling User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-scaleoutcooldown
            '''
            result = self._values.get("scale_out_cooldown")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def target_value(self) -> typing.Optional[jsii.Number]:
            '''The target value for the metric.

            Although this property accepts numbers of type Double, it won't accept values that are either too small or too large. Values must be in the range of -2^360 to 2^360. The value must be a valid number based on the choice of metric. For example, if the metric is CPU utilization, then the target value is a percent value that represents how much of the CPU can be used before scaling out.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-targetvalue
            '''
            result = self._values.get("target_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingScalingPolicyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnScalableTargetMixinProps",
    "CfnScalableTargetPropsMixin",
    "CfnScalingPolicyMixinProps",
    "CfnScalingPolicyPropsMixin",
]

publication.publish()

def _typecheckingstub__d746e165b1787f1a21596bb9cfffd2fc4be923c05fc7ef2091b9f08d12792fd3(
    *,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
    resource_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    scalable_dimension: typing.Optional[builtins.str] = None,
    scheduled_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalableTargetPropsMixin.ScheduledActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    service_namespace: typing.Optional[builtins.str] = None,
    suspended_state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalableTargetPropsMixin.SuspendedStateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f085b5f1c60e69e9c1d91bf3507ce41fe0062eded98bf81e88918be39f8f73(
    props: typing.Union[CfnScalableTargetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71090bdc436b331d4568c9b8cade7e5dd4daef3a393b273a8990c7f9ff667225(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda8098b784e0402e60ddb0e2a21cbacd69a18f21ef7980a1929c53c43898aa4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e7cac209d2bec1b6d64365f4efcfdca02f0eaf5277d690770d24c9da4d5260(
    *,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e92abc186e22f43180acb28d793193ba0a7b128da992695e2899e60b6fb1acd(
    *,
    end_time: typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]] = None,
    scalable_target_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalableTargetPropsMixin.ScalableTargetActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schedule: typing.Optional[builtins.str] = None,
    scheduled_action_name: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdbde4a25286dd05c8c77ebd67e7334a6d3609c97fdfb5a4e49d1fd7bda2aed1(
    *,
    dynamic_scaling_in_suspended: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    dynamic_scaling_out_suspended: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    scheduled_scaling_suspended: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c34e67301ee8d0c479a05f580c20b4f4e18061059c69e51ee6f199c21cdc629(
    *,
    policy_name: typing.Optional[builtins.str] = None,
    policy_type: typing.Optional[builtins.str] = None,
    predictive_scaling_policy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingPolicyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_id: typing.Optional[builtins.str] = None,
    scalable_dimension: typing.Optional[builtins.str] = None,
    scaling_target_id: typing.Optional[builtins.str] = None,
    service_namespace: typing.Optional[builtins.str] = None,
    step_scaling_policy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.StepScalingPolicyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_tracking_scaling_policy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.TargetTrackingScalingPolicyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__932aaf740a6a1435196f066ae3dc479dbca49da6054590006760ad6c7005c62c(
    props: typing.Union[CfnScalingPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a954b3da6b57ef86b01e364f80d119cfdc1cb74c7f16c8483c476a56cb483fe(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d511615d56de3a2964111baad16cdc5f74f428db935868d03b404935e4f358b6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8afbcda4ad27d0c22ee099b805507b12bad062007f5bd7fe823f35e366d3de62(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.MetricDimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    namespace: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056aa8eb80fa82904b9a738d22b8ebe5a4ac45679ffe2856ae3a05fd18b15016(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28b44359760e1302f08f5faf8ce5bd7c7a656bd34e0fe26e2f2d769daa5acb2(
    *,
    predefined_metric_type: typing.Optional[builtins.str] = None,
    resource_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ffb0cbdae4ecc2f4b18c128f667105620d63ab6d046ac33dbd1b808b535416e(
    *,
    metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c5eed138acad76bc740a8213cf25674ec254f07044f087d7eb9b7a53550e2f(
    *,
    metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6271c324ecb0ebb213294e8f41c66ce2fd0e3712e2f03c9b3b3443d150ba2fe(
    *,
    metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingMetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1cd71bcb12d8818c4ee665cf114e6a8d6e29210a0027ebcb92b87f2ba46c11c(
    *,
    expression: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
    metric_stat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingMetricStatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    return_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8070f3ef92724e83279e91c46e1b5ec49aa73a2bfd343011e8c14b6ce12767(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077664a9309c3b45e697083a49221eea10faf26443a91ad4375eed712f1c00f5(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingMetricDimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca18e6910fd0fb22f9473e97f8ecbc4133469cf68b559ac45f2de253b5f91ec0(
    *,
    customized_capacity_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    customized_load_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    customized_scaling_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    predefined_load_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    predefined_metric_pair_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    predefined_scaling_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b1e1d88fe137e14c136a4588d278a7ce6dafda668bb28817f35d9c67e6f918(
    *,
    metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stat: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2c9cbdbb3a30239956d38ec8ede1347fa63be40b777472eed09b5ff62a17d5(
    *,
    max_capacity_breach_behavior: typing.Optional[builtins.str] = None,
    max_capacity_buffer: typing.Optional[jsii.Number] = None,
    metric_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    mode: typing.Optional[builtins.str] = None,
    scheduling_buffer_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4936dca5996bf7399a5aea56aaf77d72e381e6ee1a4143d1d6a2704c6d3946f0(
    *,
    predefined_metric_type: typing.Optional[builtins.str] = None,
    resource_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ee91ad66f40f633663008094aa047fc5cdd0df7e3df7a2cd4c4012f62e5aa9(
    *,
    predefined_metric_type: typing.Optional[builtins.str] = None,
    resource_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b62b10c963a9b352358366ce63b5bcd51d54f43326baf1e2bc414ab0d458b3a(
    *,
    predefined_metric_type: typing.Optional[builtins.str] = None,
    resource_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c3e088c87d293dd039f98c21e91691f12147dc4d2aefb0fbe2a6761c28d30e(
    *,
    metric_interval_lower_bound: typing.Optional[jsii.Number] = None,
    metric_interval_upper_bound: typing.Optional[jsii.Number] = None,
    scaling_adjustment: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ee881c981103a974efd4fd77fd131e564b7a2a5720000049f207f72d59f46b(
    *,
    adjustment_type: typing.Optional[builtins.str] = None,
    cooldown: typing.Optional[jsii.Number] = None,
    metric_aggregation_type: typing.Optional[builtins.str] = None,
    min_adjustment_magnitude: typing.Optional[jsii.Number] = None,
    step_adjustments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.StepAdjustmentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3292c6b2f9747b9b82ab07a84997e26c32630618dfc25c83ec4f49b658db9f03(
    *,
    expression: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
    metric_stat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    return_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89aa8ff507ee7374abf5c3c03fc679e3225d204a4ee477deca84d55e1377bf06(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f64bcd95eba6e7fa8732f1b4cb7d5f4b231ffc95e53e126d5454dd72df11e6(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.TargetTrackingMetricDimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28f55a7beb9f4de36e94cdbd87609ebd3b1afa7a7d6c8a2be10bbf73ce15bfd8(
    *,
    metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.TargetTrackingMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stat: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d705004db594d44fd193ab0a83e7a54ee48285cf56975b6dd3e01485e4da21(
    *,
    customized_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    disable_scale_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    predefined_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scale_in_cooldown: typing.Optional[jsii.Number] = None,
    scale_out_cooldown: typing.Optional[jsii.Number] = None,
    target_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
