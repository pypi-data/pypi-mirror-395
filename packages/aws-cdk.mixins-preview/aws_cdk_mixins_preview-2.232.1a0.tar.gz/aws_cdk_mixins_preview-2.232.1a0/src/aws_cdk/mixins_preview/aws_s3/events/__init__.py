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
import aws_cdk.interfaces.aws_s3 as _aws_cdk_interfaces_aws_s3_ceddda9d


class BucketEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents",
):
    '''(experimental) EventBridge event patterns for Bucket.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.mixins_preview.aws_s3.events import BucketEvents
        
        # bucket: s3.Bucket
        
        bucket_events = BucketEvents.from_bucket(bucket)
        
        pattern = bucket_events.object_created_pattern(
            event_metadata=AWSEventMetadataProps(
                region=["us-east-1", "us-west-2"],
                version=["0"]
            )
        )
    '''

    @jsii.member(jsii_name="fromBucket")
    @builtins.classmethod
    def from_bucket(
        cls,
        bucket_ref: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "BucketEvents":
        '''(experimental) Create BucketEvents from a Bucket reference.

        :param bucket_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8845cfe51d7496b37755a7037f2d27a6431cd115419057db034a1a305c26d0cf)
            check_type(argname="argument bucket_ref", value=bucket_ref, expected_type=type_hints["bucket_ref"])
        return typing.cast("BucketEvents", jsii.sinvoke(cls, "fromBucket", [bucket_ref]))

    @jsii.member(jsii_name="awsAPICallViaCloudTrailPattern")
    def aws_api_call_via_cloud_trail_pattern(
        self,
        *,
        additional_event_data: typing.Optional[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.AdditionalEventData", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_category: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        management_event: typing.Optional[typing.Sequence[builtins.str]] = None,
        read_only: typing.Optional[typing.Sequence[builtins.str]] = None,
        recipient_account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_parameters: typing.Optional[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.RequestParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        resources: typing.Optional[typing.Sequence[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem", typing.Dict[builtins.str, typing.Any]]]] = None,
        response_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        tls_details: typing.Optional[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.TlsDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_identity: typing.Optional[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_endpoint_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Bucket AWS API Call via CloudTrail.

        :param additional_event_data: (experimental) additionalEventData property. Specify an array of string values to match this event if the actual value of additionalEventData is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param aws_region: (experimental) awsRegion property. Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_category: (experimental) eventCategory property. Specify an array of string values to match this event if the actual value of eventCategory is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_id: (experimental) eventID property. Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param event_name: (experimental) eventName property. Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_source: (experimental) eventSource property. Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_time: (experimental) eventTime property. Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_version: (experimental) eventVersion property. Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param management_event: (experimental) managementEvent property. Specify an array of string values to match this event if the actual value of managementEvent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param read_only: (experimental) readOnly property. Specify an array of string values to match this event if the actual value of readOnly is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param recipient_account_id: (experimental) recipientAccountId property. Specify an array of string values to match this event if the actual value of recipientAccountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) requestID property. Specify an array of string values to match this event if the actual value of requestID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_parameters: (experimental) requestParameters property. Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param resources: (experimental) resources property. Specify an array of string values to match this event if the actual value of resources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param response_elements: (experimental) responseElements property. Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_ip_address: (experimental) sourceIPAddress property. Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param tls_details: (experimental) tlsDetails property. Specify an array of string values to match this event if the actual value of tlsDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param user_identity: (experimental) userIdentity property. Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param vpc_endpoint_id: (experimental) vpcEndpointId property. Specify an array of string values to match this event if the actual value of vpcEndpointId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = BucketEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
            additional_event_data=additional_event_data,
            aws_region=aws_region,
            error_code=error_code,
            error_message=error_message,
            event_category=event_category,
            event_id=event_id,
            event_metadata=event_metadata,
            event_name=event_name,
            event_source=event_source,
            event_time=event_time,
            event_type=event_type,
            event_version=event_version,
            management_event=management_event,
            read_only=read_only,
            recipient_account_id=recipient_account_id,
            request_id=request_id,
            request_parameters=request_parameters,
            resources=resources,
            response_elements=response_elements,
            source_ip_address=source_ip_address,
            tls_details=tls_details,
            user_agent=user_agent,
            user_identity=user_identity,
            vpc_endpoint_id=vpc_endpoint_id,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "awsAPICallViaCloudTrailPattern", [options]))

    @jsii.member(jsii_name="objectAccessTierChangedPattern")
    def object_access_tier_changed_pattern(
        self,
        *,
        bucket: typing.Optional[typing.Union["BucketEvents.ObjectAccessTierChanged.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
        destination_access_tier: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        object: typing.Optional[typing.Union["BucketEvents.ObjectAccessTierChanged.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
        requester: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Bucket Object Access Tier Changed.

        :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param destination_access_tier: (experimental) destination-access-tier property. Specify an array of string values to match this event if the actual value of destination-access-tier is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = BucketEvents.ObjectAccessTierChanged.ObjectAccessTierChangedProps(
            bucket=bucket,
            destination_access_tier=destination_access_tier,
            event_metadata=event_metadata,
            object=object,
            requester=requester,
            request_id=request_id,
            version=version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "objectAccessTierChangedPattern", [options]))

    @jsii.member(jsii_name="objectACLUpdatedPattern")
    def object_acl_updated_pattern(
        self,
        *,
        bucket: typing.Optional[typing.Union["BucketEvents.ObjectACLUpdated.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        object: typing.Optional[typing.Union["BucketEvents.ObjectACLUpdated.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
        requester: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Bucket Object ACL Updated.

        :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_ip_address: (experimental) source-ip-address property. Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = BucketEvents.ObjectACLUpdated.ObjectACLUpdatedProps(
            bucket=bucket,
            event_metadata=event_metadata,
            object=object,
            requester=requester,
            request_id=request_id,
            source_ip_address=source_ip_address,
            version=version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "objectACLUpdatedPattern", [options]))

    @jsii.member(jsii_name="objectCreatedPattern")
    def object_created_pattern(
        self,
        *,
        bucket: typing.Optional[typing.Union["BucketEvents.ObjectCreated.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        object: typing.Optional[typing.Union["BucketEvents.ObjectCreated.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
        reason: typing.Optional[typing.Sequence[builtins.str]] = None,
        requester: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Bucket Object Created.

        :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param reason: (experimental) reason property. Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_ip_address: (experimental) source-ip-address property. Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = BucketEvents.ObjectCreated.ObjectCreatedProps(
            bucket=bucket,
            event_metadata=event_metadata,
            object=object,
            reason=reason,
            requester=requester,
            request_id=request_id,
            source_ip_address=source_ip_address,
            version=version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "objectCreatedPattern", [options]))

    @jsii.member(jsii_name="objectDeletedPattern")
    def object_deleted_pattern(
        self,
        *,
        bucket: typing.Optional[typing.Union["BucketEvents.ObjectDeleted.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        object: typing.Optional[typing.Union["BucketEvents.ObjectDeleted.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
        reason: typing.Optional[typing.Sequence[builtins.str]] = None,
        requester: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Bucket Object Deleted.

        :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param deletion_type: (experimental) deletion-type property. Specify an array of string values to match this event if the actual value of deletion-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param reason: (experimental) reason property. Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_ip_address: (experimental) source-ip-address property. Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = BucketEvents.ObjectDeleted.ObjectDeletedProps(
            bucket=bucket,
            deletion_type=deletion_type,
            event_metadata=event_metadata,
            object=object,
            reason=reason,
            requester=requester,
            request_id=request_id,
            source_ip_address=source_ip_address,
            version=version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "objectDeletedPattern", [options]))

    @jsii.member(jsii_name="objectRestoreCompletedPattern")
    def object_restore_completed_pattern(
        self,
        *,
        bucket: typing.Optional[typing.Union["BucketEvents.ObjectRestoreCompleted.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        object: typing.Optional[typing.Union["BucketEvents.ObjectRestoreCompleted.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
        requester: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        restore_expiry_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_storage_class: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Bucket Object Restore Completed.

        :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param restore_expiry_time: (experimental) restore-expiry-time property. Specify an array of string values to match this event if the actual value of restore-expiry-time is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_storage_class: (experimental) source-storage-class property. Specify an array of string values to match this event if the actual value of source-storage-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = BucketEvents.ObjectRestoreCompleted.ObjectRestoreCompletedProps(
            bucket=bucket,
            event_metadata=event_metadata,
            object=object,
            requester=requester,
            request_id=request_id,
            restore_expiry_time=restore_expiry_time,
            source_storage_class=source_storage_class,
            version=version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "objectRestoreCompletedPattern", [options]))

    @jsii.member(jsii_name="objectRestoreExpiredPattern")
    def object_restore_expired_pattern(
        self,
        *,
        bucket: typing.Optional[typing.Union["BucketEvents.ObjectRestoreExpired.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        object: typing.Optional[typing.Union["BucketEvents.ObjectRestoreExpired.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
        requester: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Bucket Object Restore Expired.

        :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = BucketEvents.ObjectRestoreExpired.ObjectRestoreExpiredProps(
            bucket=bucket,
            event_metadata=event_metadata,
            object=object,
            requester=requester,
            request_id=request_id,
            version=version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "objectRestoreExpiredPattern", [options]))

    @jsii.member(jsii_name="objectRestoreInitiatedPattern")
    def object_restore_initiated_pattern(
        self,
        *,
        bucket: typing.Optional[typing.Union["BucketEvents.ObjectRestoreInitiated.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        object: typing.Optional[typing.Union["BucketEvents.ObjectRestoreInitiated.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
        requester: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_storage_class: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Bucket Object Restore Initiated.

        :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_ip_address: (experimental) source-ip-address property. Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_storage_class: (experimental) source-storage-class property. Specify an array of string values to match this event if the actual value of source-storage-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = BucketEvents.ObjectRestoreInitiated.ObjectRestoreInitiatedProps(
            bucket=bucket,
            event_metadata=event_metadata,
            object=object,
            requester=requester,
            request_id=request_id,
            source_ip_address=source_ip_address,
            source_storage_class=source_storage_class,
            version=version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "objectRestoreInitiatedPattern", [options]))

    @jsii.member(jsii_name="objectStorageClassChangedPattern")
    def object_storage_class_changed_pattern(
        self,
        *,
        bucket: typing.Optional[typing.Union["BucketEvents.ObjectStorageClassChanged.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
        destination_storage_class: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        object: typing.Optional[typing.Union["BucketEvents.ObjectStorageClassChanged.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
        requester: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Bucket Object Storage Class Changed.

        :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param destination_storage_class: (experimental) destination-storage-class property. Specify an array of string values to match this event if the actual value of destination-storage-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = BucketEvents.ObjectStorageClassChanged.ObjectStorageClassChangedProps(
            bucket=bucket,
            destination_storage_class=destination_storage_class,
            event_metadata=event_metadata,
            object=object,
            requester=requester,
            request_id=request_id,
            version=version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "objectStorageClassChangedPattern", [options]))

    @jsii.member(jsii_name="objectTagsAddedPattern")
    def object_tags_added_pattern(
        self,
        *,
        bucket: typing.Optional[typing.Union["BucketEvents.ObjectTagsAdded.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        object: typing.Optional[typing.Union["BucketEvents.ObjectTagsAdded.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
        requester: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Bucket Object Tags Added.

        :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_ip_address: (experimental) source-ip-address property. Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = BucketEvents.ObjectTagsAdded.ObjectTagsAddedProps(
            bucket=bucket,
            event_metadata=event_metadata,
            object=object,
            requester=requester,
            request_id=request_id,
            source_ip_address=source_ip_address,
            version=version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "objectTagsAddedPattern", [options]))

    @jsii.member(jsii_name="objectTagsDeletedPattern")
    def object_tags_deleted_pattern(
        self,
        *,
        bucket: typing.Optional[typing.Union["BucketEvents.ObjectTagsDeleted.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        object: typing.Optional[typing.Union["BucketEvents.ObjectTagsDeleted.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
        requester: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Bucket Object Tags Deleted.

        :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_ip_address: (experimental) source-ip-address property. Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = BucketEvents.ObjectTagsDeleted.ObjectTagsDeletedProps(
            bucket=bucket,
            event_metadata=event_metadata,
            object=object,
            requester=requester,
            request_id=request_id,
            source_ip_address=source_ip_address,
            version=version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "objectTagsDeletedPattern", [options]))

    class AWSAPICallViaCloudTrail(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.AWSAPICallViaCloudTrail",
    ):
        '''(experimental) aws.s3@AWSAPICallViaCloudTrail event types for Bucket.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import events as s3_events
            
            a_wSAPICall_via_cloud_trail = s3_events.BucketEvents.AWSAPICallViaCloudTrail()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps",
            jsii_struct_bases=[],
            name_mapping={
                "additional_event_data": "additionalEventData",
                "aws_region": "awsRegion",
                "error_code": "errorCode",
                "error_message": "errorMessage",
                "event_category": "eventCategory",
                "event_id": "eventId",
                "event_metadata": "eventMetadata",
                "event_name": "eventName",
                "event_source": "eventSource",
                "event_time": "eventTime",
                "event_type": "eventType",
                "event_version": "eventVersion",
                "management_event": "managementEvent",
                "read_only": "readOnly",
                "recipient_account_id": "recipientAccountId",
                "request_id": "requestId",
                "request_parameters": "requestParameters",
                "resources": "resources",
                "response_elements": "responseElements",
                "source_ip_address": "sourceIpAddress",
                "tls_details": "tlsDetails",
                "user_agent": "userAgent",
                "user_identity": "userIdentity",
                "vpc_endpoint_id": "vpcEndpointId",
            },
        )
        class AWSAPICallViaCloudTrailProps:
            def __init__(
                self,
                *,
                additional_event_data: typing.Optional[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.AdditionalEventData", typing.Dict[builtins.str, typing.Any]]] = None,
                aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_category: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                management_event: typing.Optional[typing.Sequence[builtins.str]] = None,
                read_only: typing.Optional[typing.Sequence[builtins.str]] = None,
                recipient_account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_parameters: typing.Optional[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.RequestParameters", typing.Dict[builtins.str, typing.Any]]] = None,
                resources: typing.Optional[typing.Sequence[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                response_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                tls_details: typing.Optional[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.TlsDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_identity: typing.Optional[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
                vpc_endpoint_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Bucket aws.s3@AWSAPICallViaCloudTrail event.

                :param additional_event_data: (experimental) additionalEventData property. Specify an array of string values to match this event if the actual value of additionalEventData is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param aws_region: (experimental) awsRegion property. Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_category: (experimental) eventCategory property. Specify an array of string values to match this event if the actual value of eventCategory is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_id: (experimental) eventID property. Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param event_name: (experimental) eventName property. Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_source: (experimental) eventSource property. Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_time: (experimental) eventTime property. Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_version: (experimental) eventVersion property. Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param management_event: (experimental) managementEvent property. Specify an array of string values to match this event if the actual value of managementEvent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param read_only: (experimental) readOnly property. Specify an array of string values to match this event if the actual value of readOnly is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param recipient_account_id: (experimental) recipientAccountId property. Specify an array of string values to match this event if the actual value of recipientAccountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) requestID property. Specify an array of string values to match this event if the actual value of requestID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_parameters: (experimental) requestParameters property. Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param resources: (experimental) resources property. Specify an array of string values to match this event if the actual value of resources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param response_elements: (experimental) responseElements property. Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_ip_address: (experimental) sourceIPAddress property. Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tls_details: (experimental) tlsDetails property. Specify an array of string values to match this event if the actual value of tlsDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_identity: (experimental) userIdentity property. Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param vpc_endpoint_id: (experimental) vpcEndpointId property. Specify an array of string values to match this event if the actual value of vpcEndpointId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    a_wSAPICall_via_cloud_trail_props = s3_events.BucketEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
                        additional_event_data=s3_events.BucketEvents.AWSAPICallViaCloudTrail.AdditionalEventData(
                            authentication_method=["authenticationMethod"],
                            bytes_transferred_in=["bytesTransferredIn"],
                            bytes_transferred_out=["bytesTransferredOut"],
                            cipher_suite=["cipherSuite"],
                            object_retention_info=s3_events.BucketEvents.AWSAPICallViaCloudTrail.ObjectRetentionInfo(
                                legal_hold_info=s3_events.BucketEvents.AWSAPICallViaCloudTrail.LegalHoldInfo(
                                    is_under_legal_hold=["isUnderLegalHold"],
                                    last_modified_time=["lastModifiedTime"]
                                ),
                                retention_info=s3_events.BucketEvents.AWSAPICallViaCloudTrail.RetentionInfo(
                                    last_modified_time=["lastModifiedTime"],
                                    retain_until_mode=["retainUntilMode"],
                                    retain_until_time=["retainUntilTime"]
                                )
                            ),
                            signature_version=["signatureVersion"],
                            x_amz_id2=["xAmzId2"]
                        ),
                        aws_region=["awsRegion"],
                        error_code=["errorCode"],
                        error_message=["errorMessage"],
                        event_category=["eventCategory"],
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
                        management_event=["managementEvent"],
                        read_only=["readOnly"],
                        recipient_account_id=["recipientAccountId"],
                        request_id=["requestId"],
                        request_parameters=s3_events.BucketEvents.AWSAPICallViaCloudTrail.RequestParameters(
                            bucket_name=["bucketName"],
                            host=["host"],
                            key=["key"],
                            legal_hold=["legalHold"],
                            retention=["retention"]
                        ),
                        resources=[s3_events.BucketEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem(
                            account_id=["accountId"],
                            arn=["arn"],
                            type=["type"]
                        )],
                        response_elements=["responseElements"],
                        source_ip_address=["sourceIpAddress"],
                        tls_details=s3_events.BucketEvents.AWSAPICallViaCloudTrail.TlsDetails(
                            cipher_suite=["cipherSuite"],
                            client_provided_host_header=["clientProvidedHostHeader"],
                            tls_version=["tlsVersion"]
                        ),
                        user_agent=["userAgent"],
                        user_identity=s3_events.BucketEvents.AWSAPICallViaCloudTrail.UserIdentity(
                            access_key_id=["accessKeyId"],
                            account_id=["accountId"],
                            arn=["arn"],
                            principal_id=["principalId"],
                            session_context=s3_events.BucketEvents.AWSAPICallViaCloudTrail.SessionContext(
                                attributes=s3_events.BucketEvents.AWSAPICallViaCloudTrail.Attributes(
                                    creation_date=["creationDate"],
                                    mfa_authenticated=["mfaAuthenticated"]
                                ),
                                session_issuer=s3_events.BucketEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                                    account_id=["accountId"],
                                    arn=["arn"],
                                    principal_id=["principalId"],
                                    type=["type"],
                                    user_name=["userName"]
                                ),
                                web_id_federation_data=["webIdFederationData"]
                            ),
                            type=["type"]
                        ),
                        vpc_endpoint_id=["vpcEndpointId"]
                    )
                '''
                if isinstance(additional_event_data, dict):
                    additional_event_data = BucketEvents.AWSAPICallViaCloudTrail.AdditionalEventData(**additional_event_data)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(request_parameters, dict):
                    request_parameters = BucketEvents.AWSAPICallViaCloudTrail.RequestParameters(**request_parameters)
                if isinstance(tls_details, dict):
                    tls_details = BucketEvents.AWSAPICallViaCloudTrail.TlsDetails(**tls_details)
                if isinstance(user_identity, dict):
                    user_identity = BucketEvents.AWSAPICallViaCloudTrail.UserIdentity(**user_identity)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__91d36fe61032be2ae29f5a9abe4545d60e6f1d1c42d43fd680fbe57a65dcdd77)
                    check_type(argname="argument additional_event_data", value=additional_event_data, expected_type=type_hints["additional_event_data"])
                    check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                    check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                    check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
                    check_type(argname="argument event_category", value=event_category, expected_type=type_hints["event_category"])
                    check_type(argname="argument event_id", value=event_id, expected_type=type_hints["event_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
                    check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
                    check_type(argname="argument event_time", value=event_time, expected_type=type_hints["event_time"])
                    check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
                    check_type(argname="argument event_version", value=event_version, expected_type=type_hints["event_version"])
                    check_type(argname="argument management_event", value=management_event, expected_type=type_hints["management_event"])
                    check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
                    check_type(argname="argument recipient_account_id", value=recipient_account_id, expected_type=type_hints["recipient_account_id"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument request_parameters", value=request_parameters, expected_type=type_hints["request_parameters"])
                    check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
                    check_type(argname="argument response_elements", value=response_elements, expected_type=type_hints["response_elements"])
                    check_type(argname="argument source_ip_address", value=source_ip_address, expected_type=type_hints["source_ip_address"])
                    check_type(argname="argument tls_details", value=tls_details, expected_type=type_hints["tls_details"])
                    check_type(argname="argument user_agent", value=user_agent, expected_type=type_hints["user_agent"])
                    check_type(argname="argument user_identity", value=user_identity, expected_type=type_hints["user_identity"])
                    check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if additional_event_data is not None:
                    self._values["additional_event_data"] = additional_event_data
                if aws_region is not None:
                    self._values["aws_region"] = aws_region
                if error_code is not None:
                    self._values["error_code"] = error_code
                if error_message is not None:
                    self._values["error_message"] = error_message
                if event_category is not None:
                    self._values["event_category"] = event_category
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
                if management_event is not None:
                    self._values["management_event"] = management_event
                if read_only is not None:
                    self._values["read_only"] = read_only
                if recipient_account_id is not None:
                    self._values["recipient_account_id"] = recipient_account_id
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
                if tls_details is not None:
                    self._values["tls_details"] = tls_details
                if user_agent is not None:
                    self._values["user_agent"] = user_agent
                if user_identity is not None:
                    self._values["user_identity"] = user_identity
                if vpc_endpoint_id is not None:
                    self._values["vpc_endpoint_id"] = vpc_endpoint_id

            @builtins.property
            def additional_event_data(
                self,
            ) -> typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.AdditionalEventData"]:
                '''(experimental) additionalEventData property.

                Specify an array of string values to match this event if the actual value of additionalEventData is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("additional_event_data")
                return typing.cast(typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.AdditionalEventData"], result)

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
            def error_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorCode property.

                Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorMessage property.

                Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_category(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventCategory property.

                Specify an array of string values to match this event if the actual value of eventCategory is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_category")
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
            def management_event(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) managementEvent property.

                Specify an array of string values to match this event if the actual value of managementEvent is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("management_event")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def read_only(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) readOnly property.

                Specify an array of string values to match this event if the actual value of readOnly is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("read_only")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def recipient_account_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) recipientAccountId property.

                Specify an array of string values to match this event if the actual value of recipientAccountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("recipient_account_id")
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
            ) -> typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.RequestParameters"]:
                '''(experimental) requestParameters property.

                Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_parameters")
                return typing.cast(typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.RequestParameters"], result)

            @builtins.property
            def resources(
                self,
            ) -> typing.Optional[typing.List["BucketEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem"]]:
                '''(experimental) resources property.

                Specify an array of string values to match this event if the actual value of resources is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resources")
                return typing.cast(typing.Optional[typing.List["BucketEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem"]], result)

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
            def tls_details(
                self,
            ) -> typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.TlsDetails"]:
                '''(experimental) tlsDetails property.

                Specify an array of string values to match this event if the actual value of tlsDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tls_details")
                return typing.cast(typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.TlsDetails"], result)

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
            ) -> typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.UserIdentity"]:
                '''(experimental) userIdentity property.

                Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_identity")
                return typing.cast(typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.UserIdentity"], result)

            @builtins.property
            def vpc_endpoint_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) vpcEndpointId property.

                Specify an array of string values to match this event if the actual value of vpcEndpointId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("vpc_endpoint_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AWSAPICallViaCloudTrailProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.AWSAPICallViaCloudTrail.AdditionalEventData",
            jsii_struct_bases=[],
            name_mapping={
                "authentication_method": "authenticationMethod",
                "bytes_transferred_in": "bytesTransferredIn",
                "bytes_transferred_out": "bytesTransferredOut",
                "cipher_suite": "cipherSuite",
                "object_retention_info": "objectRetentionInfo",
                "signature_version": "signatureVersion",
                "x_amz_id2": "xAmzId2",
            },
        )
        class AdditionalEventData:
            def __init__(
                self,
                *,
                authentication_method: typing.Optional[typing.Sequence[builtins.str]] = None,
                bytes_transferred_in: typing.Optional[typing.Sequence[builtins.str]] = None,
                bytes_transferred_out: typing.Optional[typing.Sequence[builtins.str]] = None,
                cipher_suite: typing.Optional[typing.Sequence[builtins.str]] = None,
                object_retention_info: typing.Optional[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.ObjectRetentionInfo", typing.Dict[builtins.str, typing.Any]]] = None,
                signature_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                x_amz_id2: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AdditionalEventData.

                :param authentication_method: (experimental) AuthenticationMethod property. Specify an array of string values to match this event if the actual value of AuthenticationMethod is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param bytes_transferred_in: (experimental) bytesTransferredIn property. Specify an array of string values to match this event if the actual value of bytesTransferredIn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param bytes_transferred_out: (experimental) bytesTransferredOut property. Specify an array of string values to match this event if the actual value of bytesTransferredOut is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param cipher_suite: (experimental) CipherSuite property. Specify an array of string values to match this event if the actual value of CipherSuite is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param object_retention_info: (experimental) objectRetentionInfo property. Specify an array of string values to match this event if the actual value of objectRetentionInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param signature_version: (experimental) SignatureVersion property. Specify an array of string values to match this event if the actual value of SignatureVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param x_amz_id2: (experimental) x-amz-id-2 property. Specify an array of string values to match this event if the actual value of x-amz-id-2 is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    additional_event_data = s3_events.BucketEvents.AWSAPICallViaCloudTrail.AdditionalEventData(
                        authentication_method=["authenticationMethod"],
                        bytes_transferred_in=["bytesTransferredIn"],
                        bytes_transferred_out=["bytesTransferredOut"],
                        cipher_suite=["cipherSuite"],
                        object_retention_info=s3_events.BucketEvents.AWSAPICallViaCloudTrail.ObjectRetentionInfo(
                            legal_hold_info=s3_events.BucketEvents.AWSAPICallViaCloudTrail.LegalHoldInfo(
                                is_under_legal_hold=["isUnderLegalHold"],
                                last_modified_time=["lastModifiedTime"]
                            ),
                            retention_info=s3_events.BucketEvents.AWSAPICallViaCloudTrail.RetentionInfo(
                                last_modified_time=["lastModifiedTime"],
                                retain_until_mode=["retainUntilMode"],
                                retain_until_time=["retainUntilTime"]
                            )
                        ),
                        signature_version=["signatureVersion"],
                        x_amz_id2=["xAmzId2"]
                    )
                '''
                if isinstance(object_retention_info, dict):
                    object_retention_info = BucketEvents.AWSAPICallViaCloudTrail.ObjectRetentionInfo(**object_retention_info)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__978c39418628123b13f1c4fb305549a626f2926333a112e417bffb9fecd67ba2)
                    check_type(argname="argument authentication_method", value=authentication_method, expected_type=type_hints["authentication_method"])
                    check_type(argname="argument bytes_transferred_in", value=bytes_transferred_in, expected_type=type_hints["bytes_transferred_in"])
                    check_type(argname="argument bytes_transferred_out", value=bytes_transferred_out, expected_type=type_hints["bytes_transferred_out"])
                    check_type(argname="argument cipher_suite", value=cipher_suite, expected_type=type_hints["cipher_suite"])
                    check_type(argname="argument object_retention_info", value=object_retention_info, expected_type=type_hints["object_retention_info"])
                    check_type(argname="argument signature_version", value=signature_version, expected_type=type_hints["signature_version"])
                    check_type(argname="argument x_amz_id2", value=x_amz_id2, expected_type=type_hints["x_amz_id2"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if authentication_method is not None:
                    self._values["authentication_method"] = authentication_method
                if bytes_transferred_in is not None:
                    self._values["bytes_transferred_in"] = bytes_transferred_in
                if bytes_transferred_out is not None:
                    self._values["bytes_transferred_out"] = bytes_transferred_out
                if cipher_suite is not None:
                    self._values["cipher_suite"] = cipher_suite
                if object_retention_info is not None:
                    self._values["object_retention_info"] = object_retention_info
                if signature_version is not None:
                    self._values["signature_version"] = signature_version
                if x_amz_id2 is not None:
                    self._values["x_amz_id2"] = x_amz_id2

            @builtins.property
            def authentication_method(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) AuthenticationMethod property.

                Specify an array of string values to match this event if the actual value of AuthenticationMethod is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("authentication_method")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def bytes_transferred_in(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bytesTransferredIn property.

                Specify an array of string values to match this event if the actual value of bytesTransferredIn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bytes_transferred_in")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def bytes_transferred_out(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bytesTransferredOut property.

                Specify an array of string values to match this event if the actual value of bytesTransferredOut is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bytes_transferred_out")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def cipher_suite(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) CipherSuite property.

                Specify an array of string values to match this event if the actual value of CipherSuite is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cipher_suite")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def object_retention_info(
                self,
            ) -> typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.ObjectRetentionInfo"]:
                '''(experimental) objectRetentionInfo property.

                Specify an array of string values to match this event if the actual value of objectRetentionInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("object_retention_info")
                return typing.cast(typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.ObjectRetentionInfo"], result)

            @builtins.property
            def signature_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) SignatureVersion property.

                Specify an array of string values to match this event if the actual value of SignatureVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("signature_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def x_amz_id2(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) x-amz-id-2 property.

                Specify an array of string values to match this event if the actual value of x-amz-id-2 is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("x_amz_id2")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AdditionalEventData(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.AWSAPICallViaCloudTrail.Attributes",
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
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    attributes = s3_events.BucketEvents.AWSAPICallViaCloudTrail.Attributes(
                        creation_date=["creationDate"],
                        mfa_authenticated=["mfaAuthenticated"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__c16c0d946fe52018b9aeae85cb27c8073f57634acbe1d762219fa72a8046072c)
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
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem",
            jsii_struct_bases=[],
            name_mapping={"account_id": "accountId", "arn": "arn", "type": "type"},
        )
        class AwsapiCallViaCloudTrailItem:
            def __init__(
                self,
                *,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AWSAPICallViaCloudTrailItem.

                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param arn: (experimental) ARN property. Specify an array of string values to match this event if the actual value of ARN is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    awsapi_call_via_cloud_trail_item = s3_events.BucketEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem(
                        account_id=["accountId"],
                        arn=["arn"],
                        type=["type"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__c8f9002b41147bb82d139c2d0414a964ecee587fc51a270228275570556b15df)
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if account_id is not None:
                    self._values["account_id"] = account_id
                if arn is not None:
                    self._values["arn"] = arn
                if type is not None:
                    self._values["type"] = type

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
                return "AwsapiCallViaCloudTrailItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.AWSAPICallViaCloudTrail.LegalHoldInfo",
            jsii_struct_bases=[],
            name_mapping={
                "is_under_legal_hold": "isUnderLegalHold",
                "last_modified_time": "lastModifiedTime",
            },
        )
        class LegalHoldInfo:
            def __init__(
                self,
                *,
                is_under_legal_hold: typing.Optional[typing.Sequence[builtins.str]] = None,
                last_modified_time: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for LegalHoldInfo.

                :param is_under_legal_hold: (experimental) isUnderLegalHold property. Specify an array of string values to match this event if the actual value of isUnderLegalHold is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param last_modified_time: (experimental) lastModifiedTime property. Specify an array of string values to match this event if the actual value of lastModifiedTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    legal_hold_info = s3_events.BucketEvents.AWSAPICallViaCloudTrail.LegalHoldInfo(
                        is_under_legal_hold=["isUnderLegalHold"],
                        last_modified_time=["lastModifiedTime"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a1540917d2158e1f4d9258b7ad0f4a49510cf2a5aaa93307b5de3bb0100d4d7e)
                    check_type(argname="argument is_under_legal_hold", value=is_under_legal_hold, expected_type=type_hints["is_under_legal_hold"])
                    check_type(argname="argument last_modified_time", value=last_modified_time, expected_type=type_hints["last_modified_time"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if is_under_legal_hold is not None:
                    self._values["is_under_legal_hold"] = is_under_legal_hold
                if last_modified_time is not None:
                    self._values["last_modified_time"] = last_modified_time

            @builtins.property
            def is_under_legal_hold(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) isUnderLegalHold property.

                Specify an array of string values to match this event if the actual value of isUnderLegalHold is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("is_under_legal_hold")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def last_modified_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) lastModifiedTime property.

                Specify an array of string values to match this event if the actual value of lastModifiedTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("last_modified_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "LegalHoldInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.AWSAPICallViaCloudTrail.ObjectRetentionInfo",
            jsii_struct_bases=[],
            name_mapping={
                "legal_hold_info": "legalHoldInfo",
                "retention_info": "retentionInfo",
            },
        )
        class ObjectRetentionInfo:
            def __init__(
                self,
                *,
                legal_hold_info: typing.Optional[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.LegalHoldInfo", typing.Dict[builtins.str, typing.Any]]] = None,
                retention_info: typing.Optional[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.RetentionInfo", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for ObjectRetentionInfo.

                :param legal_hold_info: (experimental) legalHoldInfo property. Specify an array of string values to match this event if the actual value of legalHoldInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param retention_info: (experimental) retentionInfo property. Specify an array of string values to match this event if the actual value of retentionInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_retention_info = s3_events.BucketEvents.AWSAPICallViaCloudTrail.ObjectRetentionInfo(
                        legal_hold_info=s3_events.BucketEvents.AWSAPICallViaCloudTrail.LegalHoldInfo(
                            is_under_legal_hold=["isUnderLegalHold"],
                            last_modified_time=["lastModifiedTime"]
                        ),
                        retention_info=s3_events.BucketEvents.AWSAPICallViaCloudTrail.RetentionInfo(
                            last_modified_time=["lastModifiedTime"],
                            retain_until_mode=["retainUntilMode"],
                            retain_until_time=["retainUntilTime"]
                        )
                    )
                '''
                if isinstance(legal_hold_info, dict):
                    legal_hold_info = BucketEvents.AWSAPICallViaCloudTrail.LegalHoldInfo(**legal_hold_info)
                if isinstance(retention_info, dict):
                    retention_info = BucketEvents.AWSAPICallViaCloudTrail.RetentionInfo(**retention_info)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f7a773d93c77ec9a4c0e6c2b4a556ec59346c1d14266d81b05b668d549a77fdc)
                    check_type(argname="argument legal_hold_info", value=legal_hold_info, expected_type=type_hints["legal_hold_info"])
                    check_type(argname="argument retention_info", value=retention_info, expected_type=type_hints["retention_info"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if legal_hold_info is not None:
                    self._values["legal_hold_info"] = legal_hold_info
                if retention_info is not None:
                    self._values["retention_info"] = retention_info

            @builtins.property
            def legal_hold_info(
                self,
            ) -> typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.LegalHoldInfo"]:
                '''(experimental) legalHoldInfo property.

                Specify an array of string values to match this event if the actual value of legalHoldInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("legal_hold_info")
                return typing.cast(typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.LegalHoldInfo"], result)

            @builtins.property
            def retention_info(
                self,
            ) -> typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.RetentionInfo"]:
                '''(experimental) retentionInfo property.

                Specify an array of string values to match this event if the actual value of retentionInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("retention_info")
                return typing.cast(typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.RetentionInfo"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ObjectRetentionInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.AWSAPICallViaCloudTrail.RequestParameters",
            jsii_struct_bases=[],
            name_mapping={
                "bucket_name": "bucketName",
                "host": "host",
                "key": "key",
                "legal_hold": "legalHold",
                "retention": "retention",
            },
        )
        class RequestParameters:
            def __init__(
                self,
                *,
                bucket_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                host: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                legal_hold: typing.Optional[typing.Sequence[builtins.str]] = None,
                retention: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParameters.

                :param bucket_name: (experimental) bucketName property. Specify an array of string values to match this event if the actual value of bucketName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Bucket reference
                :param host: (experimental) Host property. Specify an array of string values to match this event if the actual value of Host is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param legal_hold: (experimental) legal-hold property. Specify an array of string values to match this event if the actual value of legal-hold is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param retention: (experimental) retention property. Specify an array of string values to match this event if the actual value of retention is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    request_parameters = s3_events.BucketEvents.AWSAPICallViaCloudTrail.RequestParameters(
                        bucket_name=["bucketName"],
                        host=["host"],
                        key=["key"],
                        legal_hold=["legalHold"],
                        retention=["retention"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__514c077a90d9ed4ce5b956e1cbed4d21d1458ec72037ff66851382e2d78df420)
                    check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                    check_type(argname="argument host", value=host, expected_type=type_hints["host"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument legal_hold", value=legal_hold, expected_type=type_hints["legal_hold"])
                    check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket_name is not None:
                    self._values["bucket_name"] = bucket_name
                if host is not None:
                    self._values["host"] = host
                if key is not None:
                    self._values["key"] = key
                if legal_hold is not None:
                    self._values["legal_hold"] = legal_hold
                if retention is not None:
                    self._values["retention"] = retention

            @builtins.property
            def bucket_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bucketName property.

                Specify an array of string values to match this event if the actual value of bucketName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Bucket reference

                :stability: experimental
                '''
                result = self._values.get("bucket_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def host(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Host property.

                Specify an array of string values to match this event if the actual value of Host is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("host")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) key property.

                Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def legal_hold(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) legal-hold property.

                Specify an array of string values to match this event if the actual value of legal-hold is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("legal_hold")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def retention(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) retention property.

                Specify an array of string values to match this event if the actual value of retention is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("retention")
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
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.AWSAPICallViaCloudTrail.RetentionInfo",
            jsii_struct_bases=[],
            name_mapping={
                "last_modified_time": "lastModifiedTime",
                "retain_until_mode": "retainUntilMode",
                "retain_until_time": "retainUntilTime",
            },
        )
        class RetentionInfo:
            def __init__(
                self,
                *,
                last_modified_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                retain_until_mode: typing.Optional[typing.Sequence[builtins.str]] = None,
                retain_until_time: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RetentionInfo.

                :param last_modified_time: (experimental) lastModifiedTime property. Specify an array of string values to match this event if the actual value of lastModifiedTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param retain_until_mode: (experimental) retainUntilMode property. Specify an array of string values to match this event if the actual value of retainUntilMode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param retain_until_time: (experimental) retainUntilTime property. Specify an array of string values to match this event if the actual value of retainUntilTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    retention_info = s3_events.BucketEvents.AWSAPICallViaCloudTrail.RetentionInfo(
                        last_modified_time=["lastModifiedTime"],
                        retain_until_mode=["retainUntilMode"],
                        retain_until_time=["retainUntilTime"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3d3b23f9aa10d6eda8495857018a9ebdc05f9c45c425bd6bb8340cc39ff8af1f)
                    check_type(argname="argument last_modified_time", value=last_modified_time, expected_type=type_hints["last_modified_time"])
                    check_type(argname="argument retain_until_mode", value=retain_until_mode, expected_type=type_hints["retain_until_mode"])
                    check_type(argname="argument retain_until_time", value=retain_until_time, expected_type=type_hints["retain_until_time"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if last_modified_time is not None:
                    self._values["last_modified_time"] = last_modified_time
                if retain_until_mode is not None:
                    self._values["retain_until_mode"] = retain_until_mode
                if retain_until_time is not None:
                    self._values["retain_until_time"] = retain_until_time

            @builtins.property
            def last_modified_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) lastModifiedTime property.

                Specify an array of string values to match this event if the actual value of lastModifiedTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("last_modified_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def retain_until_mode(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) retainUntilMode property.

                Specify an array of string values to match this event if the actual value of retainUntilMode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("retain_until_mode")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def retain_until_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) retainUntilTime property.

                Specify an array of string values to match this event if the actual value of retainUntilTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("retain_until_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RetentionInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.AWSAPICallViaCloudTrail.SessionContext",
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
                attributes: typing.Optional[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                session_issuer: typing.Optional[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.SessionIssuer", typing.Dict[builtins.str, typing.Any]]] = None,
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
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    session_context = s3_events.BucketEvents.AWSAPICallViaCloudTrail.SessionContext(
                        attributes=s3_events.BucketEvents.AWSAPICallViaCloudTrail.Attributes(
                            creation_date=["creationDate"],
                            mfa_authenticated=["mfaAuthenticated"]
                        ),
                        session_issuer=s3_events.BucketEvents.AWSAPICallViaCloudTrail.SessionIssuer(
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
                    attributes = BucketEvents.AWSAPICallViaCloudTrail.Attributes(**attributes)
                if isinstance(session_issuer, dict):
                    session_issuer = BucketEvents.AWSAPICallViaCloudTrail.SessionIssuer(**session_issuer)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__d4f6134a878e54a89a9c2ecfc026295329f586cf97383dcaa62261dd50cc3409)
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
            ) -> typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.Attributes"]:
                '''(experimental) attributes property.

                Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attributes")
                return typing.cast(typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.Attributes"], result)

            @builtins.property
            def session_issuer(
                self,
            ) -> typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.SessionIssuer"]:
                '''(experimental) sessionIssuer property.

                Specify an array of string values to match this event if the actual value of sessionIssuer is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_issuer")
                return typing.cast(typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.SessionIssuer"], result)

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
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.AWSAPICallViaCloudTrail.SessionIssuer",
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
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    session_issuer = s3_events.BucketEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                        account_id=["accountId"],
                        arn=["arn"],
                        principal_id=["principalId"],
                        type=["type"],
                        user_name=["userName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8b3e84ccedf9084612c4f30fc151fa19ec11cf3b444e7d916996b4d5f9e360ee)
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
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.AWSAPICallViaCloudTrail.TlsDetails",
            jsii_struct_bases=[],
            name_mapping={
                "cipher_suite": "cipherSuite",
                "client_provided_host_header": "clientProvidedHostHeader",
                "tls_version": "tlsVersion",
            },
        )
        class TlsDetails:
            def __init__(
                self,
                *,
                cipher_suite: typing.Optional[typing.Sequence[builtins.str]] = None,
                client_provided_host_header: typing.Optional[typing.Sequence[builtins.str]] = None,
                tls_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for TlsDetails.

                :param cipher_suite: (experimental) cipherSuite property. Specify an array of string values to match this event if the actual value of cipherSuite is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param client_provided_host_header: (experimental) clientProvidedHostHeader property. Specify an array of string values to match this event if the actual value of clientProvidedHostHeader is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tls_version: (experimental) tlsVersion property. Specify an array of string values to match this event if the actual value of tlsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    tls_details = s3_events.BucketEvents.AWSAPICallViaCloudTrail.TlsDetails(
                        cipher_suite=["cipherSuite"],
                        client_provided_host_header=["clientProvidedHostHeader"],
                        tls_version=["tlsVersion"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__96818f37100cf1bbc6e6f0fb7269c2c6b1a3df089cba106707bf30b1dd5d5ccb)
                    check_type(argname="argument cipher_suite", value=cipher_suite, expected_type=type_hints["cipher_suite"])
                    check_type(argname="argument client_provided_host_header", value=client_provided_host_header, expected_type=type_hints["client_provided_host_header"])
                    check_type(argname="argument tls_version", value=tls_version, expected_type=type_hints["tls_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if cipher_suite is not None:
                    self._values["cipher_suite"] = cipher_suite
                if client_provided_host_header is not None:
                    self._values["client_provided_host_header"] = client_provided_host_header
                if tls_version is not None:
                    self._values["tls_version"] = tls_version

            @builtins.property
            def cipher_suite(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cipherSuite property.

                Specify an array of string values to match this event if the actual value of cipherSuite is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cipher_suite")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def client_provided_host_header(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) clientProvidedHostHeader property.

                Specify an array of string values to match this event if the actual value of clientProvidedHostHeader is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("client_provided_host_header")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tls_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) tlsVersion property.

                Specify an array of string values to match this event if the actual value of tlsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tls_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TlsDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.AWSAPICallViaCloudTrail.UserIdentity",
            jsii_struct_bases=[],
            name_mapping={
                "access_key_id": "accessKeyId",
                "account_id": "accountId",
                "arn": "arn",
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
                principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                session_context: typing.Optional[typing.Union["BucketEvents.AWSAPICallViaCloudTrail.SessionContext", typing.Dict[builtins.str, typing.Any]]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for UserIdentity.

                :param access_key_id: (experimental) accessKeyId property. Specify an array of string values to match this event if the actual value of accessKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param principal_id: (experimental) principalId property. Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_context: (experimental) sessionContext property. Specify an array of string values to match this event if the actual value of sessionContext is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    user_identity = s3_events.BucketEvents.AWSAPICallViaCloudTrail.UserIdentity(
                        access_key_id=["accessKeyId"],
                        account_id=["accountId"],
                        arn=["arn"],
                        principal_id=["principalId"],
                        session_context=s3_events.BucketEvents.AWSAPICallViaCloudTrail.SessionContext(
                            attributes=s3_events.BucketEvents.AWSAPICallViaCloudTrail.Attributes(
                                creation_date=["creationDate"],
                                mfa_authenticated=["mfaAuthenticated"]
                            ),
                            session_issuer=s3_events.BucketEvents.AWSAPICallViaCloudTrail.SessionIssuer(
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
                    session_context = BucketEvents.AWSAPICallViaCloudTrail.SessionContext(**session_context)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3a55a46ad1960bf8a53533a2fe3ce5a102566bac1c77377e45e5fcb7ec6966b5)
                    check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
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
            ) -> typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.SessionContext"]:
                '''(experimental) sessionContext property.

                Specify an array of string values to match this event if the actual value of sessionContext is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_context")
                return typing.cast(typing.Optional["BucketEvents.AWSAPICallViaCloudTrail.SessionContext"], result)

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

    class ObjectACLUpdated(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectACLUpdated",
    ):
        '''(experimental) aws.s3@ObjectACLUpdated event types for Bucket.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import events as s3_events
            
            object_aCLUpdated = s3_events.BucketEvents.ObjectACLUpdated()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectACLUpdated.Bucket",
            jsii_struct_bases=[],
            name_mapping={"name": "name"},
        )
        class Bucket:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Bucket.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Bucket reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    bucket = s3_events.BucketEvents.ObjectACLUpdated.Bucket(
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__79624e255f1b11910c576fec17e045e4aa368a158fe87f0301a5ae4413a3b55f)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Bucket reference

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Bucket(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectACLUpdated.ObjectACLUpdatedProps",
            jsii_struct_bases=[],
            name_mapping={
                "bucket": "bucket",
                "event_metadata": "eventMetadata",
                "object": "object",
                "requester": "requester",
                "request_id": "requestId",
                "source_ip_address": "sourceIpAddress",
                "version": "version",
            },
        )
        class ObjectACLUpdatedProps:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Union["BucketEvents.ObjectACLUpdated.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                object: typing.Optional[typing.Union["BucketEvents.ObjectACLUpdated.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
                requester: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Bucket aws.s3@ObjectACLUpdated event.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_ip_address: (experimental) source-ip-address property. Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_aCLUpdated_props = s3_events.BucketEvents.ObjectACLUpdated.ObjectACLUpdatedProps(
                        bucket=s3_events.BucketEvents.ObjectACLUpdated.Bucket(
                            name=["name"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        object=s3_events.BucketEvents.ObjectACLUpdated.ObjectType(
                            etag=["etag"],
                            key=["key"],
                            version_id=["versionId"]
                        ),
                        requester=["requester"],
                        request_id=["requestId"],
                        source_ip_address=["sourceIpAddress"],
                        version=["version"]
                    )
                '''
                if isinstance(bucket, dict):
                    bucket = BucketEvents.ObjectACLUpdated.Bucket(**bucket)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(object, dict):
                    object = BucketEvents.ObjectACLUpdated.ObjectType(**object)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4bb9f6c55b38aa44ccf96f31ad9bdc39de16643104296c764c8ac2f4005b4b22)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                    check_type(argname="argument requester", value=requester, expected_type=type_hints["requester"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument source_ip_address", value=source_ip_address, expected_type=type_hints["source_ip_address"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if object is not None:
                    self._values["object"] = object
                if requester is not None:
                    self._values["requester"] = requester
                if request_id is not None:
                    self._values["request_id"] = request_id
                if source_ip_address is not None:
                    self._values["source_ip_address"] = source_ip_address
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def bucket(self) -> typing.Optional["BucketEvents.ObjectACLUpdated.Bucket"]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional["BucketEvents.ObjectACLUpdated.Bucket"], result)

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
            def object(
                self,
            ) -> typing.Optional["BucketEvents.ObjectACLUpdated.ObjectType"]:
                '''(experimental) object property.

                Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("object")
                return typing.cast(typing.Optional["BucketEvents.ObjectACLUpdated.ObjectType"], result)

            @builtins.property
            def requester(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester property.

                Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) request-id property.

                Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) source-ip-address property.

                Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_ip_address")
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
                return "ObjectACLUpdatedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectACLUpdated.ObjectType",
            jsii_struct_bases=[],
            name_mapping={"etag": "etag", "key": "key", "version_id": "versionId"},
        )
        class ObjectType:
            def __init__(
                self,
                *,
                etag: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Object.

                :param etag: (experimental) etag property. Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version_id: (experimental) version-id property. Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_type = s3_events.BucketEvents.ObjectACLUpdated.ObjectType(
                        etag=["etag"],
                        key=["key"],
                        version_id=["versionId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__bbbc4c95b7fed9ef076431e01317f6debfa81e293a59ae7110ddd440c7082084)
                    check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if etag is not None:
                    self._values["etag"] = etag
                if key is not None:
                    self._values["key"] = key
                if version_id is not None:
                    self._values["version_id"] = version_id

            @builtins.property
            def etag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) etag property.

                Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("etag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) key property.

                Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version-id property.

                Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ObjectType(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ObjectAccessTierChanged(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectAccessTierChanged",
    ):
        '''(experimental) aws.s3@ObjectAccessTierChanged event types for Bucket.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import events as s3_events
            
            object_access_tier_changed = s3_events.BucketEvents.ObjectAccessTierChanged()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectAccessTierChanged.Bucket",
            jsii_struct_bases=[],
            name_mapping={"name": "name"},
        )
        class Bucket:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Bucket.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Bucket reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    bucket = s3_events.BucketEvents.ObjectAccessTierChanged.Bucket(
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8e61bd6af7a386803fef002eb141f0ac4f08ba26fca927cbfaf1844296c0a809)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Bucket reference

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Bucket(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectAccessTierChanged.ObjectAccessTierChangedProps",
            jsii_struct_bases=[],
            name_mapping={
                "bucket": "bucket",
                "destination_access_tier": "destinationAccessTier",
                "event_metadata": "eventMetadata",
                "object": "object",
                "requester": "requester",
                "request_id": "requestId",
                "version": "version",
            },
        )
        class ObjectAccessTierChangedProps:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Union["BucketEvents.ObjectAccessTierChanged.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
                destination_access_tier: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                object: typing.Optional[typing.Union["BucketEvents.ObjectAccessTierChanged.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
                requester: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Bucket aws.s3@ObjectAccessTierChanged event.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param destination_access_tier: (experimental) destination-access-tier property. Specify an array of string values to match this event if the actual value of destination-access-tier is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_access_tier_changed_props = s3_events.BucketEvents.ObjectAccessTierChanged.ObjectAccessTierChangedProps(
                        bucket=s3_events.BucketEvents.ObjectAccessTierChanged.Bucket(
                            name=["name"]
                        ),
                        destination_access_tier=["destinationAccessTier"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        object=s3_events.BucketEvents.ObjectAccessTierChanged.ObjectType(
                            etag=["etag"],
                            key=["key"],
                            size=["size"],
                            version_id=["versionId"]
                        ),
                        requester=["requester"],
                        request_id=["requestId"],
                        version=["version"]
                    )
                '''
                if isinstance(bucket, dict):
                    bucket = BucketEvents.ObjectAccessTierChanged.Bucket(**bucket)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(object, dict):
                    object = BucketEvents.ObjectAccessTierChanged.ObjectType(**object)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__677759226741286518177834e324509bbe5796f3c6649eeb674d12c56d26f4cd)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument destination_access_tier", value=destination_access_tier, expected_type=type_hints["destination_access_tier"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                    check_type(argname="argument requester", value=requester, expected_type=type_hints["requester"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if destination_access_tier is not None:
                    self._values["destination_access_tier"] = destination_access_tier
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if object is not None:
                    self._values["object"] = object
                if requester is not None:
                    self._values["requester"] = requester
                if request_id is not None:
                    self._values["request_id"] = request_id
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def bucket(
                self,
            ) -> typing.Optional["BucketEvents.ObjectAccessTierChanged.Bucket"]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional["BucketEvents.ObjectAccessTierChanged.Bucket"], result)

            @builtins.property
            def destination_access_tier(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) destination-access-tier property.

                Specify an array of string values to match this event if the actual value of destination-access-tier is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("destination_access_tier")
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
            def object(
                self,
            ) -> typing.Optional["BucketEvents.ObjectAccessTierChanged.ObjectType"]:
                '''(experimental) object property.

                Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("object")
                return typing.cast(typing.Optional["BucketEvents.ObjectAccessTierChanged.ObjectType"], result)

            @builtins.property
            def requester(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester property.

                Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) request-id property.

                Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
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
                return "ObjectAccessTierChangedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectAccessTierChanged.ObjectType",
            jsii_struct_bases=[],
            name_mapping={
                "etag": "etag",
                "key": "key",
                "size": "size",
                "version_id": "versionId",
            },
        )
        class ObjectType:
            def __init__(
                self,
                *,
                etag: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                size: typing.Optional[typing.Sequence[builtins.str]] = None,
                version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Object.

                :param etag: (experimental) etag property. Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param size: (experimental) size property. Specify an array of string values to match this event if the actual value of size is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version_id: (experimental) version-id property. Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_type = s3_events.BucketEvents.ObjectAccessTierChanged.ObjectType(
                        etag=["etag"],
                        key=["key"],
                        size=["size"],
                        version_id=["versionId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__d1994d8e3ec0759c94a09054eda482d2e870212f8d8de841fb2965aa0c947d6d)
                    check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument size", value=size, expected_type=type_hints["size"])
                    check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if etag is not None:
                    self._values["etag"] = etag
                if key is not None:
                    self._values["key"] = key
                if size is not None:
                    self._values["size"] = size
                if version_id is not None:
                    self._values["version_id"] = version_id

            @builtins.property
            def etag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) etag property.

                Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("etag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) key property.

                Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def size(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) size property.

                Specify an array of string values to match this event if the actual value of size is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("size")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version-id property.

                Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ObjectType(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ObjectCreated(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectCreated",
    ):
        '''(experimental) aws.s3@ObjectCreated event types for Bucket.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import events as s3_events
            
            object_created = s3_events.BucketEvents.ObjectCreated()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectCreated.Bucket",
            jsii_struct_bases=[],
            name_mapping={"name": "name"},
        )
        class Bucket:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Bucket.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Bucket reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    bucket = s3_events.BucketEvents.ObjectCreated.Bucket(
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__56aa57fef98dc3b87e578af3e4a30ee9c21c4ab8f79febc0ff4d216906086e34)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Bucket reference

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Bucket(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectCreated.ObjectCreatedProps",
            jsii_struct_bases=[],
            name_mapping={
                "bucket": "bucket",
                "event_metadata": "eventMetadata",
                "object": "object",
                "reason": "reason",
                "requester": "requester",
                "request_id": "requestId",
                "source_ip_address": "sourceIpAddress",
                "version": "version",
            },
        )
        class ObjectCreatedProps:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Union["BucketEvents.ObjectCreated.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                object: typing.Optional[typing.Union["BucketEvents.ObjectCreated.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
                reason: typing.Optional[typing.Sequence[builtins.str]] = None,
                requester: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Bucket aws.s3@ObjectCreated event.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reason: (experimental) reason property. Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_ip_address: (experimental) source-ip-address property. Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: infused

                Example::

                    from aws_cdk.mixins_preview.aws_s3.events import BucketEvents
                    import aws_cdk.aws_events as events
                    import aws_cdk.aws_events_targets as targets
                    # fn: lambda.Function
                    
                    
                    # Works with L2 constructs
                    bucket = s3.Bucket(scope, "Bucket")
                    bucket_events = BucketEvents.from_bucket(bucket)
                    
                    events.Rule(scope, "Rule",
                        event_pattern=bucket_events.object_created_pattern(
                            object=BucketEvents.ObjectCreated.ObjectType(key=["uploads/*"])
                        ),
                        targets=[targets.LambdaFunction(fn)]
                    )
                    
                    # Also works with L1 constructs
                    cfn_bucket = s3.CfnBucket(scope, "CfnBucket")
                    cfn_bucket_events = BucketEvents.from_bucket(cfn_bucket)
                    
                    events.CfnRule(scope, "CfnRule",
                        state="ENABLED",
                        event_pattern=cfn_bucket_events.object_created_pattern(
                            object=BucketEvents.ObjectCreated.ObjectType(key=["uploads/*"])
                        ),
                        targets=[events.CfnRule.TargetProperty(arn=fn.function_arn, id="L1")]
                    )
                '''
                if isinstance(bucket, dict):
                    bucket = BucketEvents.ObjectCreated.Bucket(**bucket)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(object, dict):
                    object = BucketEvents.ObjectCreated.ObjectType(**object)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__602129be747ca8e87a419f3ab3a3b4774eb0baa17c9883b2e21d8ed01787ea44)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                    check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                    check_type(argname="argument requester", value=requester, expected_type=type_hints["requester"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument source_ip_address", value=source_ip_address, expected_type=type_hints["source_ip_address"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if object is not None:
                    self._values["object"] = object
                if reason is not None:
                    self._values["reason"] = reason
                if requester is not None:
                    self._values["requester"] = requester
                if request_id is not None:
                    self._values["request_id"] = request_id
                if source_ip_address is not None:
                    self._values["source_ip_address"] = source_ip_address
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def bucket(self) -> typing.Optional["BucketEvents.ObjectCreated.Bucket"]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional["BucketEvents.ObjectCreated.Bucket"], result)

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
            def object(
                self,
            ) -> typing.Optional["BucketEvents.ObjectCreated.ObjectType"]:
                '''(experimental) object property.

                Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("object")
                return typing.cast(typing.Optional["BucketEvents.ObjectCreated.ObjectType"], result)

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
            def requester(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester property.

                Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) request-id property.

                Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) source-ip-address property.

                Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_ip_address")
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
                return "ObjectCreatedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectCreated.ObjectType",
            jsii_struct_bases=[],
            name_mapping={
                "etag": "etag",
                "key": "key",
                "sequencer": "sequencer",
                "size": "size",
                "version_id": "versionId",
            },
        )
        class ObjectType:
            def __init__(
                self,
                *,
                etag: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                sequencer: typing.Optional[typing.Sequence[builtins.str]] = None,
                size: typing.Optional[typing.Sequence[builtins.str]] = None,
                version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Object.

                :param etag: (experimental) etag property. Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param sequencer: (experimental) sequencer property. Specify an array of string values to match this event if the actual value of sequencer is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param size: (experimental) size property. Specify an array of string values to match this event if the actual value of size is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version_id: (experimental) version-id property. Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: infused

                Example::

                    from aws_cdk.mixins_preview.aws_s3.events import BucketEvents
                    import aws_cdk.aws_events as events
                    import aws_cdk.aws_events_targets as targets
                    # fn: lambda.Function
                    
                    
                    # Works with L2 constructs
                    bucket = s3.Bucket(scope, "Bucket")
                    bucket_events = BucketEvents.from_bucket(bucket)
                    
                    events.Rule(scope, "Rule",
                        event_pattern=bucket_events.object_created_pattern(
                            object=BucketEvents.ObjectCreated.ObjectType(key=["uploads/*"])
                        ),
                        targets=[targets.LambdaFunction(fn)]
                    )
                    
                    # Also works with L1 constructs
                    cfn_bucket = s3.CfnBucket(scope, "CfnBucket")
                    cfn_bucket_events = BucketEvents.from_bucket(cfn_bucket)
                    
                    events.CfnRule(scope, "CfnRule",
                        state="ENABLED",
                        event_pattern=cfn_bucket_events.object_created_pattern(
                            object=BucketEvents.ObjectCreated.ObjectType(key=["uploads/*"])
                        ),
                        targets=[events.CfnRule.TargetProperty(arn=fn.function_arn, id="L1")]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__20d91c1779ea5ce4eb606d804d63905b1cb2f7a6bc2398e8807c5a9ae052b5c5)
                    check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument sequencer", value=sequencer, expected_type=type_hints["sequencer"])
                    check_type(argname="argument size", value=size, expected_type=type_hints["size"])
                    check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if etag is not None:
                    self._values["etag"] = etag
                if key is not None:
                    self._values["key"] = key
                if sequencer is not None:
                    self._values["sequencer"] = sequencer
                if size is not None:
                    self._values["size"] = size
                if version_id is not None:
                    self._values["version_id"] = version_id

            @builtins.property
            def etag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) etag property.

                Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("etag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) key property.

                Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def sequencer(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sequencer property.

                Specify an array of string values to match this event if the actual value of sequencer is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("sequencer")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def size(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) size property.

                Specify an array of string values to match this event if the actual value of size is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("size")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version-id property.

                Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ObjectType(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ObjectDeleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectDeleted",
    ):
        '''(experimental) aws.s3@ObjectDeleted event types for Bucket.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import events as s3_events
            
            object_deleted = s3_events.BucketEvents.ObjectDeleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectDeleted.Bucket",
            jsii_struct_bases=[],
            name_mapping={"name": "name"},
        )
        class Bucket:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Bucket.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Bucket reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    bucket = s3_events.BucketEvents.ObjectDeleted.Bucket(
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__285a7194159677c65e016078648da1c82d52936e0a1962f989ecc5a9daee9d99)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Bucket reference

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Bucket(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectDeleted.ObjectDeletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "bucket": "bucket",
                "deletion_type": "deletionType",
                "event_metadata": "eventMetadata",
                "object": "object",
                "reason": "reason",
                "requester": "requester",
                "request_id": "requestId",
                "source_ip_address": "sourceIpAddress",
                "version": "version",
            },
        )
        class ObjectDeletedProps:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Union["BucketEvents.ObjectDeleted.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
                deletion_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                object: typing.Optional[typing.Union["BucketEvents.ObjectDeleted.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
                reason: typing.Optional[typing.Sequence[builtins.str]] = None,
                requester: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Bucket aws.s3@ObjectDeleted event.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param deletion_type: (experimental) deletion-type property. Specify an array of string values to match this event if the actual value of deletion-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reason: (experimental) reason property. Specify an array of string values to match this event if the actual value of reason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_ip_address: (experimental) source-ip-address property. Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_deleted_props = s3_events.BucketEvents.ObjectDeleted.ObjectDeletedProps(
                        bucket=s3_events.BucketEvents.ObjectDeleted.Bucket(
                            name=["name"]
                        ),
                        deletion_type=["deletionType"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        object=s3_events.BucketEvents.ObjectDeleted.ObjectType(
                            etag=["etag"],
                            key=["key"],
                            sequencer=["sequencer"],
                            version_id=["versionId"]
                        ),
                        reason=["reason"],
                        requester=["requester"],
                        request_id=["requestId"],
                        source_ip_address=["sourceIpAddress"],
                        version=["version"]
                    )
                '''
                if isinstance(bucket, dict):
                    bucket = BucketEvents.ObjectDeleted.Bucket(**bucket)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(object, dict):
                    object = BucketEvents.ObjectDeleted.ObjectType(**object)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__864a88170a771d553ec6e23a4197d17e004cab55c52b2e24df0b772db127cf73)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument deletion_type", value=deletion_type, expected_type=type_hints["deletion_type"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                    check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                    check_type(argname="argument requester", value=requester, expected_type=type_hints["requester"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument source_ip_address", value=source_ip_address, expected_type=type_hints["source_ip_address"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if deletion_type is not None:
                    self._values["deletion_type"] = deletion_type
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if object is not None:
                    self._values["object"] = object
                if reason is not None:
                    self._values["reason"] = reason
                if requester is not None:
                    self._values["requester"] = requester
                if request_id is not None:
                    self._values["request_id"] = request_id
                if source_ip_address is not None:
                    self._values["source_ip_address"] = source_ip_address
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def bucket(self) -> typing.Optional["BucketEvents.ObjectDeleted.Bucket"]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional["BucketEvents.ObjectDeleted.Bucket"], result)

            @builtins.property
            def deletion_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) deletion-type property.

                Specify an array of string values to match this event if the actual value of deletion-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("deletion_type")
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
            def object(
                self,
            ) -> typing.Optional["BucketEvents.ObjectDeleted.ObjectType"]:
                '''(experimental) object property.

                Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("object")
                return typing.cast(typing.Optional["BucketEvents.ObjectDeleted.ObjectType"], result)

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
            def requester(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester property.

                Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) request-id property.

                Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) source-ip-address property.

                Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_ip_address")
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
                return "ObjectDeletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectDeleted.ObjectType",
            jsii_struct_bases=[],
            name_mapping={
                "etag": "etag",
                "key": "key",
                "sequencer": "sequencer",
                "version_id": "versionId",
            },
        )
        class ObjectType:
            def __init__(
                self,
                *,
                etag: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                sequencer: typing.Optional[typing.Sequence[builtins.str]] = None,
                version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Object.

                :param etag: (experimental) etag property. Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param sequencer: (experimental) sequencer property. Specify an array of string values to match this event if the actual value of sequencer is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version_id: (experimental) version-id property. Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_type = s3_events.BucketEvents.ObjectDeleted.ObjectType(
                        etag=["etag"],
                        key=["key"],
                        sequencer=["sequencer"],
                        version_id=["versionId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__b554a718b7cbd70f36979f3a3e31f98ba0ff823f6c4f0bae2f16ea7fb502e19f)
                    check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument sequencer", value=sequencer, expected_type=type_hints["sequencer"])
                    check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if etag is not None:
                    self._values["etag"] = etag
                if key is not None:
                    self._values["key"] = key
                if sequencer is not None:
                    self._values["sequencer"] = sequencer
                if version_id is not None:
                    self._values["version_id"] = version_id

            @builtins.property
            def etag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) etag property.

                Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("etag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) key property.

                Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def sequencer(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sequencer property.

                Specify an array of string values to match this event if the actual value of sequencer is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("sequencer")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version-id property.

                Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ObjectType(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ObjectRestoreCompleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectRestoreCompleted",
    ):
        '''(experimental) aws.s3@ObjectRestoreCompleted event types for Bucket.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import events as s3_events
            
            object_restore_completed = s3_events.BucketEvents.ObjectRestoreCompleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectRestoreCompleted.Bucket",
            jsii_struct_bases=[],
            name_mapping={"name": "name"},
        )
        class Bucket:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Bucket.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Bucket reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    bucket = s3_events.BucketEvents.ObjectRestoreCompleted.Bucket(
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7ee2803b1c4790b6083ed75c09961c7b4f2221982e7c7eaf493a0c5ead8aad82)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Bucket reference

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Bucket(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectRestoreCompleted.ObjectRestoreCompletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "bucket": "bucket",
                "event_metadata": "eventMetadata",
                "object": "object",
                "requester": "requester",
                "request_id": "requestId",
                "restore_expiry_time": "restoreExpiryTime",
                "source_storage_class": "sourceStorageClass",
                "version": "version",
            },
        )
        class ObjectRestoreCompletedProps:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Union["BucketEvents.ObjectRestoreCompleted.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                object: typing.Optional[typing.Union["BucketEvents.ObjectRestoreCompleted.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
                requester: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                restore_expiry_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_storage_class: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Bucket aws.s3@ObjectRestoreCompleted event.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param restore_expiry_time: (experimental) restore-expiry-time property. Specify an array of string values to match this event if the actual value of restore-expiry-time is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_storage_class: (experimental) source-storage-class property. Specify an array of string values to match this event if the actual value of source-storage-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_restore_completed_props = s3_events.BucketEvents.ObjectRestoreCompleted.ObjectRestoreCompletedProps(
                        bucket=s3_events.BucketEvents.ObjectRestoreCompleted.Bucket(
                            name=["name"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        object=s3_events.BucketEvents.ObjectRestoreCompleted.ObjectType(
                            etag=["etag"],
                            key=["key"],
                            size=["size"],
                            version_id=["versionId"]
                        ),
                        requester=["requester"],
                        request_id=["requestId"],
                        restore_expiry_time=["restoreExpiryTime"],
                        source_storage_class=["sourceStorageClass"],
                        version=["version"]
                    )
                '''
                if isinstance(bucket, dict):
                    bucket = BucketEvents.ObjectRestoreCompleted.Bucket(**bucket)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(object, dict):
                    object = BucketEvents.ObjectRestoreCompleted.ObjectType(**object)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1223f200d906355ae0f59566787ec2b672ae375c7adc49a97071d322adcfef8c)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                    check_type(argname="argument requester", value=requester, expected_type=type_hints["requester"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument restore_expiry_time", value=restore_expiry_time, expected_type=type_hints["restore_expiry_time"])
                    check_type(argname="argument source_storage_class", value=source_storage_class, expected_type=type_hints["source_storage_class"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if object is not None:
                    self._values["object"] = object
                if requester is not None:
                    self._values["requester"] = requester
                if request_id is not None:
                    self._values["request_id"] = request_id
                if restore_expiry_time is not None:
                    self._values["restore_expiry_time"] = restore_expiry_time
                if source_storage_class is not None:
                    self._values["source_storage_class"] = source_storage_class
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def bucket(
                self,
            ) -> typing.Optional["BucketEvents.ObjectRestoreCompleted.Bucket"]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional["BucketEvents.ObjectRestoreCompleted.Bucket"], result)

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
            def object(
                self,
            ) -> typing.Optional["BucketEvents.ObjectRestoreCompleted.ObjectType"]:
                '''(experimental) object property.

                Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("object")
                return typing.cast(typing.Optional["BucketEvents.ObjectRestoreCompleted.ObjectType"], result)

            @builtins.property
            def requester(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester property.

                Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) request-id property.

                Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def restore_expiry_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) restore-expiry-time property.

                Specify an array of string values to match this event if the actual value of restore-expiry-time is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("restore_expiry_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_storage_class(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) source-storage-class property.

                Specify an array of string values to match this event if the actual value of source-storage-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_storage_class")
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
                return "ObjectRestoreCompletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectRestoreCompleted.ObjectType",
            jsii_struct_bases=[],
            name_mapping={
                "etag": "etag",
                "key": "key",
                "size": "size",
                "version_id": "versionId",
            },
        )
        class ObjectType:
            def __init__(
                self,
                *,
                etag: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                size: typing.Optional[typing.Sequence[builtins.str]] = None,
                version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Object.

                :param etag: (experimental) etag property. Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param size: (experimental) size property. Specify an array of string values to match this event if the actual value of size is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version_id: (experimental) version-id property. Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_type = s3_events.BucketEvents.ObjectRestoreCompleted.ObjectType(
                        etag=["etag"],
                        key=["key"],
                        size=["size"],
                        version_id=["versionId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__2df0c188684131916b089757f1a3c0712b5e28d99c750dc66ff40ebeeacc49ff)
                    check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument size", value=size, expected_type=type_hints["size"])
                    check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if etag is not None:
                    self._values["etag"] = etag
                if key is not None:
                    self._values["key"] = key
                if size is not None:
                    self._values["size"] = size
                if version_id is not None:
                    self._values["version_id"] = version_id

            @builtins.property
            def etag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) etag property.

                Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("etag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) key property.

                Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def size(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) size property.

                Specify an array of string values to match this event if the actual value of size is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("size")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version-id property.

                Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ObjectType(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ObjectRestoreExpired(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectRestoreExpired",
    ):
        '''(experimental) aws.s3@ObjectRestoreExpired event types for Bucket.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import events as s3_events
            
            object_restore_expired = s3_events.BucketEvents.ObjectRestoreExpired()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectRestoreExpired.Bucket",
            jsii_struct_bases=[],
            name_mapping={"name": "name"},
        )
        class Bucket:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Bucket.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Bucket reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    bucket = s3_events.BucketEvents.ObjectRestoreExpired.Bucket(
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7ed0223c641eba1877beef37408551f96482d373a528a6f8e926cc774bd03c25)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Bucket reference

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Bucket(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectRestoreExpired.ObjectRestoreExpiredProps",
            jsii_struct_bases=[],
            name_mapping={
                "bucket": "bucket",
                "event_metadata": "eventMetadata",
                "object": "object",
                "requester": "requester",
                "request_id": "requestId",
                "version": "version",
            },
        )
        class ObjectRestoreExpiredProps:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Union["BucketEvents.ObjectRestoreExpired.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                object: typing.Optional[typing.Union["BucketEvents.ObjectRestoreExpired.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
                requester: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Bucket aws.s3@ObjectRestoreExpired event.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_restore_expired_props = s3_events.BucketEvents.ObjectRestoreExpired.ObjectRestoreExpiredProps(
                        bucket=s3_events.BucketEvents.ObjectRestoreExpired.Bucket(
                            name=["name"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        object=s3_events.BucketEvents.ObjectRestoreExpired.ObjectType(
                            etag=["etag"],
                            key=["key"],
                            version_id=["versionId"]
                        ),
                        requester=["requester"],
                        request_id=["requestId"],
                        version=["version"]
                    )
                '''
                if isinstance(bucket, dict):
                    bucket = BucketEvents.ObjectRestoreExpired.Bucket(**bucket)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(object, dict):
                    object = BucketEvents.ObjectRestoreExpired.ObjectType(**object)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__5a3ed35478cb122c6c7a752b05dc0428d92624f5d102369f9d2fd81c6d32c03d)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                    check_type(argname="argument requester", value=requester, expected_type=type_hints["requester"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if object is not None:
                    self._values["object"] = object
                if requester is not None:
                    self._values["requester"] = requester
                if request_id is not None:
                    self._values["request_id"] = request_id
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def bucket(
                self,
            ) -> typing.Optional["BucketEvents.ObjectRestoreExpired.Bucket"]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional["BucketEvents.ObjectRestoreExpired.Bucket"], result)

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
            def object(
                self,
            ) -> typing.Optional["BucketEvents.ObjectRestoreExpired.ObjectType"]:
                '''(experimental) object property.

                Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("object")
                return typing.cast(typing.Optional["BucketEvents.ObjectRestoreExpired.ObjectType"], result)

            @builtins.property
            def requester(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester property.

                Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) request-id property.

                Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
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
                return "ObjectRestoreExpiredProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectRestoreExpired.ObjectType",
            jsii_struct_bases=[],
            name_mapping={"etag": "etag", "key": "key", "version_id": "versionId"},
        )
        class ObjectType:
            def __init__(
                self,
                *,
                etag: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Object.

                :param etag: (experimental) etag property. Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version_id: (experimental) version-id property. Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_type = s3_events.BucketEvents.ObjectRestoreExpired.ObjectType(
                        etag=["etag"],
                        key=["key"],
                        version_id=["versionId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4b4ef44b0b9511ccdb6ac8c9d93c5ae2aba915fc3a1e050c640202a6adbb652c)
                    check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if etag is not None:
                    self._values["etag"] = etag
                if key is not None:
                    self._values["key"] = key
                if version_id is not None:
                    self._values["version_id"] = version_id

            @builtins.property
            def etag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) etag property.

                Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("etag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) key property.

                Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version-id property.

                Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ObjectType(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ObjectRestoreInitiated(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectRestoreInitiated",
    ):
        '''(experimental) aws.s3@ObjectRestoreInitiated event types for Bucket.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import events as s3_events
            
            object_restore_initiated = s3_events.BucketEvents.ObjectRestoreInitiated()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectRestoreInitiated.Bucket",
            jsii_struct_bases=[],
            name_mapping={"name": "name"},
        )
        class Bucket:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Bucket.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Bucket reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    bucket = s3_events.BucketEvents.ObjectRestoreInitiated.Bucket(
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__24eb5988b049ef988c175a10ff8b368adf39cfb6a04b9c739e4121419ba3d2bd)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Bucket reference

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Bucket(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectRestoreInitiated.ObjectRestoreInitiatedProps",
            jsii_struct_bases=[],
            name_mapping={
                "bucket": "bucket",
                "event_metadata": "eventMetadata",
                "object": "object",
                "requester": "requester",
                "request_id": "requestId",
                "source_ip_address": "sourceIpAddress",
                "source_storage_class": "sourceStorageClass",
                "version": "version",
            },
        )
        class ObjectRestoreInitiatedProps:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Union["BucketEvents.ObjectRestoreInitiated.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                object: typing.Optional[typing.Union["BucketEvents.ObjectRestoreInitiated.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
                requester: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_storage_class: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Bucket aws.s3@ObjectRestoreInitiated event.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_ip_address: (experimental) source-ip-address property. Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_storage_class: (experimental) source-storage-class property. Specify an array of string values to match this event if the actual value of source-storage-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_restore_initiated_props = s3_events.BucketEvents.ObjectRestoreInitiated.ObjectRestoreInitiatedProps(
                        bucket=s3_events.BucketEvents.ObjectRestoreInitiated.Bucket(
                            name=["name"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        object=s3_events.BucketEvents.ObjectRestoreInitiated.ObjectType(
                            etag=["etag"],
                            key=["key"],
                            size=["size"],
                            version_id=["versionId"]
                        ),
                        requester=["requester"],
                        request_id=["requestId"],
                        source_ip_address=["sourceIpAddress"],
                        source_storage_class=["sourceStorageClass"],
                        version=["version"]
                    )
                '''
                if isinstance(bucket, dict):
                    bucket = BucketEvents.ObjectRestoreInitiated.Bucket(**bucket)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(object, dict):
                    object = BucketEvents.ObjectRestoreInitiated.ObjectType(**object)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__279102aecd842e5a0ac34ee026f9b384434913d89c23f9cd5529fee3a15c0e35)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                    check_type(argname="argument requester", value=requester, expected_type=type_hints["requester"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument source_ip_address", value=source_ip_address, expected_type=type_hints["source_ip_address"])
                    check_type(argname="argument source_storage_class", value=source_storage_class, expected_type=type_hints["source_storage_class"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if object is not None:
                    self._values["object"] = object
                if requester is not None:
                    self._values["requester"] = requester
                if request_id is not None:
                    self._values["request_id"] = request_id
                if source_ip_address is not None:
                    self._values["source_ip_address"] = source_ip_address
                if source_storage_class is not None:
                    self._values["source_storage_class"] = source_storage_class
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def bucket(
                self,
            ) -> typing.Optional["BucketEvents.ObjectRestoreInitiated.Bucket"]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional["BucketEvents.ObjectRestoreInitiated.Bucket"], result)

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
            def object(
                self,
            ) -> typing.Optional["BucketEvents.ObjectRestoreInitiated.ObjectType"]:
                '''(experimental) object property.

                Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("object")
                return typing.cast(typing.Optional["BucketEvents.ObjectRestoreInitiated.ObjectType"], result)

            @builtins.property
            def requester(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester property.

                Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) request-id property.

                Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) source-ip-address property.

                Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_ip_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_storage_class(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) source-storage-class property.

                Specify an array of string values to match this event if the actual value of source-storage-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_storage_class")
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
                return "ObjectRestoreInitiatedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectRestoreInitiated.ObjectType",
            jsii_struct_bases=[],
            name_mapping={
                "etag": "etag",
                "key": "key",
                "size": "size",
                "version_id": "versionId",
            },
        )
        class ObjectType:
            def __init__(
                self,
                *,
                etag: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                size: typing.Optional[typing.Sequence[builtins.str]] = None,
                version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Object.

                :param etag: (experimental) etag property. Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param size: (experimental) size property. Specify an array of string values to match this event if the actual value of size is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version_id: (experimental) version-id property. Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_type = s3_events.BucketEvents.ObjectRestoreInitiated.ObjectType(
                        etag=["etag"],
                        key=["key"],
                        size=["size"],
                        version_id=["versionId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cbdba86dfb82e8966d8ba510eefb864c0fe4511f6e50d6fb313ba83d4403d615)
                    check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument size", value=size, expected_type=type_hints["size"])
                    check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if etag is not None:
                    self._values["etag"] = etag
                if key is not None:
                    self._values["key"] = key
                if size is not None:
                    self._values["size"] = size
                if version_id is not None:
                    self._values["version_id"] = version_id

            @builtins.property
            def etag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) etag property.

                Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("etag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) key property.

                Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def size(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) size property.

                Specify an array of string values to match this event if the actual value of size is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("size")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version-id property.

                Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ObjectType(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ObjectStorageClassChanged(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectStorageClassChanged",
    ):
        '''(experimental) aws.s3@ObjectStorageClassChanged event types for Bucket.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import events as s3_events
            
            object_storage_class_changed = s3_events.BucketEvents.ObjectStorageClassChanged()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectStorageClassChanged.Bucket",
            jsii_struct_bases=[],
            name_mapping={"name": "name"},
        )
        class Bucket:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Bucket.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Bucket reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    bucket = s3_events.BucketEvents.ObjectStorageClassChanged.Bucket(
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__9f7469469631e7420ef3881a72b6acf3d31719797ea12981ef73660e8d493a21)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Bucket reference

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Bucket(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectStorageClassChanged.ObjectStorageClassChangedProps",
            jsii_struct_bases=[],
            name_mapping={
                "bucket": "bucket",
                "destination_storage_class": "destinationStorageClass",
                "event_metadata": "eventMetadata",
                "object": "object",
                "requester": "requester",
                "request_id": "requestId",
                "version": "version",
            },
        )
        class ObjectStorageClassChangedProps:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Union["BucketEvents.ObjectStorageClassChanged.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
                destination_storage_class: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                object: typing.Optional[typing.Union["BucketEvents.ObjectStorageClassChanged.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
                requester: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Bucket aws.s3@ObjectStorageClassChanged event.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param destination_storage_class: (experimental) destination-storage-class property. Specify an array of string values to match this event if the actual value of destination-storage-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_storage_class_changed_props = s3_events.BucketEvents.ObjectStorageClassChanged.ObjectStorageClassChangedProps(
                        bucket=s3_events.BucketEvents.ObjectStorageClassChanged.Bucket(
                            name=["name"]
                        ),
                        destination_storage_class=["destinationStorageClass"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        object=s3_events.BucketEvents.ObjectStorageClassChanged.ObjectType(
                            etag=["etag"],
                            key=["key"],
                            size=["size"],
                            version_id=["versionId"]
                        ),
                        requester=["requester"],
                        request_id=["requestId"],
                        version=["version"]
                    )
                '''
                if isinstance(bucket, dict):
                    bucket = BucketEvents.ObjectStorageClassChanged.Bucket(**bucket)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(object, dict):
                    object = BucketEvents.ObjectStorageClassChanged.ObjectType(**object)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cec9be9f373cda5651134174ed8f61ae2b3b7584a37d2ab94b666295f978a51a)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument destination_storage_class", value=destination_storage_class, expected_type=type_hints["destination_storage_class"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                    check_type(argname="argument requester", value=requester, expected_type=type_hints["requester"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if destination_storage_class is not None:
                    self._values["destination_storage_class"] = destination_storage_class
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if object is not None:
                    self._values["object"] = object
                if requester is not None:
                    self._values["requester"] = requester
                if request_id is not None:
                    self._values["request_id"] = request_id
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def bucket(
                self,
            ) -> typing.Optional["BucketEvents.ObjectStorageClassChanged.Bucket"]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional["BucketEvents.ObjectStorageClassChanged.Bucket"], result)

            @builtins.property
            def destination_storage_class(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) destination-storage-class property.

                Specify an array of string values to match this event if the actual value of destination-storage-class is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("destination_storage_class")
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
            def object(
                self,
            ) -> typing.Optional["BucketEvents.ObjectStorageClassChanged.ObjectType"]:
                '''(experimental) object property.

                Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("object")
                return typing.cast(typing.Optional["BucketEvents.ObjectStorageClassChanged.ObjectType"], result)

            @builtins.property
            def requester(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester property.

                Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) request-id property.

                Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
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
                return "ObjectStorageClassChangedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectStorageClassChanged.ObjectType",
            jsii_struct_bases=[],
            name_mapping={
                "etag": "etag",
                "key": "key",
                "size": "size",
                "version_id": "versionId",
            },
        )
        class ObjectType:
            def __init__(
                self,
                *,
                etag: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                size: typing.Optional[typing.Sequence[builtins.str]] = None,
                version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Object.

                :param etag: (experimental) etag property. Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param size: (experimental) size property. Specify an array of string values to match this event if the actual value of size is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version_id: (experimental) version-id property. Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_type = s3_events.BucketEvents.ObjectStorageClassChanged.ObjectType(
                        etag=["etag"],
                        key=["key"],
                        size=["size"],
                        version_id=["versionId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__79ed74d2ff5ae16d6b027c75884473d6a4abb4af78f52d2e1e2cf6a6642d8e33)
                    check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument size", value=size, expected_type=type_hints["size"])
                    check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if etag is not None:
                    self._values["etag"] = etag
                if key is not None:
                    self._values["key"] = key
                if size is not None:
                    self._values["size"] = size
                if version_id is not None:
                    self._values["version_id"] = version_id

            @builtins.property
            def etag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) etag property.

                Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("etag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) key property.

                Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def size(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) size property.

                Specify an array of string values to match this event if the actual value of size is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("size")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version-id property.

                Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ObjectType(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ObjectTagsAdded(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectTagsAdded",
    ):
        '''(experimental) aws.s3@ObjectTagsAdded event types for Bucket.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import events as s3_events
            
            object_tags_added = s3_events.BucketEvents.ObjectTagsAdded()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectTagsAdded.Bucket",
            jsii_struct_bases=[],
            name_mapping={"name": "name"},
        )
        class Bucket:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Bucket.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Bucket reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    bucket = s3_events.BucketEvents.ObjectTagsAdded.Bucket(
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__22388f4126961dc03bd508a8d42766063b7ba7bd5d13225475455fa8e72744ce)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Bucket reference

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Bucket(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectTagsAdded.ObjectTagsAddedProps",
            jsii_struct_bases=[],
            name_mapping={
                "bucket": "bucket",
                "event_metadata": "eventMetadata",
                "object": "object",
                "requester": "requester",
                "request_id": "requestId",
                "source_ip_address": "sourceIpAddress",
                "version": "version",
            },
        )
        class ObjectTagsAddedProps:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Union["BucketEvents.ObjectTagsAdded.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                object: typing.Optional[typing.Union["BucketEvents.ObjectTagsAdded.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
                requester: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Bucket aws.s3@ObjectTagsAdded event.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_ip_address: (experimental) source-ip-address property. Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_tags_added_props = s3_events.BucketEvents.ObjectTagsAdded.ObjectTagsAddedProps(
                        bucket=s3_events.BucketEvents.ObjectTagsAdded.Bucket(
                            name=["name"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        object=s3_events.BucketEvents.ObjectTagsAdded.ObjectType(
                            etag=["etag"],
                            key=["key"],
                            version_id=["versionId"]
                        ),
                        requester=["requester"],
                        request_id=["requestId"],
                        source_ip_address=["sourceIpAddress"],
                        version=["version"]
                    )
                '''
                if isinstance(bucket, dict):
                    bucket = BucketEvents.ObjectTagsAdded.Bucket(**bucket)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(object, dict):
                    object = BucketEvents.ObjectTagsAdded.ObjectType(**object)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__0c87bd36082ff98f8bbe53a20ce975c171dfcd6a5b49643fc7b67ccc49f445d6)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                    check_type(argname="argument requester", value=requester, expected_type=type_hints["requester"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument source_ip_address", value=source_ip_address, expected_type=type_hints["source_ip_address"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if object is not None:
                    self._values["object"] = object
                if requester is not None:
                    self._values["requester"] = requester
                if request_id is not None:
                    self._values["request_id"] = request_id
                if source_ip_address is not None:
                    self._values["source_ip_address"] = source_ip_address
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def bucket(self) -> typing.Optional["BucketEvents.ObjectTagsAdded.Bucket"]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional["BucketEvents.ObjectTagsAdded.Bucket"], result)

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
            def object(
                self,
            ) -> typing.Optional["BucketEvents.ObjectTagsAdded.ObjectType"]:
                '''(experimental) object property.

                Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("object")
                return typing.cast(typing.Optional["BucketEvents.ObjectTagsAdded.ObjectType"], result)

            @builtins.property
            def requester(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester property.

                Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) request-id property.

                Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) source-ip-address property.

                Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_ip_address")
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
                return "ObjectTagsAddedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectTagsAdded.ObjectType",
            jsii_struct_bases=[],
            name_mapping={"etag": "etag", "key": "key", "version_id": "versionId"},
        )
        class ObjectType:
            def __init__(
                self,
                *,
                etag: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Object.

                :param etag: (experimental) etag property. Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version_id: (experimental) version-id property. Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_type = s3_events.BucketEvents.ObjectTagsAdded.ObjectType(
                        etag=["etag"],
                        key=["key"],
                        version_id=["versionId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__5da27a508a15808b42526c0453019293b7bcd03eabb48eaeaef100a0af302ac2)
                    check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if etag is not None:
                    self._values["etag"] = etag
                if key is not None:
                    self._values["key"] = key
                if version_id is not None:
                    self._values["version_id"] = version_id

            @builtins.property
            def etag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) etag property.

                Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("etag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) key property.

                Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version-id property.

                Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ObjectType(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ObjectTagsDeleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectTagsDeleted",
    ):
        '''(experimental) aws.s3@ObjectTagsDeleted event types for Bucket.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import events as s3_events
            
            object_tags_deleted = s3_events.BucketEvents.ObjectTagsDeleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectTagsDeleted.Bucket",
            jsii_struct_bases=[],
            name_mapping={"name": "name"},
        )
        class Bucket:
            def __init__(
                self,
                *,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Bucket.

                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Bucket reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    bucket = s3_events.BucketEvents.ObjectTagsDeleted.Bucket(
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7a2ac0545d15e7dd7c0b416b20821be7fc34e2ac18a1b9e4840fdd83805fcff1)
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Bucket reference

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Bucket(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectTagsDeleted.ObjectTagsDeletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "bucket": "bucket",
                "event_metadata": "eventMetadata",
                "object": "object",
                "requester": "requester",
                "request_id": "requestId",
                "source_ip_address": "sourceIpAddress",
                "version": "version",
            },
        )
        class ObjectTagsDeletedProps:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Union["BucketEvents.ObjectTagsDeleted.Bucket", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                object: typing.Optional[typing.Union["BucketEvents.ObjectTagsDeleted.ObjectType", typing.Dict[builtins.str, typing.Any]]] = None,
                requester: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Bucket aws.s3@ObjectTagsDeleted event.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param object: (experimental) object property. Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester: (experimental) requester property. Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) request-id property. Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_ip_address: (experimental) source-ip-address property. Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_tags_deleted_props = s3_events.BucketEvents.ObjectTagsDeleted.ObjectTagsDeletedProps(
                        bucket=s3_events.BucketEvents.ObjectTagsDeleted.Bucket(
                            name=["name"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        object=s3_events.BucketEvents.ObjectTagsDeleted.ObjectType(
                            etag=["etag"],
                            key=["key"],
                            version_id=["versionId"]
                        ),
                        requester=["requester"],
                        request_id=["requestId"],
                        source_ip_address=["sourceIpAddress"],
                        version=["version"]
                    )
                '''
                if isinstance(bucket, dict):
                    bucket = BucketEvents.ObjectTagsDeleted.Bucket(**bucket)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(object, dict):
                    object = BucketEvents.ObjectTagsDeleted.ObjectType(**object)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__409f3b41d0aa14ecaace1a8a722291d854000dabde63118e7d3d554ebc03c3c3)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                    check_type(argname="argument requester", value=requester, expected_type=type_hints["requester"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument source_ip_address", value=source_ip_address, expected_type=type_hints["source_ip_address"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if object is not None:
                    self._values["object"] = object
                if requester is not None:
                    self._values["requester"] = requester
                if request_id is not None:
                    self._values["request_id"] = request_id
                if source_ip_address is not None:
                    self._values["source_ip_address"] = source_ip_address
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def bucket(
                self,
            ) -> typing.Optional["BucketEvents.ObjectTagsDeleted.Bucket"]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional["BucketEvents.ObjectTagsDeleted.Bucket"], result)

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
            def object(
                self,
            ) -> typing.Optional["BucketEvents.ObjectTagsDeleted.ObjectType"]:
                '''(experimental) object property.

                Specify an array of string values to match this event if the actual value of object is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("object")
                return typing.cast(typing.Optional["BucketEvents.ObjectTagsDeleted.ObjectType"], result)

            @builtins.property
            def requester(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester property.

                Specify an array of string values to match this event if the actual value of requester is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) request-id property.

                Specify an array of string values to match this event if the actual value of request-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) source-ip-address property.

                Specify an array of string values to match this event if the actual value of source-ip-address is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_ip_address")
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
                return "ObjectTagsDeletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_s3.events.BucketEvents.ObjectTagsDeleted.ObjectType",
            jsii_struct_bases=[],
            name_mapping={"etag": "etag", "key": "key", "version_id": "versionId"},
        )
        class ObjectType:
            def __init__(
                self,
                *,
                etag: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Object.

                :param etag: (experimental) etag property. Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version_id: (experimental) version-id property. Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_s3 import events as s3_events
                    
                    object_type = s3_events.BucketEvents.ObjectTagsDeleted.ObjectType(
                        etag=["etag"],
                        key=["key"],
                        version_id=["versionId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__6e15668e73b796d7cd3ea118987bc9a9b74298e1c9d74616327d3184796fefde)
                    check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if etag is not None:
                    self._values["etag"] = etag
                if key is not None:
                    self._values["key"] = key
                if version_id is not None:
                    self._values["version_id"] = version_id

            @builtins.property
            def etag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) etag property.

                Specify an array of string values to match this event if the actual value of etag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("etag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) key property.

                Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version-id property.

                Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ObjectType(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "BucketEvents",
]

publication.publish()

def _typecheckingstub__8845cfe51d7496b37755a7037f2d27a6431cd115419057db034a1a305c26d0cf(
    bucket_ref: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d36fe61032be2ae29f5a9abe4545d60e6f1d1c42d43fd680fbe57a65dcdd77(
    *,
    additional_event_data: typing.Optional[typing.Union[BucketEvents.AWSAPICallViaCloudTrail.AdditionalEventData, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_category: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    management_event: typing.Optional[typing.Sequence[builtins.str]] = None,
    read_only: typing.Optional[typing.Sequence[builtins.str]] = None,
    recipient_account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_parameters: typing.Optional[typing.Union[BucketEvents.AWSAPICallViaCloudTrail.RequestParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    resources: typing.Optional[typing.Sequence[typing.Union[BucketEvents.AWSAPICallViaCloudTrail.AwsapiCallViaCloudTrailItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    response_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    tls_details: typing.Optional[typing.Union[BucketEvents.AWSAPICallViaCloudTrail.TlsDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_identity: typing.Optional[typing.Union[BucketEvents.AWSAPICallViaCloudTrail.UserIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_endpoint_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978c39418628123b13f1c4fb305549a626f2926333a112e417bffb9fecd67ba2(
    *,
    authentication_method: typing.Optional[typing.Sequence[builtins.str]] = None,
    bytes_transferred_in: typing.Optional[typing.Sequence[builtins.str]] = None,
    bytes_transferred_out: typing.Optional[typing.Sequence[builtins.str]] = None,
    cipher_suite: typing.Optional[typing.Sequence[builtins.str]] = None,
    object_retention_info: typing.Optional[typing.Union[BucketEvents.AWSAPICallViaCloudTrail.ObjectRetentionInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    signature_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_amz_id2: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16c0d946fe52018b9aeae85cb27c8073f57634acbe1d762219fa72a8046072c(
    *,
    creation_date: typing.Optional[typing.Sequence[builtins.str]] = None,
    mfa_authenticated: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f9002b41147bb82d139c2d0414a964ecee587fc51a270228275570556b15df(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1540917d2158e1f4d9258b7ad0f4a49510cf2a5aaa93307b5de3bb0100d4d7e(
    *,
    is_under_legal_hold: typing.Optional[typing.Sequence[builtins.str]] = None,
    last_modified_time: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a773d93c77ec9a4c0e6c2b4a556ec59346c1d14266d81b05b668d549a77fdc(
    *,
    legal_hold_info: typing.Optional[typing.Union[BucketEvents.AWSAPICallViaCloudTrail.LegalHoldInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    retention_info: typing.Optional[typing.Union[BucketEvents.AWSAPICallViaCloudTrail.RetentionInfo, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514c077a90d9ed4ce5b956e1cbed4d21d1458ec72037ff66851382e2d78df420(
    *,
    bucket_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    host: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    legal_hold: typing.Optional[typing.Sequence[builtins.str]] = None,
    retention: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d3b23f9aa10d6eda8495857018a9ebdc05f9c45c425bd6bb8340cc39ff8af1f(
    *,
    last_modified_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    retain_until_mode: typing.Optional[typing.Sequence[builtins.str]] = None,
    retain_until_time: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f6134a878e54a89a9c2ecfc026295329f586cf97383dcaa62261dd50cc3409(
    *,
    attributes: typing.Optional[typing.Union[BucketEvents.AWSAPICallViaCloudTrail.Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    session_issuer: typing.Optional[typing.Union[BucketEvents.AWSAPICallViaCloudTrail.SessionIssuer, typing.Dict[builtins.str, typing.Any]]] = None,
    web_id_federation_data: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3e84ccedf9084612c4f30fc151fa19ec11cf3b444e7d916996b4d5f9e360ee(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96818f37100cf1bbc6e6f0fb7269c2c6b1a3df089cba106707bf30b1dd5d5ccb(
    *,
    cipher_suite: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_provided_host_header: typing.Optional[typing.Sequence[builtins.str]] = None,
    tls_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a55a46ad1960bf8a53533a2fe3ce5a102566bac1c77377e45e5fcb7ec6966b5(
    *,
    access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_context: typing.Optional[typing.Union[BucketEvents.AWSAPICallViaCloudTrail.SessionContext, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79624e255f1b11910c576fec17e045e4aa368a158fe87f0301a5ae4413a3b55f(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb9f6c55b38aa44ccf96f31ad9bdc39de16643104296c764c8ac2f4005b4b22(
    *,
    bucket: typing.Optional[typing.Union[BucketEvents.ObjectACLUpdated.Bucket, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    object: typing.Optional[typing.Union[BucketEvents.ObjectACLUpdated.ObjectType, typing.Dict[builtins.str, typing.Any]]] = None,
    requester: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbc4c95b7fed9ef076431e01317f6debfa81e293a59ae7110ddd440c7082084(
    *,
    etag: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e61bd6af7a386803fef002eb141f0ac4f08ba26fca927cbfaf1844296c0a809(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__677759226741286518177834e324509bbe5796f3c6649eeb674d12c56d26f4cd(
    *,
    bucket: typing.Optional[typing.Union[BucketEvents.ObjectAccessTierChanged.Bucket, typing.Dict[builtins.str, typing.Any]]] = None,
    destination_access_tier: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    object: typing.Optional[typing.Union[BucketEvents.ObjectAccessTierChanged.ObjectType, typing.Dict[builtins.str, typing.Any]]] = None,
    requester: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1994d8e3ec0759c94a09054eda482d2e870212f8d8de841fb2965aa0c947d6d(
    *,
    etag: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    size: typing.Optional[typing.Sequence[builtins.str]] = None,
    version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56aa57fef98dc3b87e578af3e4a30ee9c21c4ab8f79febc0ff4d216906086e34(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602129be747ca8e87a419f3ab3a3b4774eb0baa17c9883b2e21d8ed01787ea44(
    *,
    bucket: typing.Optional[typing.Union[BucketEvents.ObjectCreated.Bucket, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    object: typing.Optional[typing.Union[BucketEvents.ObjectCreated.ObjectType, typing.Dict[builtins.str, typing.Any]]] = None,
    reason: typing.Optional[typing.Sequence[builtins.str]] = None,
    requester: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d91c1779ea5ce4eb606d804d63905b1cb2f7a6bc2398e8807c5a9ae052b5c5(
    *,
    etag: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    sequencer: typing.Optional[typing.Sequence[builtins.str]] = None,
    size: typing.Optional[typing.Sequence[builtins.str]] = None,
    version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285a7194159677c65e016078648da1c82d52936e0a1962f989ecc5a9daee9d99(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864a88170a771d553ec6e23a4197d17e004cab55c52b2e24df0b772db127cf73(
    *,
    bucket: typing.Optional[typing.Union[BucketEvents.ObjectDeleted.Bucket, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    object: typing.Optional[typing.Union[BucketEvents.ObjectDeleted.ObjectType, typing.Dict[builtins.str, typing.Any]]] = None,
    reason: typing.Optional[typing.Sequence[builtins.str]] = None,
    requester: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b554a718b7cbd70f36979f3a3e31f98ba0ff823f6c4f0bae2f16ea7fb502e19f(
    *,
    etag: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    sequencer: typing.Optional[typing.Sequence[builtins.str]] = None,
    version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee2803b1c4790b6083ed75c09961c7b4f2221982e7c7eaf493a0c5ead8aad82(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1223f200d906355ae0f59566787ec2b672ae375c7adc49a97071d322adcfef8c(
    *,
    bucket: typing.Optional[typing.Union[BucketEvents.ObjectRestoreCompleted.Bucket, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    object: typing.Optional[typing.Union[BucketEvents.ObjectRestoreCompleted.ObjectType, typing.Dict[builtins.str, typing.Any]]] = None,
    requester: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    restore_expiry_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_storage_class: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df0c188684131916b089757f1a3c0712b5e28d99c750dc66ff40ebeeacc49ff(
    *,
    etag: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    size: typing.Optional[typing.Sequence[builtins.str]] = None,
    version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed0223c641eba1877beef37408551f96482d373a528a6f8e926cc774bd03c25(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3ed35478cb122c6c7a752b05dc0428d92624f5d102369f9d2fd81c6d32c03d(
    *,
    bucket: typing.Optional[typing.Union[BucketEvents.ObjectRestoreExpired.Bucket, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    object: typing.Optional[typing.Union[BucketEvents.ObjectRestoreExpired.ObjectType, typing.Dict[builtins.str, typing.Any]]] = None,
    requester: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4ef44b0b9511ccdb6ac8c9d93c5ae2aba915fc3a1e050c640202a6adbb652c(
    *,
    etag: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24eb5988b049ef988c175a10ff8b368adf39cfb6a04b9c739e4121419ba3d2bd(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279102aecd842e5a0ac34ee026f9b384434913d89c23f9cd5529fee3a15c0e35(
    *,
    bucket: typing.Optional[typing.Union[BucketEvents.ObjectRestoreInitiated.Bucket, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    object: typing.Optional[typing.Union[BucketEvents.ObjectRestoreInitiated.ObjectType, typing.Dict[builtins.str, typing.Any]]] = None,
    requester: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_storage_class: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdba86dfb82e8966d8ba510eefb864c0fe4511f6e50d6fb313ba83d4403d615(
    *,
    etag: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    size: typing.Optional[typing.Sequence[builtins.str]] = None,
    version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7469469631e7420ef3881a72b6acf3d31719797ea12981ef73660e8d493a21(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec9be9f373cda5651134174ed8f61ae2b3b7584a37d2ab94b666295f978a51a(
    *,
    bucket: typing.Optional[typing.Union[BucketEvents.ObjectStorageClassChanged.Bucket, typing.Dict[builtins.str, typing.Any]]] = None,
    destination_storage_class: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    object: typing.Optional[typing.Union[BucketEvents.ObjectStorageClassChanged.ObjectType, typing.Dict[builtins.str, typing.Any]]] = None,
    requester: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ed74d2ff5ae16d6b027c75884473d6a4abb4af78f52d2e1e2cf6a6642d8e33(
    *,
    etag: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    size: typing.Optional[typing.Sequence[builtins.str]] = None,
    version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22388f4126961dc03bd508a8d42766063b7ba7bd5d13225475455fa8e72744ce(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c87bd36082ff98f8bbe53a20ce975c171dfcd6a5b49643fc7b67ccc49f445d6(
    *,
    bucket: typing.Optional[typing.Union[BucketEvents.ObjectTagsAdded.Bucket, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    object: typing.Optional[typing.Union[BucketEvents.ObjectTagsAdded.ObjectType, typing.Dict[builtins.str, typing.Any]]] = None,
    requester: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da27a508a15808b42526c0453019293b7bcd03eabb48eaeaef100a0af302ac2(
    *,
    etag: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2ac0545d15e7dd7c0b416b20821be7fc34e2ac18a1b9e4840fdd83805fcff1(
    *,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409f3b41d0aa14ecaace1a8a722291d854000dabde63118e7d3d554ebc03c3c3(
    *,
    bucket: typing.Optional[typing.Union[BucketEvents.ObjectTagsDeleted.Bucket, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    object: typing.Optional[typing.Union[BucketEvents.ObjectTagsDeleted.ObjectType, typing.Dict[builtins.str, typing.Any]]] = None,
    requester: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e15668e73b796d7cd3ea118987bc9a9b74298e1c9d74616327d3184796fefde(
    *,
    etag: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
