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
import aws_cdk.interfaces.aws_mediapackage as _aws_cdk_interfaces_aws_mediapackage_ceddda9d


class OriginEndpointEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.events.OriginEndpointEvents",
):
    '''(experimental) EventBridge event patterns for OriginEndpoint.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_mediapackage import events as mediapackage_events
        from aws_cdk.interfaces import aws_mediapackage as interfaces_mediapackage
        
        # origin_endpoint_ref: interfaces_mediapackage.IOriginEndpointRef
        
        origin_endpoint_events = mediapackage_events.OriginEndpointEvents.from_origin_endpoint(origin_endpoint_ref)
    '''

    @jsii.member(jsii_name="fromOriginEndpoint")
    @builtins.classmethod
    def from_origin_endpoint(
        cls,
        origin_endpoint_ref: _aws_cdk_interfaces_aws_mediapackage_ceddda9d.IOriginEndpointRef,
    ) -> "OriginEndpointEvents":
        '''(experimental) Create OriginEndpointEvents from a OriginEndpoint reference.

        :param origin_endpoint_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de5a89fbc860b045a954f88550698abe86b0ed7d27530afd5bc1d2c0cb91f29f)
            check_type(argname="argument origin_endpoint_ref", value=origin_endpoint_ref, expected_type=type_hints["origin_endpoint_ref"])
        return typing.cast("OriginEndpointEvents", jsii.sinvoke(cls, "fromOriginEndpoint", [origin_endpoint_ref]))

    @jsii.member(jsii_name="mediaPackageHarvestJobNotificationPattern")
    def media_package_harvest_job_notification_pattern(
        self,
        *,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        harvest_job: typing.Optional[typing.Union["OriginEndpointEvents.MediaPackageHarvestJobNotification.HarvestJob", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for OriginEndpoint MediaPackage HarvestJob Notification.

        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param harvest_job: (experimental) harvest_job property. Specify an array of string values to match this event if the actual value of harvest_job is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = OriginEndpointEvents.MediaPackageHarvestJobNotification.MediaPackageHarvestJobNotificationProps(
            event_metadata=event_metadata, harvest_job=harvest_job
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "mediaPackageHarvestJobNotificationPattern", [options]))

    class MediaPackageHarvestJobNotification(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.events.OriginEndpointEvents.MediaPackageHarvestJobNotification",
    ):
        '''(experimental) aws.mediapackage@MediaPackageHarvestJobNotification event types for OriginEndpoint.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediapackage import events as mediapackage_events
            
            media_package_harvest_job_notification = mediapackage_events.OriginEndpointEvents.MediaPackageHarvestJobNotification()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.events.OriginEndpointEvents.MediaPackageHarvestJobNotification.HarvestJob",
            jsii_struct_bases=[],
            name_mapping={
                "arn": "arn",
                "created_at": "createdAt",
                "end_time": "endTime",
                "id": "id",
                "origin_endpoint_id": "originEndpointId",
                "s3_destination": "s3Destination",
                "start_time": "startTime",
                "status": "status",
            },
        )
        class HarvestJob:
            def __init__(
                self,
                *,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                origin_endpoint_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_destination: typing.Optional[typing.Union["OriginEndpointEvents.MediaPackageHarvestJobNotification.S3Destination", typing.Dict[builtins.str, typing.Any]]] = None,
                start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Harvest_job.

                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param created_at: (experimental) created_at property. Specify an array of string values to match this event if the actual value of created_at is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param end_time: (experimental) end_time property. Specify an array of string values to match this event if the actual value of end_time is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param origin_endpoint_id: (experimental) origin_endpoint_id property. Specify an array of string values to match this event if the actual value of origin_endpoint_id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the OriginEndpoint reference
                :param s3_destination: (experimental) s3_destination property. Specify an array of string values to match this event if the actual value of s3_destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_time: (experimental) start_time property. Specify an array of string values to match this event if the actual value of start_time is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_mediapackage import events as mediapackage_events
                    
                    harvest_job = mediapackage_events.OriginEndpointEvents.MediaPackageHarvestJobNotification.HarvestJob(
                        arn=["arn"],
                        created_at=["createdAt"],
                        end_time=["endTime"],
                        id=["id"],
                        origin_endpoint_id=["originEndpointId"],
                        s3_destination=mediapackage_events.OriginEndpointEvents.MediaPackageHarvestJobNotification.S3Destination(
                            bucket_name=["bucketName"],
                            manifest_key=["manifestKey"],
                            role_arn=["roleArn"]
                        ),
                        start_time=["startTime"],
                        status=["status"]
                    )
                '''
                if isinstance(s3_destination, dict):
                    s3_destination = OriginEndpointEvents.MediaPackageHarvestJobNotification.S3Destination(**s3_destination)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__341e96812dced7ac1675ddd42cd5a46d8fe73f918290af7dcbd2ab763264656c)
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                    check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument origin_endpoint_id", value=origin_endpoint_id, expected_type=type_hints["origin_endpoint_id"])
                    check_type(argname="argument s3_destination", value=s3_destination, expected_type=type_hints["s3_destination"])
                    check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if arn is not None:
                    self._values["arn"] = arn
                if created_at is not None:
                    self._values["created_at"] = created_at
                if end_time is not None:
                    self._values["end_time"] = end_time
                if id is not None:
                    self._values["id"] = id
                if origin_endpoint_id is not None:
                    self._values["origin_endpoint_id"] = origin_endpoint_id
                if s3_destination is not None:
                    self._values["s3_destination"] = s3_destination
                if start_time is not None:
                    self._values["start_time"] = start_time
                if status is not None:
                    self._values["status"] = status

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
            def created_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) created_at property.

                Specify an array of string values to match this event if the actual value of created_at is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("created_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end_time property.

                Specify an array of string values to match this event if the actual value of end_time is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

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
            def origin_endpoint_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) origin_endpoint_id property.

                Specify an array of string values to match this event if the actual value of origin_endpoint_id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the OriginEndpoint reference

                :stability: experimental
                '''
                result = self._values.get("origin_endpoint_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_destination(
                self,
            ) -> typing.Optional["OriginEndpointEvents.MediaPackageHarvestJobNotification.S3Destination"]:
                '''(experimental) s3_destination property.

                Specify an array of string values to match this event if the actual value of s3_destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_destination")
                return typing.cast(typing.Optional["OriginEndpointEvents.MediaPackageHarvestJobNotification.S3Destination"], result)

            @builtins.property
            def start_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start_time property.

                Specify an array of string values to match this event if the actual value of start_time is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_time")
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

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "HarvestJob(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.events.OriginEndpointEvents.MediaPackageHarvestJobNotification.MediaPackageHarvestJobNotificationProps",
            jsii_struct_bases=[],
            name_mapping={
                "event_metadata": "eventMetadata",
                "harvest_job": "harvestJob",
            },
        )
        class MediaPackageHarvestJobNotificationProps:
            def __init__(
                self,
                *,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                harvest_job: typing.Optional[typing.Union["OriginEndpointEvents.MediaPackageHarvestJobNotification.HarvestJob", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for OriginEndpoint aws.mediapackage@MediaPackageHarvestJobNotification event.

                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param harvest_job: (experimental) harvest_job property. Specify an array of string values to match this event if the actual value of harvest_job is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_mediapackage import events as mediapackage_events
                    
                    media_package_harvest_job_notification_props = mediapackage_events.OriginEndpointEvents.MediaPackageHarvestJobNotification.MediaPackageHarvestJobNotificationProps(
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        harvest_job=mediapackage_events.OriginEndpointEvents.MediaPackageHarvestJobNotification.HarvestJob(
                            arn=["arn"],
                            created_at=["createdAt"],
                            end_time=["endTime"],
                            id=["id"],
                            origin_endpoint_id=["originEndpointId"],
                            s3_destination=mediapackage_events.OriginEndpointEvents.MediaPackageHarvestJobNotification.S3Destination(
                                bucket_name=["bucketName"],
                                manifest_key=["manifestKey"],
                                role_arn=["roleArn"]
                            ),
                            start_time=["startTime"],
                            status=["status"]
                        )
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(harvest_job, dict):
                    harvest_job = OriginEndpointEvents.MediaPackageHarvestJobNotification.HarvestJob(**harvest_job)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__5a29e7ad62bec10c78dd0e8b01eee7f65cb6df14efb56ef124fff4eb58bb5edf)
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument harvest_job", value=harvest_job, expected_type=type_hints["harvest_job"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if harvest_job is not None:
                    self._values["harvest_job"] = harvest_job

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
            def harvest_job(
                self,
            ) -> typing.Optional["OriginEndpointEvents.MediaPackageHarvestJobNotification.HarvestJob"]:
                '''(experimental) harvest_job property.

                Specify an array of string values to match this event if the actual value of harvest_job is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("harvest_job")
                return typing.cast(typing.Optional["OriginEndpointEvents.MediaPackageHarvestJobNotification.HarvestJob"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "MediaPackageHarvestJobNotificationProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_mediapackage.events.OriginEndpointEvents.MediaPackageHarvestJobNotification.S3Destination",
            jsii_struct_bases=[],
            name_mapping={
                "bucket_name": "bucketName",
                "manifest_key": "manifestKey",
                "role_arn": "roleArn",
            },
        )
        class S3Destination:
            def __init__(
                self,
                *,
                bucket_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                manifest_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                role_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for S3_destination.

                :param bucket_name: (experimental) bucket_name property. Specify an array of string values to match this event if the actual value of bucket_name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param manifest_key: (experimental) manifest_key property. Specify an array of string values to match this event if the actual value of manifest_key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param role_arn: (experimental) role_arn property. Specify an array of string values to match this event if the actual value of role_arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_mediapackage import events as mediapackage_events
                    
                    s3_destination = mediapackage_events.OriginEndpointEvents.MediaPackageHarvestJobNotification.S3Destination(
                        bucket_name=["bucketName"],
                        manifest_key=["manifestKey"],
                        role_arn=["roleArn"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__bc7d8d3631b24210962411ee8a993121b4b61b5ee6e1043ff811370378403c1a)
                    check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                    check_type(argname="argument manifest_key", value=manifest_key, expected_type=type_hints["manifest_key"])
                    check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket_name is not None:
                    self._values["bucket_name"] = bucket_name
                if manifest_key is not None:
                    self._values["manifest_key"] = manifest_key
                if role_arn is not None:
                    self._values["role_arn"] = role_arn

            @builtins.property
            def bucket_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bucket_name property.

                Specify an array of string values to match this event if the actual value of bucket_name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def manifest_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) manifest_key property.

                Specify an array of string values to match this event if the actual value of manifest_key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("manifest_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def role_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) role_arn property.

                Specify an array of string values to match this event if the actual value of role_arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("role_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "S3Destination(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "OriginEndpointEvents",
]

publication.publish()

def _typecheckingstub__de5a89fbc860b045a954f88550698abe86b0ed7d27530afd5bc1d2c0cb91f29f(
    origin_endpoint_ref: _aws_cdk_interfaces_aws_mediapackage_ceddda9d.IOriginEndpointRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341e96812dced7ac1675ddd42cd5a46d8fe73f918290af7dcbd2ab763264656c(
    *,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    origin_endpoint_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_destination: typing.Optional[typing.Union[OriginEndpointEvents.MediaPackageHarvestJobNotification.S3Destination, typing.Dict[builtins.str, typing.Any]]] = None,
    start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a29e7ad62bec10c78dd0e8b01eee7f65cb6df14efb56ef124fff4eb58bb5edf(
    *,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    harvest_job: typing.Optional[typing.Union[OriginEndpointEvents.MediaPackageHarvestJobNotification.HarvestJob, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7d8d3631b24210962411ee8a993121b4b61b5ee6e1043ff811370378403c1a(
    *,
    bucket_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    manifest_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
