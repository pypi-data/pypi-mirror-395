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
import aws_cdk.interfaces.aws_organizations as _aws_cdk_interfaces_aws_organizations_ceddda9d


class AccountEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.events.AccountEvents",
):
    '''(experimental) EventBridge event patterns for Account.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_organizations import events as organizations_events
        from aws_cdk.interfaces import aws_organizations as interfaces_organizations
        
        # account_ref: interfaces_organizations.IAccountRef
        
        account_events = organizations_events.AccountEvents.from_account(account_ref)
    '''

    @jsii.member(jsii_name="fromAccount")
    @builtins.classmethod
    def from_account(
        cls,
        account_ref: _aws_cdk_interfaces_aws_organizations_ceddda9d.IAccountRef,
    ) -> "AccountEvents":
        '''(experimental) Create AccountEvents from a Account reference.

        :param account_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce46fbe927bf9242890f8192b6ee77fd188385873d2b2363944616e0a068a328)
            check_type(argname="argument account_ref", value=account_ref, expected_type=type_hints["account_ref"])
        return typing.cast("AccountEvents", jsii.sinvoke(cls, "fromAccount", [account_ref]))

    @jsii.member(jsii_name="awsServiceEventViaCloudTrailPattern")
    def aws_service_event_via_cloud_trail_pattern(
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
        read_only: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_event_details: typing.Optional[typing.Union["AccountEvents.AWSServiceEventViaCloudTrail.ServiceEventDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_identity: typing.Optional[typing.Union["AccountEvents.AWSServiceEventViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Account AWS Service Event via CloudTrail.

        :param aws_region: (experimental) awsRegion property. Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_id: (experimental) eventID property. Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param event_name: (experimental) eventName property. Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_source: (experimental) eventSource property. Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_time: (experimental) eventTime property. Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_version: (experimental) eventVersion property. Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param read_only: (experimental) readOnly property. Specify an array of string values to match this event if the actual value of readOnly is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param service_event_details: (experimental) serviceEventDetails property. Specify an array of string values to match this event if the actual value of serviceEventDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_ip_address: (experimental) sourceIPAddress property. Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param user_identity: (experimental) userIdentity property. Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = AccountEvents.AWSServiceEventViaCloudTrail.AWSServiceEventViaCloudTrailProps(
            aws_region=aws_region,
            event_id=event_id,
            event_metadata=event_metadata,
            event_name=event_name,
            event_source=event_source,
            event_time=event_time,
            event_type=event_type,
            event_version=event_version,
            read_only=read_only,
            service_event_details=service_event_details,
            source_ip_address=source_ip_address,
            user_agent=user_agent,
            user_identity=user_identity,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "awsServiceEventViaCloudTrailPattern", [options]))

    class AWSServiceEventViaCloudTrail(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_organizations.events.AccountEvents.AWSServiceEventViaCloudTrail",
    ):
        '''(experimental) aws.organizations@AWSServiceEventViaCloudTrail event types for Account.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_organizations import events as organizations_events
            
            a_wSService_event_via_cloud_trail = organizations_events.AccountEvents.AWSServiceEventViaCloudTrail()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_organizations.events.AccountEvents.AWSServiceEventViaCloudTrail.AWSServiceEventViaCloudTrailProps",
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
                "read_only": "readOnly",
                "service_event_details": "serviceEventDetails",
                "source_ip_address": "sourceIpAddress",
                "user_agent": "userAgent",
                "user_identity": "userIdentity",
            },
        )
        class AWSServiceEventViaCloudTrailProps:
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
                read_only: typing.Optional[typing.Sequence[builtins.str]] = None,
                service_event_details: typing.Optional[typing.Union["AccountEvents.AWSServiceEventViaCloudTrail.ServiceEventDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_identity: typing.Optional[typing.Union["AccountEvents.AWSServiceEventViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Account aws.organizations@AWSServiceEventViaCloudTrail event.

                :param aws_region: (experimental) awsRegion property. Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_id: (experimental) eventID property. Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param event_name: (experimental) eventName property. Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_source: (experimental) eventSource property. Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_time: (experimental) eventTime property. Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_version: (experimental) eventVersion property. Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param read_only: (experimental) readOnly property. Specify an array of string values to match this event if the actual value of readOnly is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param service_event_details: (experimental) serviceEventDetails property. Specify an array of string values to match this event if the actual value of serviceEventDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_ip_address: (experimental) sourceIPAddress property. Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_identity: (experimental) userIdentity property. Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_organizations import events as organizations_events
                    
                    a_wSService_event_via_cloud_trail_props = organizations_events.AccountEvents.AWSServiceEventViaCloudTrail.AWSServiceEventViaCloudTrailProps(
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
                        read_only=["readOnly"],
                        service_event_details=organizations_events.AccountEvents.AWSServiceEventViaCloudTrail.ServiceEventDetails(
                            create_account_status=organizations_events.AccountEvents.AWSServiceEventViaCloudTrail.CreateAccountStatus(
                                account_id=["accountId"],
                                account_name=["accountName"],
                                completed_timestamp=["completedTimestamp"],
                                id=["id"],
                                requested_timestamp=["requestedTimestamp"],
                                state=["state"]
                            )
                        ),
                        source_ip_address=["sourceIpAddress"],
                        user_agent=["userAgent"],
                        user_identity=organizations_events.AccountEvents.AWSServiceEventViaCloudTrail.UserIdentity(
                            account_id=["accountId"],
                            invoked_by=["invokedBy"]
                        )
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(service_event_details, dict):
                    service_event_details = AccountEvents.AWSServiceEventViaCloudTrail.ServiceEventDetails(**service_event_details)
                if isinstance(user_identity, dict):
                    user_identity = AccountEvents.AWSServiceEventViaCloudTrail.UserIdentity(**user_identity)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__308ebc37eea0b335d7d4767226c832a2bba471787e3fe07fc126c96535643049)
                    check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                    check_type(argname="argument event_id", value=event_id, expected_type=type_hints["event_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
                    check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
                    check_type(argname="argument event_time", value=event_time, expected_type=type_hints["event_time"])
                    check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
                    check_type(argname="argument event_version", value=event_version, expected_type=type_hints["event_version"])
                    check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
                    check_type(argname="argument service_event_details", value=service_event_details, expected_type=type_hints["service_event_details"])
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
                if read_only is not None:
                    self._values["read_only"] = read_only
                if service_event_details is not None:
                    self._values["service_event_details"] = service_event_details
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
            def read_only(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) readOnly property.

                Specify an array of string values to match this event if the actual value of readOnly is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("read_only")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def service_event_details(
                self,
            ) -> typing.Optional["AccountEvents.AWSServiceEventViaCloudTrail.ServiceEventDetails"]:
                '''(experimental) serviceEventDetails property.

                Specify an array of string values to match this event if the actual value of serviceEventDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("service_event_details")
                return typing.cast(typing.Optional["AccountEvents.AWSServiceEventViaCloudTrail.ServiceEventDetails"], result)

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
            ) -> typing.Optional["AccountEvents.AWSServiceEventViaCloudTrail.UserIdentity"]:
                '''(experimental) userIdentity property.

                Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_identity")
                return typing.cast(typing.Optional["AccountEvents.AWSServiceEventViaCloudTrail.UserIdentity"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AWSServiceEventViaCloudTrailProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_organizations.events.AccountEvents.AWSServiceEventViaCloudTrail.CreateAccountStatus",
            jsii_struct_bases=[],
            name_mapping={
                "account_id": "accountId",
                "account_name": "accountName",
                "completed_timestamp": "completedTimestamp",
                "id": "id",
                "requested_timestamp": "requestedTimestamp",
                "state": "state",
            },
        )
        class CreateAccountStatus:
            def __init__(
                self,
                *,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                account_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                completed_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                requested_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                state: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for CreateAccountStatus.

                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Account reference
                :param account_name: (experimental) accountName property. Specify an array of string values to match this event if the actual value of accountName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param completed_timestamp: (experimental) completedTimestamp property. Specify an array of string values to match this event if the actual value of completedTimestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requested_timestamp: (experimental) requestedTimestamp property. Specify an array of string values to match this event if the actual value of requestedTimestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param state: (experimental) state property. Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_organizations import events as organizations_events
                    
                    create_account_status = organizations_events.AccountEvents.AWSServiceEventViaCloudTrail.CreateAccountStatus(
                        account_id=["accountId"],
                        account_name=["accountName"],
                        completed_timestamp=["completedTimestamp"],
                        id=["id"],
                        requested_timestamp=["requestedTimestamp"],
                        state=["state"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__806244b480d4899b44b10f73586ef24df698c99d7ed3d43910a6673e59232f4f)
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
                    check_type(argname="argument completed_timestamp", value=completed_timestamp, expected_type=type_hints["completed_timestamp"])
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument requested_timestamp", value=requested_timestamp, expected_type=type_hints["requested_timestamp"])
                    check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if account_id is not None:
                    self._values["account_id"] = account_id
                if account_name is not None:
                    self._values["account_name"] = account_name
                if completed_timestamp is not None:
                    self._values["completed_timestamp"] = completed_timestamp
                if id is not None:
                    self._values["id"] = id
                if requested_timestamp is not None:
                    self._values["requested_timestamp"] = requested_timestamp
                if state is not None:
                    self._values["state"] = state

            @builtins.property
            def account_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accountId property.

                Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Account reference

                :stability: experimental
                '''
                result = self._values.get("account_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def account_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accountName property.

                Specify an array of string values to match this event if the actual value of accountName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("account_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def completed_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) completedTimestamp property.

                Specify an array of string values to match this event if the actual value of completedTimestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("completed_timestamp")
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
            def requested_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requestedTimestamp property.

                Specify an array of string values to match this event if the actual value of requestedTimestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requested_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) state property.

                Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "CreateAccountStatus(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_organizations.events.AccountEvents.AWSServiceEventViaCloudTrail.ServiceEventDetails",
            jsii_struct_bases=[],
            name_mapping={"create_account_status": "createAccountStatus"},
        )
        class ServiceEventDetails:
            def __init__(
                self,
                *,
                create_account_status: typing.Optional[typing.Union["AccountEvents.AWSServiceEventViaCloudTrail.CreateAccountStatus", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for ServiceEventDetails.

                :param create_account_status: (experimental) createAccountStatus property. Specify an array of string values to match this event if the actual value of createAccountStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_organizations import events as organizations_events
                    
                    service_event_details = organizations_events.AccountEvents.AWSServiceEventViaCloudTrail.ServiceEventDetails(
                        create_account_status=organizations_events.AccountEvents.AWSServiceEventViaCloudTrail.CreateAccountStatus(
                            account_id=["accountId"],
                            account_name=["accountName"],
                            completed_timestamp=["completedTimestamp"],
                            id=["id"],
                            requested_timestamp=["requestedTimestamp"],
                            state=["state"]
                        )
                    )
                '''
                if isinstance(create_account_status, dict):
                    create_account_status = AccountEvents.AWSServiceEventViaCloudTrail.CreateAccountStatus(**create_account_status)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__6d8d2a7ccb0466ce9329a0b742395dd0a8a358e9a6172c324dbe9960b6c1ab59)
                    check_type(argname="argument create_account_status", value=create_account_status, expected_type=type_hints["create_account_status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if create_account_status is not None:
                    self._values["create_account_status"] = create_account_status

            @builtins.property
            def create_account_status(
                self,
            ) -> typing.Optional["AccountEvents.AWSServiceEventViaCloudTrail.CreateAccountStatus"]:
                '''(experimental) createAccountStatus property.

                Specify an array of string values to match this event if the actual value of createAccountStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("create_account_status")
                return typing.cast(typing.Optional["AccountEvents.AWSServiceEventViaCloudTrail.CreateAccountStatus"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ServiceEventDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_organizations.events.AccountEvents.AWSServiceEventViaCloudTrail.UserIdentity",
            jsii_struct_bases=[],
            name_mapping={"account_id": "accountId", "invoked_by": "invokedBy"},
        )
        class UserIdentity:
            def __init__(
                self,
                *,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                invoked_by: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for UserIdentity.

                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param invoked_by: (experimental) invokedBy property. Specify an array of string values to match this event if the actual value of invokedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_organizations import events as organizations_events
                    
                    user_identity = organizations_events.AccountEvents.AWSServiceEventViaCloudTrail.UserIdentity(
                        account_id=["accountId"],
                        invoked_by=["invokedBy"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__37351fca3cd7da7ca365b84d471c73c6a4ab17a0799b4bd2ffb9a6da2a992601)
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument invoked_by", value=invoked_by, expected_type=type_hints["invoked_by"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if account_id is not None:
                    self._values["account_id"] = account_id
                if invoked_by is not None:
                    self._values["invoked_by"] = invoked_by

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
            def invoked_by(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) invokedBy property.

                Specify an array of string values to match this event if the actual value of invokedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("invoked_by")
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
    "AccountEvents",
]

publication.publish()

def _typecheckingstub__ce46fbe927bf9242890f8192b6ee77fd188385873d2b2363944616e0a068a328(
    account_ref: _aws_cdk_interfaces_aws_organizations_ceddda9d.IAccountRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308ebc37eea0b335d7d4767226c832a2bba471787e3fe07fc126c96535643049(
    *,
    aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    read_only: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_event_details: typing.Optional[typing.Union[AccountEvents.AWSServiceEventViaCloudTrail.ServiceEventDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_identity: typing.Optional[typing.Union[AccountEvents.AWSServiceEventViaCloudTrail.UserIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806244b480d4899b44b10f73586ef24df698c99d7ed3d43910a6673e59232f4f(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    account_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    completed_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    requested_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    state: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8d2a7ccb0466ce9329a0b742395dd0a8a358e9a6172c324dbe9960b6c1ab59(
    *,
    create_account_status: typing.Optional[typing.Union[AccountEvents.AWSServiceEventViaCloudTrail.CreateAccountStatus, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37351fca3cd7da7ca365b84d471c73c6a4ab17a0799b4bd2ffb9a6da2a992601(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    invoked_by: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
