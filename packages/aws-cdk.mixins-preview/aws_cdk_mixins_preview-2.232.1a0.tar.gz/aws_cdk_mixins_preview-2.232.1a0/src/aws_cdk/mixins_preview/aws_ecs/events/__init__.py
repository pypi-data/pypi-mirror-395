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
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.interfaces.aws_ecs as _aws_cdk_interfaces_aws_ecs_ceddda9d


class ClusterEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents",
):
    '''(experimental) EventBridge event patterns for Cluster.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
        from aws_cdk.interfaces import aws_ecs as interfaces_ecs
        
        # cluster_ref: interfaces_ecs.IClusterRef
        
        cluster_events = ecs_events.ClusterEvents.from_cluster(cluster_ref)
    '''

    @jsii.member(jsii_name="fromCluster")
    @builtins.classmethod
    def from_cluster(
        cls,
        cluster_ref: _aws_cdk_interfaces_aws_ecs_ceddda9d.IClusterRef,
    ) -> "ClusterEvents":
        '''(experimental) Create ClusterEvents from a Cluster reference.

        :param cluster_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b042faef39d2f05c64c4c0185563eb20eb8a3fc259e9cf791303358aa13d9ec)
            check_type(argname="argument cluster_ref", value=cluster_ref, expected_type=type_hints["cluster_ref"])
        return typing.cast("ClusterEvents", jsii.sinvoke(cls, "fromCluster", [cluster_ref]))

    @jsii.member(jsii_name="awsAPICallViaCloudTrailPattern")
    def aws_api_call_via_cloud_trail_pattern(
        self,
        *,
        aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_parameters: typing.Optional[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.RequestParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        response_elements: typing.Optional[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElements", typing.Dict[builtins.str, typing.Any]]] = None,
        source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_identity: typing.Optional[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Cluster AWS API Call via CloudTrail.

        :param aws_region: (experimental) awsRegion property. Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_id: (experimental) eventID property. Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param event_name: (experimental) eventName property. Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_source: (experimental) eventSource property. Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_time: (experimental) eventTime property. Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_version: (experimental) eventVersion property. Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) requestID property. Specify an array of string values to match this event if the actual value of requestID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_parameters: (experimental) requestParameters property. Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param response_elements: (experimental) responseElements property. Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_ip_address: (experimental) sourceIPAddress property. Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param user_identity: (experimental) userIdentity property. Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ClusterEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
            aws_region=aws_region,
            event_id=event_id,
            event_metadata=event_metadata,
            event_name=event_name,
            event_source=event_source,
            event_time=event_time,
            event_type=event_type,
            event_version=event_version,
            request_id=request_id,
            request_parameters=request_parameters,
            response_elements=response_elements,
            source_ip_address=source_ip_address,
            user_agent=user_agent,
            user_identity=user_identity,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "awsAPICallViaCloudTrailPattern", [options]))

    @jsii.member(jsii_name="eCSContainerInstanceStateChangePattern")
    def e_cs_container_instance_state_change_pattern(
        self,
        *,
        account_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        agent_connected: typing.Optional[typing.Sequence[builtins.str]] = None,
        agent_update_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        attachments: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSContainerInstanceStateChange.AttachmentDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
        attributes: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSContainerInstanceStateChange.AttributesDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
        cluster_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        pending_tasks_count: typing.Optional[typing.Sequence[builtins.str]] = None,
        registered_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        registered_resources: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSContainerInstanceStateChange.ResourceDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
        remaining_resources: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSContainerInstanceStateChange.ResourceDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
        running_tasks_count: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_reason: typing.Optional[typing.Sequence[builtins.str]] = None,
        updated_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
        version_info: typing.Optional[typing.Union["ClusterEvents.ECSContainerInstanceStateChange.VersionInfo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Cluster ECS Container Instance State Change.

        :param account_type: (experimental) accountType property. Specify an array of string values to match this event if the actual value of accountType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param agent_connected: (experimental) agentConnected property. Specify an array of string values to match this event if the actual value of agentConnected is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param agent_update_status: (experimental) agentUpdateStatus property. Specify an array of string values to match this event if the actual value of agentUpdateStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param attachments: (experimental) attachments property. Specify an array of string values to match this event if the actual value of attachments is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param attributes: (experimental) attributes property. Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param cluster_arn: (experimental) clusterArn property. Specify an array of string values to match this event if the actual value of clusterArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Cluster reference
        :param container_instance_arn: (experimental) containerInstanceArn property. Specify an array of string values to match this event if the actual value of containerInstanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param ec2_instance_id: (experimental) ec2InstanceId property. Specify an array of string values to match this event if the actual value of ec2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param pending_tasks_count: (experimental) pendingTasksCount property. Specify an array of string values to match this event if the actual value of pendingTasksCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param registered_at: (experimental) registeredAt property. Specify an array of string values to match this event if the actual value of registeredAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param registered_resources: (experimental) registeredResources property. Specify an array of string values to match this event if the actual value of registeredResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param remaining_resources: (experimental) remainingResources property. Specify an array of string values to match this event if the actual value of remainingResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param running_tasks_count: (experimental) runningTasksCount property. Specify an array of string values to match this event if the actual value of runningTasksCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_reason: (experimental) statusReason property. Specify an array of string values to match this event if the actual value of statusReason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param updated_at: (experimental) updatedAt property. Specify an array of string values to match this event if the actual value of updatedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version_info: (experimental) versionInfo property. Specify an array of string values to match this event if the actual value of versionInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ClusterEvents.ECSContainerInstanceStateChange.ECSContainerInstanceStateChangeProps(
            account_type=account_type,
            agent_connected=agent_connected,
            agent_update_status=agent_update_status,
            attachments=attachments,
            attributes=attributes,
            cluster_arn=cluster_arn,
            container_instance_arn=container_instance_arn,
            ec2_instance_id=ec2_instance_id,
            event_metadata=event_metadata,
            pending_tasks_count=pending_tasks_count,
            registered_at=registered_at,
            registered_resources=registered_resources,
            remaining_resources=remaining_resources,
            running_tasks_count=running_tasks_count,
            status=status,
            status_reason=status_reason,
            updated_at=updated_at,
            version=version,
            version_info=version_info,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eCSContainerInstanceStateChangePattern", [options]))

    @jsii.member(jsii_name="eCSServiceActionPattern")
    def e_cs_service_action_pattern(
        self,
        *,
        capacity_provider_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        cluster_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_instance_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_port: typing.Optional[typing.Sequence[builtins.str]] = None,
        created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        desired_count: typing.Optional[typing.Sequence[builtins.str]] = None,
        ec2_instance_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        reason: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_registry_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        targets: typing.Optional[typing.Sequence[builtins.str]] = None,
        task_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        task_set_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Cluster ECS Service Action.

        :param capacity_provider_arns: (experimental) capacityProviderArns property. Specify an array of string values to match this event if the actual value of capacityProviderArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param cluster_arn: (experimental) clusterArn property. Specify an array of string values to match this event if the actual value of clusterArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Cluster reference
        :param container_instance_arns: (experimental) containerInstanceArns property. Specify an array of string values to match this event if the actual value of containerInstanceArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param container_port: (experimental) containerPort property. Specify an array of string values to match this event if the actual value of containerPort is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param created_at: (experimental) createdAt property. Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param desired_count: (experimental) desiredCount property. Specify an array of string values to match this event if the actual value of desiredCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param ec2_instance_ids: (experimental) ec2InstanceIds property. Specify an array of string values to match this event if the actual value of ec2InstanceIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param event_name: (experimental) eventName property. Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param reason: (experimental) reason property. Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param service_registry_arns: (experimental) serviceRegistryArns property. Specify an array of string values to match this event if the actual value of serviceRegistryArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param target_group_arns: (experimental) targetGroupArns property. Specify an array of string values to match this event if the actual value of targetGroupArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param targets: (experimental) targets property. Specify an array of string values to match this event if the actual value of targets is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param task_arns: (experimental) taskArns property. Specify an array of string values to match this event if the actual value of taskArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param task_set_arns: (experimental) taskSetArns property. Specify an array of string values to match this event if the actual value of taskSetArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ClusterEvents.ECSServiceAction.ECSServiceActionProps(
            capacity_provider_arns=capacity_provider_arns,
            cluster_arn=cluster_arn,
            container_instance_arns=container_instance_arns,
            container_port=container_port,
            created_at=created_at,
            desired_count=desired_count,
            ec2_instance_ids=ec2_instance_ids,
            event_metadata=event_metadata,
            event_name=event_name,
            event_type=event_type,
            reason=reason,
            service_registry_arns=service_registry_arns,
            target_group_arns=target_group_arns,
            targets=targets,
            task_arns=task_arns,
            task_set_arns=task_set_arns,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eCSServiceActionPattern", [options]))

    @jsii.member(jsii_name="eCSTaskStateChangePattern")
    def e_cs_task_state_change_pattern(
        self,
        *,
        attachments: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSTaskStateChange.AttachmentDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
        attributes: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSTaskStateChange.AttributesDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
        availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
        cluster_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        connectivity: typing.Optional[typing.Sequence[builtins.str]] = None,
        connectivity_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        containers: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSTaskStateChange.ContainerDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
        cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
        created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        desired_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        execution_stopped_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        group: typing.Optional[typing.Sequence[builtins.str]] = None,
        last_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        launch_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory: typing.Optional[typing.Sequence[builtins.str]] = None,
        overrides: typing.Optional[typing.Union["ClusterEvents.ECSTaskStateChange.Overrides", typing.Dict[builtins.str, typing.Any]]] = None,
        platform_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        pull_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        pull_stopped_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        started_by: typing.Optional[typing.Sequence[builtins.str]] = None,
        stop_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        stopped_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        stopped_reason: typing.Optional[typing.Sequence[builtins.str]] = None,
        stopping_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        task_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        task_definition_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        updated_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Cluster ECS Task State Change.

        :param attachments: (experimental) attachments property. Specify an array of string values to match this event if the actual value of attachments is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param attributes: (experimental) attributes property. Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param availability_zone: (experimental) availabilityZone property. Specify an array of string values to match this event if the actual value of availabilityZone is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param cluster_arn: (experimental) clusterArn property. Specify an array of string values to match this event if the actual value of clusterArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Cluster reference
        :param connectivity: (experimental) connectivity property. Specify an array of string values to match this event if the actual value of connectivity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param connectivity_at: (experimental) connectivityAt property. Specify an array of string values to match this event if the actual value of connectivityAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param container_instance_arn: (experimental) containerInstanceArn property. Specify an array of string values to match this event if the actual value of containerInstanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param containers: (experimental) containers property. Specify an array of string values to match this event if the actual value of containers is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param cpu: (experimental) cpu property. Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param created_at: (experimental) createdAt property. Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param desired_status: (experimental) desiredStatus property. Specify an array of string values to match this event if the actual value of desiredStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param execution_stopped_at: (experimental) executionStoppedAt property. Specify an array of string values to match this event if the actual value of executionStoppedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param group: (experimental) group property. Specify an array of string values to match this event if the actual value of group is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param last_status: (experimental) lastStatus property. Specify an array of string values to match this event if the actual value of lastStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param launch_type: (experimental) launchType property. Specify an array of string values to match this event if the actual value of launchType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param memory: (experimental) memory property. Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param overrides: (experimental) overrides property. Specify an array of string values to match this event if the actual value of overrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param platform_version: (experimental) platformVersion property. Specify an array of string values to match this event if the actual value of platformVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param pull_started_at: (experimental) pullStartedAt property. Specify an array of string values to match this event if the actual value of pullStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param pull_stopped_at: (experimental) pullStoppedAt property. Specify an array of string values to match this event if the actual value of pullStoppedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param started_at: (experimental) startedAt property. Specify an array of string values to match this event if the actual value of startedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param started_by: (experimental) startedBy property. Specify an array of string values to match this event if the actual value of startedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param stop_code: (experimental) stopCode property. Specify an array of string values to match this event if the actual value of stopCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param stopped_at: (experimental) stoppedAt property. Specify an array of string values to match this event if the actual value of stoppedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param stopped_reason: (experimental) stoppedReason property. Specify an array of string values to match this event if the actual value of stoppedReason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param stopping_at: (experimental) stoppingAt property. Specify an array of string values to match this event if the actual value of stoppingAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param task_arn: (experimental) taskArn property. Specify an array of string values to match this event if the actual value of taskArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param task_definition_arn: (experimental) taskDefinitionArn property. Specify an array of string values to match this event if the actual value of taskDefinitionArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param updated_at: (experimental) updatedAt property. Specify an array of string values to match this event if the actual value of updatedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ClusterEvents.ECSTaskStateChange.ECSTaskStateChangeProps(
            attachments=attachments,
            attributes=attributes,
            availability_zone=availability_zone,
            cluster_arn=cluster_arn,
            connectivity=connectivity,
            connectivity_at=connectivity_at,
            container_instance_arn=container_instance_arn,
            containers=containers,
            cpu=cpu,
            created_at=created_at,
            desired_status=desired_status,
            event_metadata=event_metadata,
            execution_stopped_at=execution_stopped_at,
            group=group,
            last_status=last_status,
            launch_type=launch_type,
            memory=memory,
            overrides=overrides,
            platform_version=platform_version,
            pull_started_at=pull_started_at,
            pull_stopped_at=pull_stopped_at,
            started_at=started_at,
            started_by=started_by,
            stop_code=stop_code,
            stopped_at=stopped_at,
            stopped_reason=stopped_reason,
            stopping_at=stopping_at,
            task_arn=task_arn,
            task_definition_arn=task_definition_arn,
            updated_at=updated_at,
            version=version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eCSTaskStateChangePattern", [options]))

    class AWSAPICallViaCloudTrail(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail",
    ):
        '''(experimental) aws.ecs@AWSAPICallViaCloudTrail event types for Cluster.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
            
            a_wSAPICall_via_cloud_trail = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps",
            jsii_struct_bases=[],
            name_mapping={
                "aws_region": "awsRegion",
                "event_id": "eventId",
                "event_metadata": "eventMetadata",
                "event_name": "eventName",
                "event_source": "eventSource",
                "event_time": "eventTime",
                "event_type": "eventType",
                "event_version": "eventVersion",
                "request_id": "requestId",
                "request_parameters": "requestParameters",
                "response_elements": "responseElements",
                "source_ip_address": "sourceIpAddress",
                "user_agent": "userAgent",
                "user_identity": "userIdentity",
            },
        )
        class AWSAPICallViaCloudTrailProps:
            def __init__(
                self,
                *,
                aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_parameters: typing.Optional[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.RequestParameters", typing.Dict[builtins.str, typing.Any]]] = None,
                response_elements: typing.Optional[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElements", typing.Dict[builtins.str, typing.Any]]] = None,
                source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_identity: typing.Optional[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Cluster aws.ecs@AWSAPICallViaCloudTrail event.

                :param aws_region: (experimental) awsRegion property. Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_id: (experimental) eventID property. Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param event_name: (experimental) eventName property. Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_source: (experimental) eventSource property. Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_time: (experimental) eventTime property. Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_version: (experimental) eventVersion property. Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) requestID property. Specify an array of string values to match this event if the actual value of requestID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_parameters: (experimental) requestParameters property. Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param response_elements: (experimental) responseElements property. Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_ip_address: (experimental) sourceIPAddress property. Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_identity: (experimental) userIdentity property. Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    # environment: Any
                    # inference_accelerator_overrides: Any
                    # network_bindings: Any
                    # network_interfaces: Any
                    # resource_requirements: Any
                    # tags: Any
                    
                    a_wSAPICall_via_cloud_trail_props = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
                        aws_region=["awsRegion"],
                        event_id=["eventId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        event_name=["eventName"],
                        event_source=["eventSource"],
                        event_time=["eventTime"],
                        event_type=["eventType"],
                        event_version=["eventVersion"],
                        request_id=["requestId"],
                        request_parameters=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.RequestParameters(
                            cluster=["cluster"],
                            container_instance=["containerInstance"],
                            containers=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem1(
                                container_name=["containerName"],
                                exit_code=["exitCode"],
                                network_bindings=[network_bindings],
                                status=["status"]
                            )],
                            count=["count"],
                            enable_ecs_managed_tags=["enableEcsManagedTags"],
                            execution_stopped_at=["executionStoppedAt"],
                            launch_type=["launchType"],
                            network_configuration=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.NetworkConfiguration(
                                awsvpc_configuration=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.AwsvpcConfiguration(
                                    assign_public_ip=["assignPublicIp"],
                                    subnets=["subnets"]
                                )
                            ),
                            overrides=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides(
                                container_overrides=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.OverridesItem(
                                    command=["command"],
                                    cpu=["cpu"],
                                    environment=[environment],
                                    memory=["memory"],
                                    name=["name"],
                                    resource_requirements=[resource_requirements]
                                )]
                            ),
                            placement_constraints=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem(
                                expression=["expression"],
                                type=["type"]
                            )],
                            pull_started_at=["pullStartedAt"],
                            pull_stopped_at=["pullStoppedAt"],
                            reason=["reason"],
                            started_by=["startedBy"],
                            status=["status"],
                            task=["task"],
                            task_definition=["taskDefinition"]
                        ),
                        response_elements=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElements(
                            acknowledgment=["acknowledgment"],
                            endpoint=["endpoint"],
                            failures=["failures"],
                            tasks=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItem(
                                attachments=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem(
                                    details=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItemItem(
                                        name=["name"],
                                        value=["value"]
                                    )],
                                    id=["id"],
                                    status=["status"],
                                    type=["type"]
                                )],
                                cluster_arn=["clusterArn"],
                                container_instance_arn=["containerInstanceArn"],
                                containers=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem1(
                                    container_arn=["containerArn"],
                                    cpu=["cpu"],
                                    image=["image"],
                                    last_status=["lastStatus"],
                                    memory=["memory"],
                                    name=["name"],
                                    network_interfaces=[network_interfaces],
                                    task_arn=["taskArn"]
                                )],
                                cpu=["cpu"],
                                created_at=["createdAt"],
                                desired_status=["desiredStatus"],
                                group=["group"],
                                last_status=["lastStatus"],
                                launch_type=["launchType"],
                                memory=["memory"],
                                overrides=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides1(
                                    container_overrides=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides1Item(
                                        command=["command"],
                                        cpu=["cpu"],
                                        environment=[environment],
                                        memory=["memory"],
                                        name=["name"],
                                        resource_requirements=[resource_requirements]
                                    )],
                                    inference_accelerator_overrides=[inference_accelerator_overrides]
                                ),
                                platform_version=["platformVersion"],
                                started_by=["startedBy"],
                                tags=[tags],
                                task_arn=["taskArn"],
                                task_definition_arn=["taskDefinitionArn"],
                                version=["version"]
                            )],
                            telemetry_endpoint=["telemetryEndpoint"]
                        ),
                        source_ip_address=["sourceIpAddress"],
                        user_agent=["userAgent"],
                        user_identity=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.UserIdentity(
                            access_key_id=["accessKeyId"],
                            account_id=["accountId"],
                            arn=["arn"],
                            invoked_by=["invokedBy"],
                            principal_id=["principalId"],
                            session_context=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.SessionContext(
                                attributes=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Attributes(
                                    creation_date=["creationDate"],
                                    mfa_authenticated=["mfaAuthenticated"]
                                ),
                                session_issuer=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                                    account_id=["accountId"],
                                    arn=["arn"],
                                    principal_id=["principalId"],
                                    type=["type"],
                                    user_name=["userName"]
                                ),
                                web_id_federation_data=["webIdFederationData"]
                            ),
                            type=["type"]
                        )
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(request_parameters, dict):
                    request_parameters = ClusterEvents.AWSAPICallViaCloudTrail.RequestParameters(**request_parameters)
                if isinstance(response_elements, dict):
                    response_elements = ClusterEvents.AWSAPICallViaCloudTrail.ResponseElements(**response_elements)
                if isinstance(user_identity, dict):
                    user_identity = ClusterEvents.AWSAPICallViaCloudTrail.UserIdentity(**user_identity)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__2751f6a5b6ab4dca4d2635f8840c6c7bce541f228272026bab91df596c2e4c96)
                    check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                    check_type(argname="argument event_id", value=event_id, expected_type=type_hints["event_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
                    check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
                    check_type(argname="argument event_time", value=event_time, expected_type=type_hints["event_time"])
                    check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
                    check_type(argname="argument event_version", value=event_version, expected_type=type_hints["event_version"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument request_parameters", value=request_parameters, expected_type=type_hints["request_parameters"])
                    check_type(argname="argument response_elements", value=response_elements, expected_type=type_hints["response_elements"])
                    check_type(argname="argument source_ip_address", value=source_ip_address, expected_type=type_hints["source_ip_address"])
                    check_type(argname="argument user_agent", value=user_agent, expected_type=type_hints["user_agent"])
                    check_type(argname="argument user_identity", value=user_identity, expected_type=type_hints["user_identity"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if aws_region is not None:
                    self._values["aws_region"] = aws_region
                if event_id is not None:
                    self._values["event_id"] = event_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if event_name is not None:
                    self._values["event_name"] = event_name
                if event_source is not None:
                    self._values["event_source"] = event_source
                if event_time is not None:
                    self._values["event_time"] = event_time
                if event_type is not None:
                    self._values["event_type"] = event_type
                if event_version is not None:
                    self._values["event_version"] = event_version
                if request_id is not None:
                    self._values["request_id"] = request_id
                if request_parameters is not None:
                    self._values["request_parameters"] = request_parameters
                if response_elements is not None:
                    self._values["response_elements"] = response_elements
                if source_ip_address is not None:
                    self._values["source_ip_address"] = source_ip_address
                if user_agent is not None:
                    self._values["user_agent"] = user_agent
                if user_identity is not None:
                    self._values["user_identity"] = user_identity

            @builtins.property
            def aws_region(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) awsRegion property.

                Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("aws_region")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventID property.

                Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def event_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventName property.

                Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_source(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventSource property.

                Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_source")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventTime property.

                Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventType property.

                Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventVersion property.

                Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requestID property.

                Specify an array of string values to match this event if the actual value of requestID is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_parameters(
                self,
            ) -> typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.RequestParameters"]:
                '''(experimental) requestParameters property.

                Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_parameters")
                return typing.cast(typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.RequestParameters"], result)

            @builtins.property
            def response_elements(
                self,
            ) -> typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElements"]:
                '''(experimental) responseElements property.

                Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("response_elements")
                return typing.cast(typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElements"], result)

            @builtins.property
            def source_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceIPAddress property.

                Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_ip_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def user_agent(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) userAgent property.

                Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_agent")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def user_identity(
                self,
            ) -> typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.UserIdentity"]:
                '''(experimental) userIdentity property.

                Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_identity")
                return typing.cast(typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.UserIdentity"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AWSAPICallViaCloudTrailProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.Attributes",
            jsii_struct_bases=[],
            name_mapping={
                "creation_date": "creationDate",
                "mfa_authenticated": "mfaAuthenticated",
            },
        )
        class Attributes:
            def __init__(
                self,
                *,
                creation_date: typing.Optional[typing.Sequence[builtins.str]] = None,
                mfa_authenticated: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Attributes.

                :param creation_date: (experimental) creationDate property. Specify an array of string values to match this event if the actual value of creationDate is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mfa_authenticated: (experimental) mfaAuthenticated property. Specify an array of string values to match this event if the actual value of mfaAuthenticated is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    attributes = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Attributes(
                        creation_date=["creationDate"],
                        mfa_authenticated=["mfaAuthenticated"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__774f462593573cfb62d2ca825924225cf0cf5ef785d9958f95160790a69265a5)
                    check_type(argname="argument creation_date", value=creation_date, expected_type=type_hints["creation_date"])
                    check_type(argname="argument mfa_authenticated", value=mfa_authenticated, expected_type=type_hints["mfa_authenticated"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if creation_date is not None:
                    self._values["creation_date"] = creation_date
                if mfa_authenticated is not None:
                    self._values["mfa_authenticated"] = mfa_authenticated

            @builtins.property
            def creation_date(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) creationDate property.

                Specify an array of string values to match this event if the actual value of creationDate is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("creation_date")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mfa_authenticated(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mfaAuthenticated property.

                Specify an array of string values to match this event if the actual value of mfaAuthenticated is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mfa_authenticated")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Attributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.AwsvpcConfiguration",
            jsii_struct_bases=[],
            name_mapping={"assign_public_ip": "assignPublicIp", "subnets": "subnets"},
        )
        class AwsvpcConfiguration:
            def __init__(
                self,
                *,
                assign_public_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
                subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AwsvpcConfiguration.

                :param assign_public_ip: (experimental) assignPublicIp property. Specify an array of string values to match this event if the actual value of assignPublicIp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param subnets: (experimental) subnets property. Specify an array of string values to match this event if the actual value of subnets is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    awsvpc_configuration = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.AwsvpcConfiguration(
                        assign_public_ip=["assignPublicIp"],
                        subnets=["subnets"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__24531672e239657b6052396301ee02063137e519fd94f3a7a150c723b406fc7c)
                    check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
                    check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if assign_public_ip is not None:
                    self._values["assign_public_ip"] = assign_public_ip
                if subnets is not None:
                    self._values["subnets"] = subnets

            @builtins.property
            def assign_public_ip(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) assignPublicIp property.

                Specify an array of string values to match this event if the actual value of assignPublicIp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("assign_public_ip")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) subnets property.

                Specify an array of string values to match this event if the actual value of subnets is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("subnets")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AwsvpcConfiguration(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.NetworkConfiguration",
            jsii_struct_bases=[],
            name_mapping={"awsvpc_configuration": "awsvpcConfiguration"},
        )
        class NetworkConfiguration:
            def __init__(
                self,
                *,
                awsvpc_configuration: typing.Optional[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.AwsvpcConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for NetworkConfiguration.

                :param awsvpc_configuration: (experimental) awsvpcConfiguration property. Specify an array of string values to match this event if the actual value of awsvpcConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    network_configuration = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.NetworkConfiguration(
                        awsvpc_configuration=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.AwsvpcConfiguration(
                            assign_public_ip=["assignPublicIp"],
                            subnets=["subnets"]
                        )
                    )
                '''
                if isinstance(awsvpc_configuration, dict):
                    awsvpc_configuration = ClusterEvents.AWSAPICallViaCloudTrail.AwsvpcConfiguration(**awsvpc_configuration)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8e47dfca3a19f7cd2d19d1fac6e930d82a766f0d0ace13e7a2dc40f1ef63b1e5)
                    check_type(argname="argument awsvpc_configuration", value=awsvpc_configuration, expected_type=type_hints["awsvpc_configuration"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if awsvpc_configuration is not None:
                    self._values["awsvpc_configuration"] = awsvpc_configuration

            @builtins.property
            def awsvpc_configuration(
                self,
            ) -> typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.AwsvpcConfiguration"]:
                '''(experimental) awsvpcConfiguration property.

                Specify an array of string values to match this event if the actual value of awsvpcConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("awsvpc_configuration")
                return typing.cast(typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.AwsvpcConfiguration"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "NetworkConfiguration(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides",
            jsii_struct_bases=[],
            name_mapping={"container_overrides": "containerOverrides"},
        )
        class Overrides:
            def __init__(
                self,
                *,
                container_overrides: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.OverridesItem", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for Overrides.

                :param container_overrides: (experimental) containerOverrides property. Specify an array of string values to match this event if the actual value of containerOverrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    # environment: Any
                    # resource_requirements: Any
                    
                    overrides = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides(
                        container_overrides=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.OverridesItem(
                            command=["command"],
                            cpu=["cpu"],
                            environment=[environment],
                            memory=["memory"],
                            name=["name"],
                            resource_requirements=[resource_requirements]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__362d0a473a62c2fa205602be920a5ee2135d3f02ac9cd0664e992f0d9efdd69d)
                    check_type(argname="argument container_overrides", value=container_overrides, expected_type=type_hints["container_overrides"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if container_overrides is not None:
                    self._values["container_overrides"] = container_overrides

            @builtins.property
            def container_overrides(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.OverridesItem"]]:
                '''(experimental) containerOverrides property.

                Specify an array of string values to match this event if the actual value of containerOverrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_overrides")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.OverridesItem"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Overrides(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides1",
            jsii_struct_bases=[],
            name_mapping={
                "container_overrides": "containerOverrides",
                "inference_accelerator_overrides": "inferenceAcceleratorOverrides",
            },
        )
        class Overrides1:
            def __init__(
                self,
                *,
                container_overrides: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.Overrides1Item", typing.Dict[builtins.str, typing.Any]]]] = None,
                inference_accelerator_overrides: typing.Optional[typing.Sequence[typing.Any]] = None,
            ) -> None:
                '''(experimental) Type definition for Overrides_1.

                :param container_overrides: (experimental) containerOverrides property. Specify an array of string values to match this event if the actual value of containerOverrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param inference_accelerator_overrides: (experimental) inferenceAcceleratorOverrides property. Specify an array of string values to match this event if the actual value of inferenceAcceleratorOverrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    # environment: Any
                    # inference_accelerator_overrides: Any
                    # resource_requirements: Any
                    
                    overrides1 = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides1(
                        container_overrides=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides1Item(
                            command=["command"],
                            cpu=["cpu"],
                            environment=[environment],
                            memory=["memory"],
                            name=["name"],
                            resource_requirements=[resource_requirements]
                        )],
                        inference_accelerator_overrides=[inference_accelerator_overrides]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__65c11bf4ef4687b7882f293ce5493782553a847065d958bead45f7fb79462d39)
                    check_type(argname="argument container_overrides", value=container_overrides, expected_type=type_hints["container_overrides"])
                    check_type(argname="argument inference_accelerator_overrides", value=inference_accelerator_overrides, expected_type=type_hints["inference_accelerator_overrides"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if container_overrides is not None:
                    self._values["container_overrides"] = container_overrides
                if inference_accelerator_overrides is not None:
                    self._values["inference_accelerator_overrides"] = inference_accelerator_overrides

            @builtins.property
            def container_overrides(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.Overrides1Item"]]:
                '''(experimental) containerOverrides property.

                Specify an array of string values to match this event if the actual value of containerOverrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_overrides")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.Overrides1Item"]], result)

            @builtins.property
            def inference_accelerator_overrides(
                self,
            ) -> typing.Optional[typing.List[typing.Any]]:
                '''(experimental) inferenceAcceleratorOverrides property.

                Specify an array of string values to match this event if the actual value of inferenceAcceleratorOverrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("inference_accelerator_overrides")
                return typing.cast(typing.Optional[typing.List[typing.Any]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Overrides1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides1Item",
            jsii_struct_bases=[],
            name_mapping={
                "command": "command",
                "cpu": "cpu",
                "environment": "environment",
                "memory": "memory",
                "name": "name",
                "resource_requirements": "resourceRequirements",
            },
        )
        class Overrides1Item:
            def __init__(
                self,
                *,
                command: typing.Optional[typing.Sequence[builtins.str]] = None,
                cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
                environment: typing.Optional[typing.Sequence[typing.Any]] = None,
                memory: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                resource_requirements: typing.Optional[typing.Sequence[typing.Any]] = None,
            ) -> None:
                '''(experimental) Type definition for Overrides_1Item.

                :param command: (experimental) command property. Specify an array of string values to match this event if the actual value of command is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param cpu: (experimental) cpu property. Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param environment: (experimental) environment property. Specify an array of string values to match this event if the actual value of environment is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param memory: (experimental) memory property. Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param resource_requirements: (experimental) resourceRequirements property. Specify an array of string values to match this event if the actual value of resourceRequirements is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    # environment: Any
                    # resource_requirements: Any
                    
                    overrides1_item = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides1Item(
                        command=["command"],
                        cpu=["cpu"],
                        environment=[environment],
                        memory=["memory"],
                        name=["name"],
                        resource_requirements=[resource_requirements]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__49168f44a140b30d3515b7d4e80615b65ad625421dfba1eb632b6bbff2d0691e)
                    check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                    check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                    check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
                    check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument resource_requirements", value=resource_requirements, expected_type=type_hints["resource_requirements"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if command is not None:
                    self._values["command"] = command
                if cpu is not None:
                    self._values["cpu"] = cpu
                if environment is not None:
                    self._values["environment"] = environment
                if memory is not None:
                    self._values["memory"] = memory
                if name is not None:
                    self._values["name"] = name
                if resource_requirements is not None:
                    self._values["resource_requirements"] = resource_requirements

            @builtins.property
            def command(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) command property.

                Specify an array of string values to match this event if the actual value of command is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("command")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def cpu(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cpu property.

                Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cpu")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def environment(self) -> typing.Optional[typing.List[typing.Any]]:
                '''(experimental) environment property.

                Specify an array of string values to match this event if the actual value of environment is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("environment")
                return typing.cast(typing.Optional[typing.List[typing.Any]], result)

            @builtins.property
            def memory(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) memory property.

                Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("memory")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def resource_requirements(self) -> typing.Optional[typing.List[typing.Any]]:
                '''(experimental) resourceRequirements property.

                Specify an array of string values to match this event if the actual value of resourceRequirements is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resource_requirements")
                return typing.cast(typing.Optional[typing.List[typing.Any]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Overrides1Item(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.OverridesItem",
            jsii_struct_bases=[],
            name_mapping={
                "command": "command",
                "cpu": "cpu",
                "environment": "environment",
                "memory": "memory",
                "name": "name",
                "resource_requirements": "resourceRequirements",
            },
        )
        class OverridesItem:
            def __init__(
                self,
                *,
                command: typing.Optional[typing.Sequence[builtins.str]] = None,
                cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
                environment: typing.Optional[typing.Sequence[typing.Any]] = None,
                memory: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                resource_requirements: typing.Optional[typing.Sequence[typing.Any]] = None,
            ) -> None:
                '''(experimental) Type definition for OverridesItem.

                :param command: (experimental) command property. Specify an array of string values to match this event if the actual value of command is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param cpu: (experimental) cpu property. Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param environment: (experimental) environment property. Specify an array of string values to match this event if the actual value of environment is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param memory: (experimental) memory property. Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param resource_requirements: (experimental) resourceRequirements property. Specify an array of string values to match this event if the actual value of resourceRequirements is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    # environment: Any
                    # resource_requirements: Any
                    
                    overrides_item = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.OverridesItem(
                        command=["command"],
                        cpu=["cpu"],
                        environment=[environment],
                        memory=["memory"],
                        name=["name"],
                        resource_requirements=[resource_requirements]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__15d36bf7d3e03a5afc12197abea5c97ba5f34622df091641b62dcd294f7c3bdc)
                    check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                    check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                    check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
                    check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument resource_requirements", value=resource_requirements, expected_type=type_hints["resource_requirements"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if command is not None:
                    self._values["command"] = command
                if cpu is not None:
                    self._values["cpu"] = cpu
                if environment is not None:
                    self._values["environment"] = environment
                if memory is not None:
                    self._values["memory"] = memory
                if name is not None:
                    self._values["name"] = name
                if resource_requirements is not None:
                    self._values["resource_requirements"] = resource_requirements

            @builtins.property
            def command(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) command property.

                Specify an array of string values to match this event if the actual value of command is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("command")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def cpu(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cpu property.

                Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cpu")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def environment(self) -> typing.Optional[typing.List[typing.Any]]:
                '''(experimental) environment property.

                Specify an array of string values to match this event if the actual value of environment is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("environment")
                return typing.cast(typing.Optional[typing.List[typing.Any]], result)

            @builtins.property
            def memory(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) memory property.

                Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("memory")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def resource_requirements(self) -> typing.Optional[typing.List[typing.Any]]:
                '''(experimental) resourceRequirements property.

                Specify an array of string values to match this event if the actual value of resourceRequirements is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resource_requirements")
                return typing.cast(typing.Optional[typing.List[typing.Any]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "OverridesItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.RequestParameters",
            jsii_struct_bases=[],
            name_mapping={
                "cluster": "cluster",
                "container_instance": "containerInstance",
                "containers": "containers",
                "count": "count",
                "enable_ecs_managed_tags": "enableEcsManagedTags",
                "execution_stopped_at": "executionStoppedAt",
                "launch_type": "launchType",
                "network_configuration": "networkConfiguration",
                "overrides": "overrides",
                "placement_constraints": "placementConstraints",
                "pull_started_at": "pullStartedAt",
                "pull_stopped_at": "pullStoppedAt",
                "reason": "reason",
                "started_by": "startedBy",
                "status": "status",
                "task": "task",
                "task_definition": "taskDefinition",
            },
        )
        class RequestParameters:
            def __init__(
                self,
                *,
                cluster: typing.Optional[typing.Sequence[builtins.str]] = None,
                container_instance: typing.Optional[typing.Sequence[builtins.str]] = None,
                containers: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem1", typing.Dict[builtins.str, typing.Any]]]] = None,
                count: typing.Optional[typing.Sequence[builtins.str]] = None,
                enable_ecs_managed_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
                execution_stopped_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                launch_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                network_configuration: typing.Optional[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.NetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
                overrides: typing.Optional[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.Overrides", typing.Dict[builtins.str, typing.Any]]] = None,
                placement_constraints: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                pull_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                pull_stopped_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                reason: typing.Optional[typing.Sequence[builtins.str]] = None,
                started_by: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                task: typing.Optional[typing.Sequence[builtins.str]] = None,
                task_definition: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParameters.

                :param cluster: (experimental) cluster property. Specify an array of string values to match this event if the actual value of cluster is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param container_instance: (experimental) containerInstance property. Specify an array of string values to match this event if the actual value of containerInstance is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param containers: (experimental) containers property. Specify an array of string values to match this event if the actual value of containers is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param count: (experimental) count property. Specify an array of string values to match this event if the actual value of count is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param enable_ecs_managed_tags: (experimental) enableECSManagedTags property. Specify an array of string values to match this event if the actual value of enableECSManagedTags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param execution_stopped_at: (experimental) executionStoppedAt property. Specify an array of string values to match this event if the actual value of executionStoppedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param launch_type: (experimental) launchType property. Specify an array of string values to match this event if the actual value of launchType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_configuration: (experimental) networkConfiguration property. Specify an array of string values to match this event if the actual value of networkConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param overrides: (experimental) overrides property. Specify an array of string values to match this event if the actual value of overrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param placement_constraints: (experimental) placementConstraints property. Specify an array of string values to match this event if the actual value of placementConstraints is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param pull_started_at: (experimental) pullStartedAt property. Specify an array of string values to match this event if the actual value of pullStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param pull_stopped_at: (experimental) pullStoppedAt property. Specify an array of string values to match this event if the actual value of pullStoppedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reason: (experimental) reason property. Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param started_by: (experimental) startedBy property. Specify an array of string values to match this event if the actual value of startedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param task: (experimental) task property. Specify an array of string values to match this event if the actual value of task is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param task_definition: (experimental) taskDefinition property. Specify an array of string values to match this event if the actual value of taskDefinition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    # environment: Any
                    # network_bindings: Any
                    # resource_requirements: Any
                    
                    request_parameters = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.RequestParameters(
                        cluster=["cluster"],
                        container_instance=["containerInstance"],
                        containers=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem1(
                            container_name=["containerName"],
                            exit_code=["exitCode"],
                            network_bindings=[network_bindings],
                            status=["status"]
                        )],
                        count=["count"],
                        enable_ecs_managed_tags=["enableEcsManagedTags"],
                        execution_stopped_at=["executionStoppedAt"],
                        launch_type=["launchType"],
                        network_configuration=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.NetworkConfiguration(
                            awsvpc_configuration=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.AwsvpcConfiguration(
                                assign_public_ip=["assignPublicIp"],
                                subnets=["subnets"]
                            )
                        ),
                        overrides=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides(
                            container_overrides=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.OverridesItem(
                                command=["command"],
                                cpu=["cpu"],
                                environment=[environment],
                                memory=["memory"],
                                name=["name"],
                                resource_requirements=[resource_requirements]
                            )]
                        ),
                        placement_constraints=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem(
                            expression=["expression"],
                            type=["type"]
                        )],
                        pull_started_at=["pullStartedAt"],
                        pull_stopped_at=["pullStoppedAt"],
                        reason=["reason"],
                        started_by=["startedBy"],
                        status=["status"],
                        task=["task"],
                        task_definition=["taskDefinition"]
                    )
                '''
                if isinstance(network_configuration, dict):
                    network_configuration = ClusterEvents.AWSAPICallViaCloudTrail.NetworkConfiguration(**network_configuration)
                if isinstance(overrides, dict):
                    overrides = ClusterEvents.AWSAPICallViaCloudTrail.Overrides(**overrides)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__dfbf6f0cade3343137ef53b5428034cebac9f7efc67e9cf3dbc674c17be45136)
                    check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
                    check_type(argname="argument container_instance", value=container_instance, expected_type=type_hints["container_instance"])
                    check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
                    check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                    check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
                    check_type(argname="argument execution_stopped_at", value=execution_stopped_at, expected_type=type_hints["execution_stopped_at"])
                    check_type(argname="argument launch_type", value=launch_type, expected_type=type_hints["launch_type"])
                    check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
                    check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
                    check_type(argname="argument placement_constraints", value=placement_constraints, expected_type=type_hints["placement_constraints"])
                    check_type(argname="argument pull_started_at", value=pull_started_at, expected_type=type_hints["pull_started_at"])
                    check_type(argname="argument pull_stopped_at", value=pull_stopped_at, expected_type=type_hints["pull_stopped_at"])
                    check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                    check_type(argname="argument started_by", value=started_by, expected_type=type_hints["started_by"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument task", value=task, expected_type=type_hints["task"])
                    check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if cluster is not None:
                    self._values["cluster"] = cluster
                if container_instance is not None:
                    self._values["container_instance"] = container_instance
                if containers is not None:
                    self._values["containers"] = containers
                if count is not None:
                    self._values["count"] = count
                if enable_ecs_managed_tags is not None:
                    self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
                if execution_stopped_at is not None:
                    self._values["execution_stopped_at"] = execution_stopped_at
                if launch_type is not None:
                    self._values["launch_type"] = launch_type
                if network_configuration is not None:
                    self._values["network_configuration"] = network_configuration
                if overrides is not None:
                    self._values["overrides"] = overrides
                if placement_constraints is not None:
                    self._values["placement_constraints"] = placement_constraints
                if pull_started_at is not None:
                    self._values["pull_started_at"] = pull_started_at
                if pull_stopped_at is not None:
                    self._values["pull_stopped_at"] = pull_stopped_at
                if reason is not None:
                    self._values["reason"] = reason
                if started_by is not None:
                    self._values["started_by"] = started_by
                if status is not None:
                    self._values["status"] = status
                if task is not None:
                    self._values["task"] = task
                if task_definition is not None:
                    self._values["task_definition"] = task_definition

            @builtins.property
            def cluster(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cluster property.

                Specify an array of string values to match this event if the actual value of cluster is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cluster")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def container_instance(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) containerInstance property.

                Specify an array of string values to match this event if the actual value of containerInstance is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_instance")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def containers(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem1"]]:
                '''(experimental) containers property.

                Specify an array of string values to match this event if the actual value of containers is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("containers")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem1"]], result)

            @builtins.property
            def count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) count property.

                Specify an array of string values to match this event if the actual value of count is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def enable_ecs_managed_tags(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) enableECSManagedTags property.

                Specify an array of string values to match this event if the actual value of enableECSManagedTags is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("enable_ecs_managed_tags")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def execution_stopped_at(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) executionStoppedAt property.

                Specify an array of string values to match this event if the actual value of executionStoppedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("execution_stopped_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def launch_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) launchType property.

                Specify an array of string values to match this event if the actual value of launchType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def network_configuration(
                self,
            ) -> typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.NetworkConfiguration"]:
                '''(experimental) networkConfiguration property.

                Specify an array of string values to match this event if the actual value of networkConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_configuration")
                return typing.cast(typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.NetworkConfiguration"], result)

            @builtins.property
            def overrides(
                self,
            ) -> typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.Overrides"]:
                '''(experimental) overrides property.

                Specify an array of string values to match this event if the actual value of overrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("overrides")
                return typing.cast(typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.Overrides"], result)

            @builtins.property
            def placement_constraints(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem"]]:
                '''(experimental) placementConstraints property.

                Specify an array of string values to match this event if the actual value of placementConstraints is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("placement_constraints")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem"]], result)

            @builtins.property
            def pull_started_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) pullStartedAt property.

                Specify an array of string values to match this event if the actual value of pullStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("pull_started_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def pull_stopped_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) pullStoppedAt property.

                Specify an array of string values to match this event if the actual value of pullStoppedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("pull_stopped_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def reason(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) reason property.

                Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("reason")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def started_by(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) startedBy property.

                Specify an array of string values to match this event if the actual value of startedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("started_by")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status property.

                Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def task(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) task property.

                Specify an array of string values to match this event if the actual value of task is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("task")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def task_definition(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) taskDefinition property.

                Specify an array of string values to match this event if the actual value of taskDefinition is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("task_definition")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RequestParameters(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem",
            jsii_struct_bases=[],
            name_mapping={"expression": "expression", "type": "type"},
        )
        class RequestParametersItem:
            def __init__(
                self,
                *,
                expression: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParametersItem.

                :param expression: (experimental) expression property. Specify an array of string values to match this event if the actual value of expression is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    request_parameters_item = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem(
                        expression=["expression"],
                        type=["type"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__0e2aa3ab6c42857d0b1048122116c9033b3e9393bb7714a038f5c23757deffb0)
                    check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if expression is not None:
                    self._values["expression"] = expression
                if type is not None:
                    self._values["type"] = type

            @builtins.property
            def expression(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) expression property.

                Specify an array of string values to match this event if the actual value of expression is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("expression")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RequestParametersItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem1",
            jsii_struct_bases=[],
            name_mapping={
                "container_name": "containerName",
                "exit_code": "exitCode",
                "network_bindings": "networkBindings",
                "status": "status",
            },
        )
        class RequestParametersItem1:
            def __init__(
                self,
                *,
                container_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                exit_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                network_bindings: typing.Optional[typing.Sequence[typing.Any]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParametersItem_1.

                :param container_name: (experimental) containerName property. Specify an array of string values to match this event if the actual value of containerName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param exit_code: (experimental) exitCode property. Specify an array of string values to match this event if the actual value of exitCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_bindings: (experimental) networkBindings property. Specify an array of string values to match this event if the actual value of networkBindings is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    # network_bindings: Any
                    
                    request_parameters_item1 = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem1(
                        container_name=["containerName"],
                        exit_code=["exitCode"],
                        network_bindings=[network_bindings],
                        status=["status"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__6141154cb3f914df3a989980e13857065b0afc2fe77c71f1c274e77786d32e06)
                    check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
                    check_type(argname="argument exit_code", value=exit_code, expected_type=type_hints["exit_code"])
                    check_type(argname="argument network_bindings", value=network_bindings, expected_type=type_hints["network_bindings"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if container_name is not None:
                    self._values["container_name"] = container_name
                if exit_code is not None:
                    self._values["exit_code"] = exit_code
                if network_bindings is not None:
                    self._values["network_bindings"] = network_bindings
                if status is not None:
                    self._values["status"] = status

            @builtins.property
            def container_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) containerName property.

                Specify an array of string values to match this event if the actual value of containerName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def exit_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) exitCode property.

                Specify an array of string values to match this event if the actual value of exitCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("exit_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def network_bindings(self) -> typing.Optional[typing.List[typing.Any]]:
                '''(experimental) networkBindings property.

                Specify an array of string values to match this event if the actual value of networkBindings is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_bindings")
                return typing.cast(typing.Optional[typing.List[typing.Any]], result)

            @builtins.property
            def status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status property.

                Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RequestParametersItem1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElements",
            jsii_struct_bases=[],
            name_mapping={
                "acknowledgment": "acknowledgment",
                "endpoint": "endpoint",
                "failures": "failures",
                "tasks": "tasks",
                "telemetry_endpoint": "telemetryEndpoint",
            },
        )
        class ResponseElements:
            def __init__(
                self,
                *,
                acknowledgment: typing.Optional[typing.Sequence[builtins.str]] = None,
                endpoint: typing.Optional[typing.Sequence[builtins.str]] = None,
                failures: typing.Optional[typing.Sequence[builtins.str]] = None,
                tasks: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                telemetry_endpoint: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ResponseElements.

                :param acknowledgment: (experimental) acknowledgment property. Specify an array of string values to match this event if the actual value of acknowledgment is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param endpoint: (experimental) endpoint property. Specify an array of string values to match this event if the actual value of endpoint is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param failures: (experimental) failures property. Specify an array of string values to match this event if the actual value of failures is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tasks: (experimental) tasks property. Specify an array of string values to match this event if the actual value of tasks is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param telemetry_endpoint: (experimental) telemetryEndpoint property. Specify an array of string values to match this event if the actual value of telemetryEndpoint is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    # environment: Any
                    # inference_accelerator_overrides: Any
                    # network_interfaces: Any
                    # resource_requirements: Any
                    # tags: Any
                    
                    response_elements = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElements(
                        acknowledgment=["acknowledgment"],
                        endpoint=["endpoint"],
                        failures=["failures"],
                        tasks=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItem(
                            attachments=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem(
                                details=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItemItem(
                                    name=["name"],
                                    value=["value"]
                                )],
                                id=["id"],
                                status=["status"],
                                type=["type"]
                            )],
                            cluster_arn=["clusterArn"],
                            container_instance_arn=["containerInstanceArn"],
                            containers=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem1(
                                container_arn=["containerArn"],
                                cpu=["cpu"],
                                image=["image"],
                                last_status=["lastStatus"],
                                memory=["memory"],
                                name=["name"],
                                network_interfaces=[network_interfaces],
                                task_arn=["taskArn"]
                            )],
                            cpu=["cpu"],
                            created_at=["createdAt"],
                            desired_status=["desiredStatus"],
                            group=["group"],
                            last_status=["lastStatus"],
                            launch_type=["launchType"],
                            memory=["memory"],
                            overrides=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides1(
                                container_overrides=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides1Item(
                                    command=["command"],
                                    cpu=["cpu"],
                                    environment=[environment],
                                    memory=["memory"],
                                    name=["name"],
                                    resource_requirements=[resource_requirements]
                                )],
                                inference_accelerator_overrides=[inference_accelerator_overrides]
                            ),
                            platform_version=["platformVersion"],
                            started_by=["startedBy"],
                            tags=[tags],
                            task_arn=["taskArn"],
                            task_definition_arn=["taskDefinitionArn"],
                            version=["version"]
                        )],
                        telemetry_endpoint=["telemetryEndpoint"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__61b4cbd9b48826dbe70fd733d96a07838cf087c6122a2d08a53e515522cd6f08)
                    check_type(argname="argument acknowledgment", value=acknowledgment, expected_type=type_hints["acknowledgment"])
                    check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                    check_type(argname="argument failures", value=failures, expected_type=type_hints["failures"])
                    check_type(argname="argument tasks", value=tasks, expected_type=type_hints["tasks"])
                    check_type(argname="argument telemetry_endpoint", value=telemetry_endpoint, expected_type=type_hints["telemetry_endpoint"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if acknowledgment is not None:
                    self._values["acknowledgment"] = acknowledgment
                if endpoint is not None:
                    self._values["endpoint"] = endpoint
                if failures is not None:
                    self._values["failures"] = failures
                if tasks is not None:
                    self._values["tasks"] = tasks
                if telemetry_endpoint is not None:
                    self._values["telemetry_endpoint"] = telemetry_endpoint

            @builtins.property
            def acknowledgment(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) acknowledgment property.

                Specify an array of string values to match this event if the actual value of acknowledgment is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("acknowledgment")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def endpoint(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) endpoint property.

                Specify an array of string values to match this event if the actual value of endpoint is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("endpoint")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def failures(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) failures property.

                Specify an array of string values to match this event if the actual value of failures is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("failures")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tasks(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItem"]]:
                '''(experimental) tasks property.

                Specify an array of string values to match this event if the actual value of tasks is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tasks")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItem"]], result)

            @builtins.property
            def telemetry_endpoint(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) telemetryEndpoint property.

                Specify an array of string values to match this event if the actual value of telemetryEndpoint is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("telemetry_endpoint")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResponseElements(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItem",
            jsii_struct_bases=[],
            name_mapping={
                "attachments": "attachments",
                "cluster_arn": "clusterArn",
                "container_instance_arn": "containerInstanceArn",
                "containers": "containers",
                "cpu": "cpu",
                "created_at": "createdAt",
                "desired_status": "desiredStatus",
                "group": "group",
                "last_status": "lastStatus",
                "launch_type": "launchType",
                "memory": "memory",
                "overrides": "overrides",
                "platform_version": "platformVersion",
                "started_by": "startedBy",
                "tags": "tags",
                "task_arn": "taskArn",
                "task_definition_arn": "taskDefinitionArn",
                "version": "version",
            },
        )
        class ResponseElementsItem:
            def __init__(
                self,
                *,
                attachments: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                cluster_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                container_instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                containers: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem1", typing.Dict[builtins.str, typing.Any]]]] = None,
                cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
                created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                desired_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                group: typing.Optional[typing.Sequence[builtins.str]] = None,
                last_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                launch_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                memory: typing.Optional[typing.Sequence[builtins.str]] = None,
                overrides: typing.Optional[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.Overrides1", typing.Dict[builtins.str, typing.Any]]] = None,
                platform_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                started_by: typing.Optional[typing.Sequence[builtins.str]] = None,
                tags: typing.Optional[typing.Sequence[typing.Any]] = None,
                task_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                task_definition_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ResponseElementsItem.

                :param attachments: (experimental) attachments property. Specify an array of string values to match this event if the actual value of attachments is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param cluster_arn: (experimental) clusterArn property. Specify an array of string values to match this event if the actual value of clusterArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Cluster reference
                :param container_instance_arn: (experimental) containerInstanceArn property. Specify an array of string values to match this event if the actual value of containerInstanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param containers: (experimental) containers property. Specify an array of string values to match this event if the actual value of containers is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param cpu: (experimental) cpu property. Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param created_at: (experimental) createdAt property. Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param desired_status: (experimental) desiredStatus property. Specify an array of string values to match this event if the actual value of desiredStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param group: (experimental) group property. Specify an array of string values to match this event if the actual value of group is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param last_status: (experimental) lastStatus property. Specify an array of string values to match this event if the actual value of lastStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param launch_type: (experimental) launchType property. Specify an array of string values to match this event if the actual value of launchType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param memory: (experimental) memory property. Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param overrides: (experimental) overrides property. Specify an array of string values to match this event if the actual value of overrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param platform_version: (experimental) platformVersion property. Specify an array of string values to match this event if the actual value of platformVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param started_by: (experimental) startedBy property. Specify an array of string values to match this event if the actual value of startedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tags: (experimental) tags property. Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param task_arn: (experimental) taskArn property. Specify an array of string values to match this event if the actual value of taskArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param task_definition_arn: (experimental) taskDefinitionArn property. Specify an array of string values to match this event if the actual value of taskDefinitionArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    # environment: Any
                    # inference_accelerator_overrides: Any
                    # network_interfaces: Any
                    # resource_requirements: Any
                    # tags: Any
                    
                    response_elements_item = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItem(
                        attachments=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem(
                            details=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItemItem(
                                name=["name"],
                                value=["value"]
                            )],
                            id=["id"],
                            status=["status"],
                            type=["type"]
                        )],
                        cluster_arn=["clusterArn"],
                        container_instance_arn=["containerInstanceArn"],
                        containers=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem1(
                            container_arn=["containerArn"],
                            cpu=["cpu"],
                            image=["image"],
                            last_status=["lastStatus"],
                            memory=["memory"],
                            name=["name"],
                            network_interfaces=[network_interfaces],
                            task_arn=["taskArn"]
                        )],
                        cpu=["cpu"],
                        created_at=["createdAt"],
                        desired_status=["desiredStatus"],
                        group=["group"],
                        last_status=["lastStatus"],
                        launch_type=["launchType"],
                        memory=["memory"],
                        overrides=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides1(
                            container_overrides=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Overrides1Item(
                                command=["command"],
                                cpu=["cpu"],
                                environment=[environment],
                                memory=["memory"],
                                name=["name"],
                                resource_requirements=[resource_requirements]
                            )],
                            inference_accelerator_overrides=[inference_accelerator_overrides]
                        ),
                        platform_version=["platformVersion"],
                        started_by=["startedBy"],
                        tags=[tags],
                        task_arn=["taskArn"],
                        task_definition_arn=["taskDefinitionArn"],
                        version=["version"]
                    )
                '''
                if isinstance(overrides, dict):
                    overrides = ClusterEvents.AWSAPICallViaCloudTrail.Overrides1(**overrides)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ba8b3469580b1b0420562166033b82072adb9438c411349d9acd2ccc73e2a72a)
                    check_type(argname="argument attachments", value=attachments, expected_type=type_hints["attachments"])
                    check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
                    check_type(argname="argument container_instance_arn", value=container_instance_arn, expected_type=type_hints["container_instance_arn"])
                    check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
                    check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                    check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                    check_type(argname="argument desired_status", value=desired_status, expected_type=type_hints["desired_status"])
                    check_type(argname="argument group", value=group, expected_type=type_hints["group"])
                    check_type(argname="argument last_status", value=last_status, expected_type=type_hints["last_status"])
                    check_type(argname="argument launch_type", value=launch_type, expected_type=type_hints["launch_type"])
                    check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
                    check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
                    check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
                    check_type(argname="argument started_by", value=started_by, expected_type=type_hints["started_by"])
                    check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                    check_type(argname="argument task_arn", value=task_arn, expected_type=type_hints["task_arn"])
                    check_type(argname="argument task_definition_arn", value=task_definition_arn, expected_type=type_hints["task_definition_arn"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if attachments is not None:
                    self._values["attachments"] = attachments
                if cluster_arn is not None:
                    self._values["cluster_arn"] = cluster_arn
                if container_instance_arn is not None:
                    self._values["container_instance_arn"] = container_instance_arn
                if containers is not None:
                    self._values["containers"] = containers
                if cpu is not None:
                    self._values["cpu"] = cpu
                if created_at is not None:
                    self._values["created_at"] = created_at
                if desired_status is not None:
                    self._values["desired_status"] = desired_status
                if group is not None:
                    self._values["group"] = group
                if last_status is not None:
                    self._values["last_status"] = last_status
                if launch_type is not None:
                    self._values["launch_type"] = launch_type
                if memory is not None:
                    self._values["memory"] = memory
                if overrides is not None:
                    self._values["overrides"] = overrides
                if platform_version is not None:
                    self._values["platform_version"] = platform_version
                if started_by is not None:
                    self._values["started_by"] = started_by
                if tags is not None:
                    self._values["tags"] = tags
                if task_arn is not None:
                    self._values["task_arn"] = task_arn
                if task_definition_arn is not None:
                    self._values["task_definition_arn"] = task_definition_arn
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def attachments(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem"]]:
                '''(experimental) attachments property.

                Specify an array of string values to match this event if the actual value of attachments is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attachments")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem"]], result)

            @builtins.property
            def cluster_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) clusterArn property.

                Specify an array of string values to match this event if the actual value of clusterArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Cluster reference

                :stability: experimental
                '''
                result = self._values.get("cluster_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def container_instance_arn(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) containerInstanceArn property.

                Specify an array of string values to match this event if the actual value of containerInstanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_instance_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def containers(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem1"]]:
                '''(experimental) containers property.

                Specify an array of string values to match this event if the actual value of containers is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("containers")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem1"]], result)

            @builtins.property
            def cpu(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cpu property.

                Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cpu")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def created_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) createdAt property.

                Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("created_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def desired_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) desiredStatus property.

                Specify an array of string values to match this event if the actual value of desiredStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("desired_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def group(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) group property.

                Specify an array of string values to match this event if the actual value of group is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def last_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) lastStatus property.

                Specify an array of string values to match this event if the actual value of lastStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("last_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def launch_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) launchType property.

                Specify an array of string values to match this event if the actual value of launchType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def memory(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) memory property.

                Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("memory")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def overrides(
                self,
            ) -> typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.Overrides1"]:
                '''(experimental) overrides property.

                Specify an array of string values to match this event if the actual value of overrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("overrides")
                return typing.cast(typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.Overrides1"], result)

            @builtins.property
            def platform_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) platformVersion property.

                Specify an array of string values to match this event if the actual value of platformVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("platform_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def started_by(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) startedBy property.

                Specify an array of string values to match this event if the actual value of startedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("started_by")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tags(self) -> typing.Optional[typing.List[typing.Any]]:
                '''(experimental) tags property.

                Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tags")
                return typing.cast(typing.Optional[typing.List[typing.Any]], result)

            @builtins.property
            def task_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) taskArn property.

                Specify an array of string values to match this event if the actual value of taskArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("task_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def task_definition_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) taskDefinitionArn property.

                Specify an array of string values to match this event if the actual value of taskDefinitionArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("task_definition_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version property.

                Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResponseElementsItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem",
            jsii_struct_bases=[],
            name_mapping={
                "details": "details",
                "id": "id",
                "status": "status",
                "type": "type",
            },
        )
        class ResponseElementsItemItem:
            def __init__(
                self,
                *,
                details: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItemItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ResponseElementsItemItem.

                :param details: (experimental) details property. Specify an array of string values to match this event if the actual value of details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    response_elements_item_item = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem(
                        details=[ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItemItem(
                            name=["name"],
                            value=["value"]
                        )],
                        id=["id"],
                        status=["status"],
                        type=["type"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__d85b68964afd0df58756745bbb2e81a069e8c00d6cb9b203b60e73d0f472f8f8)
                    check_type(argname="argument details", value=details, expected_type=type_hints["details"])
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if details is not None:
                    self._values["details"] = details
                if id is not None:
                    self._values["id"] = id
                if status is not None:
                    self._values["status"] = status
                if type is not None:
                    self._values["type"] = type

            @builtins.property
            def details(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItemItem"]]:
                '''(experimental) details property.

                Specify an array of string values to match this event if the actual value of details is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("details")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItemItem"]], result)

            @builtins.property
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status property.

                Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResponseElementsItemItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem1",
            jsii_struct_bases=[],
            name_mapping={
                "container_arn": "containerArn",
                "cpu": "cpu",
                "image": "image",
                "last_status": "lastStatus",
                "memory": "memory",
                "name": "name",
                "network_interfaces": "networkInterfaces",
                "task_arn": "taskArn",
            },
        )
        class ResponseElementsItemItem1:
            def __init__(
                self,
                *,
                container_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
                image: typing.Optional[typing.Sequence[builtins.str]] = None,
                last_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                memory: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                network_interfaces: typing.Optional[typing.Sequence[typing.Any]] = None,
                task_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ResponseElementsItemItem_1.

                :param container_arn: (experimental) containerArn property. Specify an array of string values to match this event if the actual value of containerArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param cpu: (experimental) cpu property. Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image: (experimental) image property. Specify an array of string values to match this event if the actual value of image is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param last_status: (experimental) lastStatus property. Specify an array of string values to match this event if the actual value of lastStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param memory: (experimental) memory property. Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_interfaces: (experimental) networkInterfaces property. Specify an array of string values to match this event if the actual value of networkInterfaces is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param task_arn: (experimental) taskArn property. Specify an array of string values to match this event if the actual value of taskArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    # network_interfaces: Any
                    
                    response_elements_item_item1 = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem1(
                        container_arn=["containerArn"],
                        cpu=["cpu"],
                        image=["image"],
                        last_status=["lastStatus"],
                        memory=["memory"],
                        name=["name"],
                        network_interfaces=[network_interfaces],
                        task_arn=["taskArn"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__39309d79e2ff26c549e5c49afedf303b2bc0d7753efce6d5329d6dc0088efee1)
                    check_type(argname="argument container_arn", value=container_arn, expected_type=type_hints["container_arn"])
                    check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                    check_type(argname="argument image", value=image, expected_type=type_hints["image"])
                    check_type(argname="argument last_status", value=last_status, expected_type=type_hints["last_status"])
                    check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
                    check_type(argname="argument task_arn", value=task_arn, expected_type=type_hints["task_arn"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if container_arn is not None:
                    self._values["container_arn"] = container_arn
                if cpu is not None:
                    self._values["cpu"] = cpu
                if image is not None:
                    self._values["image"] = image
                if last_status is not None:
                    self._values["last_status"] = last_status
                if memory is not None:
                    self._values["memory"] = memory
                if name is not None:
                    self._values["name"] = name
                if network_interfaces is not None:
                    self._values["network_interfaces"] = network_interfaces
                if task_arn is not None:
                    self._values["task_arn"] = task_arn

            @builtins.property
            def container_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) containerArn property.

                Specify an array of string values to match this event if the actual value of containerArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def cpu(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cpu property.

                Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cpu")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image property.

                Specify an array of string values to match this event if the actual value of image is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def last_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) lastStatus property.

                Specify an array of string values to match this event if the actual value of lastStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("last_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def memory(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) memory property.

                Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("memory")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def network_interfaces(self) -> typing.Optional[typing.List[typing.Any]]:
                '''(experimental) networkInterfaces property.

                Specify an array of string values to match this event if the actual value of networkInterfaces is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_interfaces")
                return typing.cast(typing.Optional[typing.List[typing.Any]], result)

            @builtins.property
            def task_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) taskArn property.

                Specify an array of string values to match this event if the actual value of taskArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("task_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResponseElementsItemItem1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItemItem",
            jsii_struct_bases=[],
            name_mapping={"name": "name", "value": "value"},
        )
        class ResponseElementsItemItemItem:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                value: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ResponseElementsItemItemItem.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param value: (experimental) value property. Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    response_elements_item_item_item = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItemItem(
                        name=["name"],
                        value=["value"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__14399473b14d14720fb566c96ff8a2b8a8218701c1e3a7034ae3586759cd1f4e)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name
                if value is not None:
                    self._values["value"] = value

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) value property.

                Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResponseElementsItemItemItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.SessionContext",
            jsii_struct_bases=[],
            name_mapping={
                "attributes": "attributes",
                "session_issuer": "sessionIssuer",
                "web_id_federation_data": "webIdFederationData",
            },
        )
        class SessionContext:
            def __init__(
                self,
                *,
                attributes: typing.Optional[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                session_issuer: typing.Optional[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.SessionIssuer", typing.Dict[builtins.str, typing.Any]]] = None,
                web_id_federation_data: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SessionContext.

                :param attributes: (experimental) attributes property. Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_issuer: (experimental) sessionIssuer property. Specify an array of string values to match this event if the actual value of sessionIssuer is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param web_id_federation_data: (experimental) webIdFederationData property. Specify an array of string values to match this event if the actual value of webIdFederationData is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    session_context = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.SessionContext(
                        attributes=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Attributes(
                            creation_date=["creationDate"],
                            mfa_authenticated=["mfaAuthenticated"]
                        ),
                        session_issuer=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                            account_id=["accountId"],
                            arn=["arn"],
                            principal_id=["principalId"],
                            type=["type"],
                            user_name=["userName"]
                        ),
                        web_id_federation_data=["webIdFederationData"]
                    )
                '''
                if isinstance(attributes, dict):
                    attributes = ClusterEvents.AWSAPICallViaCloudTrail.Attributes(**attributes)
                if isinstance(session_issuer, dict):
                    session_issuer = ClusterEvents.AWSAPICallViaCloudTrail.SessionIssuer(**session_issuer)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4461447b51edfabb629fcc63899c00b0858c9f2a1a3b0c655d96cb03945e6e36)
                    check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                    check_type(argname="argument session_issuer", value=session_issuer, expected_type=type_hints["session_issuer"])
                    check_type(argname="argument web_id_federation_data", value=web_id_federation_data, expected_type=type_hints["web_id_federation_data"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if attributes is not None:
                    self._values["attributes"] = attributes
                if session_issuer is not None:
                    self._values["session_issuer"] = session_issuer
                if web_id_federation_data is not None:
                    self._values["web_id_federation_data"] = web_id_federation_data

            @builtins.property
            def attributes(
                self,
            ) -> typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.Attributes"]:
                '''(experimental) attributes property.

                Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attributes")
                return typing.cast(typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.Attributes"], result)

            @builtins.property
            def session_issuer(
                self,
            ) -> typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.SessionIssuer"]:
                '''(experimental) sessionIssuer property.

                Specify an array of string values to match this event if the actual value of sessionIssuer is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_issuer")
                return typing.cast(typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.SessionIssuer"], result)

            @builtins.property
            def web_id_federation_data(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) webIdFederationData property.

                Specify an array of string values to match this event if the actual value of webIdFederationData is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("web_id_federation_data")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SessionContext(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.SessionIssuer",
            jsii_struct_bases=[],
            name_mapping={
                "account_id": "accountId",
                "arn": "arn",
                "principal_id": "principalId",
                "type": "type",
                "user_name": "userName",
            },
        )
        class SessionIssuer:
            def __init__(
                self,
                *,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SessionIssuer.

                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param principal_id: (experimental) principalId property. Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_name: (experimental) userName property. Specify an array of string values to match this event if the actual value of userName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    session_issuer = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                        account_id=["accountId"],
                        arn=["arn"],
                        principal_id=["principalId"],
                        type=["type"],
                        user_name=["userName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__79d61278c8c3994e8e8c666f5b9b729aceecd2df2a42d830ff1951b82a5a1ab7)
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                    check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if account_id is not None:
                    self._values["account_id"] = account_id
                if arn is not None:
                    self._values["arn"] = arn
                if principal_id is not None:
                    self._values["principal_id"] = principal_id
                if type is not None:
                    self._values["type"] = type
                if user_name is not None:
                    self._values["user_name"] = user_name

            @builtins.property
            def account_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accountId property.

                Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("account_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) arn property.

                Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def principal_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) principalId property.

                Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("principal_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def user_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) userName property.

                Specify an array of string values to match this event if the actual value of userName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SessionIssuer(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.AWSAPICallViaCloudTrail.UserIdentity",
            jsii_struct_bases=[],
            name_mapping={
                "access_key_id": "accessKeyId",
                "account_id": "accountId",
                "arn": "arn",
                "invoked_by": "invokedBy",
                "principal_id": "principalId",
                "session_context": "sessionContext",
                "type": "type",
            },
        )
        class UserIdentity:
            def __init__(
                self,
                *,
                access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                invoked_by: typing.Optional[typing.Sequence[builtins.str]] = None,
                principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                session_context: typing.Optional[typing.Union["ClusterEvents.AWSAPICallViaCloudTrail.SessionContext", typing.Dict[builtins.str, typing.Any]]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for UserIdentity.

                :param access_key_id: (experimental) accessKeyId property. Specify an array of string values to match this event if the actual value of accessKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param invoked_by: (experimental) invokedBy property. Specify an array of string values to match this event if the actual value of invokedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param principal_id: (experimental) principalId property. Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_context: (experimental) sessionContext property. Specify an array of string values to match this event if the actual value of sessionContext is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    user_identity = ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.UserIdentity(
                        access_key_id=["accessKeyId"],
                        account_id=["accountId"],
                        arn=["arn"],
                        invoked_by=["invokedBy"],
                        principal_id=["principalId"],
                        session_context=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.SessionContext(
                            attributes=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.Attributes(
                                creation_date=["creationDate"],
                                mfa_authenticated=["mfaAuthenticated"]
                            ),
                            session_issuer=ecs_events.ClusterEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                                account_id=["accountId"],
                                arn=["arn"],
                                principal_id=["principalId"],
                                type=["type"],
                                user_name=["userName"]
                            ),
                            web_id_federation_data=["webIdFederationData"]
                        ),
                        type=["type"]
                    )
                '''
                if isinstance(session_context, dict):
                    session_context = ClusterEvents.AWSAPICallViaCloudTrail.SessionContext(**session_context)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__aa1ade0b52155174dc08f2b615d707e017763cf2076cb408a26286e692f701ef)
                    check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument invoked_by", value=invoked_by, expected_type=type_hints["invoked_by"])
                    check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
                    check_type(argname="argument session_context", value=session_context, expected_type=type_hints["session_context"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if access_key_id is not None:
                    self._values["access_key_id"] = access_key_id
                if account_id is not None:
                    self._values["account_id"] = account_id
                if arn is not None:
                    self._values["arn"] = arn
                if invoked_by is not None:
                    self._values["invoked_by"] = invoked_by
                if principal_id is not None:
                    self._values["principal_id"] = principal_id
                if session_context is not None:
                    self._values["session_context"] = session_context
                if type is not None:
                    self._values["type"] = type

            @builtins.property
            def access_key_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accessKeyId property.

                Specify an array of string values to match this event if the actual value of accessKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("access_key_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def account_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accountId property.

                Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("account_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) arn property.

                Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def invoked_by(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) invokedBy property.

                Specify an array of string values to match this event if the actual value of invokedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("invoked_by")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def principal_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) principalId property.

                Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("principal_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def session_context(
                self,
            ) -> typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.SessionContext"]:
                '''(experimental) sessionContext property.

                Specify an array of string values to match this event if the actual value of sessionContext is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_context")
                return typing.cast(typing.Optional["ClusterEvents.AWSAPICallViaCloudTrail.SessionContext"], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "UserIdentity(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ECSContainerInstanceStateChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSContainerInstanceStateChange",
    ):
        '''(experimental) aws.ecs@ECSContainerInstanceStateChange event types for Cluster.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
            
            e_cSContainer_instance_state_change = ecs_events.ClusterEvents.ECSContainerInstanceStateChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSContainerInstanceStateChange.AttachmentDetails",
            jsii_struct_bases=[],
            name_mapping={
                "details": "details",
                "id": "id",
                "status": "status",
                "type": "type",
            },
        )
        class AttachmentDetails:
            def __init__(
                self,
                *,
                details: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSContainerInstanceStateChange.DetailsItems", typing.Dict[builtins.str, typing.Any]]]] = None,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AttachmentDetails.

                :param details: (experimental) details property. Specify an array of string values to match this event if the actual value of details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    attachment_details = ecs_events.ClusterEvents.ECSContainerInstanceStateChange.AttachmentDetails(
                        details=[ecs_events.ClusterEvents.ECSContainerInstanceStateChange.DetailsItems(
                            name=["name"],
                            value=["value"]
                        )],
                        id=["id"],
                        status=["status"],
                        type=["type"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__920c4d55a30decb878bdd5690610fcfe1a5246ee02c1604b726905859f3751dd)
                    check_type(argname="argument details", value=details, expected_type=type_hints["details"])
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if details is not None:
                    self._values["details"] = details
                if id is not None:
                    self._values["id"] = id
                if status is not None:
                    self._values["status"] = status
                if type is not None:
                    self._values["type"] = type

            @builtins.property
            def details(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.ECSContainerInstanceStateChange.DetailsItems"]]:
                '''(experimental) details property.

                Specify an array of string values to match this event if the actual value of details is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("details")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.ECSContainerInstanceStateChange.DetailsItems"]], result)

            @builtins.property
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status property.

                Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AttachmentDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSContainerInstanceStateChange.AttributesDetails",
            jsii_struct_bases=[],
            name_mapping={"name": "name", "value": "value"},
        )
        class AttributesDetails:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                value: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AttributesDetails.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param value: (experimental) value property. Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    attributes_details = ecs_events.ClusterEvents.ECSContainerInstanceStateChange.AttributesDetails(
                        name=["name"],
                        value=["value"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4711e8481ff08a5d0451015de144783dfc7e286460b4cd0149c25742bf222e78)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name
                if value is not None:
                    self._values["value"] = value

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) value property.

                Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AttributesDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSContainerInstanceStateChange.DetailsItems",
            jsii_struct_bases=[],
            name_mapping={"name": "name", "value": "value"},
        )
        class DetailsItems:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                value: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for detailsItems.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param value: (experimental) value property. Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    details_items = ecs_events.ClusterEvents.ECSContainerInstanceStateChange.DetailsItems(
                        name=["name"],
                        value=["value"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__bd8d1c7a5bae5ff833350edbda1f1bce0768bae86ea2f8a50a7dc53a29694d5e)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name
                if value is not None:
                    self._values["value"] = value

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) value property.

                Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DetailsItems(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSContainerInstanceStateChange.ECSContainerInstanceStateChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "account_type": "accountType",
                "agent_connected": "agentConnected",
                "agent_update_status": "agentUpdateStatus",
                "attachments": "attachments",
                "attributes": "attributes",
                "cluster_arn": "clusterArn",
                "container_instance_arn": "containerInstanceArn",
                "ec2_instance_id": "ec2InstanceId",
                "event_metadata": "eventMetadata",
                "pending_tasks_count": "pendingTasksCount",
                "registered_at": "registeredAt",
                "registered_resources": "registeredResources",
                "remaining_resources": "remainingResources",
                "running_tasks_count": "runningTasksCount",
                "status": "status",
                "status_reason": "statusReason",
                "updated_at": "updatedAt",
                "version": "version",
                "version_info": "versionInfo",
            },
        )
        class ECSContainerInstanceStateChangeProps:
            def __init__(
                self,
                *,
                account_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                agent_connected: typing.Optional[typing.Sequence[builtins.str]] = None,
                agent_update_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                attachments: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSContainerInstanceStateChange.AttachmentDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
                attributes: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSContainerInstanceStateChange.AttributesDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
                cluster_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                container_instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                pending_tasks_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                registered_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                registered_resources: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSContainerInstanceStateChange.ResourceDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
                remaining_resources: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSContainerInstanceStateChange.ResourceDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
                running_tasks_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_reason: typing.Optional[typing.Sequence[builtins.str]] = None,
                updated_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
                version_info: typing.Optional[typing.Union["ClusterEvents.ECSContainerInstanceStateChange.VersionInfo", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Cluster aws.ecs@ECSContainerInstanceStateChange event.

                :param account_type: (experimental) accountType property. Specify an array of string values to match this event if the actual value of accountType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param agent_connected: (experimental) agentConnected property. Specify an array of string values to match this event if the actual value of agentConnected is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param agent_update_status: (experimental) agentUpdateStatus property. Specify an array of string values to match this event if the actual value of agentUpdateStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param attachments: (experimental) attachments property. Specify an array of string values to match this event if the actual value of attachments is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param attributes: (experimental) attributes property. Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param cluster_arn: (experimental) clusterArn property. Specify an array of string values to match this event if the actual value of clusterArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Cluster reference
                :param container_instance_arn: (experimental) containerInstanceArn property. Specify an array of string values to match this event if the actual value of containerInstanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ec2_instance_id: (experimental) ec2InstanceId property. Specify an array of string values to match this event if the actual value of ec2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param pending_tasks_count: (experimental) pendingTasksCount property. Specify an array of string values to match this event if the actual value of pendingTasksCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param registered_at: (experimental) registeredAt property. Specify an array of string values to match this event if the actual value of registeredAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param registered_resources: (experimental) registeredResources property. Specify an array of string values to match this event if the actual value of registeredResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param remaining_resources: (experimental) remainingResources property. Specify an array of string values to match this event if the actual value of remainingResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param running_tasks_count: (experimental) runningTasksCount property. Specify an array of string values to match this event if the actual value of runningTasksCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_reason: (experimental) statusReason property. Specify an array of string values to match this event if the actual value of statusReason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param updated_at: (experimental) updatedAt property. Specify an array of string values to match this event if the actual value of updatedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version_info: (experimental) versionInfo property. Specify an array of string values to match this event if the actual value of versionInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    e_cSContainer_instance_state_change_props = ecs_events.ClusterEvents.ECSContainerInstanceStateChange.ECSContainerInstanceStateChangeProps(
                        account_type=["accountType"],
                        agent_connected=["agentConnected"],
                        agent_update_status=["agentUpdateStatus"],
                        attachments=[ecs_events.ClusterEvents.ECSContainerInstanceStateChange.AttachmentDetails(
                            details=[ecs_events.ClusterEvents.ECSContainerInstanceStateChange.DetailsItems(
                                name=["name"],
                                value=["value"]
                            )],
                            id=["id"],
                            status=["status"],
                            type=["type"]
                        )],
                        attributes=[ecs_events.ClusterEvents.ECSContainerInstanceStateChange.AttributesDetails(
                            name=["name"],
                            value=["value"]
                        )],
                        cluster_arn=["clusterArn"],
                        container_instance_arn=["containerInstanceArn"],
                        ec2_instance_id=["ec2InstanceId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        pending_tasks_count=["pendingTasksCount"],
                        registered_at=["registeredAt"],
                        registered_resources=[ecs_events.ClusterEvents.ECSContainerInstanceStateChange.ResourceDetails(
                            double_value=["doubleValue"],
                            integer_value=["integerValue"],
                            long_value=["longValue"],
                            name=["name"],
                            string_set_value=["stringSetValue"],
                            type=["type"]
                        )],
                        remaining_resources=[ecs_events.ClusterEvents.ECSContainerInstanceStateChange.ResourceDetails(
                            double_value=["doubleValue"],
                            integer_value=["integerValue"],
                            long_value=["longValue"],
                            name=["name"],
                            string_set_value=["stringSetValue"],
                            type=["type"]
                        )],
                        running_tasks_count=["runningTasksCount"],
                        status=["status"],
                        status_reason=["statusReason"],
                        updated_at=["updatedAt"],
                        version=["version"],
                        version_info=ecs_events.ClusterEvents.ECSContainerInstanceStateChange.VersionInfo(
                            agent_hash=["agentHash"],
                            agent_version=["agentVersion"],
                            docker_version=["dockerVersion"]
                        )
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(version_info, dict):
                    version_info = ClusterEvents.ECSContainerInstanceStateChange.VersionInfo(**version_info)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__22c391a286041019cf5ce99e641542c121aafff9c70df9c65bb40c392f3ce8b0)
                    check_type(argname="argument account_type", value=account_type, expected_type=type_hints["account_type"])
                    check_type(argname="argument agent_connected", value=agent_connected, expected_type=type_hints["agent_connected"])
                    check_type(argname="argument agent_update_status", value=agent_update_status, expected_type=type_hints["agent_update_status"])
                    check_type(argname="argument attachments", value=attachments, expected_type=type_hints["attachments"])
                    check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                    check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
                    check_type(argname="argument container_instance_arn", value=container_instance_arn, expected_type=type_hints["container_instance_arn"])
                    check_type(argname="argument ec2_instance_id", value=ec2_instance_id, expected_type=type_hints["ec2_instance_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument pending_tasks_count", value=pending_tasks_count, expected_type=type_hints["pending_tasks_count"])
                    check_type(argname="argument registered_at", value=registered_at, expected_type=type_hints["registered_at"])
                    check_type(argname="argument registered_resources", value=registered_resources, expected_type=type_hints["registered_resources"])
                    check_type(argname="argument remaining_resources", value=remaining_resources, expected_type=type_hints["remaining_resources"])
                    check_type(argname="argument running_tasks_count", value=running_tasks_count, expected_type=type_hints["running_tasks_count"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument status_reason", value=status_reason, expected_type=type_hints["status_reason"])
                    check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                    check_type(argname="argument version_info", value=version_info, expected_type=type_hints["version_info"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if account_type is not None:
                    self._values["account_type"] = account_type
                if agent_connected is not None:
                    self._values["agent_connected"] = agent_connected
                if agent_update_status is not None:
                    self._values["agent_update_status"] = agent_update_status
                if attachments is not None:
                    self._values["attachments"] = attachments
                if attributes is not None:
                    self._values["attributes"] = attributes
                if cluster_arn is not None:
                    self._values["cluster_arn"] = cluster_arn
                if container_instance_arn is not None:
                    self._values["container_instance_arn"] = container_instance_arn
                if ec2_instance_id is not None:
                    self._values["ec2_instance_id"] = ec2_instance_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if pending_tasks_count is not None:
                    self._values["pending_tasks_count"] = pending_tasks_count
                if registered_at is not None:
                    self._values["registered_at"] = registered_at
                if registered_resources is not None:
                    self._values["registered_resources"] = registered_resources
                if remaining_resources is not None:
                    self._values["remaining_resources"] = remaining_resources
                if running_tasks_count is not None:
                    self._values["running_tasks_count"] = running_tasks_count
                if status is not None:
                    self._values["status"] = status
                if status_reason is not None:
                    self._values["status_reason"] = status_reason
                if updated_at is not None:
                    self._values["updated_at"] = updated_at
                if version is not None:
                    self._values["version"] = version
                if version_info is not None:
                    self._values["version_info"] = version_info

            @builtins.property
            def account_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accountType property.

                Specify an array of string values to match this event if the actual value of accountType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("account_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def agent_connected(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) agentConnected property.

                Specify an array of string values to match this event if the actual value of agentConnected is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("agent_connected")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def agent_update_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) agentUpdateStatus property.

                Specify an array of string values to match this event if the actual value of agentUpdateStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("agent_update_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def attachments(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.ECSContainerInstanceStateChange.AttachmentDetails"]]:
                '''(experimental) attachments property.

                Specify an array of string values to match this event if the actual value of attachments is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attachments")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.ECSContainerInstanceStateChange.AttachmentDetails"]], result)

            @builtins.property
            def attributes(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.ECSContainerInstanceStateChange.AttributesDetails"]]:
                '''(experimental) attributes property.

                Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attributes")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.ECSContainerInstanceStateChange.AttributesDetails"]], result)

            @builtins.property
            def cluster_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) clusterArn property.

                Specify an array of string values to match this event if the actual value of clusterArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Cluster reference

                :stability: experimental
                '''
                result = self._values.get("cluster_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def container_instance_arn(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) containerInstanceArn property.

                Specify an array of string values to match this event if the actual value of containerInstanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_instance_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def ec2_instance_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ec2InstanceId property.

                Specify an array of string values to match this event if the actual value of ec2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ec2_instance_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def pending_tasks_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) pendingTasksCount property.

                Specify an array of string values to match this event if the actual value of pendingTasksCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("pending_tasks_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def registered_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) registeredAt property.

                Specify an array of string values to match this event if the actual value of registeredAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("registered_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def registered_resources(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.ECSContainerInstanceStateChange.ResourceDetails"]]:
                '''(experimental) registeredResources property.

                Specify an array of string values to match this event if the actual value of registeredResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("registered_resources")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.ECSContainerInstanceStateChange.ResourceDetails"]], result)

            @builtins.property
            def remaining_resources(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.ECSContainerInstanceStateChange.ResourceDetails"]]:
                '''(experimental) remainingResources property.

                Specify an array of string values to match this event if the actual value of remainingResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("remaining_resources")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.ECSContainerInstanceStateChange.ResourceDetails"]], result)

            @builtins.property
            def running_tasks_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) runningTasksCount property.

                Specify an array of string values to match this event if the actual value of runningTasksCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("running_tasks_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status property.

                Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_reason(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) statusReason property.

                Specify an array of string values to match this event if the actual value of statusReason is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_reason")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def updated_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) updatedAt property.

                Specify an array of string values to match this event if the actual value of updatedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("updated_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version property.

                Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version_info(
                self,
            ) -> typing.Optional["ClusterEvents.ECSContainerInstanceStateChange.VersionInfo"]:
                '''(experimental) versionInfo property.

                Specify an array of string values to match this event if the actual value of versionInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version_info")
                return typing.cast(typing.Optional["ClusterEvents.ECSContainerInstanceStateChange.VersionInfo"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ECSContainerInstanceStateChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSContainerInstanceStateChange.ResourceDetails",
            jsii_struct_bases=[],
            name_mapping={
                "double_value": "doubleValue",
                "integer_value": "integerValue",
                "long_value": "longValue",
                "name": "name",
                "string_set_value": "stringSetValue",
                "type": "type",
            },
        )
        class ResourceDetails:
            def __init__(
                self,
                *,
                double_value: typing.Optional[typing.Sequence[builtins.str]] = None,
                integer_value: typing.Optional[typing.Sequence[builtins.str]] = None,
                long_value: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                string_set_value: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ResourceDetails.

                :param double_value: (experimental) doubleValue property. Specify an array of string values to match this event if the actual value of doubleValue is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param integer_value: (experimental) integerValue property. Specify an array of string values to match this event if the actual value of integerValue is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param long_value: (experimental) longValue property. Specify an array of string values to match this event if the actual value of longValue is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param string_set_value: (experimental) stringSetValue property. Specify an array of string values to match this event if the actual value of stringSetValue is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    resource_details = ecs_events.ClusterEvents.ECSContainerInstanceStateChange.ResourceDetails(
                        double_value=["doubleValue"],
                        integer_value=["integerValue"],
                        long_value=["longValue"],
                        name=["name"],
                        string_set_value=["stringSetValue"],
                        type=["type"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__74a5c889c9c9f61be00e4f105e3374a0c76bf8423f6c0e7a5500bb0cd27e8f87)
                    check_type(argname="argument double_value", value=double_value, expected_type=type_hints["double_value"])
                    check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
                    check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument string_set_value", value=string_set_value, expected_type=type_hints["string_set_value"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if double_value is not None:
                    self._values["double_value"] = double_value
                if integer_value is not None:
                    self._values["integer_value"] = integer_value
                if long_value is not None:
                    self._values["long_value"] = long_value
                if name is not None:
                    self._values["name"] = name
                if string_set_value is not None:
                    self._values["string_set_value"] = string_set_value
                if type is not None:
                    self._values["type"] = type

            @builtins.property
            def double_value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) doubleValue property.

                Specify an array of string values to match this event if the actual value of doubleValue is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("double_value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def integer_value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) integerValue property.

                Specify an array of string values to match this event if the actual value of integerValue is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("integer_value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def long_value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) longValue property.

                Specify an array of string values to match this event if the actual value of longValue is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("long_value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def string_set_value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) stringSetValue property.

                Specify an array of string values to match this event if the actual value of stringSetValue is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("string_set_value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResourceDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSContainerInstanceStateChange.VersionInfo",
            jsii_struct_bases=[],
            name_mapping={
                "agent_hash": "agentHash",
                "agent_version": "agentVersion",
                "docker_version": "dockerVersion",
            },
        )
        class VersionInfo:
            def __init__(
                self,
                *,
                agent_hash: typing.Optional[typing.Sequence[builtins.str]] = None,
                agent_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                docker_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for VersionInfo.

                :param agent_hash: (experimental) agentHash property. Specify an array of string values to match this event if the actual value of agentHash is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param agent_version: (experimental) agentVersion property. Specify an array of string values to match this event if the actual value of agentVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param docker_version: (experimental) dockerVersion property. Specify an array of string values to match this event if the actual value of dockerVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    version_info = ecs_events.ClusterEvents.ECSContainerInstanceStateChange.VersionInfo(
                        agent_hash=["agentHash"],
                        agent_version=["agentVersion"],
                        docker_version=["dockerVersion"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__47e7ea87fa9f6fbc789960f61cef985caa305e18a8665ee857e69f03f14d1e79)
                    check_type(argname="argument agent_hash", value=agent_hash, expected_type=type_hints["agent_hash"])
                    check_type(argname="argument agent_version", value=agent_version, expected_type=type_hints["agent_version"])
                    check_type(argname="argument docker_version", value=docker_version, expected_type=type_hints["docker_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if agent_hash is not None:
                    self._values["agent_hash"] = agent_hash
                if agent_version is not None:
                    self._values["agent_version"] = agent_version
                if docker_version is not None:
                    self._values["docker_version"] = docker_version

            @builtins.property
            def agent_hash(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) agentHash property.

                Specify an array of string values to match this event if the actual value of agentHash is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("agent_hash")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def agent_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) agentVersion property.

                Specify an array of string values to match this event if the actual value of agentVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("agent_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def docker_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) dockerVersion property.

                Specify an array of string values to match this event if the actual value of dockerVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("docker_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "VersionInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ECSServiceAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSServiceAction",
    ):
        '''(experimental) aws.ecs@ECSServiceAction event types for Cluster.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
            
            e_cSService_action = ecs_events.ClusterEvents.ECSServiceAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSServiceAction.ECSServiceActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "capacity_provider_arns": "capacityProviderArns",
                "cluster_arn": "clusterArn",
                "container_instance_arns": "containerInstanceArns",
                "container_port": "containerPort",
                "created_at": "createdAt",
                "desired_count": "desiredCount",
                "ec2_instance_ids": "ec2InstanceIds",
                "event_metadata": "eventMetadata",
                "event_name": "eventName",
                "event_type": "eventType",
                "reason": "reason",
                "service_registry_arns": "serviceRegistryArns",
                "target_group_arns": "targetGroupArns",
                "targets": "targets",
                "task_arns": "taskArns",
                "task_set_arns": "taskSetArns",
            },
        )
        class ECSServiceActionProps:
            def __init__(
                self,
                *,
                capacity_provider_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
                cluster_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                container_instance_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
                container_port: typing.Optional[typing.Sequence[builtins.str]] = None,
                created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                desired_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                ec2_instance_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                reason: typing.Optional[typing.Sequence[builtins.str]] = None,
                service_registry_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
                target_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
                targets: typing.Optional[typing.Sequence[builtins.str]] = None,
                task_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
                task_set_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Cluster aws.ecs@ECSServiceAction event.

                :param capacity_provider_arns: (experimental) capacityProviderArns property. Specify an array of string values to match this event if the actual value of capacityProviderArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param cluster_arn: (experimental) clusterArn property. Specify an array of string values to match this event if the actual value of clusterArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Cluster reference
                :param container_instance_arns: (experimental) containerInstanceArns property. Specify an array of string values to match this event if the actual value of containerInstanceArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param container_port: (experimental) containerPort property. Specify an array of string values to match this event if the actual value of containerPort is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param created_at: (experimental) createdAt property. Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param desired_count: (experimental) desiredCount property. Specify an array of string values to match this event if the actual value of desiredCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ec2_instance_ids: (experimental) ec2InstanceIds property. Specify an array of string values to match this event if the actual value of ec2InstanceIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param event_name: (experimental) eventName property. Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reason: (experimental) reason property. Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param service_registry_arns: (experimental) serviceRegistryArns property. Specify an array of string values to match this event if the actual value of serviceRegistryArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param target_group_arns: (experimental) targetGroupArns property. Specify an array of string values to match this event if the actual value of targetGroupArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param targets: (experimental) targets property. Specify an array of string values to match this event if the actual value of targets is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param task_arns: (experimental) taskArns property. Specify an array of string values to match this event if the actual value of taskArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param task_set_arns: (experimental) taskSetArns property. Specify an array of string values to match this event if the actual value of taskSetArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    e_cSService_action_props = ecs_events.ClusterEvents.ECSServiceAction.ECSServiceActionProps(
                        capacity_provider_arns=["capacityProviderArns"],
                        cluster_arn=["clusterArn"],
                        container_instance_arns=["containerInstanceArns"],
                        container_port=["containerPort"],
                        created_at=["createdAt"],
                        desired_count=["desiredCount"],
                        ec2_instance_ids=["ec2InstanceIds"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        event_name=["eventName"],
                        event_type=["eventType"],
                        reason=["reason"],
                        service_registry_arns=["serviceRegistryArns"],
                        target_group_arns=["targetGroupArns"],
                        targets=["targets"],
                        task_arns=["taskArns"],
                        task_set_arns=["taskSetArns"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__63665b4297688d85d048584a5c7d49b7f3bb1b46901a7f78875defc0f56f2f25)
                    check_type(argname="argument capacity_provider_arns", value=capacity_provider_arns, expected_type=type_hints["capacity_provider_arns"])
                    check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
                    check_type(argname="argument container_instance_arns", value=container_instance_arns, expected_type=type_hints["container_instance_arns"])
                    check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
                    check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                    check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
                    check_type(argname="argument ec2_instance_ids", value=ec2_instance_ids, expected_type=type_hints["ec2_instance_ids"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
                    check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
                    check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                    check_type(argname="argument service_registry_arns", value=service_registry_arns, expected_type=type_hints["service_registry_arns"])
                    check_type(argname="argument target_group_arns", value=target_group_arns, expected_type=type_hints["target_group_arns"])
                    check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
                    check_type(argname="argument task_arns", value=task_arns, expected_type=type_hints["task_arns"])
                    check_type(argname="argument task_set_arns", value=task_set_arns, expected_type=type_hints["task_set_arns"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if capacity_provider_arns is not None:
                    self._values["capacity_provider_arns"] = capacity_provider_arns
                if cluster_arn is not None:
                    self._values["cluster_arn"] = cluster_arn
                if container_instance_arns is not None:
                    self._values["container_instance_arns"] = container_instance_arns
                if container_port is not None:
                    self._values["container_port"] = container_port
                if created_at is not None:
                    self._values["created_at"] = created_at
                if desired_count is not None:
                    self._values["desired_count"] = desired_count
                if ec2_instance_ids is not None:
                    self._values["ec2_instance_ids"] = ec2_instance_ids
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if event_name is not None:
                    self._values["event_name"] = event_name
                if event_type is not None:
                    self._values["event_type"] = event_type
                if reason is not None:
                    self._values["reason"] = reason
                if service_registry_arns is not None:
                    self._values["service_registry_arns"] = service_registry_arns
                if target_group_arns is not None:
                    self._values["target_group_arns"] = target_group_arns
                if targets is not None:
                    self._values["targets"] = targets
                if task_arns is not None:
                    self._values["task_arns"] = task_arns
                if task_set_arns is not None:
                    self._values["task_set_arns"] = task_set_arns

            @builtins.property
            def capacity_provider_arns(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) capacityProviderArns property.

                Specify an array of string values to match this event if the actual value of capacityProviderArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("capacity_provider_arns")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def cluster_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) clusterArn property.

                Specify an array of string values to match this event if the actual value of clusterArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Cluster reference

                :stability: experimental
                '''
                result = self._values.get("cluster_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def container_instance_arns(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) containerInstanceArns property.

                Specify an array of string values to match this event if the actual value of containerInstanceArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_instance_arns")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def container_port(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) containerPort property.

                Specify an array of string values to match this event if the actual value of containerPort is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_port")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def created_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) createdAt property.

                Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("created_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def desired_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) desiredCount property.

                Specify an array of string values to match this event if the actual value of desiredCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("desired_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def ec2_instance_ids(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ec2InstanceIds property.

                Specify an array of string values to match this event if the actual value of ec2InstanceIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ec2_instance_ids")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def event_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventName property.

                Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventType property.

                Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def reason(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) reason property.

                Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("reason")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def service_registry_arns(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) serviceRegistryArns property.

                Specify an array of string values to match this event if the actual value of serviceRegistryArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("service_registry_arns")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def target_group_arns(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) targetGroupArns property.

                Specify an array of string values to match this event if the actual value of targetGroupArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("target_group_arns")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def targets(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) targets property.

                Specify an array of string values to match this event if the actual value of targets is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("targets")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def task_arns(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) taskArns property.

                Specify an array of string values to match this event if the actual value of taskArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("task_arns")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def task_set_arns(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) taskSetArns property.

                Specify an array of string values to match this event if the actual value of taskSetArns is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("task_set_arns")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ECSServiceActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ECSTaskStateChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSTaskStateChange",
    ):
        '''(experimental) aws.ecs@ECSTaskStateChange event types for Cluster.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
            
            e_cSTask_state_change = ecs_events.ClusterEvents.ECSTaskStateChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSTaskStateChange.AttachmentDetails",
            jsii_struct_bases=[],
            name_mapping={
                "details": "details",
                "id": "id",
                "status": "status",
                "type": "type",
            },
        )
        class AttachmentDetails:
            def __init__(
                self,
                *,
                details: typing.Optional[typing.Union["ClusterEvents.ECSTaskStateChange.Details", typing.Dict[builtins.str, typing.Any]]] = None,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AttachmentDetails.

                :param details: (experimental) details property. Specify an array of string values to match this event if the actual value of details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    attachment_details = ecs_events.ClusterEvents.ECSTaskStateChange.AttachmentDetails(
                        details=ecs_events.ClusterEvents.ECSTaskStateChange.Details(
                            name=["name"],
                            value=["value"]
                        ),
                        id=["id"],
                        status=["status"],
                        type=["type"]
                    )
                '''
                if isinstance(details, dict):
                    details = ClusterEvents.ECSTaskStateChange.Details(**details)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f035306e2887225c50812f249840c7464f7bded9c133211a00a7e0578e036672)
                    check_type(argname="argument details", value=details, expected_type=type_hints["details"])
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if details is not None:
                    self._values["details"] = details
                if id is not None:
                    self._values["id"] = id
                if status is not None:
                    self._values["status"] = status
                if type is not None:
                    self._values["type"] = type

            @builtins.property
            def details(
                self,
            ) -> typing.Optional["ClusterEvents.ECSTaskStateChange.Details"]:
                '''(experimental) details property.

                Specify an array of string values to match this event if the actual value of details is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("details")
                return typing.cast(typing.Optional["ClusterEvents.ECSTaskStateChange.Details"], result)

            @builtins.property
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status property.

                Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AttachmentDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSTaskStateChange.AttributesDetails",
            jsii_struct_bases=[],
            name_mapping={"name": "name", "value": "value"},
        )
        class AttributesDetails:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                value: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AttributesDetails.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param value: (experimental) value property. Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    attributes_details = ecs_events.ClusterEvents.ECSTaskStateChange.AttributesDetails(
                        name=["name"],
                        value=["value"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3319557df882fc4f77425cd741c169e581c0b3e207cbcb8e099d808684b6ac03)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name
                if value is not None:
                    self._values["value"] = value

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) value property.

                Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AttributesDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSTaskStateChange.ContainerDetails",
            jsii_struct_bases=[],
            name_mapping={
                "container_arn": "containerArn",
                "cpu": "cpu",
                "exit_code": "exitCode",
                "gpu_ids": "gpuIds",
                "image": "image",
                "image_digest": "imageDigest",
                "last_status": "lastStatus",
                "memory": "memory",
                "memory_reservation": "memoryReservation",
                "name": "name",
                "network_bindings": "networkBindings",
                "network_interfaces": "networkInterfaces",
                "reason": "reason",
                "runtime_id": "runtimeId",
                "task_arn": "taskArn",
            },
        )
        class ContainerDetails:
            def __init__(
                self,
                *,
                container_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
                exit_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                gpu_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
                image: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
                last_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                memory: typing.Optional[typing.Sequence[builtins.str]] = None,
                memory_reservation: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                network_bindings: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSTaskStateChange.NetworkBindingDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
                network_interfaces: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSTaskStateChange.NetworkInterfaceDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
                reason: typing.Optional[typing.Sequence[builtins.str]] = None,
                runtime_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                task_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ContainerDetails.

                :param container_arn: (experimental) containerArn property. Specify an array of string values to match this event if the actual value of containerArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param cpu: (experimental) cpu property. Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param exit_code: (experimental) exitCode property. Specify an array of string values to match this event if the actual value of exitCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param gpu_ids: (experimental) gpuIds property. Specify an array of string values to match this event if the actual value of gpuIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image: (experimental) image property. Specify an array of string values to match this event if the actual value of image is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_digest: (experimental) imageDigest property. Specify an array of string values to match this event if the actual value of imageDigest is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param last_status: (experimental) lastStatus property. Specify an array of string values to match this event if the actual value of lastStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param memory: (experimental) memory property. Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param memory_reservation: (experimental) memoryReservation property. Specify an array of string values to match this event if the actual value of memoryReservation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_bindings: (experimental) networkBindings property. Specify an array of string values to match this event if the actual value of networkBindings is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_interfaces: (experimental) networkInterfaces property. Specify an array of string values to match this event if the actual value of networkInterfaces is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reason: (experimental) reason property. Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param runtime_id: (experimental) runtimeId property. Specify an array of string values to match this event if the actual value of runtimeId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param task_arn: (experimental) taskArn property. Specify an array of string values to match this event if the actual value of taskArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    container_details = ecs_events.ClusterEvents.ECSTaskStateChange.ContainerDetails(
                        container_arn=["containerArn"],
                        cpu=["cpu"],
                        exit_code=["exitCode"],
                        gpu_ids=["gpuIds"],
                        image=["image"],
                        image_digest=["imageDigest"],
                        last_status=["lastStatus"],
                        memory=["memory"],
                        memory_reservation=["memoryReservation"],
                        name=["name"],
                        network_bindings=[ecs_events.ClusterEvents.ECSTaskStateChange.NetworkBindingDetails(
                            bind_ip=["bindIp"],
                            container_port=["containerPort"],
                            host_port=["hostPort"],
                            protocol=["protocol"]
                        )],
                        network_interfaces=[ecs_events.ClusterEvents.ECSTaskStateChange.NetworkInterfaceDetails(
                            attachment_id=["attachmentId"],
                            ipv6_address=["ipv6Address"],
                            private_ipv4_address=["privateIpv4Address"]
                        )],
                        reason=["reason"],
                        runtime_id=["runtimeId"],
                        task_arn=["taskArn"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__6684f3821276f91e205ef191dc93dd89161cad271946c2d61412c634502e9799)
                    check_type(argname="argument container_arn", value=container_arn, expected_type=type_hints["container_arn"])
                    check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                    check_type(argname="argument exit_code", value=exit_code, expected_type=type_hints["exit_code"])
                    check_type(argname="argument gpu_ids", value=gpu_ids, expected_type=type_hints["gpu_ids"])
                    check_type(argname="argument image", value=image, expected_type=type_hints["image"])
                    check_type(argname="argument image_digest", value=image_digest, expected_type=type_hints["image_digest"])
                    check_type(argname="argument last_status", value=last_status, expected_type=type_hints["last_status"])
                    check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
                    check_type(argname="argument memory_reservation", value=memory_reservation, expected_type=type_hints["memory_reservation"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument network_bindings", value=network_bindings, expected_type=type_hints["network_bindings"])
                    check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
                    check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                    check_type(argname="argument runtime_id", value=runtime_id, expected_type=type_hints["runtime_id"])
                    check_type(argname="argument task_arn", value=task_arn, expected_type=type_hints["task_arn"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if container_arn is not None:
                    self._values["container_arn"] = container_arn
                if cpu is not None:
                    self._values["cpu"] = cpu
                if exit_code is not None:
                    self._values["exit_code"] = exit_code
                if gpu_ids is not None:
                    self._values["gpu_ids"] = gpu_ids
                if image is not None:
                    self._values["image"] = image
                if image_digest is not None:
                    self._values["image_digest"] = image_digest
                if last_status is not None:
                    self._values["last_status"] = last_status
                if memory is not None:
                    self._values["memory"] = memory
                if memory_reservation is not None:
                    self._values["memory_reservation"] = memory_reservation
                if name is not None:
                    self._values["name"] = name
                if network_bindings is not None:
                    self._values["network_bindings"] = network_bindings
                if network_interfaces is not None:
                    self._values["network_interfaces"] = network_interfaces
                if reason is not None:
                    self._values["reason"] = reason
                if runtime_id is not None:
                    self._values["runtime_id"] = runtime_id
                if task_arn is not None:
                    self._values["task_arn"] = task_arn

            @builtins.property
            def container_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) containerArn property.

                Specify an array of string values to match this event if the actual value of containerArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def cpu(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cpu property.

                Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cpu")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def exit_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) exitCode property.

                Specify an array of string values to match this event if the actual value of exitCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("exit_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def gpu_ids(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) gpuIds property.

                Specify an array of string values to match this event if the actual value of gpuIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("gpu_ids")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image property.

                Specify an array of string values to match this event if the actual value of image is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_digest(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageDigest property.

                Specify an array of string values to match this event if the actual value of imageDigest is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_digest")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def last_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) lastStatus property.

                Specify an array of string values to match this event if the actual value of lastStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("last_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def memory(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) memory property.

                Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("memory")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def memory_reservation(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) memoryReservation property.

                Specify an array of string values to match this event if the actual value of memoryReservation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("memory_reservation")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def network_bindings(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.ECSTaskStateChange.NetworkBindingDetails"]]:
                '''(experimental) networkBindings property.

                Specify an array of string values to match this event if the actual value of networkBindings is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_bindings")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.ECSTaskStateChange.NetworkBindingDetails"]], result)

            @builtins.property
            def network_interfaces(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.ECSTaskStateChange.NetworkInterfaceDetails"]]:
                '''(experimental) networkInterfaces property.

                Specify an array of string values to match this event if the actual value of networkInterfaces is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_interfaces")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.ECSTaskStateChange.NetworkInterfaceDetails"]], result)

            @builtins.property
            def reason(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) reason property.

                Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("reason")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def runtime_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) runtimeId property.

                Specify an array of string values to match this event if the actual value of runtimeId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("runtime_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def task_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) taskArn property.

                Specify an array of string values to match this event if the actual value of taskArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("task_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ContainerDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSTaskStateChange.Details",
            jsii_struct_bases=[],
            name_mapping={"name": "name", "value": "value"},
        )
        class Details:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                value: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for details.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param value: (experimental) value property. Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    details = ecs_events.ClusterEvents.ECSTaskStateChange.Details(
                        name=["name"],
                        value=["value"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7a0bb09cf33c084b2b9da6f8991c14ecdbf101180c0e478177682da9d0c67e86)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name
                if value is not None:
                    self._values["value"] = value

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) value property.

                Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Details(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSTaskStateChange.ECSTaskStateChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "attachments": "attachments",
                "attributes": "attributes",
                "availability_zone": "availabilityZone",
                "cluster_arn": "clusterArn",
                "connectivity": "connectivity",
                "connectivity_at": "connectivityAt",
                "container_instance_arn": "containerInstanceArn",
                "containers": "containers",
                "cpu": "cpu",
                "created_at": "createdAt",
                "desired_status": "desiredStatus",
                "event_metadata": "eventMetadata",
                "execution_stopped_at": "executionStoppedAt",
                "group": "group",
                "last_status": "lastStatus",
                "launch_type": "launchType",
                "memory": "memory",
                "overrides": "overrides",
                "platform_version": "platformVersion",
                "pull_started_at": "pullStartedAt",
                "pull_stopped_at": "pullStoppedAt",
                "started_at": "startedAt",
                "started_by": "startedBy",
                "stop_code": "stopCode",
                "stopped_at": "stoppedAt",
                "stopped_reason": "stoppedReason",
                "stopping_at": "stoppingAt",
                "task_arn": "taskArn",
                "task_definition_arn": "taskDefinitionArn",
                "updated_at": "updatedAt",
                "version": "version",
            },
        )
        class ECSTaskStateChangeProps:
            def __init__(
                self,
                *,
                attachments: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSTaskStateChange.AttachmentDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
                attributes: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSTaskStateChange.AttributesDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
                availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
                cluster_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                connectivity: typing.Optional[typing.Sequence[builtins.str]] = None,
                connectivity_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                container_instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                containers: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSTaskStateChange.ContainerDetails", typing.Dict[builtins.str, typing.Any]]]] = None,
                cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
                created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                desired_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                execution_stopped_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                group: typing.Optional[typing.Sequence[builtins.str]] = None,
                last_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                launch_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                memory: typing.Optional[typing.Sequence[builtins.str]] = None,
                overrides: typing.Optional[typing.Union["ClusterEvents.ECSTaskStateChange.Overrides", typing.Dict[builtins.str, typing.Any]]] = None,
                platform_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                pull_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                pull_stopped_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                started_by: typing.Optional[typing.Sequence[builtins.str]] = None,
                stop_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                stopped_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                stopped_reason: typing.Optional[typing.Sequence[builtins.str]] = None,
                stopping_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                task_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                task_definition_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                updated_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Cluster aws.ecs@ECSTaskStateChange event.

                :param attachments: (experimental) attachments property. Specify an array of string values to match this event if the actual value of attachments is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param attributes: (experimental) attributes property. Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param availability_zone: (experimental) availabilityZone property. Specify an array of string values to match this event if the actual value of availabilityZone is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param cluster_arn: (experimental) clusterArn property. Specify an array of string values to match this event if the actual value of clusterArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Cluster reference
                :param connectivity: (experimental) connectivity property. Specify an array of string values to match this event if the actual value of connectivity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param connectivity_at: (experimental) connectivityAt property. Specify an array of string values to match this event if the actual value of connectivityAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param container_instance_arn: (experimental) containerInstanceArn property. Specify an array of string values to match this event if the actual value of containerInstanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param containers: (experimental) containers property. Specify an array of string values to match this event if the actual value of containers is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param cpu: (experimental) cpu property. Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param created_at: (experimental) createdAt property. Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param desired_status: (experimental) desiredStatus property. Specify an array of string values to match this event if the actual value of desiredStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param execution_stopped_at: (experimental) executionStoppedAt property. Specify an array of string values to match this event if the actual value of executionStoppedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param group: (experimental) group property. Specify an array of string values to match this event if the actual value of group is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param last_status: (experimental) lastStatus property. Specify an array of string values to match this event if the actual value of lastStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param launch_type: (experimental) launchType property. Specify an array of string values to match this event if the actual value of launchType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param memory: (experimental) memory property. Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param overrides: (experimental) overrides property. Specify an array of string values to match this event if the actual value of overrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param platform_version: (experimental) platformVersion property. Specify an array of string values to match this event if the actual value of platformVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param pull_started_at: (experimental) pullStartedAt property. Specify an array of string values to match this event if the actual value of pullStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param pull_stopped_at: (experimental) pullStoppedAt property. Specify an array of string values to match this event if the actual value of pullStoppedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param started_at: (experimental) startedAt property. Specify an array of string values to match this event if the actual value of startedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param started_by: (experimental) startedBy property. Specify an array of string values to match this event if the actual value of startedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param stop_code: (experimental) stopCode property. Specify an array of string values to match this event if the actual value of stopCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param stopped_at: (experimental) stoppedAt property. Specify an array of string values to match this event if the actual value of stoppedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param stopped_reason: (experimental) stoppedReason property. Specify an array of string values to match this event if the actual value of stoppedReason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param stopping_at: (experimental) stoppingAt property. Specify an array of string values to match this event if the actual value of stoppingAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param task_arn: (experimental) taskArn property. Specify an array of string values to match this event if the actual value of taskArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param task_definition_arn: (experimental) taskDefinitionArn property. Specify an array of string values to match this event if the actual value of taskDefinitionArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param updated_at: (experimental) updatedAt property. Specify an array of string values to match this event if the actual value of updatedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    e_cSTask_state_change_props = ecs_events.ClusterEvents.ECSTaskStateChange.ECSTaskStateChangeProps(
                        attachments=[ecs_events.ClusterEvents.ECSTaskStateChange.AttachmentDetails(
                            details=ecs_events.ClusterEvents.ECSTaskStateChange.Details(
                                name=["name"],
                                value=["value"]
                            ),
                            id=["id"],
                            status=["status"],
                            type=["type"]
                        )],
                        attributes=[ecs_events.ClusterEvents.ECSTaskStateChange.AttributesDetails(
                            name=["name"],
                            value=["value"]
                        )],
                        availability_zone=["availabilityZone"],
                        cluster_arn=["clusterArn"],
                        connectivity=["connectivity"],
                        connectivity_at=["connectivityAt"],
                        container_instance_arn=["containerInstanceArn"],
                        containers=[ecs_events.ClusterEvents.ECSTaskStateChange.ContainerDetails(
                            container_arn=["containerArn"],
                            cpu=["cpu"],
                            exit_code=["exitCode"],
                            gpu_ids=["gpuIds"],
                            image=["image"],
                            image_digest=["imageDigest"],
                            last_status=["lastStatus"],
                            memory=["memory"],
                            memory_reservation=["memoryReservation"],
                            name=["name"],
                            network_bindings=[ecs_events.ClusterEvents.ECSTaskStateChange.NetworkBindingDetails(
                                bind_ip=["bindIp"],
                                container_port=["containerPort"],
                                host_port=["hostPort"],
                                protocol=["protocol"]
                            )],
                            network_interfaces=[ecs_events.ClusterEvents.ECSTaskStateChange.NetworkInterfaceDetails(
                                attachment_id=["attachmentId"],
                                ipv6_address=["ipv6Address"],
                                private_ipv4_address=["privateIpv4Address"]
                            )],
                            reason=["reason"],
                            runtime_id=["runtimeId"],
                            task_arn=["taskArn"]
                        )],
                        cpu=["cpu"],
                        created_at=["createdAt"],
                        desired_status=["desiredStatus"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        execution_stopped_at=["executionStoppedAt"],
                        group=["group"],
                        last_status=["lastStatus"],
                        launch_type=["launchType"],
                        memory=["memory"],
                        overrides=ecs_events.ClusterEvents.ECSTaskStateChange.Overrides(
                            container_overrides=[ecs_events.ClusterEvents.ECSTaskStateChange.OverridesItem(
                                command=["command"],
                                cpu=["cpu"],
                                environment=[{
                                    "environment_key": "environment"
                                }],
                                memory=["memory"],
                                name=["name"]
                            )]
                        ),
                        platform_version=["platformVersion"],
                        pull_started_at=["pullStartedAt"],
                        pull_stopped_at=["pullStoppedAt"],
                        started_at=["startedAt"],
                        started_by=["startedBy"],
                        stop_code=["stopCode"],
                        stopped_at=["stoppedAt"],
                        stopped_reason=["stoppedReason"],
                        stopping_at=["stoppingAt"],
                        task_arn=["taskArn"],
                        task_definition_arn=["taskDefinitionArn"],
                        updated_at=["updatedAt"],
                        version=["version"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(overrides, dict):
                    overrides = ClusterEvents.ECSTaskStateChange.Overrides(**overrides)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4ed4ea18353c27a315dce8699d84ba83529d4423745206ca80eb27d9c020199d)
                    check_type(argname="argument attachments", value=attachments, expected_type=type_hints["attachments"])
                    check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                    check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                    check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
                    check_type(argname="argument connectivity", value=connectivity, expected_type=type_hints["connectivity"])
                    check_type(argname="argument connectivity_at", value=connectivity_at, expected_type=type_hints["connectivity_at"])
                    check_type(argname="argument container_instance_arn", value=container_instance_arn, expected_type=type_hints["container_instance_arn"])
                    check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
                    check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                    check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                    check_type(argname="argument desired_status", value=desired_status, expected_type=type_hints["desired_status"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument execution_stopped_at", value=execution_stopped_at, expected_type=type_hints["execution_stopped_at"])
                    check_type(argname="argument group", value=group, expected_type=type_hints["group"])
                    check_type(argname="argument last_status", value=last_status, expected_type=type_hints["last_status"])
                    check_type(argname="argument launch_type", value=launch_type, expected_type=type_hints["launch_type"])
                    check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
                    check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
                    check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
                    check_type(argname="argument pull_started_at", value=pull_started_at, expected_type=type_hints["pull_started_at"])
                    check_type(argname="argument pull_stopped_at", value=pull_stopped_at, expected_type=type_hints["pull_stopped_at"])
                    check_type(argname="argument started_at", value=started_at, expected_type=type_hints["started_at"])
                    check_type(argname="argument started_by", value=started_by, expected_type=type_hints["started_by"])
                    check_type(argname="argument stop_code", value=stop_code, expected_type=type_hints["stop_code"])
                    check_type(argname="argument stopped_at", value=stopped_at, expected_type=type_hints["stopped_at"])
                    check_type(argname="argument stopped_reason", value=stopped_reason, expected_type=type_hints["stopped_reason"])
                    check_type(argname="argument stopping_at", value=stopping_at, expected_type=type_hints["stopping_at"])
                    check_type(argname="argument task_arn", value=task_arn, expected_type=type_hints["task_arn"])
                    check_type(argname="argument task_definition_arn", value=task_definition_arn, expected_type=type_hints["task_definition_arn"])
                    check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if attachments is not None:
                    self._values["attachments"] = attachments
                if attributes is not None:
                    self._values["attributes"] = attributes
                if availability_zone is not None:
                    self._values["availability_zone"] = availability_zone
                if cluster_arn is not None:
                    self._values["cluster_arn"] = cluster_arn
                if connectivity is not None:
                    self._values["connectivity"] = connectivity
                if connectivity_at is not None:
                    self._values["connectivity_at"] = connectivity_at
                if container_instance_arn is not None:
                    self._values["container_instance_arn"] = container_instance_arn
                if containers is not None:
                    self._values["containers"] = containers
                if cpu is not None:
                    self._values["cpu"] = cpu
                if created_at is not None:
                    self._values["created_at"] = created_at
                if desired_status is not None:
                    self._values["desired_status"] = desired_status
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if execution_stopped_at is not None:
                    self._values["execution_stopped_at"] = execution_stopped_at
                if group is not None:
                    self._values["group"] = group
                if last_status is not None:
                    self._values["last_status"] = last_status
                if launch_type is not None:
                    self._values["launch_type"] = launch_type
                if memory is not None:
                    self._values["memory"] = memory
                if overrides is not None:
                    self._values["overrides"] = overrides
                if platform_version is not None:
                    self._values["platform_version"] = platform_version
                if pull_started_at is not None:
                    self._values["pull_started_at"] = pull_started_at
                if pull_stopped_at is not None:
                    self._values["pull_stopped_at"] = pull_stopped_at
                if started_at is not None:
                    self._values["started_at"] = started_at
                if started_by is not None:
                    self._values["started_by"] = started_by
                if stop_code is not None:
                    self._values["stop_code"] = stop_code
                if stopped_at is not None:
                    self._values["stopped_at"] = stopped_at
                if stopped_reason is not None:
                    self._values["stopped_reason"] = stopped_reason
                if stopping_at is not None:
                    self._values["stopping_at"] = stopping_at
                if task_arn is not None:
                    self._values["task_arn"] = task_arn
                if task_definition_arn is not None:
                    self._values["task_definition_arn"] = task_definition_arn
                if updated_at is not None:
                    self._values["updated_at"] = updated_at
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def attachments(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.ECSTaskStateChange.AttachmentDetails"]]:
                '''(experimental) attachments property.

                Specify an array of string values to match this event if the actual value of attachments is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attachments")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.ECSTaskStateChange.AttachmentDetails"]], result)

            @builtins.property
            def attributes(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.ECSTaskStateChange.AttributesDetails"]]:
                '''(experimental) attributes property.

                Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attributes")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.ECSTaskStateChange.AttributesDetails"]], result)

            @builtins.property
            def availability_zone(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) availabilityZone property.

                Specify an array of string values to match this event if the actual value of availabilityZone is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("availability_zone")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def cluster_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) clusterArn property.

                Specify an array of string values to match this event if the actual value of clusterArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Cluster reference

                :stability: experimental
                '''
                result = self._values.get("cluster_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def connectivity(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connectivity property.

                Specify an array of string values to match this event if the actual value of connectivity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("connectivity")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def connectivity_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connectivityAt property.

                Specify an array of string values to match this event if the actual value of connectivityAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("connectivity_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def container_instance_arn(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) containerInstanceArn property.

                Specify an array of string values to match this event if the actual value of containerInstanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_instance_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def containers(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.ECSTaskStateChange.ContainerDetails"]]:
                '''(experimental) containers property.

                Specify an array of string values to match this event if the actual value of containers is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("containers")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.ECSTaskStateChange.ContainerDetails"]], result)

            @builtins.property
            def cpu(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cpu property.

                Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cpu")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def created_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) createdAt property.

                Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("created_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def desired_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) desiredStatus property.

                Specify an array of string values to match this event if the actual value of desiredStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("desired_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def execution_stopped_at(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) executionStoppedAt property.

                Specify an array of string values to match this event if the actual value of executionStoppedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("execution_stopped_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def group(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) group property.

                Specify an array of string values to match this event if the actual value of group is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def last_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) lastStatus property.

                Specify an array of string values to match this event if the actual value of lastStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("last_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def launch_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) launchType property.

                Specify an array of string values to match this event if the actual value of launchType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def memory(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) memory property.

                Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("memory")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def overrides(
                self,
            ) -> typing.Optional["ClusterEvents.ECSTaskStateChange.Overrides"]:
                '''(experimental) overrides property.

                Specify an array of string values to match this event if the actual value of overrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("overrides")
                return typing.cast(typing.Optional["ClusterEvents.ECSTaskStateChange.Overrides"], result)

            @builtins.property
            def platform_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) platformVersion property.

                Specify an array of string values to match this event if the actual value of platformVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("platform_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def pull_started_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) pullStartedAt property.

                Specify an array of string values to match this event if the actual value of pullStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("pull_started_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def pull_stopped_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) pullStoppedAt property.

                Specify an array of string values to match this event if the actual value of pullStoppedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("pull_stopped_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def started_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) startedAt property.

                Specify an array of string values to match this event if the actual value of startedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("started_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def started_by(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) startedBy property.

                Specify an array of string values to match this event if the actual value of startedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("started_by")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def stop_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) stopCode property.

                Specify an array of string values to match this event if the actual value of stopCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("stop_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def stopped_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) stoppedAt property.

                Specify an array of string values to match this event if the actual value of stoppedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("stopped_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def stopped_reason(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) stoppedReason property.

                Specify an array of string values to match this event if the actual value of stoppedReason is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("stopped_reason")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def stopping_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) stoppingAt property.

                Specify an array of string values to match this event if the actual value of stoppingAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("stopping_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def task_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) taskArn property.

                Specify an array of string values to match this event if the actual value of taskArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("task_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def task_definition_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) taskDefinitionArn property.

                Specify an array of string values to match this event if the actual value of taskDefinitionArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("task_definition_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def updated_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) updatedAt property.

                Specify an array of string values to match this event if the actual value of updatedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("updated_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version property.

                Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ECSTaskStateChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSTaskStateChange.NetworkBindingDetails",
            jsii_struct_bases=[],
            name_mapping={
                "bind_ip": "bindIp",
                "container_port": "containerPort",
                "host_port": "hostPort",
                "protocol": "protocol",
            },
        )
        class NetworkBindingDetails:
            def __init__(
                self,
                *,
                bind_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
                container_port: typing.Optional[typing.Sequence[builtins.str]] = None,
                host_port: typing.Optional[typing.Sequence[builtins.str]] = None,
                protocol: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for NetworkBindingDetails.

                :param bind_ip: (experimental) bindIP property. Specify an array of string values to match this event if the actual value of bindIP is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param container_port: (experimental) containerPort property. Specify an array of string values to match this event if the actual value of containerPort is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param host_port: (experimental) hostPort property. Specify an array of string values to match this event if the actual value of hostPort is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param protocol: (experimental) protocol property. Specify an array of string values to match this event if the actual value of protocol is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    network_binding_details = ecs_events.ClusterEvents.ECSTaskStateChange.NetworkBindingDetails(
                        bind_ip=["bindIp"],
                        container_port=["containerPort"],
                        host_port=["hostPort"],
                        protocol=["protocol"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8600c90c760034362730277ff298e6b6ab1ca8961d0c465d6e310a63ded98992)
                    check_type(argname="argument bind_ip", value=bind_ip, expected_type=type_hints["bind_ip"])
                    check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
                    check_type(argname="argument host_port", value=host_port, expected_type=type_hints["host_port"])
                    check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bind_ip is not None:
                    self._values["bind_ip"] = bind_ip
                if container_port is not None:
                    self._values["container_port"] = container_port
                if host_port is not None:
                    self._values["host_port"] = host_port
                if protocol is not None:
                    self._values["protocol"] = protocol

            @builtins.property
            def bind_ip(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bindIP property.

                Specify an array of string values to match this event if the actual value of bindIP is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bind_ip")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def container_port(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) containerPort property.

                Specify an array of string values to match this event if the actual value of containerPort is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_port")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def host_port(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) hostPort property.

                Specify an array of string values to match this event if the actual value of hostPort is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("host_port")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def protocol(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) protocol property.

                Specify an array of string values to match this event if the actual value of protocol is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("protocol")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "NetworkBindingDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSTaskStateChange.NetworkInterfaceDetails",
            jsii_struct_bases=[],
            name_mapping={
                "attachment_id": "attachmentId",
                "ipv6_address": "ipv6Address",
                "private_ipv4_address": "privateIpv4Address",
            },
        )
        class NetworkInterfaceDetails:
            def __init__(
                self,
                *,
                attachment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                ipv6_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                private_ipv4_address: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for NetworkInterfaceDetails.

                :param attachment_id: (experimental) attachmentId property. Specify an array of string values to match this event if the actual value of attachmentId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ipv6_address: (experimental) ipv6Address property. Specify an array of string values to match this event if the actual value of ipv6Address is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param private_ipv4_address: (experimental) privateIpv4Address property. Specify an array of string values to match this event if the actual value of privateIpv4Address is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    network_interface_details = ecs_events.ClusterEvents.ECSTaskStateChange.NetworkInterfaceDetails(
                        attachment_id=["attachmentId"],
                        ipv6_address=["ipv6Address"],
                        private_ipv4_address=["privateIpv4Address"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ab409ca0f92a1abe855408b03b4fa831937915b79b15b277201324ececa525bd)
                    check_type(argname="argument attachment_id", value=attachment_id, expected_type=type_hints["attachment_id"])
                    check_type(argname="argument ipv6_address", value=ipv6_address, expected_type=type_hints["ipv6_address"])
                    check_type(argname="argument private_ipv4_address", value=private_ipv4_address, expected_type=type_hints["private_ipv4_address"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if attachment_id is not None:
                    self._values["attachment_id"] = attachment_id
                if ipv6_address is not None:
                    self._values["ipv6_address"] = ipv6_address
                if private_ipv4_address is not None:
                    self._values["private_ipv4_address"] = private_ipv4_address

            @builtins.property
            def attachment_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) attachmentId property.

                Specify an array of string values to match this event if the actual value of attachmentId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attachment_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def ipv6_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ipv6Address property.

                Specify an array of string values to match this event if the actual value of ipv6Address is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ipv6_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def private_ipv4_address(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) privateIpv4Address property.

                Specify an array of string values to match this event if the actual value of privateIpv4Address is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("private_ipv4_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "NetworkInterfaceDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSTaskStateChange.Overrides",
            jsii_struct_bases=[],
            name_mapping={"container_overrides": "containerOverrides"},
        )
        class Overrides:
            def __init__(
                self,
                *,
                container_overrides: typing.Optional[typing.Sequence[typing.Union["ClusterEvents.ECSTaskStateChange.OverridesItem", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for Overrides.

                :param container_overrides: (experimental) containerOverrides property. Specify an array of string values to match this event if the actual value of containerOverrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    overrides = ecs_events.ClusterEvents.ECSTaskStateChange.Overrides(
                        container_overrides=[ecs_events.ClusterEvents.ECSTaskStateChange.OverridesItem(
                            command=["command"],
                            cpu=["cpu"],
                            environment=[{
                                "environment_key": "environment"
                            }],
                            memory=["memory"],
                            name=["name"]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ec9ecb17aac411e4b19d88024a95e713d2b63445a123b72d9a6906f3a1b5e0b4)
                    check_type(argname="argument container_overrides", value=container_overrides, expected_type=type_hints["container_overrides"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if container_overrides is not None:
                    self._values["container_overrides"] = container_overrides

            @builtins.property
            def container_overrides(
                self,
            ) -> typing.Optional[typing.List["ClusterEvents.ECSTaskStateChange.OverridesItem"]]:
                '''(experimental) containerOverrides property.

                Specify an array of string values to match this event if the actual value of containerOverrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_overrides")
                return typing.cast(typing.Optional[typing.List["ClusterEvents.ECSTaskStateChange.OverridesItem"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Overrides(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecs.events.ClusterEvents.ECSTaskStateChange.OverridesItem",
            jsii_struct_bases=[],
            name_mapping={
                "command": "command",
                "cpu": "cpu",
                "environment": "environment",
                "memory": "memory",
                "name": "name",
            },
        )
        class OverridesItem:
            def __init__(
                self,
                *,
                command: typing.Optional[typing.Sequence[builtins.str]] = None,
                cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
                environment: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
                memory: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for OverridesItem.

                :param command: (experimental) command property. Specify an array of string values to match this event if the actual value of command is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param cpu: (experimental) cpu property. Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param environment: (experimental) environment property. Specify an array of string values to match this event if the actual value of environment is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param memory: (experimental) memory property. Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecs import events as ecs_events
                    
                    overrides_item = ecs_events.ClusterEvents.ECSTaskStateChange.OverridesItem(
                        command=["command"],
                        cpu=["cpu"],
                        environment=[{
                            "environment_key": "environment"
                        }],
                        memory=["memory"],
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f8e93fd8d9fb058a6d78e23581dd145016da9738e0e9b8f563683530936678b7)
                    check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                    check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                    check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
                    check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if command is not None:
                    self._values["command"] = command
                if cpu is not None:
                    self._values["cpu"] = cpu
                if environment is not None:
                    self._values["environment"] = environment
                if memory is not None:
                    self._values["memory"] = memory
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def command(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) command property.

                Specify an array of string values to match this event if the actual value of command is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("command")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def cpu(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cpu property.

                Specify an array of string values to match this event if the actual value of cpu is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cpu")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def environment(
                self,
            ) -> typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]]:
                '''(experimental) environment property.

                Specify an array of string values to match this event if the actual value of environment is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("environment")
                return typing.cast(typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]], result)

            @builtins.property
            def memory(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) memory property.

                Specify an array of string values to match this event if the actual value of memory is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("memory")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "OverridesItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "ClusterEvents",
]

publication.publish()

def _typecheckingstub__6b042faef39d2f05c64c4c0185563eb20eb8a3fc259e9cf791303358aa13d9ec(
    cluster_ref: _aws_cdk_interfaces_aws_ecs_ceddda9d.IClusterRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2751f6a5b6ab4dca4d2635f8840c6c7bce541f228272026bab91df596c2e4c96(
    *,
    aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_parameters: typing.Optional[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.RequestParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    response_elements: typing.Optional[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.ResponseElements, typing.Dict[builtins.str, typing.Any]]] = None,
    source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_identity: typing.Optional[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.UserIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774f462593573cfb62d2ca825924225cf0cf5ef785d9958f95160790a69265a5(
    *,
    creation_date: typing.Optional[typing.Sequence[builtins.str]] = None,
    mfa_authenticated: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24531672e239657b6052396301ee02063137e519fd94f3a7a150c723b406fc7c(
    *,
    assign_public_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e47dfca3a19f7cd2d19d1fac6e930d82a766f0d0ace13e7a2dc40f1ef63b1e5(
    *,
    awsvpc_configuration: typing.Optional[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.AwsvpcConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362d0a473a62c2fa205602be920a5ee2135d3f02ac9cd0664e992f0d9efdd69d(
    *,
    container_overrides: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.OverridesItem, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c11bf4ef4687b7882f293ce5493782553a847065d958bead45f7fb79462d39(
    *,
    container_overrides: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.Overrides1Item, typing.Dict[builtins.str, typing.Any]]]] = None,
    inference_accelerator_overrides: typing.Optional[typing.Sequence[typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49168f44a140b30d3515b7d4e80615b65ad625421dfba1eb632b6bbff2d0691e(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Sequence[typing.Any]] = None,
    memory: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_requirements: typing.Optional[typing.Sequence[typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d36bf7d3e03a5afc12197abea5c97ba5f34622df091641b62dcd294f7c3bdc(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Sequence[typing.Any]] = None,
    memory: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_requirements: typing.Optional[typing.Sequence[typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfbf6f0cade3343137ef53b5428034cebac9f7efc67e9cf3dbc674c17be45136(
    *,
    cluster: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_instance: typing.Optional[typing.Sequence[builtins.str]] = None,
    containers: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem1, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_ecs_managed_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    execution_stopped_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    launch_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_configuration: typing.Optional[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.NetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    overrides: typing.Optional[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.Overrides, typing.Dict[builtins.str, typing.Any]]] = None,
    placement_constraints: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.RequestParametersItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    pull_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    pull_stopped_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    reason: typing.Optional[typing.Sequence[builtins.str]] = None,
    started_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    task: typing.Optional[typing.Sequence[builtins.str]] = None,
    task_definition: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e2aa3ab6c42857d0b1048122116c9033b3e9393bb7714a038f5c23757deffb0(
    *,
    expression: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6141154cb3f914df3a989980e13857065b0afc2fe77c71f1c274e77786d32e06(
    *,
    container_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    exit_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_bindings: typing.Optional[typing.Sequence[typing.Any]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b4cbd9b48826dbe70fd733d96a07838cf087c6122a2d08a53e515522cd6f08(
    *,
    acknowledgment: typing.Optional[typing.Sequence[builtins.str]] = None,
    endpoint: typing.Optional[typing.Sequence[builtins.str]] = None,
    failures: typing.Optional[typing.Sequence[builtins.str]] = None,
    tasks: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    telemetry_endpoint: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8b3469580b1b0420562166033b82072adb9438c411349d9acd2ccc73e2a72a(
    *,
    attachments: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    cluster_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    containers: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItem1, typing.Dict[builtins.str, typing.Any]]]] = None,
    cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
    created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    desired_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    group: typing.Optional[typing.Sequence[builtins.str]] = None,
    last_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    launch_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory: typing.Optional[typing.Sequence[builtins.str]] = None,
    overrides: typing.Optional[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.Overrides1, typing.Dict[builtins.str, typing.Any]]] = None,
    platform_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    started_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Any]] = None,
    task_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    task_definition_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85b68964afd0df58756745bbb2e81a069e8c00d6cb9b203b60e73d0f472f8f8(
    *,
    details: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.ResponseElementsItemItemItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39309d79e2ff26c549e5c49afedf303b2bc0d7753efce6d5329d6dc0088efee1(
    *,
    container_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
    image: typing.Optional[typing.Sequence[builtins.str]] = None,
    last_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_interfaces: typing.Optional[typing.Sequence[typing.Any]] = None,
    task_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14399473b14d14720fb566c96ff8a2b8a8218701c1e3a7034ae3586759cd1f4e(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4461447b51edfabb629fcc63899c00b0858c9f2a1a3b0c655d96cb03945e6e36(
    *,
    attributes: typing.Optional[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    session_issuer: typing.Optional[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.SessionIssuer, typing.Dict[builtins.str, typing.Any]]] = None,
    web_id_federation_data: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d61278c8c3994e8e8c666f5b9b729aceecd2df2a42d830ff1951b82a5a1ab7(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1ade0b52155174dc08f2b615d707e017763cf2076cb408a26286e692f701ef(
    *,
    access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    invoked_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_context: typing.Optional[typing.Union[ClusterEvents.AWSAPICallViaCloudTrail.SessionContext, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920c4d55a30decb878bdd5690610fcfe1a5246ee02c1604b726905859f3751dd(
    *,
    details: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.ECSContainerInstanceStateChange.DetailsItems, typing.Dict[builtins.str, typing.Any]]]] = None,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4711e8481ff08a5d0451015de144783dfc7e286460b4cd0149c25742bf222e78(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8d1c7a5bae5ff833350edbda1f1bce0768bae86ea2f8a50a7dc53a29694d5e(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c391a286041019cf5ce99e641542c121aafff9c70df9c65bb40c392f3ce8b0(
    *,
    account_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    agent_connected: typing.Optional[typing.Sequence[builtins.str]] = None,
    agent_update_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    attachments: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.ECSContainerInstanceStateChange.AttachmentDetails, typing.Dict[builtins.str, typing.Any]]]] = None,
    attributes: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.ECSContainerInstanceStateChange.AttributesDetails, typing.Dict[builtins.str, typing.Any]]]] = None,
    cluster_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    pending_tasks_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    registered_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    registered_resources: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.ECSContainerInstanceStateChange.ResourceDetails, typing.Dict[builtins.str, typing.Any]]]] = None,
    remaining_resources: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.ECSContainerInstanceStateChange.ResourceDetails, typing.Dict[builtins.str, typing.Any]]]] = None,
    running_tasks_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_reason: typing.Optional[typing.Sequence[builtins.str]] = None,
    updated_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
    version_info: typing.Optional[typing.Union[ClusterEvents.ECSContainerInstanceStateChange.VersionInfo, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a5c889c9c9f61be00e4f105e3374a0c76bf8423f6c0e7a5500bb0cd27e8f87(
    *,
    double_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    integer_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    long_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    string_set_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e7ea87fa9f6fbc789960f61cef985caa305e18a8665ee857e69f03f14d1e79(
    *,
    agent_hash: typing.Optional[typing.Sequence[builtins.str]] = None,
    agent_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    docker_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63665b4297688d85d048584a5c7d49b7f3bb1b46901a7f78875defc0f56f2f25(
    *,
    capacity_provider_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    cluster_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_instance_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_port: typing.Optional[typing.Sequence[builtins.str]] = None,
    created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    desired_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    ec2_instance_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    reason: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_registry_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    targets: typing.Optional[typing.Sequence[builtins.str]] = None,
    task_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    task_set_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f035306e2887225c50812f249840c7464f7bded9c133211a00a7e0578e036672(
    *,
    details: typing.Optional[typing.Union[ClusterEvents.ECSTaskStateChange.Details, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3319557df882fc4f77425cd741c169e581c0b3e207cbcb8e099d808684b6ac03(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6684f3821276f91e205ef191dc93dd89161cad271946c2d61412c634502e9799(
    *,
    container_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
    exit_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    gpu_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    image: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
    last_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_reservation: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_bindings: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.ECSTaskStateChange.NetworkBindingDetails, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_interfaces: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.ECSTaskStateChange.NetworkInterfaceDetails, typing.Dict[builtins.str, typing.Any]]]] = None,
    reason: typing.Optional[typing.Sequence[builtins.str]] = None,
    runtime_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    task_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0bb09cf33c084b2b9da6f8991c14ecdbf101180c0e478177682da9d0c67e86(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed4ea18353c27a315dce8699d84ba83529d4423745206ca80eb27d9c020199d(
    *,
    attachments: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.ECSTaskStateChange.AttachmentDetails, typing.Dict[builtins.str, typing.Any]]]] = None,
    attributes: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.ECSTaskStateChange.AttributesDetails, typing.Dict[builtins.str, typing.Any]]]] = None,
    availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
    cluster_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    connectivity: typing.Optional[typing.Sequence[builtins.str]] = None,
    connectivity_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    containers: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.ECSTaskStateChange.ContainerDetails, typing.Dict[builtins.str, typing.Any]]]] = None,
    cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
    created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    desired_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    execution_stopped_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    group: typing.Optional[typing.Sequence[builtins.str]] = None,
    last_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    launch_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory: typing.Optional[typing.Sequence[builtins.str]] = None,
    overrides: typing.Optional[typing.Union[ClusterEvents.ECSTaskStateChange.Overrides, typing.Dict[builtins.str, typing.Any]]] = None,
    platform_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    pull_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    pull_stopped_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    started_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    stop_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    stopped_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    stopped_reason: typing.Optional[typing.Sequence[builtins.str]] = None,
    stopping_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    task_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    task_definition_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    updated_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8600c90c760034362730277ff298e6b6ab1ca8961d0c465d6e310a63ded98992(
    *,
    bind_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_port: typing.Optional[typing.Sequence[builtins.str]] = None,
    host_port: typing.Optional[typing.Sequence[builtins.str]] = None,
    protocol: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab409ca0f92a1abe855408b03b4fa831937915b79b15b277201324ececa525bd(
    *,
    attachment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    ipv6_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_ipv4_address: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9ecb17aac411e4b19d88024a95e713d2b63445a123b72d9a6906f3a1b5e0b4(
    *,
    container_overrides: typing.Optional[typing.Sequence[typing.Union[ClusterEvents.ECSTaskStateChange.OverridesItem, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8e93fd8d9fb058a6d78e23581dd145016da9738e0e9b8f563683530936678b7(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
    memory: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
