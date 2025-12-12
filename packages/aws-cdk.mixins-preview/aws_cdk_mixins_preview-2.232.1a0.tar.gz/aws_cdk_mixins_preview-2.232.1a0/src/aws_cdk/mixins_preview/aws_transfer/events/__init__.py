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
import aws_cdk.interfaces.aws_transfer as _aws_cdk_interfaces_aws_transfer_ceddda9d


class AgreementEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.AgreementEvents",
):
    '''(experimental) EventBridge event patterns for Agreement.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
        from aws_cdk.interfaces import aws_transfer as interfaces_transfer
        
        # agreement_ref: interfaces_transfer.IAgreementRef
        
        agreement_events = transfer_events.AgreementEvents.from_agreement(agreement_ref)
    '''

    @jsii.member(jsii_name="fromAgreement")
    @builtins.classmethod
    def from_agreement(
        cls,
        agreement_ref: _aws_cdk_interfaces_aws_transfer_ceddda9d.IAgreementRef,
    ) -> "AgreementEvents":
        '''(experimental) Create AgreementEvents from a Agreement reference.

        :param agreement_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f052ad41ae6ae1e4725092042022b4444b6f12843e6247378ab3e43f638c06a9)
            check_type(argname="argument agreement_ref", value=agreement_ref, expected_type=type_hints["agreement_ref"])
        return typing.cast("AgreementEvents", jsii.sinvoke(cls, "fromAgreement", [agreement_ref]))

    @jsii.member(jsii_name="aS2MDNSendCompletedPattern")
    def a_s2_mdn_send_completed_pattern(
        self,
        *,
        agreement_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
        bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
        disposition: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        mdn_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
        mdn_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
        requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_attributes: typing.Optional[typing.Union["AgreementEvents.AS2MDNSendCompleted.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
        server_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Agreement AS2 MDN Send Completed.

        :param agreement_id: (experimental) agreement-id property. Specify an array of string values to match this event if the actual value of agreement-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Agreement reference
        :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param client_ip: (experimental) client-ip property. Specify an array of string values to match this event if the actual value of client-ip is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param disposition: (experimental) disposition property. Specify an array of string values to match this event if the actual value of disposition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param mdn_message_id: (experimental) mdn-message-id property. Specify an array of string values to match this event if the actual value of mdn-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param mdn_subject: (experimental) mdn-subject property. Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param mdn_type: (experimental) mdn-type property. Specify an array of string values to match this event if the actual value of mdn-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param message_subject: (experimental) message-subject property. Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester_file_name: (experimental) requester-file-name property. Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_path: (experimental) request-path property. Specify an array of string values to match this event if the actual value of request-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param server_id: (experimental) server-id property. Specify an array of string values to match this event if the actual value of server-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = AgreementEvents.AS2MDNSendCompleted.AS2MDNSendCompletedProps(
            agreement_id=agreement_id,
            as2_from=as2_from,
            as2_message_id=as2_message_id,
            as2_to=as2_to,
            bytes=bytes,
            client_ip=client_ip,
            disposition=disposition,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            mdn_message_id=mdn_message_id,
            mdn_subject=mdn_subject,
            mdn_type=mdn_type,
            message_subject=message_subject,
            requester_file_name=requester_file_name,
            request_path=request_path,
            s3_attributes=s3_attributes,
            server_id=server_id,
            start_timestamp=start_timestamp,
            status_code=status_code,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "aS2MDNSendCompletedPattern", [options]))

    @jsii.member(jsii_name="aS2MDNSendFailedPattern")
    def a_s2_mdn_send_failed_pattern(
        self,
        *,
        agreement_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
        bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
        disposition: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
        mdn_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
        mdn_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_attributes: typing.Optional[typing.Union["AgreementEvents.AS2MDNSendFailed.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
        server_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Agreement AS2 MDN Send Failed.

        :param agreement_id: (experimental) agreement-id property. Specify an array of string values to match this event if the actual value of agreement-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Agreement reference
        :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param client_ip: (experimental) client-ip property. Specify an array of string values to match this event if the actual value of client-ip is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param disposition: (experimental) disposition property. Specify an array of string values to match this event if the actual value of disposition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param mdn_message_id: (experimental) mdn-message-id property. Specify an array of string values to match this event if the actual value of mdn-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param mdn_subject: (experimental) mdn-subject property. Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param mdn_type: (experimental) mdn-type property. Specify an array of string values to match this event if the actual value of mdn-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester_file_name: (experimental) requester-file-name property. Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param server_id: (experimental) server-id property. Specify an array of string values to match this event if the actual value of server-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = AgreementEvents.AS2MDNSendFailed.AS2MDNSendFailedProps(
            agreement_id=agreement_id,
            as2_from=as2_from,
            as2_message_id=as2_message_id,
            as2_to=as2_to,
            bytes=bytes,
            client_ip=client_ip,
            disposition=disposition,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            failure_code=failure_code,
            failure_message=failure_message,
            mdn_message_id=mdn_message_id,
            mdn_subject=mdn_subject,
            mdn_type=mdn_type,
            requester_file_name=requester_file_name,
            s3_attributes=s3_attributes,
            server_id=server_id,
            start_timestamp=start_timestamp,
            status_code=status_code,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "aS2MDNSendFailedPattern", [options]))

    @jsii.member(jsii_name="aS2PayloadReceiveCompletedPattern")
    def a_s2_payload_receive_completed_pattern(
        self,
        *,
        agreement_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
        bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
        requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_attributes: typing.Optional[typing.Union["AgreementEvents.AS2PayloadReceiveCompleted.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
        server_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Agreement AS2 Payload Receive Completed.

        :param agreement_id: (experimental) agreement-id property. Specify an array of string values to match this event if the actual value of agreement-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Agreement reference
        :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param client_ip: (experimental) client-ip property. Specify an array of string values to match this event if the actual value of client-ip is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param message_subject: (experimental) message-subject property. Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester_file_name: (experimental) requester-file-name property. Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_path: (experimental) request-path property. Specify an array of string values to match this event if the actual value of request-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param server_id: (experimental) server-id property. Specify an array of string values to match this event if the actual value of server-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = AgreementEvents.AS2PayloadReceiveCompleted.AS2PayloadReceiveCompletedProps(
            agreement_id=agreement_id,
            as2_from=as2_from,
            as2_message_id=as2_message_id,
            as2_to=as2_to,
            bytes=bytes,
            client_ip=client_ip,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            message_subject=message_subject,
            requester_file_name=requester_file_name,
            request_path=request_path,
            s3_attributes=s3_attributes,
            server_id=server_id,
            start_timestamp=start_timestamp,
            status_code=status_code,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "aS2PayloadReceiveCompletedPattern", [options]))

    @jsii.member(jsii_name="aS2PayloadReceiveFailedPattern")
    def a_s2_payload_receive_failed_pattern(
        self,
        *,
        agreement_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
        message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_attributes: typing.Optional[typing.Union["AgreementEvents.AS2PayloadReceiveFailed.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
        server_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Agreement AS2 Payload Receive Failed.

        :param agreement_id: (experimental) agreement-id property. Specify an array of string values to match this event if the actual value of agreement-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Agreement reference
        :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param client_ip: (experimental) client-ip property. Specify an array of string values to match this event if the actual value of client-ip is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param message_subject: (experimental) message-subject property. Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param server_id: (experimental) server-id property. Specify an array of string values to match this event if the actual value of server-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = AgreementEvents.AS2PayloadReceiveFailed.AS2PayloadReceiveFailedProps(
            agreement_id=agreement_id,
            as2_from=as2_from,
            as2_message_id=as2_message_id,
            as2_to=as2_to,
            client_ip=client_ip,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            failure_code=failure_code,
            failure_message=failure_message,
            message_subject=message_subject,
            s3_attributes=s3_attributes,
            server_id=server_id,
            start_timestamp=start_timestamp,
            status_code=status_code,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "aS2PayloadReceiveFailedPattern", [options]))

    class AS2MDNSendCompleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.AgreementEvents.AS2MDNSendCompleted",
    ):
        '''(experimental) aws.transfer@AS2MDNSendCompleted event types for Agreement.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            a_s2_mDNSend_completed = transfer_events.AgreementEvents.AS2MDNSendCompleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.AgreementEvents.AS2MDNSendCompleted.AS2MDNSendCompletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "agreement_id": "agreementId",
                "as2_from": "as2From",
                "as2_message_id": "as2MessageId",
                "as2_to": "as2To",
                "bytes": "bytes",
                "client_ip": "clientIp",
                "disposition": "disposition",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "mdn_message_id": "mdnMessageId",
                "mdn_subject": "mdnSubject",
                "mdn_type": "mdnType",
                "message_subject": "messageSubject",
                "requester_file_name": "requesterFileName",
                "request_path": "requestPath",
                "s3_attributes": "s3Attributes",
                "server_id": "serverId",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
            },
        )
        class AS2MDNSendCompletedProps:
            def __init__(
                self,
                *,
                agreement_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
                bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
                client_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
                disposition: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                mdn_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
                requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_attributes: typing.Optional[typing.Union["AgreementEvents.AS2MDNSendCompleted.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                server_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Agreement aws.transfer@AS2MDNSendCompleted event.

                :param agreement_id: (experimental) agreement-id property. Specify an array of string values to match this event if the actual value of agreement-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Agreement reference
                :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param client_ip: (experimental) client-ip property. Specify an array of string values to match this event if the actual value of client-ip is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param disposition: (experimental) disposition property. Specify an array of string values to match this event if the actual value of disposition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param mdn_message_id: (experimental) mdn-message-id property. Specify an array of string values to match this event if the actual value of mdn-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_subject: (experimental) mdn-subject property. Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_type: (experimental) mdn-type property. Specify an array of string values to match this event if the actual value of mdn-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param message_subject: (experimental) message-subject property. Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester_file_name: (experimental) requester-file-name property. Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_path: (experimental) request-path property. Specify an array of string values to match this event if the actual value of request-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param server_id: (experimental) server-id property. Specify an array of string values to match this event if the actual value of server-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    a_s2_mDNSend_completed_props = transfer_events.AgreementEvents.AS2MDNSendCompleted.AS2MDNSendCompletedProps(
                        agreement_id=["agreementId"],
                        as2_from=["as2From"],
                        as2_message_id=["as2MessageId"],
                        as2_to=["as2To"],
                        bytes=["bytes"],
                        client_ip=["clientIp"],
                        disposition=["disposition"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        mdn_message_id=["mdnMessageId"],
                        mdn_subject=["mdnSubject"],
                        mdn_type=["mdnType"],
                        message_subject=["messageSubject"],
                        requester_file_name=["requesterFileName"],
                        request_path=["requestPath"],
                        s3_attributes=transfer_events.AgreementEvents.AS2MDNSendCompleted.S3Attributes(
                            file_bucket=["fileBucket"],
                            file_key=["fileKey"],
                            json_bucket=["jsonBucket"],
                            json_key=["jsonKey"],
                            mdn_bucket=["mdnBucket"],
                            mdn_key=["mdnKey"]
                        ),
                        server_id=["serverId"],
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(s3_attributes, dict):
                    s3_attributes = AgreementEvents.AS2MDNSendCompleted.S3Attributes(**s3_attributes)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7cf2723b986b0f053ee6aa3f40fb51fd1f7f1d2902f61cd5383eba79884c0605)
                    check_type(argname="argument agreement_id", value=agreement_id, expected_type=type_hints["agreement_id"])
                    check_type(argname="argument as2_from", value=as2_from, expected_type=type_hints["as2_from"])
                    check_type(argname="argument as2_message_id", value=as2_message_id, expected_type=type_hints["as2_message_id"])
                    check_type(argname="argument as2_to", value=as2_to, expected_type=type_hints["as2_to"])
                    check_type(argname="argument bytes", value=bytes, expected_type=type_hints["bytes"])
                    check_type(argname="argument client_ip", value=client_ip, expected_type=type_hints["client_ip"])
                    check_type(argname="argument disposition", value=disposition, expected_type=type_hints["disposition"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument mdn_message_id", value=mdn_message_id, expected_type=type_hints["mdn_message_id"])
                    check_type(argname="argument mdn_subject", value=mdn_subject, expected_type=type_hints["mdn_subject"])
                    check_type(argname="argument mdn_type", value=mdn_type, expected_type=type_hints["mdn_type"])
                    check_type(argname="argument message_subject", value=message_subject, expected_type=type_hints["message_subject"])
                    check_type(argname="argument requester_file_name", value=requester_file_name, expected_type=type_hints["requester_file_name"])
                    check_type(argname="argument request_path", value=request_path, expected_type=type_hints["request_path"])
                    check_type(argname="argument s3_attributes", value=s3_attributes, expected_type=type_hints["s3_attributes"])
                    check_type(argname="argument server_id", value=server_id, expected_type=type_hints["server_id"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if agreement_id is not None:
                    self._values["agreement_id"] = agreement_id
                if as2_from is not None:
                    self._values["as2_from"] = as2_from
                if as2_message_id is not None:
                    self._values["as2_message_id"] = as2_message_id
                if as2_to is not None:
                    self._values["as2_to"] = as2_to
                if bytes is not None:
                    self._values["bytes"] = bytes
                if client_ip is not None:
                    self._values["client_ip"] = client_ip
                if disposition is not None:
                    self._values["disposition"] = disposition
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if mdn_message_id is not None:
                    self._values["mdn_message_id"] = mdn_message_id
                if mdn_subject is not None:
                    self._values["mdn_subject"] = mdn_subject
                if mdn_type is not None:
                    self._values["mdn_type"] = mdn_type
                if message_subject is not None:
                    self._values["message_subject"] = message_subject
                if requester_file_name is not None:
                    self._values["requester_file_name"] = requester_file_name
                if request_path is not None:
                    self._values["request_path"] = request_path
                if s3_attributes is not None:
                    self._values["s3_attributes"] = s3_attributes
                if server_id is not None:
                    self._values["server_id"] = server_id
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code

            @builtins.property
            def agreement_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) agreement-id property.

                Specify an array of string values to match this event if the actual value of agreement-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Agreement reference

                :stability: experimental
                '''
                result = self._values.get("agreement_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_from(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-from property.

                Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_from")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_message_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-message-id property.

                Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_message_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_to(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-to property.

                Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_to")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def bytes(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bytes property.

                Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bytes")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def client_ip(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) client-ip property.

                Specify an array of string values to match this event if the actual value of client-ip is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("client_ip")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def disposition(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) disposition property.

                Specify an array of string values to match this event if the actual value of disposition is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("disposition")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def mdn_message_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-message-id property.

                Specify an array of string values to match this event if the actual value of mdn-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_message_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_subject(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-subject property.

                Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_subject")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-type property.

                Specify an array of string values to match this event if the actual value of mdn-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def message_subject(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) message-subject property.

                Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("message_subject")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def requester_file_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester-file-name property.

                Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester_file_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) request-path property.

                Specify an array of string values to match this event if the actual value of request-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_attributes(
                self,
            ) -> typing.Optional["AgreementEvents.AS2MDNSendCompleted.S3Attributes"]:
                '''(experimental) s3-attributes property.

                Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_attributes")
                return typing.cast(typing.Optional["AgreementEvents.AS2MDNSendCompleted.S3Attributes"], result)

            @builtins.property
            def server_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) server-id property.

                Specify an array of string values to match this event if the actual value of server-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("server_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AS2MDNSendCompletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.AgreementEvents.AS2MDNSendCompleted.S3Attributes",
            jsii_struct_bases=[],
            name_mapping={
                "file_bucket": "fileBucket",
                "file_key": "fileKey",
                "json_bucket": "jsonBucket",
                "json_key": "jsonKey",
                "mdn_bucket": "mdnBucket",
                "mdn_key": "mdnKey",
            },
        )
        class S3Attributes:
            def __init__(
                self,
                *,
                file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_key: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for S3-attributes.

                :param file_bucket: (experimental) file-bucket property. Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_key: (experimental) file-key property. Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_bucket: (experimental) json-bucket property. Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_key: (experimental) json-key property. Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_bucket: (experimental) mdn-bucket property. Specify an array of string values to match this event if the actual value of mdn-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_key: (experimental) mdn-key property. Specify an array of string values to match this event if the actual value of mdn-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s3_attributes = transfer_events.AgreementEvents.AS2MDNSendCompleted.S3Attributes(
                        file_bucket=["fileBucket"],
                        file_key=["fileKey"],
                        json_bucket=["jsonBucket"],
                        json_key=["jsonKey"],
                        mdn_bucket=["mdnBucket"],
                        mdn_key=["mdnKey"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__19012522862a4f49dcbf4f438e9d1f878ac5e1b4a17af08e6242062f64e09711)
                    check_type(argname="argument file_bucket", value=file_bucket, expected_type=type_hints["file_bucket"])
                    check_type(argname="argument file_key", value=file_key, expected_type=type_hints["file_key"])
                    check_type(argname="argument json_bucket", value=json_bucket, expected_type=type_hints["json_bucket"])
                    check_type(argname="argument json_key", value=json_key, expected_type=type_hints["json_key"])
                    check_type(argname="argument mdn_bucket", value=mdn_bucket, expected_type=type_hints["mdn_bucket"])
                    check_type(argname="argument mdn_key", value=mdn_key, expected_type=type_hints["mdn_key"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if file_bucket is not None:
                    self._values["file_bucket"] = file_bucket
                if file_key is not None:
                    self._values["file_key"] = file_key
                if json_bucket is not None:
                    self._values["json_bucket"] = json_bucket
                if json_key is not None:
                    self._values["json_key"] = json_key
                if mdn_bucket is not None:
                    self._values["mdn_bucket"] = mdn_bucket
                if mdn_key is not None:
                    self._values["mdn_key"] = mdn_key

            @builtins.property
            def file_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-bucket property.

                Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-key property.

                Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-bucket property.

                Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-key property.

                Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-bucket property.

                Specify an array of string values to match this event if the actual value of mdn-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-key property.

                Specify an array of string values to match this event if the actual value of mdn-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "S3Attributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class AS2MDNSendFailed(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.AgreementEvents.AS2MDNSendFailed",
    ):
        '''(experimental) aws.transfer@AS2MDNSendFailed event types for Agreement.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            a_s2_mDNSend_failed = transfer_events.AgreementEvents.AS2MDNSendFailed()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.AgreementEvents.AS2MDNSendFailed.AS2MDNSendFailedProps",
            jsii_struct_bases=[],
            name_mapping={
                "agreement_id": "agreementId",
                "as2_from": "as2From",
                "as2_message_id": "as2MessageId",
                "as2_to": "as2To",
                "bytes": "bytes",
                "client_ip": "clientIp",
                "disposition": "disposition",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "failure_code": "failureCode",
                "failure_message": "failureMessage",
                "mdn_message_id": "mdnMessageId",
                "mdn_subject": "mdnSubject",
                "mdn_type": "mdnType",
                "requester_file_name": "requesterFileName",
                "s3_attributes": "s3Attributes",
                "server_id": "serverId",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
            },
        )
        class AS2MDNSendFailedProps:
            def __init__(
                self,
                *,
                agreement_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
                bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
                client_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
                disposition: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_attributes: typing.Optional[typing.Union["AgreementEvents.AS2MDNSendFailed.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                server_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Agreement aws.transfer@AS2MDNSendFailed event.

                :param agreement_id: (experimental) agreement-id property. Specify an array of string values to match this event if the actual value of agreement-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Agreement reference
                :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param client_ip: (experimental) client-ip property. Specify an array of string values to match this event if the actual value of client-ip is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param disposition: (experimental) disposition property. Specify an array of string values to match this event if the actual value of disposition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_message_id: (experimental) mdn-message-id property. Specify an array of string values to match this event if the actual value of mdn-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_subject: (experimental) mdn-subject property. Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_type: (experimental) mdn-type property. Specify an array of string values to match this event if the actual value of mdn-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester_file_name: (experimental) requester-file-name property. Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param server_id: (experimental) server-id property. Specify an array of string values to match this event if the actual value of server-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    a_s2_mDNSend_failed_props = transfer_events.AgreementEvents.AS2MDNSendFailed.AS2MDNSendFailedProps(
                        agreement_id=["agreementId"],
                        as2_from=["as2From"],
                        as2_message_id=["as2MessageId"],
                        as2_to=["as2To"],
                        bytes=["bytes"],
                        client_ip=["clientIp"],
                        disposition=["disposition"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        failure_code=["failureCode"],
                        failure_message=["failureMessage"],
                        mdn_message_id=["mdnMessageId"],
                        mdn_subject=["mdnSubject"],
                        mdn_type=["mdnType"],
                        requester_file_name=["requesterFileName"],
                        s3_attributes=transfer_events.AgreementEvents.AS2MDNSendFailed.S3Attributes(
                            file_bucket=["fileBucket"],
                            file_key=["fileKey"],
                            json_bucket=["jsonBucket"],
                            json_key=["jsonKey"],
                            mdn_bucket=["mdnBucket"],
                            mdn_key=["mdnKey"]
                        ),
                        server_id=["serverId"],
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(s3_attributes, dict):
                    s3_attributes = AgreementEvents.AS2MDNSendFailed.S3Attributes(**s3_attributes)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__144780b5c4874c2f404e1e1c80a6463ee4a13f620e9d04f0f1807218fcee513e)
                    check_type(argname="argument agreement_id", value=agreement_id, expected_type=type_hints["agreement_id"])
                    check_type(argname="argument as2_from", value=as2_from, expected_type=type_hints["as2_from"])
                    check_type(argname="argument as2_message_id", value=as2_message_id, expected_type=type_hints["as2_message_id"])
                    check_type(argname="argument as2_to", value=as2_to, expected_type=type_hints["as2_to"])
                    check_type(argname="argument bytes", value=bytes, expected_type=type_hints["bytes"])
                    check_type(argname="argument client_ip", value=client_ip, expected_type=type_hints["client_ip"])
                    check_type(argname="argument disposition", value=disposition, expected_type=type_hints["disposition"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument failure_code", value=failure_code, expected_type=type_hints["failure_code"])
                    check_type(argname="argument failure_message", value=failure_message, expected_type=type_hints["failure_message"])
                    check_type(argname="argument mdn_message_id", value=mdn_message_id, expected_type=type_hints["mdn_message_id"])
                    check_type(argname="argument mdn_subject", value=mdn_subject, expected_type=type_hints["mdn_subject"])
                    check_type(argname="argument mdn_type", value=mdn_type, expected_type=type_hints["mdn_type"])
                    check_type(argname="argument requester_file_name", value=requester_file_name, expected_type=type_hints["requester_file_name"])
                    check_type(argname="argument s3_attributes", value=s3_attributes, expected_type=type_hints["s3_attributes"])
                    check_type(argname="argument server_id", value=server_id, expected_type=type_hints["server_id"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if agreement_id is not None:
                    self._values["agreement_id"] = agreement_id
                if as2_from is not None:
                    self._values["as2_from"] = as2_from
                if as2_message_id is not None:
                    self._values["as2_message_id"] = as2_message_id
                if as2_to is not None:
                    self._values["as2_to"] = as2_to
                if bytes is not None:
                    self._values["bytes"] = bytes
                if client_ip is not None:
                    self._values["client_ip"] = client_ip
                if disposition is not None:
                    self._values["disposition"] = disposition
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if failure_code is not None:
                    self._values["failure_code"] = failure_code
                if failure_message is not None:
                    self._values["failure_message"] = failure_message
                if mdn_message_id is not None:
                    self._values["mdn_message_id"] = mdn_message_id
                if mdn_subject is not None:
                    self._values["mdn_subject"] = mdn_subject
                if mdn_type is not None:
                    self._values["mdn_type"] = mdn_type
                if requester_file_name is not None:
                    self._values["requester_file_name"] = requester_file_name
                if s3_attributes is not None:
                    self._values["s3_attributes"] = s3_attributes
                if server_id is not None:
                    self._values["server_id"] = server_id
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code

            @builtins.property
            def agreement_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) agreement-id property.

                Specify an array of string values to match this event if the actual value of agreement-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Agreement reference

                :stability: experimental
                '''
                result = self._values.get("agreement_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_from(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-from property.

                Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_from")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_message_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-message-id property.

                Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_message_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_to(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-to property.

                Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_to")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def bytes(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bytes property.

                Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bytes")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def client_ip(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) client-ip property.

                Specify an array of string values to match this event if the actual value of client-ip is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("client_ip")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def disposition(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) disposition property.

                Specify an array of string values to match this event if the actual value of disposition is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("disposition")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def failure_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) failure-message property.

                Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("failure_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_message_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-message-id property.

                Specify an array of string values to match this event if the actual value of mdn-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_message_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_subject(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-subject property.

                Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_subject")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-type property.

                Specify an array of string values to match this event if the actual value of mdn-type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def requester_file_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester-file-name property.

                Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester_file_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_attributes(
                self,
            ) -> typing.Optional["AgreementEvents.AS2MDNSendFailed.S3Attributes"]:
                '''(experimental) s3-attributes property.

                Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_attributes")
                return typing.cast(typing.Optional["AgreementEvents.AS2MDNSendFailed.S3Attributes"], result)

            @builtins.property
            def server_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) server-id property.

                Specify an array of string values to match this event if the actual value of server-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("server_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AS2MDNSendFailedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.AgreementEvents.AS2MDNSendFailed.S3Attributes",
            jsii_struct_bases=[],
            name_mapping={
                "file_bucket": "fileBucket",
                "file_key": "fileKey",
                "json_bucket": "jsonBucket",
                "json_key": "jsonKey",
                "mdn_bucket": "mdnBucket",
                "mdn_key": "mdnKey",
            },
        )
        class S3Attributes:
            def __init__(
                self,
                *,
                file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_key: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for S3-attributes.

                :param file_bucket: (experimental) file-bucket property. Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_key: (experimental) file-key property. Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_bucket: (experimental) json-bucket property. Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_key: (experimental) json-key property. Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_bucket: (experimental) mdn-bucket property. Specify an array of string values to match this event if the actual value of mdn-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_key: (experimental) mdn-key property. Specify an array of string values to match this event if the actual value of mdn-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s3_attributes = transfer_events.AgreementEvents.AS2MDNSendFailed.S3Attributes(
                        file_bucket=["fileBucket"],
                        file_key=["fileKey"],
                        json_bucket=["jsonBucket"],
                        json_key=["jsonKey"],
                        mdn_bucket=["mdnBucket"],
                        mdn_key=["mdnKey"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ba12622626a5efc12f90cc0c524bd9bf50dd360202cae702307bb7bcb8f040b2)
                    check_type(argname="argument file_bucket", value=file_bucket, expected_type=type_hints["file_bucket"])
                    check_type(argname="argument file_key", value=file_key, expected_type=type_hints["file_key"])
                    check_type(argname="argument json_bucket", value=json_bucket, expected_type=type_hints["json_bucket"])
                    check_type(argname="argument json_key", value=json_key, expected_type=type_hints["json_key"])
                    check_type(argname="argument mdn_bucket", value=mdn_bucket, expected_type=type_hints["mdn_bucket"])
                    check_type(argname="argument mdn_key", value=mdn_key, expected_type=type_hints["mdn_key"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if file_bucket is not None:
                    self._values["file_bucket"] = file_bucket
                if file_key is not None:
                    self._values["file_key"] = file_key
                if json_bucket is not None:
                    self._values["json_bucket"] = json_bucket
                if json_key is not None:
                    self._values["json_key"] = json_key
                if mdn_bucket is not None:
                    self._values["mdn_bucket"] = mdn_bucket
                if mdn_key is not None:
                    self._values["mdn_key"] = mdn_key

            @builtins.property
            def file_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-bucket property.

                Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-key property.

                Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-bucket property.

                Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-key property.

                Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-bucket property.

                Specify an array of string values to match this event if the actual value of mdn-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-key property.

                Specify an array of string values to match this event if the actual value of mdn-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "S3Attributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class AS2PayloadReceiveCompleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.AgreementEvents.AS2PayloadReceiveCompleted",
    ):
        '''(experimental) aws.transfer@AS2PayloadReceiveCompleted event types for Agreement.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            a_s2_payload_receive_completed = transfer_events.AgreementEvents.AS2PayloadReceiveCompleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.AgreementEvents.AS2PayloadReceiveCompleted.AS2PayloadReceiveCompletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "agreement_id": "agreementId",
                "as2_from": "as2From",
                "as2_message_id": "as2MessageId",
                "as2_to": "as2To",
                "bytes": "bytes",
                "client_ip": "clientIp",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "message_subject": "messageSubject",
                "requester_file_name": "requesterFileName",
                "request_path": "requestPath",
                "s3_attributes": "s3Attributes",
                "server_id": "serverId",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
            },
        )
        class AS2PayloadReceiveCompletedProps:
            def __init__(
                self,
                *,
                agreement_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
                bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
                client_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
                requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_attributes: typing.Optional[typing.Union["AgreementEvents.AS2PayloadReceiveCompleted.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                server_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Agreement aws.transfer@AS2PayloadReceiveCompleted event.

                :param agreement_id: (experimental) agreement-id property. Specify an array of string values to match this event if the actual value of agreement-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Agreement reference
                :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param client_ip: (experimental) client-ip property. Specify an array of string values to match this event if the actual value of client-ip is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param message_subject: (experimental) message-subject property. Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester_file_name: (experimental) requester-file-name property. Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_path: (experimental) request-path property. Specify an array of string values to match this event if the actual value of request-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param server_id: (experimental) server-id property. Specify an array of string values to match this event if the actual value of server-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    a_s2_payload_receive_completed_props = transfer_events.AgreementEvents.AS2PayloadReceiveCompleted.AS2PayloadReceiveCompletedProps(
                        agreement_id=["agreementId"],
                        as2_from=["as2From"],
                        as2_message_id=["as2MessageId"],
                        as2_to=["as2To"],
                        bytes=["bytes"],
                        client_ip=["clientIp"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        message_subject=["messageSubject"],
                        requester_file_name=["requesterFileName"],
                        request_path=["requestPath"],
                        s3_attributes=transfer_events.AgreementEvents.AS2PayloadReceiveCompleted.S3Attributes(
                            file_bucket=["fileBucket"],
                            file_key=["fileKey"],
                            json_bucket=["jsonBucket"],
                            json_key=["jsonKey"]
                        ),
                        server_id=["serverId"],
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(s3_attributes, dict):
                    s3_attributes = AgreementEvents.AS2PayloadReceiveCompleted.S3Attributes(**s3_attributes)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__2ffbff16b6defcab7093bca1cd1448ca6870c7e0b314ac10d35c1c3e96cce34c)
                    check_type(argname="argument agreement_id", value=agreement_id, expected_type=type_hints["agreement_id"])
                    check_type(argname="argument as2_from", value=as2_from, expected_type=type_hints["as2_from"])
                    check_type(argname="argument as2_message_id", value=as2_message_id, expected_type=type_hints["as2_message_id"])
                    check_type(argname="argument as2_to", value=as2_to, expected_type=type_hints["as2_to"])
                    check_type(argname="argument bytes", value=bytes, expected_type=type_hints["bytes"])
                    check_type(argname="argument client_ip", value=client_ip, expected_type=type_hints["client_ip"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument message_subject", value=message_subject, expected_type=type_hints["message_subject"])
                    check_type(argname="argument requester_file_name", value=requester_file_name, expected_type=type_hints["requester_file_name"])
                    check_type(argname="argument request_path", value=request_path, expected_type=type_hints["request_path"])
                    check_type(argname="argument s3_attributes", value=s3_attributes, expected_type=type_hints["s3_attributes"])
                    check_type(argname="argument server_id", value=server_id, expected_type=type_hints["server_id"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if agreement_id is not None:
                    self._values["agreement_id"] = agreement_id
                if as2_from is not None:
                    self._values["as2_from"] = as2_from
                if as2_message_id is not None:
                    self._values["as2_message_id"] = as2_message_id
                if as2_to is not None:
                    self._values["as2_to"] = as2_to
                if bytes is not None:
                    self._values["bytes"] = bytes
                if client_ip is not None:
                    self._values["client_ip"] = client_ip
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if message_subject is not None:
                    self._values["message_subject"] = message_subject
                if requester_file_name is not None:
                    self._values["requester_file_name"] = requester_file_name
                if request_path is not None:
                    self._values["request_path"] = request_path
                if s3_attributes is not None:
                    self._values["s3_attributes"] = s3_attributes
                if server_id is not None:
                    self._values["server_id"] = server_id
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code

            @builtins.property
            def agreement_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) agreement-id property.

                Specify an array of string values to match this event if the actual value of agreement-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Agreement reference

                :stability: experimental
                '''
                result = self._values.get("agreement_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_from(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-from property.

                Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_from")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_message_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-message-id property.

                Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_message_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_to(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-to property.

                Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_to")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def bytes(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bytes property.

                Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bytes")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def client_ip(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) client-ip property.

                Specify an array of string values to match this event if the actual value of client-ip is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("client_ip")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def message_subject(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) message-subject property.

                Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("message_subject")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def requester_file_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester-file-name property.

                Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester_file_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) request-path property.

                Specify an array of string values to match this event if the actual value of request-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_attributes(
                self,
            ) -> typing.Optional["AgreementEvents.AS2PayloadReceiveCompleted.S3Attributes"]:
                '''(experimental) s3-attributes property.

                Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_attributes")
                return typing.cast(typing.Optional["AgreementEvents.AS2PayloadReceiveCompleted.S3Attributes"], result)

            @builtins.property
            def server_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) server-id property.

                Specify an array of string values to match this event if the actual value of server-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("server_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AS2PayloadReceiveCompletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.AgreementEvents.AS2PayloadReceiveCompleted.S3Attributes",
            jsii_struct_bases=[],
            name_mapping={
                "file_bucket": "fileBucket",
                "file_key": "fileKey",
                "json_bucket": "jsonBucket",
                "json_key": "jsonKey",
            },
        )
        class S3Attributes:
            def __init__(
                self,
                *,
                file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for S3-attributes.

                :param file_bucket: (experimental) file-bucket property. Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_key: (experimental) file-key property. Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_bucket: (experimental) json-bucket property. Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_key: (experimental) json-key property. Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s3_attributes = transfer_events.AgreementEvents.AS2PayloadReceiveCompleted.S3Attributes(
                        file_bucket=["fileBucket"],
                        file_key=["fileKey"],
                        json_bucket=["jsonBucket"],
                        json_key=["jsonKey"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__86fcab71d35868715dad1fd235b3a707db9873c326ad700d8bb239de8fd35a04)
                    check_type(argname="argument file_bucket", value=file_bucket, expected_type=type_hints["file_bucket"])
                    check_type(argname="argument file_key", value=file_key, expected_type=type_hints["file_key"])
                    check_type(argname="argument json_bucket", value=json_bucket, expected_type=type_hints["json_bucket"])
                    check_type(argname="argument json_key", value=json_key, expected_type=type_hints["json_key"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if file_bucket is not None:
                    self._values["file_bucket"] = file_bucket
                if file_key is not None:
                    self._values["file_key"] = file_key
                if json_bucket is not None:
                    self._values["json_bucket"] = json_bucket
                if json_key is not None:
                    self._values["json_key"] = json_key

            @builtins.property
            def file_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-bucket property.

                Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-key property.

                Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-bucket property.

                Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-key property.

                Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "S3Attributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class AS2PayloadReceiveFailed(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.AgreementEvents.AS2PayloadReceiveFailed",
    ):
        '''(experimental) aws.transfer@AS2PayloadReceiveFailed event types for Agreement.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            a_s2_payload_receive_failed = transfer_events.AgreementEvents.AS2PayloadReceiveFailed()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.AgreementEvents.AS2PayloadReceiveFailed.AS2PayloadReceiveFailedProps",
            jsii_struct_bases=[],
            name_mapping={
                "agreement_id": "agreementId",
                "as2_from": "as2From",
                "as2_message_id": "as2MessageId",
                "as2_to": "as2To",
                "client_ip": "clientIp",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "failure_code": "failureCode",
                "failure_message": "failureMessage",
                "message_subject": "messageSubject",
                "s3_attributes": "s3Attributes",
                "server_id": "serverId",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
            },
        )
        class AS2PayloadReceiveFailedProps:
            def __init__(
                self,
                *,
                agreement_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
                client_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_attributes: typing.Optional[typing.Union["AgreementEvents.AS2PayloadReceiveFailed.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                server_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Agreement aws.transfer@AS2PayloadReceiveFailed event.

                :param agreement_id: (experimental) agreement-id property. Specify an array of string values to match this event if the actual value of agreement-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Agreement reference
                :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param client_ip: (experimental) client-ip property. Specify an array of string values to match this event if the actual value of client-ip is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param message_subject: (experimental) message-subject property. Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param server_id: (experimental) server-id property. Specify an array of string values to match this event if the actual value of server-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    a_s2_payload_receive_failed_props = transfer_events.AgreementEvents.AS2PayloadReceiveFailed.AS2PayloadReceiveFailedProps(
                        agreement_id=["agreementId"],
                        as2_from=["as2From"],
                        as2_message_id=["as2MessageId"],
                        as2_to=["as2To"],
                        client_ip=["clientIp"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        failure_code=["failureCode"],
                        failure_message=["failureMessage"],
                        message_subject=["messageSubject"],
                        s3_attributes=transfer_events.AgreementEvents.AS2PayloadReceiveFailed.S3Attributes(
                            file_bucket=["fileBucket"],
                            file_key=["fileKey"],
                            json_bucket=["jsonBucket"],
                            json_key=["jsonKey"]
                        ),
                        server_id=["serverId"],
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(s3_attributes, dict):
                    s3_attributes = AgreementEvents.AS2PayloadReceiveFailed.S3Attributes(**s3_attributes)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__5e86b346796909ba2e35dd210e171c5ff26bb3513693cc247776e2180a563cce)
                    check_type(argname="argument agreement_id", value=agreement_id, expected_type=type_hints["agreement_id"])
                    check_type(argname="argument as2_from", value=as2_from, expected_type=type_hints["as2_from"])
                    check_type(argname="argument as2_message_id", value=as2_message_id, expected_type=type_hints["as2_message_id"])
                    check_type(argname="argument as2_to", value=as2_to, expected_type=type_hints["as2_to"])
                    check_type(argname="argument client_ip", value=client_ip, expected_type=type_hints["client_ip"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument failure_code", value=failure_code, expected_type=type_hints["failure_code"])
                    check_type(argname="argument failure_message", value=failure_message, expected_type=type_hints["failure_message"])
                    check_type(argname="argument message_subject", value=message_subject, expected_type=type_hints["message_subject"])
                    check_type(argname="argument s3_attributes", value=s3_attributes, expected_type=type_hints["s3_attributes"])
                    check_type(argname="argument server_id", value=server_id, expected_type=type_hints["server_id"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if agreement_id is not None:
                    self._values["agreement_id"] = agreement_id
                if as2_from is not None:
                    self._values["as2_from"] = as2_from
                if as2_message_id is not None:
                    self._values["as2_message_id"] = as2_message_id
                if as2_to is not None:
                    self._values["as2_to"] = as2_to
                if client_ip is not None:
                    self._values["client_ip"] = client_ip
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if failure_code is not None:
                    self._values["failure_code"] = failure_code
                if failure_message is not None:
                    self._values["failure_message"] = failure_message
                if message_subject is not None:
                    self._values["message_subject"] = message_subject
                if s3_attributes is not None:
                    self._values["s3_attributes"] = s3_attributes
                if server_id is not None:
                    self._values["server_id"] = server_id
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code

            @builtins.property
            def agreement_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) agreement-id property.

                Specify an array of string values to match this event if the actual value of agreement-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Agreement reference

                :stability: experimental
                '''
                result = self._values.get("agreement_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_from(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-from property.

                Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_from")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_message_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-message-id property.

                Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_message_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_to(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-to property.

                Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_to")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def client_ip(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) client-ip property.

                Specify an array of string values to match this event if the actual value of client-ip is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("client_ip")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def failure_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) failure-message property.

                Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("failure_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def message_subject(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) message-subject property.

                Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("message_subject")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_attributes(
                self,
            ) -> typing.Optional["AgreementEvents.AS2PayloadReceiveFailed.S3Attributes"]:
                '''(experimental) s3-attributes property.

                Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_attributes")
                return typing.cast(typing.Optional["AgreementEvents.AS2PayloadReceiveFailed.S3Attributes"], result)

            @builtins.property
            def server_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) server-id property.

                Specify an array of string values to match this event if the actual value of server-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("server_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AS2PayloadReceiveFailedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.AgreementEvents.AS2PayloadReceiveFailed.S3Attributes",
            jsii_struct_bases=[],
            name_mapping={
                "file_bucket": "fileBucket",
                "file_key": "fileKey",
                "json_bucket": "jsonBucket",
                "json_key": "jsonKey",
            },
        )
        class S3Attributes:
            def __init__(
                self,
                *,
                file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for S3-attributes.

                :param file_bucket: (experimental) file-bucket property. Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_key: (experimental) file-key property. Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_bucket: (experimental) json-bucket property. Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_key: (experimental) json-key property. Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s3_attributes = transfer_events.AgreementEvents.AS2PayloadReceiveFailed.S3Attributes(
                        file_bucket=["fileBucket"],
                        file_key=["fileKey"],
                        json_bucket=["jsonBucket"],
                        json_key=["jsonKey"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3ae82f29b97c60add789e4819a603d91c058a564869ec20194cb4519d352c91f)
                    check_type(argname="argument file_bucket", value=file_bucket, expected_type=type_hints["file_bucket"])
                    check_type(argname="argument file_key", value=file_key, expected_type=type_hints["file_key"])
                    check_type(argname="argument json_bucket", value=json_bucket, expected_type=type_hints["json_bucket"])
                    check_type(argname="argument json_key", value=json_key, expected_type=type_hints["json_key"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if file_bucket is not None:
                    self._values["file_bucket"] = file_bucket
                if file_key is not None:
                    self._values["file_key"] = file_key
                if json_bucket is not None:
                    self._values["json_bucket"] = json_bucket
                if json_key is not None:
                    self._values["json_key"] = json_key

            @builtins.property
            def file_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-bucket property.

                Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-key property.

                Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-bucket property.

                Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-key property.

                Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "S3Attributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


class ConnectorEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents",
):
    '''(experimental) EventBridge event patterns for Connector.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
        from aws_cdk.interfaces import aws_transfer as interfaces_transfer
        
        # connector_ref: interfaces_transfer.IConnectorRef
        
        connector_events = transfer_events.ConnectorEvents.from_connector(connector_ref)
    '''

    @jsii.member(jsii_name="fromConnector")
    @builtins.classmethod
    def from_connector(
        cls,
        connector_ref: _aws_cdk_interfaces_aws_transfer_ceddda9d.IConnectorRef,
    ) -> "ConnectorEvents":
        '''(experimental) Create ConnectorEvents from a Connector reference.

        :param connector_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0530f3fa356cedec3188ea511d834e381ad8d3f0d072ee37c9839f47d31fe4)
            check_type(argname="argument connector_ref", value=connector_ref, expected_type=type_hints["connector_ref"])
        return typing.cast("ConnectorEvents", jsii.sinvoke(cls, "fromConnector", [connector_ref]))

    @jsii.member(jsii_name="aS2MDNReceiveCompletedPattern")
    def a_s2_mdn_receive_completed_pattern(
        self,
        *,
        as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
        bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
        connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        disposition: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        mdn_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
        message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
        requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_attributes: typing.Optional[typing.Union["ConnectorEvents.AS2MDNReceiveCompleted.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Connector AS2 MDN Receive Completed.

        :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
        :param disposition: (experimental) disposition property. Specify an array of string values to match this event if the actual value of disposition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param mdn_message_id: (experimental) mdn-message-id property. Specify an array of string values to match this event if the actual value of mdn-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param mdn_subject: (experimental) mdn-subject property. Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param message_subject: (experimental) message-subject property. Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester_file_name: (experimental) requester-file-name property. Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ConnectorEvents.AS2MDNReceiveCompleted.AS2MDNReceiveCompletedProps(
            as2_from=as2_from,
            as2_message_id=as2_message_id,
            as2_to=as2_to,
            bytes=bytes,
            connector_id=connector_id,
            disposition=disposition,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            mdn_message_id=mdn_message_id,
            mdn_subject=mdn_subject,
            message_subject=message_subject,
            requester_file_name=requester_file_name,
            s3_attributes=s3_attributes,
            start_timestamp=start_timestamp,
            status_code=status_code,
            transfer_id=transfer_id,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "aS2MDNReceiveCompletedPattern", [options]))

    @jsii.member(jsii_name="aS2MDNReceiveFailedPattern")
    def a_s2_mdn_receive_failed_pattern(
        self,
        *,
        as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
        connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
        mdn_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
        message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_attributes: typing.Optional[typing.Union["ConnectorEvents.AS2MDNReceiveFailed.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Connector AS2 MDN Receive Failed.

        :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param mdn_message_id: (experimental) mdn-message-id property. Specify an array of string values to match this event if the actual value of mdn-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param mdn_subject: (experimental) mdn-subject property. Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param message_subject: (experimental) message-subject property. Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ConnectorEvents.AS2MDNReceiveFailed.AS2MDNReceiveFailedProps(
            as2_from=as2_from,
            as2_message_id=as2_message_id,
            as2_to=as2_to,
            connector_id=connector_id,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            failure_code=failure_code,
            failure_message=failure_message,
            mdn_message_id=mdn_message_id,
            mdn_subject=mdn_subject,
            message_subject=message_subject,
            s3_attributes=s3_attributes,
            start_timestamp=start_timestamp,
            status_code=status_code,
            transfer_id=transfer_id,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "aS2MDNReceiveFailedPattern", [options]))

    @jsii.member(jsii_name="aS2PayloadSendCompletedPattern")
    def a_s2_payload_send_completed_pattern(
        self,
        *,
        as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
        bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
        connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
        message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
        requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_attributes: typing.Optional[typing.Union["ConnectorEvents.AS2PayloadSendCompleted.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Connector AS2 Payload Send Completed.

        :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param mdn_subject: (experimental) mdn-subject property. Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param message_subject: (experimental) message-subject property. Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester_file_name: (experimental) requester-file-name property. Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ConnectorEvents.AS2PayloadSendCompleted.AS2PayloadSendCompletedProps(
            as2_from=as2_from,
            as2_message_id=as2_message_id,
            as2_to=as2_to,
            bytes=bytes,
            connector_id=connector_id,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            mdn_subject=mdn_subject,
            message_subject=message_subject,
            requester_file_name=requester_file_name,
            s3_attributes=s3_attributes,
            start_timestamp=start_timestamp,
            status_code=status_code,
            transfer_id=transfer_id,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "aS2PayloadSendCompletedPattern", [options]))

    @jsii.member(jsii_name="aS2PayloadSendFailedPattern")
    def a_s2_payload_send_failed_pattern(
        self,
        *,
        as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
        bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
        connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
        message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
        requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_attributes: typing.Optional[typing.Union["ConnectorEvents.AS2PayloadSendFailed.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Connector AS2 Payload Send Failed.

        :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param message_subject: (experimental) message-subject property. Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param requester_file_name: (experimental) requester-file-name property. Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ConnectorEvents.AS2PayloadSendFailed.AS2PayloadSendFailedProps(
            as2_from=as2_from,
            as2_message_id=as2_message_id,
            as2_to=as2_to,
            bytes=bytes,
            connector_id=connector_id,
            event_metadata=event_metadata,
            failure_code=failure_code,
            failure_message=failure_message,
            message_subject=message_subject,
            requester_file_name=requester_file_name,
            s3_attributes=s3_attributes,
            status_code=status_code,
            transfer_id=transfer_id,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "aS2PayloadSendFailedPattern", [options]))

    @jsii.member(jsii_name="sFTPConnectorDirectoryListingCompletedPattern")
    def s_ftp_connector_directory_listing_completed_pattern(
        self,
        *,
        connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        item_count: typing.Optional[typing.Sequence[builtins.str]] = None,
        listing_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_items: typing.Optional[typing.Sequence[builtins.str]] = None,
        output_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        output_file_location: typing.Optional[typing.Union["ConnectorEvents.SFTPConnectorDirectoryListingCompleted.OutputFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        remote_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        truncated: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Connector SFTP Connector Directory Listing Completed.

        :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param item_count: (experimental) item-count property. Specify an array of string values to match this event if the actual value of item-count is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param listing_id: (experimental) listing-id property. Specify an array of string values to match this event if the actual value of listing-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param max_items: (experimental) max-items property. Specify an array of string values to match this event if the actual value of max-items is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param output_directory_path: (experimental) output-directory-path property. Specify an array of string values to match this event if the actual value of output-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param output_file_location: (experimental) output-file-location property. Specify an array of string values to match this event if the actual value of output-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param remote_directory_path: (experimental) remote-directory-path property. Specify an array of string values to match this event if the actual value of remote-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param truncated: (experimental) truncated property. Specify an array of string values to match this event if the actual value of truncated is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ConnectorEvents.SFTPConnectorDirectoryListingCompleted.SFTPConnectorDirectoryListingCompletedProps(
            connector_id=connector_id,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            item_count=item_count,
            listing_id=listing_id,
            max_items=max_items,
            output_directory_path=output_directory_path,
            output_file_location=output_file_location,
            remote_directory_path=remote_directory_path,
            start_timestamp=start_timestamp,
            status_code=status_code,
            truncated=truncated,
            url=url,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "sFTPConnectorDirectoryListingCompletedPattern", [options]))

    @jsii.member(jsii_name="sFTPConnectorDirectoryListingFailedPattern")
    def s_ftp_connector_directory_listing_failed_pattern(
        self,
        *,
        connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
        listing_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_items: typing.Optional[typing.Sequence[builtins.str]] = None,
        output_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        remote_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Connector SFTP Connector Directory Listing Failed.

        :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param listing_id: (experimental) listing-id property. Specify an array of string values to match this event if the actual value of listing-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param max_items: (experimental) max-items property. Specify an array of string values to match this event if the actual value of max-items is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param output_directory_path: (experimental) output-directory-path property. Specify an array of string values to match this event if the actual value of output-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param remote_directory_path: (experimental) remote-directory-path property. Specify an array of string values to match this event if the actual value of remote-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ConnectorEvents.SFTPConnectorDirectoryListingFailed.SFTPConnectorDirectoryListingFailedProps(
            connector_id=connector_id,
            event_metadata=event_metadata,
            failure_code=failure_code,
            failure_message=failure_message,
            listing_id=listing_id,
            max_items=max_items,
            output_directory_path=output_directory_path,
            remote_directory_path=remote_directory_path,
            status_code=status_code,
            url=url,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "sFTPConnectorDirectoryListingFailedPattern", [options]))

    @jsii.member(jsii_name="sFTPConnectorFileRetrieveCompletedPattern")
    def s_ftp_connector_file_retrieve_completed_pattern(
        self,
        *,
        bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
        connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_file_location: typing.Optional[typing.Union["ConnectorEvents.SFTPConnectorFileRetrieveCompleted.LocalFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        operation: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Connector SFTP Connector File Retrieve Completed.

        :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param file_path: (experimental) file-path property. Specify an array of string values to match this event if the actual value of file-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param file_transfer_id: (experimental) file-transfer-id property. Specify an array of string values to match this event if the actual value of file-transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param local_directory_path: (experimental) local-directory-path property. Specify an array of string values to match this event if the actual value of local-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param local_file_location: (experimental) local-file-location property. Specify an array of string values to match this event if the actual value of local-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ConnectorEvents.SFTPConnectorFileRetrieveCompleted.SFTPConnectorFileRetrieveCompletedProps(
            bytes=bytes,
            connector_id=connector_id,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            file_path=file_path,
            file_transfer_id=file_transfer_id,
            local_directory_path=local_directory_path,
            local_file_location=local_file_location,
            operation=operation,
            start_timestamp=start_timestamp,
            status_code=status_code,
            transfer_id=transfer_id,
            url=url,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "sFTPConnectorFileRetrieveCompletedPattern", [options]))

    @jsii.member(jsii_name="sFTPConnectorFileRetrieveFailedPattern")
    def s_ftp_connector_file_retrieve_failed_pattern(
        self,
        *,
        bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
        connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_file_location: typing.Optional[typing.Union["ConnectorEvents.SFTPConnectorFileRetrieveFailed.LocalFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        operation: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Connector SFTP Connector File Retrieve Failed.

        :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param file_path: (experimental) file-path property. Specify an array of string values to match this event if the actual value of file-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param file_transfer_id: (experimental) file-transfer-id property. Specify an array of string values to match this event if the actual value of file-transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param local_directory_path: (experimental) local-directory-path property. Specify an array of string values to match this event if the actual value of local-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param local_file_location: (experimental) local-file-location property. Specify an array of string values to match this event if the actual value of local-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ConnectorEvents.SFTPConnectorFileRetrieveFailed.SFTPConnectorFileRetrieveFailedProps(
            bytes=bytes,
            connector_id=connector_id,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            failure_code=failure_code,
            failure_message=failure_message,
            file_path=file_path,
            file_transfer_id=file_transfer_id,
            local_directory_path=local_directory_path,
            local_file_location=local_file_location,
            operation=operation,
            start_timestamp=start_timestamp,
            status_code=status_code,
            transfer_id=transfer_id,
            url=url,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "sFTPConnectorFileRetrieveFailedPattern", [options]))

    @jsii.member(jsii_name="sFTPConnectorFileSendCompletedPattern")
    def s_ftp_connector_file_send_completed_pattern(
        self,
        *,
        bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
        connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_file_location: typing.Optional[typing.Union["ConnectorEvents.SFTPConnectorFileSendCompleted.LocalFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        operation: typing.Optional[typing.Sequence[builtins.str]] = None,
        remote_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Connector SFTP Connector File Send Completed.

        :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param file_path: (experimental) file-path property. Specify an array of string values to match this event if the actual value of file-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param file_transfer_id: (experimental) file-transfer-id property. Specify an array of string values to match this event if the actual value of file-transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param local_file_location: (experimental) local-file-location property. Specify an array of string values to match this event if the actual value of local-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param remote_directory_path: (experimental) remote-directory-path property. Specify an array of string values to match this event if the actual value of remote-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ConnectorEvents.SFTPConnectorFileSendCompleted.SFTPConnectorFileSendCompletedProps(
            bytes=bytes,
            connector_id=connector_id,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            file_path=file_path,
            file_transfer_id=file_transfer_id,
            local_file_location=local_file_location,
            operation=operation,
            remote_directory_path=remote_directory_path,
            start_timestamp=start_timestamp,
            status_code=status_code,
            transfer_id=transfer_id,
            url=url,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "sFTPConnectorFileSendCompletedPattern", [options]))

    @jsii.member(jsii_name="sFTPConnectorFileSendFailedPattern")
    def s_ftp_connector_file_send_failed_pattern(
        self,
        *,
        bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
        connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_file_location: typing.Optional[typing.Union["ConnectorEvents.SFTPConnectorFileSendFailed.LocalFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        operation: typing.Optional[typing.Sequence[builtins.str]] = None,
        remote_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Connector SFTP Connector File Send Failed.

        :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param file_path: (experimental) file-path property. Specify an array of string values to match this event if the actual value of file-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param file_transfer_id: (experimental) file-transfer-id property. Specify an array of string values to match this event if the actual value of file-transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param local_file_location: (experimental) local-file-location property. Specify an array of string values to match this event if the actual value of local-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param remote_directory_path: (experimental) remote-directory-path property. Specify an array of string values to match this event if the actual value of remote-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ConnectorEvents.SFTPConnectorFileSendFailed.SFTPConnectorFileSendFailedProps(
            bytes=bytes,
            connector_id=connector_id,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            failure_code=failure_code,
            failure_message=failure_message,
            file_path=file_path,
            file_transfer_id=file_transfer_id,
            local_file_location=local_file_location,
            operation=operation,
            remote_directory_path=remote_directory_path,
            start_timestamp=start_timestamp,
            status_code=status_code,
            transfer_id=transfer_id,
            url=url,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "sFTPConnectorFileSendFailedPattern", [options]))

    @jsii.member(jsii_name="sFTPConnectorRemoteDeleteCompletedPattern")
    def s_ftp_connector_remote_delete_completed_pattern(
        self,
        *,
        connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        delete_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        delete_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        operation: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Connector SFTP Connector Remote Delete Completed.

        :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
        :param delete_id: (experimental) delete-id property. Specify an array of string values to match this event if the actual value of delete-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param delete_path: (experimental) delete-path property. Specify an array of string values to match this event if the actual value of delete-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ConnectorEvents.SFTPConnectorRemoteDeleteCompleted.SFTPConnectorRemoteDeleteCompletedProps(
            connector_id=connector_id,
            delete_id=delete_id,
            delete_path=delete_path,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            operation=operation,
            start_timestamp=start_timestamp,
            status_code=status_code,
            url=url,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "sFTPConnectorRemoteDeleteCompletedPattern", [options]))

    @jsii.member(jsii_name="sFTPConnectorRemoteDeleteFailedPattern")
    def s_ftp_connector_remote_delete_failed_pattern(
        self,
        *,
        connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        delete_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        delete_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
        operation: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Connector SFTP Connector Remote Delete Failed.

        :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
        :param delete_id: (experimental) delete-id property. Specify an array of string values to match this event if the actual value of delete-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param delete_path: (experimental) delete-path property. Specify an array of string values to match this event if the actual value of delete-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ConnectorEvents.SFTPConnectorRemoteDeleteFailed.SFTPConnectorRemoteDeleteFailedProps(
            connector_id=connector_id,
            delete_id=delete_id,
            delete_path=delete_path,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            failure_code=failure_code,
            failure_message=failure_message,
            operation=operation,
            start_timestamp=start_timestamp,
            status_code=status_code,
            url=url,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "sFTPConnectorRemoteDeleteFailedPattern", [options]))

    @jsii.member(jsii_name="sFTPConnectorRemoteMoveCompletedPattern")
    def s_ftp_connector_remote_move_completed_pattern(
        self,
        *,
        connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        move_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        move_source_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        move_target_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        operation: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Connector SFTP Connector Remote Move Completed.

        :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param move_id: (experimental) move-id property. Specify an array of string values to match this event if the actual value of move-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param move_source_path: (experimental) move-source-path property. Specify an array of string values to match this event if the actual value of move-source-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param move_target_path: (experimental) move-target-path property. Specify an array of string values to match this event if the actual value of move-target-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ConnectorEvents.SFTPConnectorRemoteMoveCompleted.SFTPConnectorRemoteMoveCompletedProps(
            connector_id=connector_id,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            move_id=move_id,
            move_source_path=move_source_path,
            move_target_path=move_target_path,
            operation=operation,
            start_timestamp=start_timestamp,
            status_code=status_code,
            url=url,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "sFTPConnectorRemoteMoveCompletedPattern", [options]))

    @jsii.member(jsii_name="sFTPConnectorRemoteMoveFailedPattern")
    def s_ftp_connector_remote_move_failed_pattern(
        self,
        *,
        connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
        move_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        move_source_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        move_target_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        operation: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Connector SFTP Connector Remote Move Failed.

        :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
        :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param move_id: (experimental) move-id property. Specify an array of string values to match this event if the actual value of move-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param move_source_path: (experimental) move-source-path property. Specify an array of string values to match this event if the actual value of move-source-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param move_target_path: (experimental) move-target-path property. Specify an array of string values to match this event if the actual value of move-target-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ConnectorEvents.SFTPConnectorRemoteMoveFailed.SFTPConnectorRemoteMoveFailedProps(
            connector_id=connector_id,
            end_timestamp=end_timestamp,
            event_metadata=event_metadata,
            failure_code=failure_code,
            failure_message=failure_message,
            move_id=move_id,
            move_source_path=move_source_path,
            move_target_path=move_target_path,
            operation=operation,
            start_timestamp=start_timestamp,
            status_code=status_code,
            url=url,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "sFTPConnectorRemoteMoveFailedPattern", [options]))

    class AS2MDNReceiveCompleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.AS2MDNReceiveCompleted",
    ):
        '''(experimental) aws.transfer@AS2MDNReceiveCompleted event types for Connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            a_s2_mDNReceive_completed = transfer_events.ConnectorEvents.AS2MDNReceiveCompleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.AS2MDNReceiveCompleted.AS2MDNReceiveCompletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "as2_from": "as2From",
                "as2_message_id": "as2MessageId",
                "as2_to": "as2To",
                "bytes": "bytes",
                "connector_id": "connectorId",
                "disposition": "disposition",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "mdn_message_id": "mdnMessageId",
                "mdn_subject": "mdnSubject",
                "message_subject": "messageSubject",
                "requester_file_name": "requesterFileName",
                "s3_attributes": "s3Attributes",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
                "transfer_id": "transferId",
            },
        )
        class AS2MDNReceiveCompletedProps:
            def __init__(
                self,
                *,
                as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
                bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
                connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                disposition: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                mdn_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
                message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
                requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_attributes: typing.Optional[typing.Union["ConnectorEvents.AS2MDNReceiveCompleted.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Connector aws.transfer@AS2MDNReceiveCompleted event.

                :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
                :param disposition: (experimental) disposition property. Specify an array of string values to match this event if the actual value of disposition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param mdn_message_id: (experimental) mdn-message-id property. Specify an array of string values to match this event if the actual value of mdn-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_subject: (experimental) mdn-subject property. Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param message_subject: (experimental) message-subject property. Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester_file_name: (experimental) requester-file-name property. Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    a_s2_mDNReceive_completed_props = transfer_events.ConnectorEvents.AS2MDNReceiveCompleted.AS2MDNReceiveCompletedProps(
                        as2_from=["as2From"],
                        as2_message_id=["as2MessageId"],
                        as2_to=["as2To"],
                        bytes=["bytes"],
                        connector_id=["connectorId"],
                        disposition=["disposition"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        mdn_message_id=["mdnMessageId"],
                        mdn_subject=["mdnSubject"],
                        message_subject=["messageSubject"],
                        requester_file_name=["requesterFileName"],
                        s3_attributes=transfer_events.ConnectorEvents.AS2MDNReceiveCompleted.S3Attributes(
                            file_bucket=["fileBucket"],
                            file_key=["fileKey"],
                            json_bucket=["jsonBucket"],
                            json_key=["jsonKey"],
                            mdn_bucket=["mdnBucket"],
                            mdn_key=["mdnKey"]
                        ),
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"],
                        transfer_id=["transferId"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(s3_attributes, dict):
                    s3_attributes = ConnectorEvents.AS2MDNReceiveCompleted.S3Attributes(**s3_attributes)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__b02c22d06f28f7c76093cdf7bfa1655649bfbfebe37724cd2e8682a1ae8ec85f)
                    check_type(argname="argument as2_from", value=as2_from, expected_type=type_hints["as2_from"])
                    check_type(argname="argument as2_message_id", value=as2_message_id, expected_type=type_hints["as2_message_id"])
                    check_type(argname="argument as2_to", value=as2_to, expected_type=type_hints["as2_to"])
                    check_type(argname="argument bytes", value=bytes, expected_type=type_hints["bytes"])
                    check_type(argname="argument connector_id", value=connector_id, expected_type=type_hints["connector_id"])
                    check_type(argname="argument disposition", value=disposition, expected_type=type_hints["disposition"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument mdn_message_id", value=mdn_message_id, expected_type=type_hints["mdn_message_id"])
                    check_type(argname="argument mdn_subject", value=mdn_subject, expected_type=type_hints["mdn_subject"])
                    check_type(argname="argument message_subject", value=message_subject, expected_type=type_hints["message_subject"])
                    check_type(argname="argument requester_file_name", value=requester_file_name, expected_type=type_hints["requester_file_name"])
                    check_type(argname="argument s3_attributes", value=s3_attributes, expected_type=type_hints["s3_attributes"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument transfer_id", value=transfer_id, expected_type=type_hints["transfer_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if as2_from is not None:
                    self._values["as2_from"] = as2_from
                if as2_message_id is not None:
                    self._values["as2_message_id"] = as2_message_id
                if as2_to is not None:
                    self._values["as2_to"] = as2_to
                if bytes is not None:
                    self._values["bytes"] = bytes
                if connector_id is not None:
                    self._values["connector_id"] = connector_id
                if disposition is not None:
                    self._values["disposition"] = disposition
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if mdn_message_id is not None:
                    self._values["mdn_message_id"] = mdn_message_id
                if mdn_subject is not None:
                    self._values["mdn_subject"] = mdn_subject
                if message_subject is not None:
                    self._values["message_subject"] = message_subject
                if requester_file_name is not None:
                    self._values["requester_file_name"] = requester_file_name
                if s3_attributes is not None:
                    self._values["s3_attributes"] = s3_attributes
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code
                if transfer_id is not None:
                    self._values["transfer_id"] = transfer_id

            @builtins.property
            def as2_from(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-from property.

                Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_from")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_message_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-message-id property.

                Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_message_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_to(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-to property.

                Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_to")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def bytes(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bytes property.

                Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bytes")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def connector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connector-id property.

                Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Connector reference

                :stability: experimental
                '''
                result = self._values.get("connector_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def disposition(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) disposition property.

                Specify an array of string values to match this event if the actual value of disposition is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("disposition")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def mdn_message_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-message-id property.

                Specify an array of string values to match this event if the actual value of mdn-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_message_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_subject(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-subject property.

                Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_subject")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def message_subject(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) message-subject property.

                Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("message_subject")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def requester_file_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester-file-name property.

                Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester_file_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_attributes(
                self,
            ) -> typing.Optional["ConnectorEvents.AS2MDNReceiveCompleted.S3Attributes"]:
                '''(experimental) s3-attributes property.

                Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_attributes")
                return typing.cast(typing.Optional["ConnectorEvents.AS2MDNReceiveCompleted.S3Attributes"], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transfer_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) transfer-id property.

                Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transfer_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AS2MDNReceiveCompletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.AS2MDNReceiveCompleted.S3Attributes",
            jsii_struct_bases=[],
            name_mapping={
                "file_bucket": "fileBucket",
                "file_key": "fileKey",
                "json_bucket": "jsonBucket",
                "json_key": "jsonKey",
                "mdn_bucket": "mdnBucket",
                "mdn_key": "mdnKey",
            },
        )
        class S3Attributes:
            def __init__(
                self,
                *,
                file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_key: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for S3-attributes.

                :param file_bucket: (experimental) file-bucket property. Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_key: (experimental) file-key property. Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_bucket: (experimental) json-bucket property. Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_key: (experimental) json-key property. Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_bucket: (experimental) mdn-bucket property. Specify an array of string values to match this event if the actual value of mdn-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_key: (experimental) mdn-key property. Specify an array of string values to match this event if the actual value of mdn-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s3_attributes = transfer_events.ConnectorEvents.AS2MDNReceiveCompleted.S3Attributes(
                        file_bucket=["fileBucket"],
                        file_key=["fileKey"],
                        json_bucket=["jsonBucket"],
                        json_key=["jsonKey"],
                        mdn_bucket=["mdnBucket"],
                        mdn_key=["mdnKey"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__6a248584b316f8bbb633a6ed946dd47c6767aa9f1174aeb5adf29abda3a00b44)
                    check_type(argname="argument file_bucket", value=file_bucket, expected_type=type_hints["file_bucket"])
                    check_type(argname="argument file_key", value=file_key, expected_type=type_hints["file_key"])
                    check_type(argname="argument json_bucket", value=json_bucket, expected_type=type_hints["json_bucket"])
                    check_type(argname="argument json_key", value=json_key, expected_type=type_hints["json_key"])
                    check_type(argname="argument mdn_bucket", value=mdn_bucket, expected_type=type_hints["mdn_bucket"])
                    check_type(argname="argument mdn_key", value=mdn_key, expected_type=type_hints["mdn_key"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if file_bucket is not None:
                    self._values["file_bucket"] = file_bucket
                if file_key is not None:
                    self._values["file_key"] = file_key
                if json_bucket is not None:
                    self._values["json_bucket"] = json_bucket
                if json_key is not None:
                    self._values["json_key"] = json_key
                if mdn_bucket is not None:
                    self._values["mdn_bucket"] = mdn_bucket
                if mdn_key is not None:
                    self._values["mdn_key"] = mdn_key

            @builtins.property
            def file_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-bucket property.

                Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-key property.

                Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-bucket property.

                Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-key property.

                Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-bucket property.

                Specify an array of string values to match this event if the actual value of mdn-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-key property.

                Specify an array of string values to match this event if the actual value of mdn-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "S3Attributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class AS2MDNReceiveFailed(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.AS2MDNReceiveFailed",
    ):
        '''(experimental) aws.transfer@AS2MDNReceiveFailed event types for Connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            a_s2_mDNReceive_failed = transfer_events.ConnectorEvents.AS2MDNReceiveFailed()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.AS2MDNReceiveFailed.AS2MDNReceiveFailedProps",
            jsii_struct_bases=[],
            name_mapping={
                "as2_from": "as2From",
                "as2_message_id": "as2MessageId",
                "as2_to": "as2To",
                "connector_id": "connectorId",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "failure_code": "failureCode",
                "failure_message": "failureMessage",
                "mdn_message_id": "mdnMessageId",
                "mdn_subject": "mdnSubject",
                "message_subject": "messageSubject",
                "s3_attributes": "s3Attributes",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
                "transfer_id": "transferId",
            },
        )
        class AS2MDNReceiveFailedProps:
            def __init__(
                self,
                *,
                as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
                connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
                message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_attributes: typing.Optional[typing.Union["ConnectorEvents.AS2MDNReceiveFailed.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Connector aws.transfer@AS2MDNReceiveFailed event.

                :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_message_id: (experimental) mdn-message-id property. Specify an array of string values to match this event if the actual value of mdn-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_subject: (experimental) mdn-subject property. Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param message_subject: (experimental) message-subject property. Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    a_s2_mDNReceive_failed_props = transfer_events.ConnectorEvents.AS2MDNReceiveFailed.AS2MDNReceiveFailedProps(
                        as2_from=["as2From"],
                        as2_message_id=["as2MessageId"],
                        as2_to=["as2To"],
                        connector_id=["connectorId"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        failure_code=["failureCode"],
                        failure_message=["failureMessage"],
                        mdn_message_id=["mdnMessageId"],
                        mdn_subject=["mdnSubject"],
                        message_subject=["messageSubject"],
                        s3_attributes=transfer_events.ConnectorEvents.AS2MDNReceiveFailed.S3Attributes(
                            file_bucket=["fileBucket"],
                            file_key=["fileKey"],
                            json_bucket=["jsonBucket"],
                            json_key=["jsonKey"],
                            mdn_bucket=["mdnBucket"],
                            mdn_key=["mdnKey"]
                        ),
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"],
                        transfer_id=["transferId"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(s3_attributes, dict):
                    s3_attributes = ConnectorEvents.AS2MDNReceiveFailed.S3Attributes(**s3_attributes)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__2bc5ec1442c5a832b4aa0485e5e0e3886b8311411154ed947cf409c11c9256ff)
                    check_type(argname="argument as2_from", value=as2_from, expected_type=type_hints["as2_from"])
                    check_type(argname="argument as2_message_id", value=as2_message_id, expected_type=type_hints["as2_message_id"])
                    check_type(argname="argument as2_to", value=as2_to, expected_type=type_hints["as2_to"])
                    check_type(argname="argument connector_id", value=connector_id, expected_type=type_hints["connector_id"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument failure_code", value=failure_code, expected_type=type_hints["failure_code"])
                    check_type(argname="argument failure_message", value=failure_message, expected_type=type_hints["failure_message"])
                    check_type(argname="argument mdn_message_id", value=mdn_message_id, expected_type=type_hints["mdn_message_id"])
                    check_type(argname="argument mdn_subject", value=mdn_subject, expected_type=type_hints["mdn_subject"])
                    check_type(argname="argument message_subject", value=message_subject, expected_type=type_hints["message_subject"])
                    check_type(argname="argument s3_attributes", value=s3_attributes, expected_type=type_hints["s3_attributes"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument transfer_id", value=transfer_id, expected_type=type_hints["transfer_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if as2_from is not None:
                    self._values["as2_from"] = as2_from
                if as2_message_id is not None:
                    self._values["as2_message_id"] = as2_message_id
                if as2_to is not None:
                    self._values["as2_to"] = as2_to
                if connector_id is not None:
                    self._values["connector_id"] = connector_id
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if failure_code is not None:
                    self._values["failure_code"] = failure_code
                if failure_message is not None:
                    self._values["failure_message"] = failure_message
                if mdn_message_id is not None:
                    self._values["mdn_message_id"] = mdn_message_id
                if mdn_subject is not None:
                    self._values["mdn_subject"] = mdn_subject
                if message_subject is not None:
                    self._values["message_subject"] = message_subject
                if s3_attributes is not None:
                    self._values["s3_attributes"] = s3_attributes
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code
                if transfer_id is not None:
                    self._values["transfer_id"] = transfer_id

            @builtins.property
            def as2_from(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-from property.

                Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_from")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_message_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-message-id property.

                Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_message_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_to(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-to property.

                Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_to")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def connector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connector-id property.

                Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Connector reference

                :stability: experimental
                '''
                result = self._values.get("connector_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def failure_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) failure-message property.

                Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("failure_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_message_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-message-id property.

                Specify an array of string values to match this event if the actual value of mdn-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_message_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_subject(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-subject property.

                Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_subject")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def message_subject(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) message-subject property.

                Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("message_subject")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_attributes(
                self,
            ) -> typing.Optional["ConnectorEvents.AS2MDNReceiveFailed.S3Attributes"]:
                '''(experimental) s3-attributes property.

                Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_attributes")
                return typing.cast(typing.Optional["ConnectorEvents.AS2MDNReceiveFailed.S3Attributes"], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transfer_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) transfer-id property.

                Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transfer_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AS2MDNReceiveFailedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.AS2MDNReceiveFailed.S3Attributes",
            jsii_struct_bases=[],
            name_mapping={
                "file_bucket": "fileBucket",
                "file_key": "fileKey",
                "json_bucket": "jsonBucket",
                "json_key": "jsonKey",
                "mdn_bucket": "mdnBucket",
                "mdn_key": "mdnKey",
            },
        )
        class S3Attributes:
            def __init__(
                self,
                *,
                file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_key: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for S3-attributes.

                :param file_bucket: (experimental) file-bucket property. Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_key: (experimental) file-key property. Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_bucket: (experimental) json-bucket property. Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_key: (experimental) json-key property. Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_bucket: (experimental) mdn-bucket property. Specify an array of string values to match this event if the actual value of mdn-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_key: (experimental) mdn-key property. Specify an array of string values to match this event if the actual value of mdn-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s3_attributes = transfer_events.ConnectorEvents.AS2MDNReceiveFailed.S3Attributes(
                        file_bucket=["fileBucket"],
                        file_key=["fileKey"],
                        json_bucket=["jsonBucket"],
                        json_key=["jsonKey"],
                        mdn_bucket=["mdnBucket"],
                        mdn_key=["mdnKey"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__066d15f0307471ade971ee67ef0635159ba1021693c3c0f2e6e2446b27f9cb43)
                    check_type(argname="argument file_bucket", value=file_bucket, expected_type=type_hints["file_bucket"])
                    check_type(argname="argument file_key", value=file_key, expected_type=type_hints["file_key"])
                    check_type(argname="argument json_bucket", value=json_bucket, expected_type=type_hints["json_bucket"])
                    check_type(argname="argument json_key", value=json_key, expected_type=type_hints["json_key"])
                    check_type(argname="argument mdn_bucket", value=mdn_bucket, expected_type=type_hints["mdn_bucket"])
                    check_type(argname="argument mdn_key", value=mdn_key, expected_type=type_hints["mdn_key"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if file_bucket is not None:
                    self._values["file_bucket"] = file_bucket
                if file_key is not None:
                    self._values["file_key"] = file_key
                if json_bucket is not None:
                    self._values["json_bucket"] = json_bucket
                if json_key is not None:
                    self._values["json_key"] = json_key
                if mdn_bucket is not None:
                    self._values["mdn_bucket"] = mdn_bucket
                if mdn_key is not None:
                    self._values["mdn_key"] = mdn_key

            @builtins.property
            def file_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-bucket property.

                Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-key property.

                Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-bucket property.

                Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-key property.

                Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-bucket property.

                Specify an array of string values to match this event if the actual value of mdn-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-key property.

                Specify an array of string values to match this event if the actual value of mdn-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "S3Attributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class AS2PayloadSendCompleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.AS2PayloadSendCompleted",
    ):
        '''(experimental) aws.transfer@AS2PayloadSendCompleted event types for Connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            a_s2_payload_send_completed = transfer_events.ConnectorEvents.AS2PayloadSendCompleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.AS2PayloadSendCompleted.AS2PayloadSendCompletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "as2_from": "as2From",
                "as2_message_id": "as2MessageId",
                "as2_to": "as2To",
                "bytes": "bytes",
                "connector_id": "connectorId",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "mdn_subject": "mdnSubject",
                "message_subject": "messageSubject",
                "requester_file_name": "requesterFileName",
                "s3_attributes": "s3Attributes",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
                "transfer_id": "transferId",
            },
        )
        class AS2PayloadSendCompletedProps:
            def __init__(
                self,
                *,
                as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
                bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
                connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
                message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
                requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_attributes: typing.Optional[typing.Union["ConnectorEvents.AS2PayloadSendCompleted.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Connector aws.transfer@AS2PayloadSendCompleted event.

                :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param mdn_subject: (experimental) mdn-subject property. Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param message_subject: (experimental) message-subject property. Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester_file_name: (experimental) requester-file-name property. Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    a_s2_payload_send_completed_props = transfer_events.ConnectorEvents.AS2PayloadSendCompleted.AS2PayloadSendCompletedProps(
                        as2_from=["as2From"],
                        as2_message_id=["as2MessageId"],
                        as2_to=["as2To"],
                        bytes=["bytes"],
                        connector_id=["connectorId"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        mdn_subject=["mdnSubject"],
                        message_subject=["messageSubject"],
                        requester_file_name=["requesterFileName"],
                        s3_attributes=transfer_events.ConnectorEvents.AS2PayloadSendCompleted.S3Attributes(
                            file_bucket=["fileBucket"],
                            file_key=["fileKey"],
                            json_bucket=["jsonBucket"],
                            json_key=["jsonKey"],
                            mdn_bucket=["mdnBucket"],
                            mdn_key=["mdnKey"]
                        ),
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"],
                        transfer_id=["transferId"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(s3_attributes, dict):
                    s3_attributes = ConnectorEvents.AS2PayloadSendCompleted.S3Attributes(**s3_attributes)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__01f05edc97d5ecc89ff6014fc829afc57ca2cb5758796bd5487f3b7e9715029f)
                    check_type(argname="argument as2_from", value=as2_from, expected_type=type_hints["as2_from"])
                    check_type(argname="argument as2_message_id", value=as2_message_id, expected_type=type_hints["as2_message_id"])
                    check_type(argname="argument as2_to", value=as2_to, expected_type=type_hints["as2_to"])
                    check_type(argname="argument bytes", value=bytes, expected_type=type_hints["bytes"])
                    check_type(argname="argument connector_id", value=connector_id, expected_type=type_hints["connector_id"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument mdn_subject", value=mdn_subject, expected_type=type_hints["mdn_subject"])
                    check_type(argname="argument message_subject", value=message_subject, expected_type=type_hints["message_subject"])
                    check_type(argname="argument requester_file_name", value=requester_file_name, expected_type=type_hints["requester_file_name"])
                    check_type(argname="argument s3_attributes", value=s3_attributes, expected_type=type_hints["s3_attributes"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument transfer_id", value=transfer_id, expected_type=type_hints["transfer_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if as2_from is not None:
                    self._values["as2_from"] = as2_from
                if as2_message_id is not None:
                    self._values["as2_message_id"] = as2_message_id
                if as2_to is not None:
                    self._values["as2_to"] = as2_to
                if bytes is not None:
                    self._values["bytes"] = bytes
                if connector_id is not None:
                    self._values["connector_id"] = connector_id
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if mdn_subject is not None:
                    self._values["mdn_subject"] = mdn_subject
                if message_subject is not None:
                    self._values["message_subject"] = message_subject
                if requester_file_name is not None:
                    self._values["requester_file_name"] = requester_file_name
                if s3_attributes is not None:
                    self._values["s3_attributes"] = s3_attributes
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code
                if transfer_id is not None:
                    self._values["transfer_id"] = transfer_id

            @builtins.property
            def as2_from(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-from property.

                Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_from")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_message_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-message-id property.

                Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_message_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_to(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-to property.

                Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_to")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def bytes(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bytes property.

                Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bytes")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def connector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connector-id property.

                Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Connector reference

                :stability: experimental
                '''
                result = self._values.get("connector_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def mdn_subject(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-subject property.

                Specify an array of string values to match this event if the actual value of mdn-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_subject")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def message_subject(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) message-subject property.

                Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("message_subject")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def requester_file_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester-file-name property.

                Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester_file_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_attributes(
                self,
            ) -> typing.Optional["ConnectorEvents.AS2PayloadSendCompleted.S3Attributes"]:
                '''(experimental) s3-attributes property.

                Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_attributes")
                return typing.cast(typing.Optional["ConnectorEvents.AS2PayloadSendCompleted.S3Attributes"], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transfer_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) transfer-id property.

                Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transfer_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AS2PayloadSendCompletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.AS2PayloadSendCompleted.S3Attributes",
            jsii_struct_bases=[],
            name_mapping={
                "file_bucket": "fileBucket",
                "file_key": "fileKey",
                "json_bucket": "jsonBucket",
                "json_key": "jsonKey",
                "mdn_bucket": "mdnBucket",
                "mdn_key": "mdnKey",
            },
        )
        class S3Attributes:
            def __init__(
                self,
                *,
                file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                mdn_key: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for S3-attributes.

                :param file_bucket: (experimental) file-bucket property. Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_key: (experimental) file-key property. Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_bucket: (experimental) json-bucket property. Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_key: (experimental) json-key property. Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_bucket: (experimental) mdn-bucket property. Specify an array of string values to match this event if the actual value of mdn-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mdn_key: (experimental) mdn-key property. Specify an array of string values to match this event if the actual value of mdn-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s3_attributes = transfer_events.ConnectorEvents.AS2PayloadSendCompleted.S3Attributes(
                        file_bucket=["fileBucket"],
                        file_key=["fileKey"],
                        json_bucket=["jsonBucket"],
                        json_key=["jsonKey"],
                        mdn_bucket=["mdnBucket"],
                        mdn_key=["mdnKey"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__568351db39d8364f8b693403c19a285fd4895c7cf1f9581d65e21c2e5d80546a)
                    check_type(argname="argument file_bucket", value=file_bucket, expected_type=type_hints["file_bucket"])
                    check_type(argname="argument file_key", value=file_key, expected_type=type_hints["file_key"])
                    check_type(argname="argument json_bucket", value=json_bucket, expected_type=type_hints["json_bucket"])
                    check_type(argname="argument json_key", value=json_key, expected_type=type_hints["json_key"])
                    check_type(argname="argument mdn_bucket", value=mdn_bucket, expected_type=type_hints["mdn_bucket"])
                    check_type(argname="argument mdn_key", value=mdn_key, expected_type=type_hints["mdn_key"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if file_bucket is not None:
                    self._values["file_bucket"] = file_bucket
                if file_key is not None:
                    self._values["file_key"] = file_key
                if json_bucket is not None:
                    self._values["json_bucket"] = json_bucket
                if json_key is not None:
                    self._values["json_key"] = json_key
                if mdn_bucket is not None:
                    self._values["mdn_bucket"] = mdn_bucket
                if mdn_key is not None:
                    self._values["mdn_key"] = mdn_key

            @builtins.property
            def file_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-bucket property.

                Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-key property.

                Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-bucket property.

                Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-key property.

                Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-bucket property.

                Specify an array of string values to match this event if the actual value of mdn-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mdn_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mdn-key property.

                Specify an array of string values to match this event if the actual value of mdn-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mdn_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "S3Attributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class AS2PayloadSendFailed(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.AS2PayloadSendFailed",
    ):
        '''(experimental) aws.transfer@AS2PayloadSendFailed event types for Connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            a_s2_payload_send_failed = transfer_events.ConnectorEvents.AS2PayloadSendFailed()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.AS2PayloadSendFailed.AS2PayloadSendFailedProps",
            jsii_struct_bases=[],
            name_mapping={
                "as2_from": "as2From",
                "as2_message_id": "as2MessageId",
                "as2_to": "as2To",
                "bytes": "bytes",
                "connector_id": "connectorId",
                "event_metadata": "eventMetadata",
                "failure_code": "failureCode",
                "failure_message": "failureMessage",
                "message_subject": "messageSubject",
                "requester_file_name": "requesterFileName",
                "s3_attributes": "s3Attributes",
                "status_code": "statusCode",
                "transfer_id": "transferId",
            },
        )
        class AS2PayloadSendFailedProps:
            def __init__(
                self,
                *,
                as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
                bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
                connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
                requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_attributes: typing.Optional[typing.Union["ConnectorEvents.AS2PayloadSendFailed.S3Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Connector aws.transfer@AS2PayloadSendFailed event.

                :param as2_from: (experimental) as2-from property. Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_message_id: (experimental) as2-message-id property. Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param as2_to: (experimental) as2-to property. Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param message_subject: (experimental) message-subject property. Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester_file_name: (experimental) requester-file-name property. Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_attributes: (experimental) s3-attributes property. Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    a_s2_payload_send_failed_props = transfer_events.ConnectorEvents.AS2PayloadSendFailed.AS2PayloadSendFailedProps(
                        as2_from=["as2From"],
                        as2_message_id=["as2MessageId"],
                        as2_to=["as2To"],
                        bytes=["bytes"],
                        connector_id=["connectorId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        failure_code=["failureCode"],
                        failure_message=["failureMessage"],
                        message_subject=["messageSubject"],
                        requester_file_name=["requesterFileName"],
                        s3_attributes=transfer_events.ConnectorEvents.AS2PayloadSendFailed.S3Attributes(
                            file_bucket=["fileBucket"],
                            file_key=["fileKey"],
                            json_bucket=["jsonBucket"],
                            json_key=["jsonKey"]
                        ),
                        status_code=["statusCode"],
                        transfer_id=["transferId"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(s3_attributes, dict):
                    s3_attributes = ConnectorEvents.AS2PayloadSendFailed.S3Attributes(**s3_attributes)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__acb30fb66551b418cdfb94d488501d33f3852029de425d4c701d68626a7f9670)
                    check_type(argname="argument as2_from", value=as2_from, expected_type=type_hints["as2_from"])
                    check_type(argname="argument as2_message_id", value=as2_message_id, expected_type=type_hints["as2_message_id"])
                    check_type(argname="argument as2_to", value=as2_to, expected_type=type_hints["as2_to"])
                    check_type(argname="argument bytes", value=bytes, expected_type=type_hints["bytes"])
                    check_type(argname="argument connector_id", value=connector_id, expected_type=type_hints["connector_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument failure_code", value=failure_code, expected_type=type_hints["failure_code"])
                    check_type(argname="argument failure_message", value=failure_message, expected_type=type_hints["failure_message"])
                    check_type(argname="argument message_subject", value=message_subject, expected_type=type_hints["message_subject"])
                    check_type(argname="argument requester_file_name", value=requester_file_name, expected_type=type_hints["requester_file_name"])
                    check_type(argname="argument s3_attributes", value=s3_attributes, expected_type=type_hints["s3_attributes"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument transfer_id", value=transfer_id, expected_type=type_hints["transfer_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if as2_from is not None:
                    self._values["as2_from"] = as2_from
                if as2_message_id is not None:
                    self._values["as2_message_id"] = as2_message_id
                if as2_to is not None:
                    self._values["as2_to"] = as2_to
                if bytes is not None:
                    self._values["bytes"] = bytes
                if connector_id is not None:
                    self._values["connector_id"] = connector_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if failure_code is not None:
                    self._values["failure_code"] = failure_code
                if failure_message is not None:
                    self._values["failure_message"] = failure_message
                if message_subject is not None:
                    self._values["message_subject"] = message_subject
                if requester_file_name is not None:
                    self._values["requester_file_name"] = requester_file_name
                if s3_attributes is not None:
                    self._values["s3_attributes"] = s3_attributes
                if status_code is not None:
                    self._values["status_code"] = status_code
                if transfer_id is not None:
                    self._values["transfer_id"] = transfer_id

            @builtins.property
            def as2_from(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-from property.

                Specify an array of string values to match this event if the actual value of as2-from is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_from")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_message_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-message-id property.

                Specify an array of string values to match this event if the actual value of as2-message-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_message_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def as2_to(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) as2-to property.

                Specify an array of string values to match this event if the actual value of as2-to is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("as2_to")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def bytes(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bytes property.

                Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bytes")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def connector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connector-id property.

                Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Connector reference

                :stability: experimental
                '''
                result = self._values.get("connector_id")
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
            def failure_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) failure-message property.

                Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("failure_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def message_subject(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) message-subject property.

                Specify an array of string values to match this event if the actual value of message-subject is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("message_subject")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def requester_file_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requester-file-name property.

                Specify an array of string values to match this event if the actual value of requester-file-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester_file_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_attributes(
                self,
            ) -> typing.Optional["ConnectorEvents.AS2PayloadSendFailed.S3Attributes"]:
                '''(experimental) s3-attributes property.

                Specify an array of string values to match this event if the actual value of s3-attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_attributes")
                return typing.cast(typing.Optional["ConnectorEvents.AS2PayloadSendFailed.S3Attributes"], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transfer_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) transfer-id property.

                Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transfer_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AS2PayloadSendFailedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.AS2PayloadSendFailed.S3Attributes",
            jsii_struct_bases=[],
            name_mapping={
                "file_bucket": "fileBucket",
                "file_key": "fileKey",
                "json_bucket": "jsonBucket",
                "json_key": "jsonKey",
            },
        )
        class S3Attributes:
            def __init__(
                self,
                *,
                file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for S3-attributes.

                :param file_bucket: (experimental) file-bucket property. Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_key: (experimental) file-key property. Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_bucket: (experimental) json-bucket property. Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param json_key: (experimental) json-key property. Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s3_attributes = transfer_events.ConnectorEvents.AS2PayloadSendFailed.S3Attributes(
                        file_bucket=["fileBucket"],
                        file_key=["fileKey"],
                        json_bucket=["jsonBucket"],
                        json_key=["jsonKey"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ba86421f85267cbc9ea80e0174f08b7028a8aee5b5e5164105f2b2e55adde308)
                    check_type(argname="argument file_bucket", value=file_bucket, expected_type=type_hints["file_bucket"])
                    check_type(argname="argument file_key", value=file_key, expected_type=type_hints["file_key"])
                    check_type(argname="argument json_bucket", value=json_bucket, expected_type=type_hints["json_bucket"])
                    check_type(argname="argument json_key", value=json_key, expected_type=type_hints["json_key"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if file_bucket is not None:
                    self._values["file_bucket"] = file_bucket
                if file_key is not None:
                    self._values["file_key"] = file_key
                if json_bucket is not None:
                    self._values["json_bucket"] = json_bucket
                if json_key is not None:
                    self._values["json_key"] = json_key

            @builtins.property
            def file_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-bucket property.

                Specify an array of string values to match this event if the actual value of file-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-key property.

                Specify an array of string values to match this event if the actual value of file-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-bucket property.

                Specify an array of string values to match this event if the actual value of json-bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def json_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) json-key property.

                Specify an array of string values to match this event if the actual value of json-key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("json_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "S3Attributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class SFTPConnectorDirectoryListingCompleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorDirectoryListingCompleted",
    ):
        '''(experimental) aws.transfer@SFTPConnectorDirectoryListingCompleted event types for Connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            s_fTPConnector_directory_listing_completed = transfer_events.ConnectorEvents.SFTPConnectorDirectoryListingCompleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorDirectoryListingCompleted.OutputFileLocation",
            jsii_struct_bases=[],
            name_mapping={"bucket": "bucket", "domain": "domain", "key": "key"},
        )
        class OutputFileLocation:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                domain: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Output-file-location.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain: (experimental) domain property. Specify an array of string values to match this event if the actual value of domain is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    output_file_location = transfer_events.ConnectorEvents.SFTPConnectorDirectoryListingCompleted.OutputFileLocation(
                        bucket=["bucket"],
                        domain=["domain"],
                        key=["key"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cfd0f2ccad9fa006f3cbdd5db1b9d19150e054575a460fe3678463e24c91fdda)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if domain is not None:
                    self._values["domain"] = domain
                if key is not None:
                    self._values["key"] = key

            @builtins.property
            def bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def domain(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domain property.

                Specify an array of string values to match this event if the actual value of domain is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("domain")
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

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "OutputFileLocation(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorDirectoryListingCompleted.SFTPConnectorDirectoryListingCompletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "connector_id": "connectorId",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "item_count": "itemCount",
                "listing_id": "listingId",
                "max_items": "maxItems",
                "output_directory_path": "outputDirectoryPath",
                "output_file_location": "outputFileLocation",
                "remote_directory_path": "remoteDirectoryPath",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
                "truncated": "truncated",
                "url": "url",
            },
        )
        class SFTPConnectorDirectoryListingCompletedProps:
            def __init__(
                self,
                *,
                connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                item_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                listing_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                max_items: typing.Optional[typing.Sequence[builtins.str]] = None,
                output_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                output_file_location: typing.Optional[typing.Union["ConnectorEvents.SFTPConnectorDirectoryListingCompleted.OutputFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
                remote_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                truncated: typing.Optional[typing.Sequence[builtins.str]] = None,
                url: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Connector aws.transfer@SFTPConnectorDirectoryListingCompleted event.

                :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param item_count: (experimental) item-count property. Specify an array of string values to match this event if the actual value of item-count is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param listing_id: (experimental) listing-id property. Specify an array of string values to match this event if the actual value of listing-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param max_items: (experimental) max-items property. Specify an array of string values to match this event if the actual value of max-items is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param output_directory_path: (experimental) output-directory-path property. Specify an array of string values to match this event if the actual value of output-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param output_file_location: (experimental) output-file-location property. Specify an array of string values to match this event if the actual value of output-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param remote_directory_path: (experimental) remote-directory-path property. Specify an array of string values to match this event if the actual value of remote-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param truncated: (experimental) truncated property. Specify an array of string values to match this event if the actual value of truncated is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s_fTPConnector_directory_listing_completed_props = transfer_events.ConnectorEvents.SFTPConnectorDirectoryListingCompleted.SFTPConnectorDirectoryListingCompletedProps(
                        connector_id=["connectorId"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        item_count=["itemCount"],
                        listing_id=["listingId"],
                        max_items=["maxItems"],
                        output_directory_path=["outputDirectoryPath"],
                        output_file_location=transfer_events.ConnectorEvents.SFTPConnectorDirectoryListingCompleted.OutputFileLocation(
                            bucket=["bucket"],
                            domain=["domain"],
                            key=["key"]
                        ),
                        remote_directory_path=["remoteDirectoryPath"],
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"],
                        truncated=["truncated"],
                        url=["url"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(output_file_location, dict):
                    output_file_location = ConnectorEvents.SFTPConnectorDirectoryListingCompleted.OutputFileLocation(**output_file_location)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__75bbe3081a8041bce6feabddccbe2fb3464d03a3d08d687dd36d07209138fdd0)
                    check_type(argname="argument connector_id", value=connector_id, expected_type=type_hints["connector_id"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument item_count", value=item_count, expected_type=type_hints["item_count"])
                    check_type(argname="argument listing_id", value=listing_id, expected_type=type_hints["listing_id"])
                    check_type(argname="argument max_items", value=max_items, expected_type=type_hints["max_items"])
                    check_type(argname="argument output_directory_path", value=output_directory_path, expected_type=type_hints["output_directory_path"])
                    check_type(argname="argument output_file_location", value=output_file_location, expected_type=type_hints["output_file_location"])
                    check_type(argname="argument remote_directory_path", value=remote_directory_path, expected_type=type_hints["remote_directory_path"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument truncated", value=truncated, expected_type=type_hints["truncated"])
                    check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if connector_id is not None:
                    self._values["connector_id"] = connector_id
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if item_count is not None:
                    self._values["item_count"] = item_count
                if listing_id is not None:
                    self._values["listing_id"] = listing_id
                if max_items is not None:
                    self._values["max_items"] = max_items
                if output_directory_path is not None:
                    self._values["output_directory_path"] = output_directory_path
                if output_file_location is not None:
                    self._values["output_file_location"] = output_file_location
                if remote_directory_path is not None:
                    self._values["remote_directory_path"] = remote_directory_path
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code
                if truncated is not None:
                    self._values["truncated"] = truncated
                if url is not None:
                    self._values["url"] = url

            @builtins.property
            def connector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connector-id property.

                Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Connector reference

                :stability: experimental
                '''
                result = self._values.get("connector_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def item_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) item-count property.

                Specify an array of string values to match this event if the actual value of item-count is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("item_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def listing_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) listing-id property.

                Specify an array of string values to match this event if the actual value of listing-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("listing_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def max_items(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) max-items property.

                Specify an array of string values to match this event if the actual value of max-items is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("max_items")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def output_directory_path(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) output-directory-path property.

                Specify an array of string values to match this event if the actual value of output-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("output_directory_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def output_file_location(
                self,
            ) -> typing.Optional["ConnectorEvents.SFTPConnectorDirectoryListingCompleted.OutputFileLocation"]:
                '''(experimental) output-file-location property.

                Specify an array of string values to match this event if the actual value of output-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("output_file_location")
                return typing.cast(typing.Optional["ConnectorEvents.SFTPConnectorDirectoryListingCompleted.OutputFileLocation"], result)

            @builtins.property
            def remote_directory_path(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) remote-directory-path property.

                Specify an array of string values to match this event if the actual value of remote-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("remote_directory_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def truncated(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) truncated property.

                Specify an array of string values to match this event if the actual value of truncated is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("truncated")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def url(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) url property.

                Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("url")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SFTPConnectorDirectoryListingCompletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class SFTPConnectorDirectoryListingFailed(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorDirectoryListingFailed",
    ):
        '''(experimental) aws.transfer@SFTPConnectorDirectoryListingFailed event types for Connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            s_fTPConnector_directory_listing_failed = transfer_events.ConnectorEvents.SFTPConnectorDirectoryListingFailed()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorDirectoryListingFailed.SFTPConnectorDirectoryListingFailedProps",
            jsii_struct_bases=[],
            name_mapping={
                "connector_id": "connectorId",
                "event_metadata": "eventMetadata",
                "failure_code": "failureCode",
                "failure_message": "failureMessage",
                "listing_id": "listingId",
                "max_items": "maxItems",
                "output_directory_path": "outputDirectoryPath",
                "remote_directory_path": "remoteDirectoryPath",
                "status_code": "statusCode",
                "url": "url",
            },
        )
        class SFTPConnectorDirectoryListingFailedProps:
            def __init__(
                self,
                *,
                connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                listing_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                max_items: typing.Optional[typing.Sequence[builtins.str]] = None,
                output_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                remote_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                url: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Connector aws.transfer@SFTPConnectorDirectoryListingFailed event.

                :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param listing_id: (experimental) listing-id property. Specify an array of string values to match this event if the actual value of listing-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param max_items: (experimental) max-items property. Specify an array of string values to match this event if the actual value of max-items is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param output_directory_path: (experimental) output-directory-path property. Specify an array of string values to match this event if the actual value of output-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param remote_directory_path: (experimental) remote-directory-path property. Specify an array of string values to match this event if the actual value of remote-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s_fTPConnector_directory_listing_failed_props = transfer_events.ConnectorEvents.SFTPConnectorDirectoryListingFailed.SFTPConnectorDirectoryListingFailedProps(
                        connector_id=["connectorId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        failure_code=["failureCode"],
                        failure_message=["failureMessage"],
                        listing_id=["listingId"],
                        max_items=["maxItems"],
                        output_directory_path=["outputDirectoryPath"],
                        remote_directory_path=["remoteDirectoryPath"],
                        status_code=["statusCode"],
                        url=["url"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__93c4a77819ddfee95c88b5b5af7b6c34b5a25d6b7dc594436917abf0631cbee6)
                    check_type(argname="argument connector_id", value=connector_id, expected_type=type_hints["connector_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument failure_code", value=failure_code, expected_type=type_hints["failure_code"])
                    check_type(argname="argument failure_message", value=failure_message, expected_type=type_hints["failure_message"])
                    check_type(argname="argument listing_id", value=listing_id, expected_type=type_hints["listing_id"])
                    check_type(argname="argument max_items", value=max_items, expected_type=type_hints["max_items"])
                    check_type(argname="argument output_directory_path", value=output_directory_path, expected_type=type_hints["output_directory_path"])
                    check_type(argname="argument remote_directory_path", value=remote_directory_path, expected_type=type_hints["remote_directory_path"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if connector_id is not None:
                    self._values["connector_id"] = connector_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if failure_code is not None:
                    self._values["failure_code"] = failure_code
                if failure_message is not None:
                    self._values["failure_message"] = failure_message
                if listing_id is not None:
                    self._values["listing_id"] = listing_id
                if max_items is not None:
                    self._values["max_items"] = max_items
                if output_directory_path is not None:
                    self._values["output_directory_path"] = output_directory_path
                if remote_directory_path is not None:
                    self._values["remote_directory_path"] = remote_directory_path
                if status_code is not None:
                    self._values["status_code"] = status_code
                if url is not None:
                    self._values["url"] = url

            @builtins.property
            def connector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connector-id property.

                Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Connector reference

                :stability: experimental
                '''
                result = self._values.get("connector_id")
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
            def failure_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) failure-message property.

                Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("failure_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def listing_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) listing-id property.

                Specify an array of string values to match this event if the actual value of listing-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("listing_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def max_items(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) max-items property.

                Specify an array of string values to match this event if the actual value of max-items is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("max_items")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def output_directory_path(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) output-directory-path property.

                Specify an array of string values to match this event if the actual value of output-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("output_directory_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def remote_directory_path(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) remote-directory-path property.

                Specify an array of string values to match this event if the actual value of remote-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("remote_directory_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def url(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) url property.

                Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("url")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SFTPConnectorDirectoryListingFailedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class SFTPConnectorFileRetrieveCompleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorFileRetrieveCompleted",
    ):
        '''(experimental) aws.transfer@SFTPConnectorFileRetrieveCompleted event types for Connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            s_fTPConnector_file_retrieve_completed = transfer_events.ConnectorEvents.SFTPConnectorFileRetrieveCompleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorFileRetrieveCompleted.LocalFileLocation",
            jsii_struct_bases=[],
            name_mapping={"bucket": "bucket", "domain": "domain", "key": "key"},
        )
        class LocalFileLocation:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                domain: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Local-file-location.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain: (experimental) domain property. Specify an array of string values to match this event if the actual value of domain is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    local_file_location = transfer_events.ConnectorEvents.SFTPConnectorFileRetrieveCompleted.LocalFileLocation(
                        bucket=["bucket"],
                        domain=["domain"],
                        key=["key"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__10cb367321f098d111c4c39d0581feecf922e241fa2663c0d8d6d1a7bb29fbfc)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if domain is not None:
                    self._values["domain"] = domain
                if key is not None:
                    self._values["key"] = key

            @builtins.property
            def bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def domain(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domain property.

                Specify an array of string values to match this event if the actual value of domain is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("domain")
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

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "LocalFileLocation(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorFileRetrieveCompleted.SFTPConnectorFileRetrieveCompletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "bytes": "bytes",
                "connector_id": "connectorId",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "file_path": "filePath",
                "file_transfer_id": "fileTransferId",
                "local_directory_path": "localDirectoryPath",
                "local_file_location": "localFileLocation",
                "operation": "operation",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
                "transfer_id": "transferId",
                "url": "url",
            },
        )
        class SFTPConnectorFileRetrieveCompletedProps:
            def __init__(
                self,
                *,
                bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
                connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                local_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                local_file_location: typing.Optional[typing.Union["ConnectorEvents.SFTPConnectorFileRetrieveCompleted.LocalFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
                operation: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                url: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Connector aws.transfer@SFTPConnectorFileRetrieveCompleted event.

                :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param file_path: (experimental) file-path property. Specify an array of string values to match this event if the actual value of file-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_transfer_id: (experimental) file-transfer-id property. Specify an array of string values to match this event if the actual value of file-transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param local_directory_path: (experimental) local-directory-path property. Specify an array of string values to match this event if the actual value of local-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param local_file_location: (experimental) local-file-location property. Specify an array of string values to match this event if the actual value of local-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s_fTPConnector_file_retrieve_completed_props = transfer_events.ConnectorEvents.SFTPConnectorFileRetrieveCompleted.SFTPConnectorFileRetrieveCompletedProps(
                        bytes=["bytes"],
                        connector_id=["connectorId"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        file_path=["filePath"],
                        file_transfer_id=["fileTransferId"],
                        local_directory_path=["localDirectoryPath"],
                        local_file_location=transfer_events.ConnectorEvents.SFTPConnectorFileRetrieveCompleted.LocalFileLocation(
                            bucket=["bucket"],
                            domain=["domain"],
                            key=["key"]
                        ),
                        operation=["operation"],
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"],
                        transfer_id=["transferId"],
                        url=["url"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(local_file_location, dict):
                    local_file_location = ConnectorEvents.SFTPConnectorFileRetrieveCompleted.LocalFileLocation(**local_file_location)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cbdd4245563e0e6f16aea380d8bf2213e573a4ca6f3f669ff257c861243259d8)
                    check_type(argname="argument bytes", value=bytes, expected_type=type_hints["bytes"])
                    check_type(argname="argument connector_id", value=connector_id, expected_type=type_hints["connector_id"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
                    check_type(argname="argument file_transfer_id", value=file_transfer_id, expected_type=type_hints["file_transfer_id"])
                    check_type(argname="argument local_directory_path", value=local_directory_path, expected_type=type_hints["local_directory_path"])
                    check_type(argname="argument local_file_location", value=local_file_location, expected_type=type_hints["local_file_location"])
                    check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument transfer_id", value=transfer_id, expected_type=type_hints["transfer_id"])
                    check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bytes is not None:
                    self._values["bytes"] = bytes
                if connector_id is not None:
                    self._values["connector_id"] = connector_id
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if file_path is not None:
                    self._values["file_path"] = file_path
                if file_transfer_id is not None:
                    self._values["file_transfer_id"] = file_transfer_id
                if local_directory_path is not None:
                    self._values["local_directory_path"] = local_directory_path
                if local_file_location is not None:
                    self._values["local_file_location"] = local_file_location
                if operation is not None:
                    self._values["operation"] = operation
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code
                if transfer_id is not None:
                    self._values["transfer_id"] = transfer_id
                if url is not None:
                    self._values["url"] = url

            @builtins.property
            def bytes(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bytes property.

                Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bytes")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def connector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connector-id property.

                Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Connector reference

                :stability: experimental
                '''
                result = self._values.get("connector_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def file_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-path property.

                Specify an array of string values to match this event if the actual value of file-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_transfer_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-transfer-id property.

                Specify an array of string values to match this event if the actual value of file-transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_transfer_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def local_directory_path(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) local-directory-path property.

                Specify an array of string values to match this event if the actual value of local-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("local_directory_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def local_file_location(
                self,
            ) -> typing.Optional["ConnectorEvents.SFTPConnectorFileRetrieveCompleted.LocalFileLocation"]:
                '''(experimental) local-file-location property.

                Specify an array of string values to match this event if the actual value of local-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("local_file_location")
                return typing.cast(typing.Optional["ConnectorEvents.SFTPConnectorFileRetrieveCompleted.LocalFileLocation"], result)

            @builtins.property
            def operation(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) operation property.

                Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("operation")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transfer_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) transfer-id property.

                Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transfer_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def url(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) url property.

                Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("url")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SFTPConnectorFileRetrieveCompletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class SFTPConnectorFileRetrieveFailed(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorFileRetrieveFailed",
    ):
        '''(experimental) aws.transfer@SFTPConnectorFileRetrieveFailed event types for Connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            s_fTPConnector_file_retrieve_failed = transfer_events.ConnectorEvents.SFTPConnectorFileRetrieveFailed()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorFileRetrieveFailed.LocalFileLocation",
            jsii_struct_bases=[],
            name_mapping={"bucket": "bucket", "domain": "domain", "key": "key"},
        )
        class LocalFileLocation:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                domain: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Local-file-location.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain: (experimental) domain property. Specify an array of string values to match this event if the actual value of domain is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    local_file_location = transfer_events.ConnectorEvents.SFTPConnectorFileRetrieveFailed.LocalFileLocation(
                        bucket=["bucket"],
                        domain=["domain"],
                        key=["key"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a9e5b5081c2f67237e143cae1eea2f2309dae8883ac1163209058da3a71bb971)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if domain is not None:
                    self._values["domain"] = domain
                if key is not None:
                    self._values["key"] = key

            @builtins.property
            def bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def domain(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domain property.

                Specify an array of string values to match this event if the actual value of domain is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("domain")
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

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "LocalFileLocation(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorFileRetrieveFailed.SFTPConnectorFileRetrieveFailedProps",
            jsii_struct_bases=[],
            name_mapping={
                "bytes": "bytes",
                "connector_id": "connectorId",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "failure_code": "failureCode",
                "failure_message": "failureMessage",
                "file_path": "filePath",
                "file_transfer_id": "fileTransferId",
                "local_directory_path": "localDirectoryPath",
                "local_file_location": "localFileLocation",
                "operation": "operation",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
                "transfer_id": "transferId",
                "url": "url",
            },
        )
        class SFTPConnectorFileRetrieveFailedProps:
            def __init__(
                self,
                *,
                bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
                connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                local_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                local_file_location: typing.Optional[typing.Union["ConnectorEvents.SFTPConnectorFileRetrieveFailed.LocalFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
                operation: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                url: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Connector aws.transfer@SFTPConnectorFileRetrieveFailed event.

                :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_path: (experimental) file-path property. Specify an array of string values to match this event if the actual value of file-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_transfer_id: (experimental) file-transfer-id property. Specify an array of string values to match this event if the actual value of file-transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param local_directory_path: (experimental) local-directory-path property. Specify an array of string values to match this event if the actual value of local-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param local_file_location: (experimental) local-file-location property. Specify an array of string values to match this event if the actual value of local-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s_fTPConnector_file_retrieve_failed_props = transfer_events.ConnectorEvents.SFTPConnectorFileRetrieveFailed.SFTPConnectorFileRetrieveFailedProps(
                        bytes=["bytes"],
                        connector_id=["connectorId"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        failure_code=["failureCode"],
                        failure_message=["failureMessage"],
                        file_path=["filePath"],
                        file_transfer_id=["fileTransferId"],
                        local_directory_path=["localDirectoryPath"],
                        local_file_location=transfer_events.ConnectorEvents.SFTPConnectorFileRetrieveFailed.LocalFileLocation(
                            bucket=["bucket"],
                            domain=["domain"],
                            key=["key"]
                        ),
                        operation=["operation"],
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"],
                        transfer_id=["transferId"],
                        url=["url"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(local_file_location, dict):
                    local_file_location = ConnectorEvents.SFTPConnectorFileRetrieveFailed.LocalFileLocation(**local_file_location)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__12a66b3d602d37137a1f3e1f5a6f806315d3c7c1f18062e18755b50d000c5867)
                    check_type(argname="argument bytes", value=bytes, expected_type=type_hints["bytes"])
                    check_type(argname="argument connector_id", value=connector_id, expected_type=type_hints["connector_id"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument failure_code", value=failure_code, expected_type=type_hints["failure_code"])
                    check_type(argname="argument failure_message", value=failure_message, expected_type=type_hints["failure_message"])
                    check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
                    check_type(argname="argument file_transfer_id", value=file_transfer_id, expected_type=type_hints["file_transfer_id"])
                    check_type(argname="argument local_directory_path", value=local_directory_path, expected_type=type_hints["local_directory_path"])
                    check_type(argname="argument local_file_location", value=local_file_location, expected_type=type_hints["local_file_location"])
                    check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument transfer_id", value=transfer_id, expected_type=type_hints["transfer_id"])
                    check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bytes is not None:
                    self._values["bytes"] = bytes
                if connector_id is not None:
                    self._values["connector_id"] = connector_id
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if failure_code is not None:
                    self._values["failure_code"] = failure_code
                if failure_message is not None:
                    self._values["failure_message"] = failure_message
                if file_path is not None:
                    self._values["file_path"] = file_path
                if file_transfer_id is not None:
                    self._values["file_transfer_id"] = file_transfer_id
                if local_directory_path is not None:
                    self._values["local_directory_path"] = local_directory_path
                if local_file_location is not None:
                    self._values["local_file_location"] = local_file_location
                if operation is not None:
                    self._values["operation"] = operation
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code
                if transfer_id is not None:
                    self._values["transfer_id"] = transfer_id
                if url is not None:
                    self._values["url"] = url

            @builtins.property
            def bytes(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bytes property.

                Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bytes")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def connector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connector-id property.

                Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Connector reference

                :stability: experimental
                '''
                result = self._values.get("connector_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def failure_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) failure-message property.

                Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("failure_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-path property.

                Specify an array of string values to match this event if the actual value of file-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_transfer_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-transfer-id property.

                Specify an array of string values to match this event if the actual value of file-transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_transfer_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def local_directory_path(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) local-directory-path property.

                Specify an array of string values to match this event if the actual value of local-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("local_directory_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def local_file_location(
                self,
            ) -> typing.Optional["ConnectorEvents.SFTPConnectorFileRetrieveFailed.LocalFileLocation"]:
                '''(experimental) local-file-location property.

                Specify an array of string values to match this event if the actual value of local-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("local_file_location")
                return typing.cast(typing.Optional["ConnectorEvents.SFTPConnectorFileRetrieveFailed.LocalFileLocation"], result)

            @builtins.property
            def operation(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) operation property.

                Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("operation")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transfer_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) transfer-id property.

                Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transfer_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def url(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) url property.

                Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("url")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SFTPConnectorFileRetrieveFailedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class SFTPConnectorFileSendCompleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorFileSendCompleted",
    ):
        '''(experimental) aws.transfer@SFTPConnectorFileSendCompleted event types for Connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            s_fTPConnector_file_send_completed = transfer_events.ConnectorEvents.SFTPConnectorFileSendCompleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorFileSendCompleted.LocalFileLocation",
            jsii_struct_bases=[],
            name_mapping={"bucket": "bucket", "domain": "domain", "key": "key"},
        )
        class LocalFileLocation:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                domain: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Local-file-location.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain: (experimental) domain property. Specify an array of string values to match this event if the actual value of domain is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    local_file_location = transfer_events.ConnectorEvents.SFTPConnectorFileSendCompleted.LocalFileLocation(
                        bucket=["bucket"],
                        domain=["domain"],
                        key=["key"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__e4a0201ab895f38d1e133276180a6de997ad7ba383aa4de01ba9811676dae7c4)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if domain is not None:
                    self._values["domain"] = domain
                if key is not None:
                    self._values["key"] = key

            @builtins.property
            def bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def domain(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domain property.

                Specify an array of string values to match this event if the actual value of domain is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("domain")
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

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "LocalFileLocation(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorFileSendCompleted.SFTPConnectorFileSendCompletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "bytes": "bytes",
                "connector_id": "connectorId",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "file_path": "filePath",
                "file_transfer_id": "fileTransferId",
                "local_file_location": "localFileLocation",
                "operation": "operation",
                "remote_directory_path": "remoteDirectoryPath",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
                "transfer_id": "transferId",
                "url": "url",
            },
        )
        class SFTPConnectorFileSendCompletedProps:
            def __init__(
                self,
                *,
                bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
                connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                local_file_location: typing.Optional[typing.Union["ConnectorEvents.SFTPConnectorFileSendCompleted.LocalFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
                operation: typing.Optional[typing.Sequence[builtins.str]] = None,
                remote_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                url: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Connector aws.transfer@SFTPConnectorFileSendCompleted event.

                :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param file_path: (experimental) file-path property. Specify an array of string values to match this event if the actual value of file-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_transfer_id: (experimental) file-transfer-id property. Specify an array of string values to match this event if the actual value of file-transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param local_file_location: (experimental) local-file-location property. Specify an array of string values to match this event if the actual value of local-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param remote_directory_path: (experimental) remote-directory-path property. Specify an array of string values to match this event if the actual value of remote-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s_fTPConnector_file_send_completed_props = transfer_events.ConnectorEvents.SFTPConnectorFileSendCompleted.SFTPConnectorFileSendCompletedProps(
                        bytes=["bytes"],
                        connector_id=["connectorId"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        file_path=["filePath"],
                        file_transfer_id=["fileTransferId"],
                        local_file_location=transfer_events.ConnectorEvents.SFTPConnectorFileSendCompleted.LocalFileLocation(
                            bucket=["bucket"],
                            domain=["domain"],
                            key=["key"]
                        ),
                        operation=["operation"],
                        remote_directory_path=["remoteDirectoryPath"],
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"],
                        transfer_id=["transferId"],
                        url=["url"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(local_file_location, dict):
                    local_file_location = ConnectorEvents.SFTPConnectorFileSendCompleted.LocalFileLocation(**local_file_location)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__431567d7ac3b1b5289b35b4d8ecfa7033bf4959579d5f348f77c47e16a9fa7d9)
                    check_type(argname="argument bytes", value=bytes, expected_type=type_hints["bytes"])
                    check_type(argname="argument connector_id", value=connector_id, expected_type=type_hints["connector_id"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
                    check_type(argname="argument file_transfer_id", value=file_transfer_id, expected_type=type_hints["file_transfer_id"])
                    check_type(argname="argument local_file_location", value=local_file_location, expected_type=type_hints["local_file_location"])
                    check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
                    check_type(argname="argument remote_directory_path", value=remote_directory_path, expected_type=type_hints["remote_directory_path"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument transfer_id", value=transfer_id, expected_type=type_hints["transfer_id"])
                    check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bytes is not None:
                    self._values["bytes"] = bytes
                if connector_id is not None:
                    self._values["connector_id"] = connector_id
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if file_path is not None:
                    self._values["file_path"] = file_path
                if file_transfer_id is not None:
                    self._values["file_transfer_id"] = file_transfer_id
                if local_file_location is not None:
                    self._values["local_file_location"] = local_file_location
                if operation is not None:
                    self._values["operation"] = operation
                if remote_directory_path is not None:
                    self._values["remote_directory_path"] = remote_directory_path
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code
                if transfer_id is not None:
                    self._values["transfer_id"] = transfer_id
                if url is not None:
                    self._values["url"] = url

            @builtins.property
            def bytes(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bytes property.

                Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bytes")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def connector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connector-id property.

                Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Connector reference

                :stability: experimental
                '''
                result = self._values.get("connector_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def file_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-path property.

                Specify an array of string values to match this event if the actual value of file-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_transfer_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-transfer-id property.

                Specify an array of string values to match this event if the actual value of file-transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_transfer_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def local_file_location(
                self,
            ) -> typing.Optional["ConnectorEvents.SFTPConnectorFileSendCompleted.LocalFileLocation"]:
                '''(experimental) local-file-location property.

                Specify an array of string values to match this event if the actual value of local-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("local_file_location")
                return typing.cast(typing.Optional["ConnectorEvents.SFTPConnectorFileSendCompleted.LocalFileLocation"], result)

            @builtins.property
            def operation(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) operation property.

                Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("operation")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def remote_directory_path(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) remote-directory-path property.

                Specify an array of string values to match this event if the actual value of remote-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("remote_directory_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transfer_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) transfer-id property.

                Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transfer_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def url(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) url property.

                Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("url")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SFTPConnectorFileSendCompletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class SFTPConnectorFileSendFailed(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorFileSendFailed",
    ):
        '''(experimental) aws.transfer@SFTPConnectorFileSendFailed event types for Connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            s_fTPConnector_file_send_failed = transfer_events.ConnectorEvents.SFTPConnectorFileSendFailed()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorFileSendFailed.LocalFileLocation",
            jsii_struct_bases=[],
            name_mapping={"bucket": "bucket", "domain": "domain", "key": "key"},
        )
        class LocalFileLocation:
            def __init__(
                self,
                *,
                bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                domain: typing.Optional[typing.Sequence[builtins.str]] = None,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Local-file-location.

                :param bucket: (experimental) bucket property. Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain: (experimental) domain property. Specify an array of string values to match this event if the actual value of domain is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    local_file_location = transfer_events.ConnectorEvents.SFTPConnectorFileSendFailed.LocalFileLocation(
                        bucket=["bucket"],
                        domain=["domain"],
                        key=["key"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8d9fb826a7cd00225e990a3021a5483ca7ec6c214c903a314732d4b8ae8b8d2e)
                    check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                    check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bucket is not None:
                    self._values["bucket"] = bucket
                if domain is not None:
                    self._values["domain"] = domain
                if key is not None:
                    self._values["key"] = key

            @builtins.property
            def bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bucket property.

                Specify an array of string values to match this event if the actual value of bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def domain(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domain property.

                Specify an array of string values to match this event if the actual value of domain is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("domain")
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

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "LocalFileLocation(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorFileSendFailed.SFTPConnectorFileSendFailedProps",
            jsii_struct_bases=[],
            name_mapping={
                "bytes": "bytes",
                "connector_id": "connectorId",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "failure_code": "failureCode",
                "failure_message": "failureMessage",
                "file_path": "filePath",
                "file_transfer_id": "fileTransferId",
                "local_file_location": "localFileLocation",
                "operation": "operation",
                "remote_directory_path": "remoteDirectoryPath",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
                "transfer_id": "transferId",
                "url": "url",
            },
        )
        class SFTPConnectorFileSendFailedProps:
            def __init__(
                self,
                *,
                bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
                connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                local_file_location: typing.Optional[typing.Union["ConnectorEvents.SFTPConnectorFileSendFailed.LocalFileLocation", typing.Dict[builtins.str, typing.Any]]] = None,
                operation: typing.Optional[typing.Sequence[builtins.str]] = None,
                remote_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                url: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Connector aws.transfer@SFTPConnectorFileSendFailed event.

                :param bytes: (experimental) bytes property. Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_path: (experimental) file-path property. Specify an array of string values to match this event if the actual value of file-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_transfer_id: (experimental) file-transfer-id property. Specify an array of string values to match this event if the actual value of file-transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param local_file_location: (experimental) local-file-location property. Specify an array of string values to match this event if the actual value of local-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param remote_directory_path: (experimental) remote-directory-path property. Specify an array of string values to match this event if the actual value of remote-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param transfer_id: (experimental) transfer-id property. Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s_fTPConnector_file_send_failed_props = transfer_events.ConnectorEvents.SFTPConnectorFileSendFailed.SFTPConnectorFileSendFailedProps(
                        bytes=["bytes"],
                        connector_id=["connectorId"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        failure_code=["failureCode"],
                        failure_message=["failureMessage"],
                        file_path=["filePath"],
                        file_transfer_id=["fileTransferId"],
                        local_file_location=transfer_events.ConnectorEvents.SFTPConnectorFileSendFailed.LocalFileLocation(
                            bucket=["bucket"],
                            domain=["domain"],
                            key=["key"]
                        ),
                        operation=["operation"],
                        remote_directory_path=["remoteDirectoryPath"],
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"],
                        transfer_id=["transferId"],
                        url=["url"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(local_file_location, dict):
                    local_file_location = ConnectorEvents.SFTPConnectorFileSendFailed.LocalFileLocation(**local_file_location)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cf488b4e9f13197d9ccff0299ffdbd9f9ffad4d472244be76e1899907dc79806)
                    check_type(argname="argument bytes", value=bytes, expected_type=type_hints["bytes"])
                    check_type(argname="argument connector_id", value=connector_id, expected_type=type_hints["connector_id"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument failure_code", value=failure_code, expected_type=type_hints["failure_code"])
                    check_type(argname="argument failure_message", value=failure_message, expected_type=type_hints["failure_message"])
                    check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
                    check_type(argname="argument file_transfer_id", value=file_transfer_id, expected_type=type_hints["file_transfer_id"])
                    check_type(argname="argument local_file_location", value=local_file_location, expected_type=type_hints["local_file_location"])
                    check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
                    check_type(argname="argument remote_directory_path", value=remote_directory_path, expected_type=type_hints["remote_directory_path"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument transfer_id", value=transfer_id, expected_type=type_hints["transfer_id"])
                    check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if bytes is not None:
                    self._values["bytes"] = bytes
                if connector_id is not None:
                    self._values["connector_id"] = connector_id
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if failure_code is not None:
                    self._values["failure_code"] = failure_code
                if failure_message is not None:
                    self._values["failure_message"] = failure_message
                if file_path is not None:
                    self._values["file_path"] = file_path
                if file_transfer_id is not None:
                    self._values["file_transfer_id"] = file_transfer_id
                if local_file_location is not None:
                    self._values["local_file_location"] = local_file_location
                if operation is not None:
                    self._values["operation"] = operation
                if remote_directory_path is not None:
                    self._values["remote_directory_path"] = remote_directory_path
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code
                if transfer_id is not None:
                    self._values["transfer_id"] = transfer_id
                if url is not None:
                    self._values["url"] = url

            @builtins.property
            def bytes(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) bytes property.

                Specify an array of string values to match this event if the actual value of bytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bytes")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def connector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connector-id property.

                Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Connector reference

                :stability: experimental
                '''
                result = self._values.get("connector_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def failure_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) failure-message property.

                Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("failure_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-path property.

                Specify an array of string values to match this event if the actual value of file-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_transfer_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) file-transfer-id property.

                Specify an array of string values to match this event if the actual value of file-transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_transfer_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def local_file_location(
                self,
            ) -> typing.Optional["ConnectorEvents.SFTPConnectorFileSendFailed.LocalFileLocation"]:
                '''(experimental) local-file-location property.

                Specify an array of string values to match this event if the actual value of local-file-location is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("local_file_location")
                return typing.cast(typing.Optional["ConnectorEvents.SFTPConnectorFileSendFailed.LocalFileLocation"], result)

            @builtins.property
            def operation(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) operation property.

                Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("operation")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def remote_directory_path(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) remote-directory-path property.

                Specify an array of string values to match this event if the actual value of remote-directory-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("remote_directory_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def transfer_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) transfer-id property.

                Specify an array of string values to match this event if the actual value of transfer-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("transfer_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def url(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) url property.

                Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("url")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SFTPConnectorFileSendFailedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class SFTPConnectorRemoteDeleteCompleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorRemoteDeleteCompleted",
    ):
        '''(experimental) aws.transfer@SFTPConnectorRemoteDeleteCompleted event types for Connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            s_fTPConnector_remote_delete_completed = transfer_events.ConnectorEvents.SFTPConnectorRemoteDeleteCompleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorRemoteDeleteCompleted.SFTPConnectorRemoteDeleteCompletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "connector_id": "connectorId",
                "delete_id": "deleteId",
                "delete_path": "deletePath",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "operation": "operation",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
                "url": "url",
            },
        )
        class SFTPConnectorRemoteDeleteCompletedProps:
            def __init__(
                self,
                *,
                connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                delete_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                delete_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                operation: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                url: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Connector aws.transfer@SFTPConnectorRemoteDeleteCompleted event.

                :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
                :param delete_id: (experimental) delete-id property. Specify an array of string values to match this event if the actual value of delete-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param delete_path: (experimental) delete-path property. Specify an array of string values to match this event if the actual value of delete-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s_fTPConnector_remote_delete_completed_props = transfer_events.ConnectorEvents.SFTPConnectorRemoteDeleteCompleted.SFTPConnectorRemoteDeleteCompletedProps(
                        connector_id=["connectorId"],
                        delete_id=["deleteId"],
                        delete_path=["deletePath"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        operation=["operation"],
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"],
                        url=["url"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1a72b297a161aecfbcf8b69cd6772e1a02e9257979d7ce1e6c1ff5b9db8dc0b3)
                    check_type(argname="argument connector_id", value=connector_id, expected_type=type_hints["connector_id"])
                    check_type(argname="argument delete_id", value=delete_id, expected_type=type_hints["delete_id"])
                    check_type(argname="argument delete_path", value=delete_path, expected_type=type_hints["delete_path"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if connector_id is not None:
                    self._values["connector_id"] = connector_id
                if delete_id is not None:
                    self._values["delete_id"] = delete_id
                if delete_path is not None:
                    self._values["delete_path"] = delete_path
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if operation is not None:
                    self._values["operation"] = operation
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code
                if url is not None:
                    self._values["url"] = url

            @builtins.property
            def connector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connector-id property.

                Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Connector reference

                :stability: experimental
                '''
                result = self._values.get("connector_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def delete_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) delete-id property.

                Specify an array of string values to match this event if the actual value of delete-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("delete_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def delete_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) delete-path property.

                Specify an array of string values to match this event if the actual value of delete-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("delete_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def operation(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) operation property.

                Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("operation")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def url(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) url property.

                Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("url")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SFTPConnectorRemoteDeleteCompletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class SFTPConnectorRemoteDeleteFailed(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorRemoteDeleteFailed",
    ):
        '''(experimental) aws.transfer@SFTPConnectorRemoteDeleteFailed event types for Connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            s_fTPConnector_remote_delete_failed = transfer_events.ConnectorEvents.SFTPConnectorRemoteDeleteFailed()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorRemoteDeleteFailed.SFTPConnectorRemoteDeleteFailedProps",
            jsii_struct_bases=[],
            name_mapping={
                "connector_id": "connectorId",
                "delete_id": "deleteId",
                "delete_path": "deletePath",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "failure_code": "failureCode",
                "failure_message": "failureMessage",
                "operation": "operation",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
                "url": "url",
            },
        )
        class SFTPConnectorRemoteDeleteFailedProps:
            def __init__(
                self,
                *,
                connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                delete_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                delete_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                operation: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                url: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Connector aws.transfer@SFTPConnectorRemoteDeleteFailed event.

                :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
                :param delete_id: (experimental) delete-id property. Specify an array of string values to match this event if the actual value of delete-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param delete_path: (experimental) delete-path property. Specify an array of string values to match this event if the actual value of delete-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s_fTPConnector_remote_delete_failed_props = transfer_events.ConnectorEvents.SFTPConnectorRemoteDeleteFailed.SFTPConnectorRemoteDeleteFailedProps(
                        connector_id=["connectorId"],
                        delete_id=["deleteId"],
                        delete_path=["deletePath"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        failure_code=["failureCode"],
                        failure_message=["failureMessage"],
                        operation=["operation"],
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"],
                        url=["url"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3ae6fd98c9fd935577519e6dde20b32584ba2b07112c5b61ddc64f21ea7bd30b)
                    check_type(argname="argument connector_id", value=connector_id, expected_type=type_hints["connector_id"])
                    check_type(argname="argument delete_id", value=delete_id, expected_type=type_hints["delete_id"])
                    check_type(argname="argument delete_path", value=delete_path, expected_type=type_hints["delete_path"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument failure_code", value=failure_code, expected_type=type_hints["failure_code"])
                    check_type(argname="argument failure_message", value=failure_message, expected_type=type_hints["failure_message"])
                    check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if connector_id is not None:
                    self._values["connector_id"] = connector_id
                if delete_id is not None:
                    self._values["delete_id"] = delete_id
                if delete_path is not None:
                    self._values["delete_path"] = delete_path
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if failure_code is not None:
                    self._values["failure_code"] = failure_code
                if failure_message is not None:
                    self._values["failure_message"] = failure_message
                if operation is not None:
                    self._values["operation"] = operation
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code
                if url is not None:
                    self._values["url"] = url

            @builtins.property
            def connector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connector-id property.

                Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Connector reference

                :stability: experimental
                '''
                result = self._values.get("connector_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def delete_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) delete-id property.

                Specify an array of string values to match this event if the actual value of delete-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("delete_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def delete_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) delete-path property.

                Specify an array of string values to match this event if the actual value of delete-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("delete_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def failure_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) failure-message property.

                Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("failure_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def operation(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) operation property.

                Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("operation")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def url(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) url property.

                Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("url")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SFTPConnectorRemoteDeleteFailedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class SFTPConnectorRemoteMoveCompleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorRemoteMoveCompleted",
    ):
        '''(experimental) aws.transfer@SFTPConnectorRemoteMoveCompleted event types for Connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            s_fTPConnector_remote_move_completed = transfer_events.ConnectorEvents.SFTPConnectorRemoteMoveCompleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorRemoteMoveCompleted.SFTPConnectorRemoteMoveCompletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "connector_id": "connectorId",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "move_id": "moveId",
                "move_source_path": "moveSourcePath",
                "move_target_path": "moveTargetPath",
                "operation": "operation",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
                "url": "url",
            },
        )
        class SFTPConnectorRemoteMoveCompletedProps:
            def __init__(
                self,
                *,
                connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                move_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                move_source_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                move_target_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                operation: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                url: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Connector aws.transfer@SFTPConnectorRemoteMoveCompleted event.

                :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param move_id: (experimental) move-id property. Specify an array of string values to match this event if the actual value of move-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param move_source_path: (experimental) move-source-path property. Specify an array of string values to match this event if the actual value of move-source-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param move_target_path: (experimental) move-target-path property. Specify an array of string values to match this event if the actual value of move-target-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s_fTPConnector_remote_move_completed_props = transfer_events.ConnectorEvents.SFTPConnectorRemoteMoveCompleted.SFTPConnectorRemoteMoveCompletedProps(
                        connector_id=["connectorId"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        move_id=["moveId"],
                        move_source_path=["moveSourcePath"],
                        move_target_path=["moveTargetPath"],
                        operation=["operation"],
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"],
                        url=["url"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7de35b78c5360259fa5477398f4834a11f6c7b5a8129673906737eca16b3abe8)
                    check_type(argname="argument connector_id", value=connector_id, expected_type=type_hints["connector_id"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument move_id", value=move_id, expected_type=type_hints["move_id"])
                    check_type(argname="argument move_source_path", value=move_source_path, expected_type=type_hints["move_source_path"])
                    check_type(argname="argument move_target_path", value=move_target_path, expected_type=type_hints["move_target_path"])
                    check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if connector_id is not None:
                    self._values["connector_id"] = connector_id
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if move_id is not None:
                    self._values["move_id"] = move_id
                if move_source_path is not None:
                    self._values["move_source_path"] = move_source_path
                if move_target_path is not None:
                    self._values["move_target_path"] = move_target_path
                if operation is not None:
                    self._values["operation"] = operation
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code
                if url is not None:
                    self._values["url"] = url

            @builtins.property
            def connector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connector-id property.

                Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Connector reference

                :stability: experimental
                '''
                result = self._values.get("connector_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def move_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) move-id property.

                Specify an array of string values to match this event if the actual value of move-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("move_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def move_source_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) move-source-path property.

                Specify an array of string values to match this event if the actual value of move-source-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("move_source_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def move_target_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) move-target-path property.

                Specify an array of string values to match this event if the actual value of move-target-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("move_target_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def operation(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) operation property.

                Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("operation")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def url(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) url property.

                Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("url")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SFTPConnectorRemoteMoveCompletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class SFTPConnectorRemoteMoveFailed(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorRemoteMoveFailed",
    ):
        '''(experimental) aws.transfer@SFTPConnectorRemoteMoveFailed event types for Connector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
            
            s_fTPConnector_remote_move_failed = transfer_events.ConnectorEvents.SFTPConnectorRemoteMoveFailed()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_transfer.events.ConnectorEvents.SFTPConnectorRemoteMoveFailed.SFTPConnectorRemoteMoveFailedProps",
            jsii_struct_bases=[],
            name_mapping={
                "connector_id": "connectorId",
                "end_timestamp": "endTimestamp",
                "event_metadata": "eventMetadata",
                "failure_code": "failureCode",
                "failure_message": "failureMessage",
                "move_id": "moveId",
                "move_source_path": "moveSourcePath",
                "move_target_path": "moveTargetPath",
                "operation": "operation",
                "start_timestamp": "startTimestamp",
                "status_code": "statusCode",
                "url": "url",
            },
        )
        class SFTPConnectorRemoteMoveFailedProps:
            def __init__(
                self,
                *,
                connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                move_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                move_source_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                move_target_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                operation: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                url: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Connector aws.transfer@SFTPConnectorRemoteMoveFailed event.

                :param connector_id: (experimental) connector-id property. Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Connector reference
                :param end_timestamp: (experimental) end-timestamp property. Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param failure_code: (experimental) failure-code property. Specify an array of string values to match this event if the actual value of failure-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param failure_message: (experimental) failure-message property. Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param move_id: (experimental) move-id property. Specify an array of string values to match this event if the actual value of move-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param move_source_path: (experimental) move-source-path property. Specify an array of string values to match this event if the actual value of move-source-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param move_target_path: (experimental) move-target-path property. Specify an array of string values to match this event if the actual value of move-target-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param operation: (experimental) operation property. Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_timestamp: (experimental) start-timestamp property. Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) status-code property. Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param url: (experimental) url property. Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_transfer import events as transfer_events
                    
                    s_fTPConnector_remote_move_failed_props = transfer_events.ConnectorEvents.SFTPConnectorRemoteMoveFailed.SFTPConnectorRemoteMoveFailedProps(
                        connector_id=["connectorId"],
                        end_timestamp=["endTimestamp"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        failure_code=["failureCode"],
                        failure_message=["failureMessage"],
                        move_id=["moveId"],
                        move_source_path=["moveSourcePath"],
                        move_target_path=["moveTargetPath"],
                        operation=["operation"],
                        start_timestamp=["startTimestamp"],
                        status_code=["statusCode"],
                        url=["url"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1691ef2e635651f3171443eaafd569169a4e0cb02b4c75d97f8c51baa40202b9)
                    check_type(argname="argument connector_id", value=connector_id, expected_type=type_hints["connector_id"])
                    check_type(argname="argument end_timestamp", value=end_timestamp, expected_type=type_hints["end_timestamp"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument failure_code", value=failure_code, expected_type=type_hints["failure_code"])
                    check_type(argname="argument failure_message", value=failure_message, expected_type=type_hints["failure_message"])
                    check_type(argname="argument move_id", value=move_id, expected_type=type_hints["move_id"])
                    check_type(argname="argument move_source_path", value=move_source_path, expected_type=type_hints["move_source_path"])
                    check_type(argname="argument move_target_path", value=move_target_path, expected_type=type_hints["move_target_path"])
                    check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
                    check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if connector_id is not None:
                    self._values["connector_id"] = connector_id
                if end_timestamp is not None:
                    self._values["end_timestamp"] = end_timestamp
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if failure_code is not None:
                    self._values["failure_code"] = failure_code
                if failure_message is not None:
                    self._values["failure_message"] = failure_message
                if move_id is not None:
                    self._values["move_id"] = move_id
                if move_source_path is not None:
                    self._values["move_source_path"] = move_source_path
                if move_target_path is not None:
                    self._values["move_target_path"] = move_target_path
                if operation is not None:
                    self._values["operation"] = operation
                if start_timestamp is not None:
                    self._values["start_timestamp"] = start_timestamp
                if status_code is not None:
                    self._values["status_code"] = status_code
                if url is not None:
                    self._values["url"] = url

            @builtins.property
            def connector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connector-id property.

                Specify an array of string values to match this event if the actual value of connector-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Connector reference

                :stability: experimental
                '''
                result = self._values.get("connector_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) end-timestamp property.

                Specify an array of string values to match this event if the actual value of end-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_timestamp")
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
            def failure_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) failure-message property.

                Specify an array of string values to match this event if the actual value of failure-message is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("failure_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def move_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) move-id property.

                Specify an array of string values to match this event if the actual value of move-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("move_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def move_source_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) move-source-path property.

                Specify an array of string values to match this event if the actual value of move-source-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("move_source_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def move_target_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) move-target-path property.

                Specify an array of string values to match this event if the actual value of move-target-path is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("move_target_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def operation(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) operation property.

                Specify an array of string values to match this event if the actual value of operation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("operation")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_timestamp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) start-timestamp property.

                Specify an array of string values to match this event if the actual value of start-timestamp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_timestamp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status-code property.

                Specify an array of string values to match this event if the actual value of status-code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def url(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) url property.

                Specify an array of string values to match this event if the actual value of url is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("url")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SFTPConnectorRemoteMoveFailedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "AgreementEvents",
    "ConnectorEvents",
]

publication.publish()

def _typecheckingstub__f052ad41ae6ae1e4725092042022b4444b6f12843e6247378ab3e43f638c06a9(
    agreement_ref: _aws_cdk_interfaces_aws_transfer_ceddda9d.IAgreementRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf2723b986b0f053ee6aa3f40fb51fd1f7f1d2902f61cd5383eba79884c0605(
    *,
    agreement_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
    disposition: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    mdn_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
    requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_attributes: typing.Optional[typing.Union[AgreementEvents.AS2MDNSendCompleted.S3Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    server_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19012522862a4f49dcbf4f438e9d1f878ac5e1b4a17af08e6242062f64e09711(
    *,
    file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_key: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144780b5c4874c2f404e1e1c80a6463ee4a13f620e9d04f0f1807218fcee513e(
    *,
    agreement_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
    disposition: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_attributes: typing.Optional[typing.Union[AgreementEvents.AS2MDNSendFailed.S3Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    server_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba12622626a5efc12f90cc0c524bd9bf50dd360202cae702307bb7bcb8f040b2(
    *,
    file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_key: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffbff16b6defcab7093bca1cd1448ca6870c7e0b314ac10d35c1c3e96cce34c(
    *,
    agreement_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
    requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_attributes: typing.Optional[typing.Union[AgreementEvents.AS2PayloadReceiveCompleted.S3Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    server_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86fcab71d35868715dad1fd235b3a707db9873c326ad700d8bb239de8fd35a04(
    *,
    file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e86b346796909ba2e35dd210e171c5ff26bb3513693cc247776e2180a563cce(
    *,
    agreement_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_attributes: typing.Optional[typing.Union[AgreementEvents.AS2PayloadReceiveFailed.S3Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    server_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae82f29b97c60add789e4819a603d91c058a564869ec20194cb4519d352c91f(
    *,
    file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0530f3fa356cedec3188ea511d834e381ad8d3f0d072ee37c9839f47d31fe4(
    connector_ref: _aws_cdk_interfaces_aws_transfer_ceddda9d.IConnectorRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02c22d06f28f7c76093cdf7bfa1655649bfbfebe37724cd2e8682a1ae8ec85f(
    *,
    as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
    connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    disposition: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    mdn_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
    message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
    requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_attributes: typing.Optional[typing.Union[ConnectorEvents.AS2MDNReceiveCompleted.S3Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a248584b316f8bbb633a6ed946dd47c6767aa9f1174aeb5adf29abda3a00b44(
    *,
    file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_key: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc5ec1442c5a832b4aa0485e5e0e3886b8311411154ed947cf409c11c9256ff(
    *,
    as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
    message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_attributes: typing.Optional[typing.Union[ConnectorEvents.AS2MDNReceiveFailed.S3Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066d15f0307471ade971ee67ef0635159ba1021693c3c0f2e6e2446b27f9cb43(
    *,
    file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_key: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f05edc97d5ecc89ff6014fc829afc57ca2cb5758796bd5487f3b7e9715029f(
    *,
    as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
    connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    mdn_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
    message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
    requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_attributes: typing.Optional[typing.Union[ConnectorEvents.AS2PayloadSendCompleted.S3Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568351db39d8364f8b693403c19a285fd4895c7cf1f9581d65e21c2e5d80546a(
    *,
    file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    mdn_key: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb30fb66551b418cdfb94d488501d33f3852029de425d4c701d68626a7f9670(
    *,
    as2_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_message_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    as2_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
    connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    message_subject: typing.Optional[typing.Sequence[builtins.str]] = None,
    requester_file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_attributes: typing.Optional[typing.Union[ConnectorEvents.AS2PayloadSendFailed.S3Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba86421f85267cbc9ea80e0174f08b7028a8aee5b5e5164105f2b2e55adde308(
    *,
    file_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    json_key: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd0f2ccad9fa006f3cbdd5db1b9d19150e054575a460fe3678463e24c91fdda(
    *,
    bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75bbe3081a8041bce6feabddccbe2fb3464d03a3d08d687dd36d07209138fdd0(
    *,
    connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    item_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    listing_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_items: typing.Optional[typing.Sequence[builtins.str]] = None,
    output_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    output_file_location: typing.Optional[typing.Union[ConnectorEvents.SFTPConnectorDirectoryListingCompleted.OutputFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    remote_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    truncated: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c4a77819ddfee95c88b5b5af7b6c34b5a25d6b7dc594436917abf0631cbee6(
    *,
    connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    listing_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_items: typing.Optional[typing.Sequence[builtins.str]] = None,
    output_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    remote_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10cb367321f098d111c4c39d0581feecf922e241fa2663c0d8d6d1a7bb29fbfc(
    *,
    bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdd4245563e0e6f16aea380d8bf2213e573a4ca6f3f669ff257c861243259d8(
    *,
    bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
    connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_file_location: typing.Optional[typing.Union[ConnectorEvents.SFTPConnectorFileRetrieveCompleted.LocalFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    operation: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e5b5081c2f67237e143cae1eea2f2309dae8883ac1163209058da3a71bb971(
    *,
    bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a66b3d602d37137a1f3e1f5a6f806315d3c7c1f18062e18755b50d000c5867(
    *,
    bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
    connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_file_location: typing.Optional[typing.Union[ConnectorEvents.SFTPConnectorFileRetrieveFailed.LocalFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    operation: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a0201ab895f38d1e133276180a6de997ad7ba383aa4de01ba9811676dae7c4(
    *,
    bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431567d7ac3b1b5289b35b4d8ecfa7033bf4959579d5f348f77c47e16a9fa7d9(
    *,
    bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
    connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_file_location: typing.Optional[typing.Union[ConnectorEvents.SFTPConnectorFileSendCompleted.LocalFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    operation: typing.Optional[typing.Sequence[builtins.str]] = None,
    remote_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d9fb826a7cd00225e990a3021a5483ca7ec6c214c903a314732d4b8ae8b8d2e(
    *,
    bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf488b4e9f13197d9ccff0299ffdbd9f9ffad4d472244be76e1899907dc79806(
    *,
    bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
    connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_file_location: typing.Optional[typing.Union[ConnectorEvents.SFTPConnectorFileSendFailed.LocalFileLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    operation: typing.Optional[typing.Sequence[builtins.str]] = None,
    remote_directory_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    transfer_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a72b297a161aecfbcf8b69cd6772e1a02e9257979d7ce1e6c1ff5b9db8dc0b3(
    *,
    connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    delete_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    delete_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    operation: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae6fd98c9fd935577519e6dde20b32584ba2b07112c5b61ddc64f21ea7bd30b(
    *,
    connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    delete_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    delete_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    operation: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de35b78c5360259fa5477398f4834a11f6c7b5a8129673906737eca16b3abe8(
    *,
    connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    move_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    move_source_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    move_target_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    operation: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1691ef2e635651f3171443eaafd569169a4e0cb02b4c75d97f8c51baa40202b9(
    *,
    connector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    failure_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    move_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    move_source_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    move_target_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    operation: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_timestamp: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
