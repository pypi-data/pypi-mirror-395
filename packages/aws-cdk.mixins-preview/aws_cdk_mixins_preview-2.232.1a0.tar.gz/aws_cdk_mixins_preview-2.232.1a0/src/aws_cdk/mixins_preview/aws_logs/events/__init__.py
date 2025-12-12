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
import aws_cdk.interfaces.aws_logs as _aws_cdk_interfaces_aws_logs_ceddda9d


class LogGroupEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.events.LogGroupEvents",
):
    '''(experimental) EventBridge event patterns for LogGroup.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_logs import events as logs_events
        from aws_cdk.interfaces import aws_logs as interfaces_logs
        
        # log_group_ref: interfaces_logs.ILogGroupRef
        
        log_group_events = logs_events.LogGroupEvents.from_log_group(log_group_ref)
    '''

    @jsii.member(jsii_name="fromLogGroup")
    @builtins.classmethod
    def from_log_group(
        cls,
        log_group_ref: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "LogGroupEvents":
        '''(experimental) Create LogGroupEvents from a LogGroup reference.

        :param log_group_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bb4330f194219f30dda5e957f1a0fca734276413a69107113de70418281ec17)
            check_type(argname="argument log_group_ref", value=log_group_ref, expected_type=type_hints["log_group_ref"])
        return typing.cast("LogGroupEvents", jsii.sinvoke(cls, "fromLogGroup", [log_group_ref]))

    @jsii.member(jsii_name="awsAPICallViaCloudTrailPattern")
    def aws_api_call_via_cloud_trail_pattern(
        self,
        *,
        api_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_parameters: typing.Optional[typing.Union["LogGroupEvents.AWSAPICallViaCloudTrail.RequestParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        response_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_identity: typing.Optional[typing.Union["LogGroupEvents.AWSAPICallViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for LogGroup AWS API Call via CloudTrail.

        :param api_version: (experimental) apiVersion property. Specify an array of string values to match this event if the actual value of apiVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param aws_region: (experimental) awsRegion property. Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
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
        options = LogGroupEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
            api_version=api_version,
            aws_region=aws_region,
            error_code=error_code,
            error_message=error_message,
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

    class AWSAPICallViaCloudTrail(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_logs.events.LogGroupEvents.AWSAPICallViaCloudTrail",
    ):
        '''(experimental) aws.logs@AWSAPICallViaCloudTrail event types for LogGroup.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import events as logs_events
            
            a_wSAPICall_via_cloud_trail = logs_events.LogGroupEvents.AWSAPICallViaCloudTrail()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_logs.events.LogGroupEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps",
            jsii_struct_bases=[],
            name_mapping={
                "api_version": "apiVersion",
                "aws_region": "awsRegion",
                "error_code": "errorCode",
                "error_message": "errorMessage",
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
                api_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_parameters: typing.Optional[typing.Union["LogGroupEvents.AWSAPICallViaCloudTrail.RequestParameters", typing.Dict[builtins.str, typing.Any]]] = None,
                response_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_identity: typing.Optional[typing.Union["LogGroupEvents.AWSAPICallViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for LogGroup aws.logs@AWSAPICallViaCloudTrail event.

                :param api_version: (experimental) apiVersion property. Specify an array of string values to match this event if the actual value of apiVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param aws_region: (experimental) awsRegion property. Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
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
                    from aws_cdk.mixins_preview.aws_logs import events as logs_events
                    
                    a_wSAPICall_via_cloud_trail_props = logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
                        api_version=["apiVersion"],
                        aws_region=["awsRegion"],
                        error_code=["errorCode"],
                        error_message=["errorMessage"],
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
                        request_parameters=logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.RequestParameters(
                            log_group_name=["logGroupName"],
                            log_stream_name=["logStreamName"]
                        ),
                        response_elements=["responseElements"],
                        source_ip_address=["sourceIpAddress"],
                        user_agent=["userAgent"],
                        user_identity=logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.UserIdentity(
                            access_key_id=["accessKeyId"],
                            account_id=["accountId"],
                            arn=["arn"],
                            invoked_by=["invokedBy"],
                            principal_id=["principalId"],
                            session_context=logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.SessionContext(
                                attributes=logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.Attributes(
                                    creation_date=["creationDate"],
                                    mfa_authenticated=["mfaAuthenticated"]
                                ),
                                session_issuer=logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                                    account_id=["accountId"],
                                    arn=["arn"],
                                    principal_id=["principalId"],
                                    type=["type"],
                                    user_name=["userName"]
                                )
                            ),
                            type=["type"]
                        )
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(request_parameters, dict):
                    request_parameters = LogGroupEvents.AWSAPICallViaCloudTrail.RequestParameters(**request_parameters)
                if isinstance(user_identity, dict):
                    user_identity = LogGroupEvents.AWSAPICallViaCloudTrail.UserIdentity(**user_identity)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__af62a8b3cba8a8cb99c9b69ae3a6bbe6c19011b4e5168b15c95b6c296bd9da31)
                    check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
                    check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                    check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                    check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
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
                if api_version is not None:
                    self._values["api_version"] = api_version
                if aws_region is not None:
                    self._values["aws_region"] = aws_region
                if error_code is not None:
                    self._values["error_code"] = error_code
                if error_message is not None:
                    self._values["error_message"] = error_message
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
            def api_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) apiVersion property.

                Specify an array of string values to match this event if the actual value of apiVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("api_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

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
            ) -> typing.Optional["LogGroupEvents.AWSAPICallViaCloudTrail.RequestParameters"]:
                '''(experimental) requestParameters property.

                Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_parameters")
                return typing.cast(typing.Optional["LogGroupEvents.AWSAPICallViaCloudTrail.RequestParameters"], result)

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
            ) -> typing.Optional["LogGroupEvents.AWSAPICallViaCloudTrail.UserIdentity"]:
                '''(experimental) userIdentity property.

                Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_identity")
                return typing.cast(typing.Optional["LogGroupEvents.AWSAPICallViaCloudTrail.UserIdentity"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AWSAPICallViaCloudTrailProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_logs.events.LogGroupEvents.AWSAPICallViaCloudTrail.Attributes",
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
                    from aws_cdk.mixins_preview.aws_logs import events as logs_events
                    
                    attributes = logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.Attributes(
                        creation_date=["creationDate"],
                        mfa_authenticated=["mfaAuthenticated"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__71f91440f5efa00481ca0df0a0a479cf4febf6a63c0e5a76d0e0de795b04d754)
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
            jsii_type="@aws-cdk/mixins-preview.aws_logs.events.LogGroupEvents.AWSAPICallViaCloudTrail.RequestParameters",
            jsii_struct_bases=[],
            name_mapping={
                "log_group_name": "logGroupName",
                "log_stream_name": "logStreamName",
            },
        )
        class RequestParameters:
            def __init__(
                self,
                *,
                log_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                log_stream_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParameters.

                :param log_group_name: (experimental) logGroupName property. Specify an array of string values to match this event if the actual value of logGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the LogGroup reference
                :param log_stream_name: (experimental) logStreamName property. Specify an array of string values to match this event if the actual value of logStreamName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_logs import events as logs_events
                    
                    request_parameters = logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.RequestParameters(
                        log_group_name=["logGroupName"],
                        log_stream_name=["logStreamName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ff7b4b0c67c193e95e7d0e42a48887b2973d1cb68746f0c73e7a70bf0375e004)
                    check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
                    check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if log_group_name is not None:
                    self._values["log_group_name"] = log_group_name
                if log_stream_name is not None:
                    self._values["log_stream_name"] = log_stream_name

            @builtins.property
            def log_group_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) logGroupName property.

                Specify an array of string values to match this event if the actual value of logGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the LogGroup reference

                :stability: experimental
                '''
                result = self._values.get("log_group_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def log_stream_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) logStreamName property.

                Specify an array of string values to match this event if the actual value of logStreamName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("log_stream_name")
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
            jsii_type="@aws-cdk/mixins-preview.aws_logs.events.LogGroupEvents.AWSAPICallViaCloudTrail.SessionContext",
            jsii_struct_bases=[],
            name_mapping={
                "attributes": "attributes",
                "session_issuer": "sessionIssuer",
            },
        )
        class SessionContext:
            def __init__(
                self,
                *,
                attributes: typing.Optional[typing.Union["LogGroupEvents.AWSAPICallViaCloudTrail.Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                session_issuer: typing.Optional[typing.Union["LogGroupEvents.AWSAPICallViaCloudTrail.SessionIssuer", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for SessionContext.

                :param attributes: (experimental) attributes property. Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_issuer: (experimental) sessionIssuer property. Specify an array of string values to match this event if the actual value of sessionIssuer is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_logs import events as logs_events
                    
                    session_context = logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.SessionContext(
                        attributes=logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.Attributes(
                            creation_date=["creationDate"],
                            mfa_authenticated=["mfaAuthenticated"]
                        ),
                        session_issuer=logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                            account_id=["accountId"],
                            arn=["arn"],
                            principal_id=["principalId"],
                            type=["type"],
                            user_name=["userName"]
                        )
                    )
                '''
                if isinstance(attributes, dict):
                    attributes = LogGroupEvents.AWSAPICallViaCloudTrail.Attributes(**attributes)
                if isinstance(session_issuer, dict):
                    session_issuer = LogGroupEvents.AWSAPICallViaCloudTrail.SessionIssuer(**session_issuer)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__efb40e2fc4e0e46b88a23508fab389022d913fc6f12fe9dba7e23ccbc87e3b8a)
                    check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                    check_type(argname="argument session_issuer", value=session_issuer, expected_type=type_hints["session_issuer"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if attributes is not None:
                    self._values["attributes"] = attributes
                if session_issuer is not None:
                    self._values["session_issuer"] = session_issuer

            @builtins.property
            def attributes(
                self,
            ) -> typing.Optional["LogGroupEvents.AWSAPICallViaCloudTrail.Attributes"]:
                '''(experimental) attributes property.

                Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attributes")
                return typing.cast(typing.Optional["LogGroupEvents.AWSAPICallViaCloudTrail.Attributes"], result)

            @builtins.property
            def session_issuer(
                self,
            ) -> typing.Optional["LogGroupEvents.AWSAPICallViaCloudTrail.SessionIssuer"]:
                '''(experimental) sessionIssuer property.

                Specify an array of string values to match this event if the actual value of sessionIssuer is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_issuer")
                return typing.cast(typing.Optional["LogGroupEvents.AWSAPICallViaCloudTrail.SessionIssuer"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SessionContext(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_logs.events.LogGroupEvents.AWSAPICallViaCloudTrail.SessionIssuer",
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
                    from aws_cdk.mixins_preview.aws_logs import events as logs_events
                    
                    session_issuer = logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                        account_id=["accountId"],
                        arn=["arn"],
                        principal_id=["principalId"],
                        type=["type"],
                        user_name=["userName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1362cd8e51b43278dafe0b0f7baa132d2e0a4e3e4b946b5af957993e0f0216f7)
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
            jsii_type="@aws-cdk/mixins-preview.aws_logs.events.LogGroupEvents.AWSAPICallViaCloudTrail.UserIdentity",
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
                session_context: typing.Optional[typing.Union["LogGroupEvents.AWSAPICallViaCloudTrail.SessionContext", typing.Dict[builtins.str, typing.Any]]] = None,
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
                    from aws_cdk.mixins_preview.aws_logs import events as logs_events
                    
                    user_identity = logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.UserIdentity(
                        access_key_id=["accessKeyId"],
                        account_id=["accountId"],
                        arn=["arn"],
                        invoked_by=["invokedBy"],
                        principal_id=["principalId"],
                        session_context=logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.SessionContext(
                            attributes=logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.Attributes(
                                creation_date=["creationDate"],
                                mfa_authenticated=["mfaAuthenticated"]
                            ),
                            session_issuer=logs_events.LogGroupEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                                account_id=["accountId"],
                                arn=["arn"],
                                principal_id=["principalId"],
                                type=["type"],
                                user_name=["userName"]
                            )
                        ),
                        type=["type"]
                    )
                '''
                if isinstance(session_context, dict):
                    session_context = LogGroupEvents.AWSAPICallViaCloudTrail.SessionContext(**session_context)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3a62b5b40fc5a1d8b66afe88e642924422f26d2d2dcf19054953d1a93ebaa55a)
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
            ) -> typing.Optional["LogGroupEvents.AWSAPICallViaCloudTrail.SessionContext"]:
                '''(experimental) sessionContext property.

                Specify an array of string values to match this event if the actual value of sessionContext is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_context")
                return typing.cast(typing.Optional["LogGroupEvents.AWSAPICallViaCloudTrail.SessionContext"], result)

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


__all__ = [
    "LogGroupEvents",
]

publication.publish()

def _typecheckingstub__0bb4330f194219f30dda5e957f1a0fca734276413a69107113de70418281ec17(
    log_group_ref: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af62a8b3cba8a8cb99c9b69ae3a6bbe6c19011b4e5168b15c95b6c296bd9da31(
    *,
    api_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_parameters: typing.Optional[typing.Union[LogGroupEvents.AWSAPICallViaCloudTrail.RequestParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    response_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_identity: typing.Optional[typing.Union[LogGroupEvents.AWSAPICallViaCloudTrail.UserIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f91440f5efa00481ca0df0a0a479cf4febf6a63c0e5a76d0e0de795b04d754(
    *,
    creation_date: typing.Optional[typing.Sequence[builtins.str]] = None,
    mfa_authenticated: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7b4b0c67c193e95e7d0e42a48887b2973d1cb68746f0c73e7a70bf0375e004(
    *,
    log_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_stream_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb40e2fc4e0e46b88a23508fab389022d913fc6f12fe9dba7e23ccbc87e3b8a(
    *,
    attributes: typing.Optional[typing.Union[LogGroupEvents.AWSAPICallViaCloudTrail.Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    session_issuer: typing.Optional[typing.Union[LogGroupEvents.AWSAPICallViaCloudTrail.SessionIssuer, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1362cd8e51b43278dafe0b0f7baa132d2e0a4e3e4b946b5af957993e0f0216f7(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a62b5b40fc5a1d8b66afe88e642924422f26d2d2dcf19054953d1a93ebaa55a(
    *,
    access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    invoked_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_context: typing.Optional[typing.Union[LogGroupEvents.AWSAPICallViaCloudTrail.SessionContext, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
