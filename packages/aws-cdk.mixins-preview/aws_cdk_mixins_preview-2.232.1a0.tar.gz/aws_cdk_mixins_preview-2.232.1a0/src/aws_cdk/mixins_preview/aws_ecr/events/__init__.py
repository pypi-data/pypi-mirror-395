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
import aws_cdk.interfaces.aws_ecr as _aws_cdk_interfaces_aws_ecr_ceddda9d


class RepositoryEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents",
):
    '''(experimental) EventBridge event patterns for Repository.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
        from aws_cdk.interfaces import aws_ecr as interfaces_ecr
        
        # repository_ref: interfaces_ecr.IRepositoryRef
        
        repository_events = ecr_events.RepositoryEvents.from_repository(repository_ref)
    '''

    @jsii.member(jsii_name="fromRepository")
    @builtins.classmethod
    def from_repository(
        cls,
        repository_ref: _aws_cdk_interfaces_aws_ecr_ceddda9d.IRepositoryRef,
    ) -> "RepositoryEvents":
        '''(experimental) Create RepositoryEvents from a Repository reference.

        :param repository_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db7d74a95b76d6a528e3130a4d9132a0e44009a478c20f752f8693482abc954)
            check_type(argname="argument repository_ref", value=repository_ref, expected_type=type_hints["repository_ref"])
        return typing.cast("RepositoryEvents", jsii.sinvoke(cls, "fromRepository", [repository_ref]))

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
        request_parameters: typing.Optional[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        resources: typing.Optional[typing.Sequence[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem", typing.Dict[builtins.str, typing.Any]]]] = None,
        response_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_identity: typing.Optional[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Repository AWS API Call via CloudTrail.

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
        :param resources: (experimental) resources property. Specify an array of string values to match this event if the actual value of resources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param response_elements: (experimental) responseElements property. Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_ip_address: (experimental) sourceIPAddress property. Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param user_identity: (experimental) userIdentity property. Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = RepositoryEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
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
            resources=resources,
            response_elements=response_elements,
            source_ip_address=source_ip_address,
            user_agent=user_agent,
            user_identity=user_identity,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "awsAPICallViaCloudTrailPattern", [options]))

    @jsii.member(jsii_name="eCRImageActionPattern")
    def e_cr_image_action_pattern(
        self,
        *,
        action_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        artifact_media_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
        manifest_media_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        result: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Repository ECR Image Action.

        :param action_type: (experimental) action-type property. Specify an array of string values to match this event if the actual value of action-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param artifact_media_type: (experimental) artifact-media-type property. Specify an array of string values to match this event if the actual value of artifact-media-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param image_digest: (experimental) image-digest property. Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_tag: (experimental) image-tag property. Specify an array of string values to match this event if the actual value of image-tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param manifest_media_type: (experimental) manifest-media-type property. Specify an array of string values to match this event if the actual value of manifest-media-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param repository_name: (experimental) repository-name property. Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
        :param result: (experimental) result property. Specify an array of string values to match this event if the actual value of result is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = RepositoryEvents.ECRImageAction.ECRImageActionProps(
            action_type=action_type,
            artifact_media_type=artifact_media_type,
            event_metadata=event_metadata,
            image_digest=image_digest,
            image_tag=image_tag,
            manifest_media_type=manifest_media_type,
            repository_name=repository_name,
            result=result,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eCRImageActionPattern", [options]))

    @jsii.member(jsii_name="eCRImageScanPattern")
    def e_cr_image_scan_pattern(
        self,
        *,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        finding_severity_counts: typing.Optional[typing.Union["RepositoryEvents.ECRImageScan.FindingSeverityCounts", typing.Dict[builtins.str, typing.Any]]] = None,
        image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        scan_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Repository ECR Image Scan.

        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param finding_severity_counts: (experimental) finding-severity-counts property. Specify an array of string values to match this event if the actual value of finding-severity-counts is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_digest: (experimental) image-digest property. Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_tags: (experimental) image-tags property. Specify an array of string values to match this event if the actual value of image-tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param repository_name: (experimental) repository-name property. Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
        :param scan_status: (experimental) scan-status property. Specify an array of string values to match this event if the actual value of scan-status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = RepositoryEvents.ECRImageScan.ECRImageScanProps(
            event_metadata=event_metadata,
            finding_severity_counts=finding_severity_counts,
            image_digest=image_digest,
            image_tags=image_tags,
            repository_name=repository_name,
            scan_status=scan_status,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eCRImageScanPattern", [options]))

    @jsii.member(jsii_name="eCRPullThroughCacheActionPattern")
    def e_cr_pull_through_cache_action_pattern(
        self,
        *,
        ecr_repository_prefix: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        failure_reason: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        sync_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        upstream_registry_url: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Repository ECR Pull Through Cache Action.

        :param ecr_repository_prefix: (experimental) ecr-repository-prefix property. Specify an array of string values to match this event if the actual value of ecr-repository-prefix is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param failure_reason: (experimental) failure-reason property. Specify an array of string values to match this event if the actual value of failure-reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_digest: (experimental) image-digest property. Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_tag: (experimental) image-tag property. Specify an array of string values to match this event if the actual value of image-tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param repository_name: (experimental) repository-name property. Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
        :param sync_status: (experimental) sync-status property. Specify an array of string values to match this event if the actual value of sync-status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param upstream_registry_url: (experimental) upstream-registry-url property. Specify an array of string values to match this event if the actual value of upstream-registry-url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = RepositoryEvents.ECRPullThroughCacheAction.ECRPullThroughCacheActionProps(
            ecr_repository_prefix=ecr_repository_prefix,
            event_metadata=event_metadata,
            failure_code=failure_code,
            failure_reason=failure_reason,
            image_digest=image_digest,
            image_tag=image_tag,
            repository_name=repository_name,
            sync_status=sync_status,
            upstream_registry_url=upstream_registry_url,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eCRPullThroughCacheActionPattern", [options]))

    @jsii.member(jsii_name="eCRReferrerActionPattern")
    def e_cr_referrer_action_pattern(
        self,
        *,
        action_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        artifact_media_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
        manifest_media_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        result: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Repository ECR Referrer Action.

        :param action_type: (experimental) action-type property. Specify an array of string values to match this event if the actual value of action-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param artifact_media_type: (experimental) artifact-media-type property. Specify an array of string values to match this event if the actual value of artifact-media-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param image_digest: (experimental) image-digest property. Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_tag: (experimental) image-tag property. Specify an array of string values to match this event if the actual value of image-tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param manifest_media_type: (experimental) manifest-media-type property. Specify an array of string values to match this event if the actual value of manifest-media-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param repository_name: (experimental) repository-name property. Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
        :param result: (experimental) result property. Specify an array of string values to match this event if the actual value of result is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = RepositoryEvents.ECRReferrerAction.ECRReferrerActionProps(
            action_type=action_type,
            artifact_media_type=artifact_media_type,
            event_metadata=event_metadata,
            image_digest=image_digest,
            image_tag=image_tag,
            manifest_media_type=manifest_media_type,
            repository_name=repository_name,
            result=result,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eCRReferrerActionPattern", [options]))

    @jsii.member(jsii_name="eCRReplicationActionPattern")
    def e_cr_replication_action_pattern(
        self,
        *,
        action_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        result: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_account: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_region: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Repository ECR Replication Action.

        :param action_type: (experimental) action-type property. Specify an array of string values to match this event if the actual value of action-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param image_digest: (experimental) image-digest property. Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_tag: (experimental) image-tag property. Specify an array of string values to match this event if the actual value of image-tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param repository_name: (experimental) repository-name property. Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
        :param result: (experimental) result property. Specify an array of string values to match this event if the actual value of result is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_account: (experimental) source-account property. Specify an array of string values to match this event if the actual value of source-account is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_region: (experimental) source-region property. Specify an array of string values to match this event if the actual value of source-region is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = RepositoryEvents.ECRReplicationAction.ECRReplicationActionProps(
            action_type=action_type,
            event_metadata=event_metadata,
            image_digest=image_digest,
            image_tag=image_tag,
            repository_name=repository_name,
            result=result,
            source_account=source_account,
            source_region=source_region,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eCRReplicationActionPattern", [options]))

    class AWSAPICallViaCloudTrail(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.AWSAPICallViaCloudTrail",
    ):
        '''(experimental) aws.ecr@AWSAPICallViaCloudTrail event types for Repository.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
            
            a_wSAPICall_via_cloud_trail = ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps",
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
                "resources": "resources",
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
                request_parameters: typing.Optional[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParameters", typing.Dict[builtins.str, typing.Any]]] = None,
                resources: typing.Optional[typing.Sequence[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                response_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_identity: typing.Optional[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Repository aws.ecr@AWSAPICallViaCloudTrail event.

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
                :param resources: (experimental) resources property. Specify an array of string values to match this event if the actual value of resources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param response_elements: (experimental) responseElements property. Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_ip_address: (experimental) sourceIPAddress property. Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_identity: (experimental) userIdentity property. Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
                    
                    a_wSAPICall_via_cloud_trail_props = ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
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
                        request_parameters=ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParameters(
                            accepted_media_types=["acceptedMediaTypes"],
                            image_ids=[ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem(
                                image_tag=["imageTag"]
                            )],
                            registry_id=["registryId"],
                            repository_name=["repositoryName"]
                        ),
                        resources=[ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem(
                            account_id=["accountId"],
                            arn=["arn"]
                        )],
                        response_elements=["responseElements"],
                        source_ip_address=["sourceIpAddress"],
                        user_agent=["userAgent"],
                        user_identity=ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.UserIdentity(
                            access_key_id=["accessKeyId"],
                            account_id=["accountId"],
                            arn=["arn"],
                            invoked_by=["invokedBy"],
                            principal_id=["principalId"],
                            session_context=ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.SessionContext(
                                attributes=ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.Attributes(
                                    creation_date=["creationDate"],
                                    mfa_authenticated=["mfaAuthenticated"]
                                ),
                                session_issuer=ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.SessionIssuer(
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
                    request_parameters = RepositoryEvents.AWSAPICallViaCloudTrail.RequestParameters(**request_parameters)
                if isinstance(user_identity, dict):
                    user_identity = RepositoryEvents.AWSAPICallViaCloudTrail.UserIdentity(**user_identity)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__524802ca210547c61fbd30f7dc0af0e7c827d74dccf232a4bdacecf681da1e66)
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
                    check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
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
                if resources is not None:
                    self._values["resources"] = resources
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
            ) -> typing.Optional["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParameters"]:
                '''(experimental) requestParameters property.

                Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_parameters")
                return typing.cast(typing.Optional["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParameters"], result)

            @builtins.property
            def resources(
                self,
            ) -> typing.Optional[typing.List["RepositoryEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem"]]:
                '''(experimental) resources property.

                Specify an array of string values to match this event if the actual value of resources is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resources")
                return typing.cast(typing.Optional[typing.List["RepositoryEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem"]], result)

            @builtins.property
            def response_elements(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) responseElements property.

                Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("response_elements")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

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
            ) -> typing.Optional["RepositoryEvents.AWSAPICallViaCloudTrail.UserIdentity"]:
                '''(experimental) userIdentity property.

                Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_identity")
                return typing.cast(typing.Optional["RepositoryEvents.AWSAPICallViaCloudTrail.UserIdentity"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AWSAPICallViaCloudTrailProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.AWSAPICallViaCloudTrail.Attributes",
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
                    from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
                    
                    attributes = ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.Attributes(
                        creation_date=["creationDate"],
                        mfa_authenticated=["mfaAuthenticated"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__329f0ed4aece49a94a7c2905d3a755b5d8a669c2b2e18c04386deac5eeb94f54)
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
            jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem",
            jsii_struct_bases=[],
            name_mapping={"account_id": "accountId", "arn": "arn"},
        )
        class AwsapiCallViaCloudTrailItem:
            def __init__(
                self,
                *,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AWSAPICallViaCloudTrailItem.

                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param arn: (experimental) ARN property. Specify an array of string values to match this event if the actual value of ARN is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
                    
                    awsapi_call_via_cloud_trail_item = ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem(
                        account_id=["accountId"],
                        arn=["arn"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a5f937f90d0813405f86ccbd5d27ffd42912dcfdc0b5524048251dd5cf2c1d2d)
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if account_id is not None:
                    self._values["account_id"] = account_id
                if arn is not None:
                    self._values["arn"] = arn

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
                '''(experimental) ARN property.

                Specify an array of string values to match this event if the actual value of ARN is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AwsapiCallViaCloudTrailItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParameters",
            jsii_struct_bases=[],
            name_mapping={
                "accepted_media_types": "acceptedMediaTypes",
                "image_ids": "imageIds",
                "registry_id": "registryId",
                "repository_name": "repositoryName",
            },
        )
        class RequestParameters:
            def __init__(
                self,
                *,
                accepted_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_ids: typing.Optional[typing.Sequence[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                registry_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParameters.

                :param accepted_media_types: (experimental) acceptedMediaTypes property. Specify an array of string values to match this event if the actual value of acceptedMediaTypes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_ids: (experimental) imageIds property. Specify an array of string values to match this event if the actual value of imageIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param registry_id: (experimental) registryId property. Specify an array of string values to match this event if the actual value of registryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param repository_name: (experimental) repositoryName property. Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
                    
                    request_parameters = ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParameters(
                        accepted_media_types=["acceptedMediaTypes"],
                        image_ids=[ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem(
                            image_tag=["imageTag"]
                        )],
                        registry_id=["registryId"],
                        repository_name=["repositoryName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__54fd40eed8eccc15a3696efc69961b3bfc2fb5baf3889799b0b6d6a6013b5146)
                    check_type(argname="argument accepted_media_types", value=accepted_media_types, expected_type=type_hints["accepted_media_types"])
                    check_type(argname="argument image_ids", value=image_ids, expected_type=type_hints["image_ids"])
                    check_type(argname="argument registry_id", value=registry_id, expected_type=type_hints["registry_id"])
                    check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if accepted_media_types is not None:
                    self._values["accepted_media_types"] = accepted_media_types
                if image_ids is not None:
                    self._values["image_ids"] = image_ids
                if registry_id is not None:
                    self._values["registry_id"] = registry_id
                if repository_name is not None:
                    self._values["repository_name"] = repository_name

            @builtins.property
            def accepted_media_types(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) acceptedMediaTypes property.

                Specify an array of string values to match this event if the actual value of acceptedMediaTypes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("accepted_media_types")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_ids(
                self,
            ) -> typing.Optional[typing.List["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem"]]:
                '''(experimental) imageIds property.

                Specify an array of string values to match this event if the actual value of imageIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_ids")
                return typing.cast(typing.Optional[typing.List["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem"]], result)

            @builtins.property
            def registry_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) registryId property.

                Specify an array of string values to match this event if the actual value of registryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("registry_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def repository_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repositoryName property.

                Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Repository reference

                :stability: experimental
                '''
                result = self._values.get("repository_name")
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
            jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem",
            jsii_struct_bases=[],
            name_mapping={"image_tag": "imageTag"},
        )
        class RequestParametersItem:
            def __init__(
                self,
                *,
                image_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParametersItem.

                :param image_tag: (experimental) imageTag property. Specify an array of string values to match this event if the actual value of imageTag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
                    
                    request_parameters_item = ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem(
                        image_tag=["imageTag"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__b3beb5563511234595ac17365b7a3f51a0abc95d73232587ed77bfc6256736f5)
                    check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if image_tag is not None:
                    self._values["image_tag"] = image_tag

            @builtins.property
            def image_tag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageTag property.

                Specify an array of string values to match this event if the actual value of imageTag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_tag")
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
            jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.AWSAPICallViaCloudTrail.SessionContext",
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
                attributes: typing.Optional[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                session_issuer: typing.Optional[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.SessionIssuer", typing.Dict[builtins.str, typing.Any]]] = None,
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
                    from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
                    
                    session_context = ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.SessionContext(
                        attributes=ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.Attributes(
                            creation_date=["creationDate"],
                            mfa_authenticated=["mfaAuthenticated"]
                        ),
                        session_issuer=ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.SessionIssuer(
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
                    attributes = RepositoryEvents.AWSAPICallViaCloudTrail.Attributes(**attributes)
                if isinstance(session_issuer, dict):
                    session_issuer = RepositoryEvents.AWSAPICallViaCloudTrail.SessionIssuer(**session_issuer)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__05a41c0fc38b157d021a85c444fd65fcdb51c6e26e86230f080abd5497c42a4a)
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
            ) -> typing.Optional["RepositoryEvents.AWSAPICallViaCloudTrail.Attributes"]:
                '''(experimental) attributes property.

                Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attributes")
                return typing.cast(typing.Optional["RepositoryEvents.AWSAPICallViaCloudTrail.Attributes"], result)

            @builtins.property
            def session_issuer(
                self,
            ) -> typing.Optional["RepositoryEvents.AWSAPICallViaCloudTrail.SessionIssuer"]:
                '''(experimental) sessionIssuer property.

                Specify an array of string values to match this event if the actual value of sessionIssuer is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_issuer")
                return typing.cast(typing.Optional["RepositoryEvents.AWSAPICallViaCloudTrail.SessionIssuer"], result)

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
            jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.AWSAPICallViaCloudTrail.SessionIssuer",
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
                    from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
                    
                    session_issuer = ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                        account_id=["accountId"],
                        arn=["arn"],
                        principal_id=["principalId"],
                        type=["type"],
                        user_name=["userName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__c21658c5318e483105ab109667b165bde1306c3720a10ab88370042d5a90c7d2)
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
            jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.AWSAPICallViaCloudTrail.UserIdentity",
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
                session_context: typing.Optional[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.SessionContext", typing.Dict[builtins.str, typing.Any]]] = None,
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
                    from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
                    
                    user_identity = ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.UserIdentity(
                        access_key_id=["accessKeyId"],
                        account_id=["accountId"],
                        arn=["arn"],
                        invoked_by=["invokedBy"],
                        principal_id=["principalId"],
                        session_context=ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.SessionContext(
                            attributes=ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.Attributes(
                                creation_date=["creationDate"],
                                mfa_authenticated=["mfaAuthenticated"]
                            ),
                            session_issuer=ecr_events.RepositoryEvents.AWSAPICallViaCloudTrail.SessionIssuer(
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
                    session_context = RepositoryEvents.AWSAPICallViaCloudTrail.SessionContext(**session_context)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__602bfe983e67d3dacf80ea0bb395565c1094b61b8d48658a4c6eb6198651c3af)
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
            ) -> typing.Optional["RepositoryEvents.AWSAPICallViaCloudTrail.SessionContext"]:
                '''(experimental) sessionContext property.

                Specify an array of string values to match this event if the actual value of sessionContext is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_context")
                return typing.cast(typing.Optional["RepositoryEvents.AWSAPICallViaCloudTrail.SessionContext"], result)

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

    class ECRImageAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.ECRImageAction",
    ):
        '''(experimental) aws.ecr@ECRImageAction event types for Repository.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
            
            e_cRImage_action = ecr_events.RepositoryEvents.ECRImageAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.ECRImageAction.ECRImageActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "action_type": "actionType",
                "artifact_media_type": "artifactMediaType",
                "event_metadata": "eventMetadata",
                "image_digest": "imageDigest",
                "image_tag": "imageTag",
                "manifest_media_type": "manifestMediaType",
                "repository_name": "repositoryName",
                "result": "result",
            },
        )
        class ECRImageActionProps:
            def __init__(
                self,
                *,
                action_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                artifact_media_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
                manifest_media_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                result: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Repository aws.ecr@ECRImageAction event.

                :param action_type: (experimental) action-type property. Specify an array of string values to match this event if the actual value of action-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param artifact_media_type: (experimental) artifact-media-type property. Specify an array of string values to match this event if the actual value of artifact-media-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param image_digest: (experimental) image-digest property. Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_tag: (experimental) image-tag property. Specify an array of string values to match this event if the actual value of image-tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param manifest_media_type: (experimental) manifest-media-type property. Specify an array of string values to match this event if the actual value of manifest-media-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param repository_name: (experimental) repository-name property. Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
                :param result: (experimental) result property. Specify an array of string values to match this event if the actual value of result is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
                    
                    e_cRImage_action_props = ecr_events.RepositoryEvents.ECRImageAction.ECRImageActionProps(
                        action_type=["actionType"],
                        artifact_media_type=["artifactMediaType"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        image_digest=["imageDigest"],
                        image_tag=["imageTag"],
                        manifest_media_type=["manifestMediaType"],
                        repository_name=["repositoryName"],
                        result=["result"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__febfb15a821b9694b0ba4098be84a7a33f17acc79e03887fd72ba7d62a9a2eb7)
                    check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
                    check_type(argname="argument artifact_media_type", value=artifact_media_type, expected_type=type_hints["artifact_media_type"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument image_digest", value=image_digest, expected_type=type_hints["image_digest"])
                    check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
                    check_type(argname="argument manifest_media_type", value=manifest_media_type, expected_type=type_hints["manifest_media_type"])
                    check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
                    check_type(argname="argument result", value=result, expected_type=type_hints["result"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action_type is not None:
                    self._values["action_type"] = action_type
                if artifact_media_type is not None:
                    self._values["artifact_media_type"] = artifact_media_type
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if image_digest is not None:
                    self._values["image_digest"] = image_digest
                if image_tag is not None:
                    self._values["image_tag"] = image_tag
                if manifest_media_type is not None:
                    self._values["manifest_media_type"] = manifest_media_type
                if repository_name is not None:
                    self._values["repository_name"] = repository_name
                if result is not None:
                    self._values["result"] = result

            @builtins.property
            def action_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) action-type property.

                Specify an array of string values to match this event if the actual value of action-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def artifact_media_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) artifact-media-type property.

                Specify an array of string values to match this event if the actual value of artifact-media-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("artifact_media_type")
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
            def image_digest(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image-digest property.

                Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_digest")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_tag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image-tag property.

                Specify an array of string values to match this event if the actual value of image-tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_tag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def manifest_media_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) manifest-media-type property.

                Specify an array of string values to match this event if the actual value of manifest-media-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("manifest_media_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def repository_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repository-name property.

                Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Repository reference

                :stability: experimental
                '''
                result = self._values.get("repository_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def result(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) result property.

                Specify an array of string values to match this event if the actual value of result is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("result")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ECRImageActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ECRImageScan(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.ECRImageScan",
    ):
        '''(experimental) aws.ecr@ECRImageScan event types for Repository.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
            
            e_cRImage_scan = ecr_events.RepositoryEvents.ECRImageScan()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.ECRImageScan.ECRImageScanProps",
            jsii_struct_bases=[],
            name_mapping={
                "event_metadata": "eventMetadata",
                "finding_severity_counts": "findingSeverityCounts",
                "image_digest": "imageDigest",
                "image_tags": "imageTags",
                "repository_name": "repositoryName",
                "scan_status": "scanStatus",
            },
        )
        class ECRImageScanProps:
            def __init__(
                self,
                *,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                finding_severity_counts: typing.Optional[typing.Union["RepositoryEvents.ECRImageScan.FindingSeverityCounts", typing.Dict[builtins.str, typing.Any]]] = None,
                image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                scan_status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Repository aws.ecr@ECRImageScan event.

                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param finding_severity_counts: (experimental) finding-severity-counts property. Specify an array of string values to match this event if the actual value of finding-severity-counts is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_digest: (experimental) image-digest property. Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_tags: (experimental) image-tags property. Specify an array of string values to match this event if the actual value of image-tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param repository_name: (experimental) repository-name property. Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
                :param scan_status: (experimental) scan-status property. Specify an array of string values to match this event if the actual value of scan-status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
                    
                    e_cRImage_scan_props = ecr_events.RepositoryEvents.ECRImageScan.ECRImageScanProps(
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        finding_severity_counts=ecr_events.RepositoryEvents.ECRImageScan.FindingSeverityCounts(
                            critical=["critical"],
                            high=["high"],
                            informational=["informational"],
                            low=["low"],
                            medium=["medium"],
                            undefined=["undefined"]
                        ),
                        image_digest=["imageDigest"],
                        image_tags=["imageTags"],
                        repository_name=["repositoryName"],
                        scan_status=["scanStatus"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(finding_severity_counts, dict):
                    finding_severity_counts = RepositoryEvents.ECRImageScan.FindingSeverityCounts(**finding_severity_counts)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3025515e7721c328eb8f17d79b4743d5ae438817729408b1845d64a8f277ccf2)
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument finding_severity_counts", value=finding_severity_counts, expected_type=type_hints["finding_severity_counts"])
                    check_type(argname="argument image_digest", value=image_digest, expected_type=type_hints["image_digest"])
                    check_type(argname="argument image_tags", value=image_tags, expected_type=type_hints["image_tags"])
                    check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
                    check_type(argname="argument scan_status", value=scan_status, expected_type=type_hints["scan_status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if finding_severity_counts is not None:
                    self._values["finding_severity_counts"] = finding_severity_counts
                if image_digest is not None:
                    self._values["image_digest"] = image_digest
                if image_tags is not None:
                    self._values["image_tags"] = image_tags
                if repository_name is not None:
                    self._values["repository_name"] = repository_name
                if scan_status is not None:
                    self._values["scan_status"] = scan_status

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
            def finding_severity_counts(
                self,
            ) -> typing.Optional["RepositoryEvents.ECRImageScan.FindingSeverityCounts"]:
                '''(experimental) finding-severity-counts property.

                Specify an array of string values to match this event if the actual value of finding-severity-counts is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("finding_severity_counts")
                return typing.cast(typing.Optional["RepositoryEvents.ECRImageScan.FindingSeverityCounts"], result)

            @builtins.property
            def image_digest(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image-digest property.

                Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_digest")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_tags(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image-tags property.

                Specify an array of string values to match this event if the actual value of image-tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_tags")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def repository_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repository-name property.

                Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Repository reference

                :stability: experimental
                '''
                result = self._values.get("repository_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def scan_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) scan-status property.

                Specify an array of string values to match this event if the actual value of scan-status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("scan_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ECRImageScanProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.ECRImageScan.FindingSeverityCounts",
            jsii_struct_bases=[],
            name_mapping={
                "critical": "critical",
                "high": "high",
                "informational": "informational",
                "low": "low",
                "medium": "medium",
                "undefined": "undefined",
            },
        )
        class FindingSeverityCounts:
            def __init__(
                self,
                *,
                critical: typing.Optional[typing.Sequence[builtins.str]] = None,
                high: typing.Optional[typing.Sequence[builtins.str]] = None,
                informational: typing.Optional[typing.Sequence[builtins.str]] = None,
                low: typing.Optional[typing.Sequence[builtins.str]] = None,
                medium: typing.Optional[typing.Sequence[builtins.str]] = None,
                undefined: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for FindingSeverityCounts.

                :param critical: (experimental) CRITICAL property. Specify an array of string values to match this event if the actual value of CRITICAL is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param high: (experimental) HIGH property. Specify an array of string values to match this event if the actual value of HIGH is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param informational: (experimental) INFORMATIONAL property. Specify an array of string values to match this event if the actual value of INFORMATIONAL is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param low: (experimental) LOW property. Specify an array of string values to match this event if the actual value of LOW is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param medium: (experimental) MEDIUM property. Specify an array of string values to match this event if the actual value of MEDIUM is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param undefined: (experimental) UNDEFINED property. Specify an array of string values to match this event if the actual value of UNDEFINED is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
                    
                    finding_severity_counts = ecr_events.RepositoryEvents.ECRImageScan.FindingSeverityCounts(
                        critical=["critical"],
                        high=["high"],
                        informational=["informational"],
                        low=["low"],
                        medium=["medium"],
                        undefined=["undefined"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__312a01c1c418371b4c697b62ceeb148122926a23e561b42a354c66a206e98f92)
                    check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
                    check_type(argname="argument high", value=high, expected_type=type_hints["high"])
                    check_type(argname="argument informational", value=informational, expected_type=type_hints["informational"])
                    check_type(argname="argument low", value=low, expected_type=type_hints["low"])
                    check_type(argname="argument medium", value=medium, expected_type=type_hints["medium"])
                    check_type(argname="argument undefined", value=undefined, expected_type=type_hints["undefined"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if critical is not None:
                    self._values["critical"] = critical
                if high is not None:
                    self._values["high"] = high
                if informational is not None:
                    self._values["informational"] = informational
                if low is not None:
                    self._values["low"] = low
                if medium is not None:
                    self._values["medium"] = medium
                if undefined is not None:
                    self._values["undefined"] = undefined

            @builtins.property
            def critical(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) CRITICAL property.

                Specify an array of string values to match this event if the actual value of CRITICAL is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("critical")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def high(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) HIGH property.

                Specify an array of string values to match this event if the actual value of HIGH is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("high")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def informational(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) INFORMATIONAL property.

                Specify an array of string values to match this event if the actual value of INFORMATIONAL is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("informational")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def low(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) LOW property.

                Specify an array of string values to match this event if the actual value of LOW is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("low")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def medium(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) MEDIUM property.

                Specify an array of string values to match this event if the actual value of MEDIUM is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("medium")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def undefined(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) UNDEFINED property.

                Specify an array of string values to match this event if the actual value of UNDEFINED is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("undefined")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "FindingSeverityCounts(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ECRPullThroughCacheAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.ECRPullThroughCacheAction",
    ):
        '''(experimental) aws.ecr@ECRPullThroughCacheAction event types for Repository.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
            
            e_cRPull_through_cache_action = ecr_events.RepositoryEvents.ECRPullThroughCacheAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.ECRPullThroughCacheAction.ECRPullThroughCacheActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "ecr_repository_prefix": "ecrRepositoryPrefix",
                "event_metadata": "eventMetadata",
                "failure_code": "failureCode",
                "failure_reason": "failureReason",
                "image_digest": "imageDigest",
                "image_tag": "imageTag",
                "repository_name": "repositoryName",
                "sync_status": "syncStatus",
                "upstream_registry_url": "upstreamRegistryUrl",
            },
        )
        class ECRPullThroughCacheActionProps:
            def __init__(
                self,
                *,
                ecr_repository_prefix: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                failure_reason: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                sync_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                upstream_registry_url: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Repository aws.ecr@ECRPullThroughCacheAction event.

                :param ecr_repository_prefix: (experimental) ecr-repository-prefix property. Specify an array of string values to match this event if the actual value of ecr-repository-prefix is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param failure_reason: (experimental) failure-reason property. Specify an array of string values to match this event if the actual value of failure-reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_digest: (experimental) image-digest property. Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_tag: (experimental) image-tag property. Specify an array of string values to match this event if the actual value of image-tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param repository_name: (experimental) repository-name property. Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
                :param sync_status: (experimental) sync-status property. Specify an array of string values to match this event if the actual value of sync-status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param upstream_registry_url: (experimental) upstream-registry-url property. Specify an array of string values to match this event if the actual value of upstream-registry-url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
                    
                    e_cRPull_through_cache_action_props = ecr_events.RepositoryEvents.ECRPullThroughCacheAction.ECRPullThroughCacheActionProps(
                        ecr_repository_prefix=["ecrRepositoryPrefix"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        failure_code=["failureCode"],
                        failure_reason=["failureReason"],
                        image_digest=["imageDigest"],
                        image_tag=["imageTag"],
                        repository_name=["repositoryName"],
                        sync_status=["syncStatus"],
                        upstream_registry_url=["upstreamRegistryUrl"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4f1711042336ba75e6d5f627864deebdf7b61ecad6031b43b0e408f4c58d1da8)
                    check_type(argname="argument ecr_repository_prefix", value=ecr_repository_prefix, expected_type=type_hints["ecr_repository_prefix"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument failure_code", value=failure_code, expected_type=type_hints["failure_code"])
                    check_type(argname="argument failure_reason", value=failure_reason, expected_type=type_hints["failure_reason"])
                    check_type(argname="argument image_digest", value=image_digest, expected_type=type_hints["image_digest"])
                    check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
                    check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
                    check_type(argname="argument sync_status", value=sync_status, expected_type=type_hints["sync_status"])
                    check_type(argname="argument upstream_registry_url", value=upstream_registry_url, expected_type=type_hints["upstream_registry_url"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if ecr_repository_prefix is not None:
                    self._values["ecr_repository_prefix"] = ecr_repository_prefix
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if failure_code is not None:
                    self._values["failure_code"] = failure_code
                if failure_reason is not None:
                    self._values["failure_reason"] = failure_reason
                if image_digest is not None:
                    self._values["image_digest"] = image_digest
                if image_tag is not None:
                    self._values["image_tag"] = image_tag
                if repository_name is not None:
                    self._values["repository_name"] = repository_name
                if sync_status is not None:
                    self._values["sync_status"] = sync_status
                if upstream_registry_url is not None:
                    self._values["upstream_registry_url"] = upstream_registry_url

            @builtins.property
            def ecr_repository_prefix(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ecr-repository-prefix property.

                Specify an array of string values to match this event if the actual value of ecr-repository-prefix is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ecr_repository_prefix")
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
            def failure_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) failure-code property.

                Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("failure_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def failure_reason(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) failure-reason property.

                Specify an array of string values to match this event if the actual value of failure-reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("failure_reason")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_digest(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image-digest property.

                Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_digest")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_tag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image-tag property.

                Specify an array of string values to match this event if the actual value of image-tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_tag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def repository_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repository-name property.

                Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Repository reference

                :stability: experimental
                '''
                result = self._values.get("repository_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def sync_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sync-status property.

                Specify an array of string values to match this event if the actual value of sync-status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("sync_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def upstream_registry_url(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) upstream-registry-url property.

                Specify an array of string values to match this event if the actual value of upstream-registry-url is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("upstream_registry_url")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ECRPullThroughCacheActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ECRReferrerAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.ECRReferrerAction",
    ):
        '''(experimental) aws.ecr@ECRReferrerAction event types for Repository.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
            
            e_cRReferrer_action = ecr_events.RepositoryEvents.ECRReferrerAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.ECRReferrerAction.ECRReferrerActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "action_type": "actionType",
                "artifact_media_type": "artifactMediaType",
                "event_metadata": "eventMetadata",
                "image_digest": "imageDigest",
                "image_tag": "imageTag",
                "manifest_media_type": "manifestMediaType",
                "repository_name": "repositoryName",
                "result": "result",
            },
        )
        class ECRReferrerActionProps:
            def __init__(
                self,
                *,
                action_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                artifact_media_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
                manifest_media_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                result: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Repository aws.ecr@ECRReferrerAction event.

                :param action_type: (experimental) action-type property. Specify an array of string values to match this event if the actual value of action-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param artifact_media_type: (experimental) artifact-media-type property. Specify an array of string values to match this event if the actual value of artifact-media-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param image_digest: (experimental) image-digest property. Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_tag: (experimental) image-tag property. Specify an array of string values to match this event if the actual value of image-tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param manifest_media_type: (experimental) manifest-media-type property. Specify an array of string values to match this event if the actual value of manifest-media-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param repository_name: (experimental) repository-name property. Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
                :param result: (experimental) result property. Specify an array of string values to match this event if the actual value of result is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
                    
                    e_cRReferrer_action_props = ecr_events.RepositoryEvents.ECRReferrerAction.ECRReferrerActionProps(
                        action_type=["actionType"],
                        artifact_media_type=["artifactMediaType"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        image_digest=["imageDigest"],
                        image_tag=["imageTag"],
                        manifest_media_type=["manifestMediaType"],
                        repository_name=["repositoryName"],
                        result=["result"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__0148e0658e96e1fcc0d66a86fa5ad261ee46ec898b818bba343a8418ce3dd8ae)
                    check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
                    check_type(argname="argument artifact_media_type", value=artifact_media_type, expected_type=type_hints["artifact_media_type"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument image_digest", value=image_digest, expected_type=type_hints["image_digest"])
                    check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
                    check_type(argname="argument manifest_media_type", value=manifest_media_type, expected_type=type_hints["manifest_media_type"])
                    check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
                    check_type(argname="argument result", value=result, expected_type=type_hints["result"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action_type is not None:
                    self._values["action_type"] = action_type
                if artifact_media_type is not None:
                    self._values["artifact_media_type"] = artifact_media_type
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if image_digest is not None:
                    self._values["image_digest"] = image_digest
                if image_tag is not None:
                    self._values["image_tag"] = image_tag
                if manifest_media_type is not None:
                    self._values["manifest_media_type"] = manifest_media_type
                if repository_name is not None:
                    self._values["repository_name"] = repository_name
                if result is not None:
                    self._values["result"] = result

            @builtins.property
            def action_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) action-type property.

                Specify an array of string values to match this event if the actual value of action-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def artifact_media_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) artifact-media-type property.

                Specify an array of string values to match this event if the actual value of artifact-media-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("artifact_media_type")
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
            def image_digest(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image-digest property.

                Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_digest")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_tag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image-tag property.

                Specify an array of string values to match this event if the actual value of image-tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_tag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def manifest_media_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) manifest-media-type property.

                Specify an array of string values to match this event if the actual value of manifest-media-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("manifest_media_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def repository_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repository-name property.

                Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Repository reference

                :stability: experimental
                '''
                result = self._values.get("repository_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def result(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) result property.

                Specify an array of string values to match this event if the actual value of result is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("result")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ECRReferrerActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ECRReplicationAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.ECRReplicationAction",
    ):
        '''(experimental) aws.ecr@ECRReplicationAction event types for Repository.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
            
            e_cRReplication_action = ecr_events.RepositoryEvents.ECRReplicationAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ecr.events.RepositoryEvents.ECRReplicationAction.ECRReplicationActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "action_type": "actionType",
                "event_metadata": "eventMetadata",
                "image_digest": "imageDigest",
                "image_tag": "imageTag",
                "repository_name": "repositoryName",
                "result": "result",
                "source_account": "sourceAccount",
                "source_region": "sourceRegion",
            },
        )
        class ECRReplicationActionProps:
            def __init__(
                self,
                *,
                action_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                result: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_account: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_region: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Repository aws.ecr@ECRReplicationAction event.

                :param action_type: (experimental) action-type property. Specify an array of string values to match this event if the actual value of action-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param image_digest: (experimental) image-digest property. Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_tag: (experimental) image-tag property. Specify an array of string values to match this event if the actual value of image-tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param repository_name: (experimental) repository-name property. Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
                :param result: (experimental) result property. Specify an array of string values to match this event if the actual value of result is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_account: (experimental) source-account property. Specify an array of string values to match this event if the actual value of source-account is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_region: (experimental) source-region property. Specify an array of string values to match this event if the actual value of source-region is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ecr import events as ecr_events
                    
                    e_cRReplication_action_props = ecr_events.RepositoryEvents.ECRReplicationAction.ECRReplicationActionProps(
                        action_type=["actionType"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        image_digest=["imageDigest"],
                        image_tag=["imageTag"],
                        repository_name=["repositoryName"],
                        result=["result"],
                        source_account=["sourceAccount"],
                        source_region=["sourceRegion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__550340fcfaf6b8849386835d997158ab1cd29414e4da95ebdb4f958e4c545732)
                    check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument image_digest", value=image_digest, expected_type=type_hints["image_digest"])
                    check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
                    check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
                    check_type(argname="argument result", value=result, expected_type=type_hints["result"])
                    check_type(argname="argument source_account", value=source_account, expected_type=type_hints["source_account"])
                    check_type(argname="argument source_region", value=source_region, expected_type=type_hints["source_region"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action_type is not None:
                    self._values["action_type"] = action_type
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if image_digest is not None:
                    self._values["image_digest"] = image_digest
                if image_tag is not None:
                    self._values["image_tag"] = image_tag
                if repository_name is not None:
                    self._values["repository_name"] = repository_name
                if result is not None:
                    self._values["result"] = result
                if source_account is not None:
                    self._values["source_account"] = source_account
                if source_region is not None:
                    self._values["source_region"] = source_region

            @builtins.property
            def action_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) action-type property.

                Specify an array of string values to match this event if the actual value of action-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action_type")
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
            def image_digest(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image-digest property.

                Specify an array of string values to match this event if the actual value of image-digest is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_digest")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_tag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image-tag property.

                Specify an array of string values to match this event if the actual value of image-tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_tag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def repository_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repository-name property.

                Specify an array of string values to match this event if the actual value of repository-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Repository reference

                :stability: experimental
                '''
                result = self._values.get("repository_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def result(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) result property.

                Specify an array of string values to match this event if the actual value of result is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("result")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_account(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) source-account property.

                Specify an array of string values to match this event if the actual value of source-account is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_account")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_region(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) source-region property.

                Specify an array of string values to match this event if the actual value of source-region is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_region")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ECRReplicationActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "RepositoryEvents",
]

publication.publish()

def _typecheckingstub__3db7d74a95b76d6a528e3130a4d9132a0e44009a478c20f752f8693482abc954(
    repository_ref: _aws_cdk_interfaces_aws_ecr_ceddda9d.IRepositoryRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524802ca210547c61fbd30f7dc0af0e7c827d74dccf232a4bdacecf681da1e66(
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
    request_parameters: typing.Optional[typing.Union[RepositoryEvents.AWSAPICallViaCloudTrail.RequestParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    resources: typing.Optional[typing.Sequence[typing.Union[RepositoryEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    response_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_identity: typing.Optional[typing.Union[RepositoryEvents.AWSAPICallViaCloudTrail.UserIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329f0ed4aece49a94a7c2905d3a755b5d8a669c2b2e18c04386deac5eeb94f54(
    *,
    creation_date: typing.Optional[typing.Sequence[builtins.str]] = None,
    mfa_authenticated: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f937f90d0813405f86ccbd5d27ffd42912dcfdc0b5524048251dd5cf2c1d2d(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54fd40eed8eccc15a3696efc69961b3bfc2fb5baf3889799b0b6d6a6013b5146(
    *,
    accepted_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_ids: typing.Optional[typing.Sequence[typing.Union[RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    registry_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3beb5563511234595ac17365b7a3f51a0abc95d73232587ed77bfc6256736f5(
    *,
    image_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a41c0fc38b157d021a85c444fd65fcdb51c6e26e86230f080abd5497c42a4a(
    *,
    attributes: typing.Optional[typing.Union[RepositoryEvents.AWSAPICallViaCloudTrail.Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    session_issuer: typing.Optional[typing.Union[RepositoryEvents.AWSAPICallViaCloudTrail.SessionIssuer, typing.Dict[builtins.str, typing.Any]]] = None,
    web_id_federation_data: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21658c5318e483105ab109667b165bde1306c3720a10ab88370042d5a90c7d2(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602bfe983e67d3dacf80ea0bb395565c1094b61b8d48658a4c6eb6198651c3af(
    *,
    access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    invoked_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_context: typing.Optional[typing.Union[RepositoryEvents.AWSAPICallViaCloudTrail.SessionContext, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__febfb15a821b9694b0ba4098be84a7a33f17acc79e03887fd72ba7d62a9a2eb7(
    *,
    action_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    artifact_media_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
    manifest_media_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    result: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3025515e7721c328eb8f17d79b4743d5ae438817729408b1845d64a8f277ccf2(
    *,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    finding_severity_counts: typing.Optional[typing.Union[RepositoryEvents.ECRImageScan.FindingSeverityCounts, typing.Dict[builtins.str, typing.Any]]] = None,
    image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    scan_status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312a01c1c418371b4c697b62ceeb148122926a23e561b42a354c66a206e98f92(
    *,
    critical: typing.Optional[typing.Sequence[builtins.str]] = None,
    high: typing.Optional[typing.Sequence[builtins.str]] = None,
    informational: typing.Optional[typing.Sequence[builtins.str]] = None,
    low: typing.Optional[typing.Sequence[builtins.str]] = None,
    medium: typing.Optional[typing.Sequence[builtins.str]] = None,
    undefined: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1711042336ba75e6d5f627864deebdf7b61ecad6031b43b0e408f4c58d1da8(
    *,
    ecr_repository_prefix: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    failure_reason: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    sync_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    upstream_registry_url: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0148e0658e96e1fcc0d66a86fa5ad261ee46ec898b818bba343a8418ce3dd8ae(
    *,
    action_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    artifact_media_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
    manifest_media_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    result: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__550340fcfaf6b8849386835d997158ab1cd29414e4da95ebdb4f958e4c545732(
    *,
    action_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_digest: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    result: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_account: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_region: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
