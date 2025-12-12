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
import aws_cdk.interfaces.aws_voiceid as _aws_cdk_interfaces_aws_voiceid_ceddda9d


class DomainEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents",
):
    '''(experimental) EventBridge event patterns for Domain.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
        from aws_cdk.interfaces import aws_voiceid as interfaces_voiceid
        
        # domain_ref: interfaces_voiceid.IDomainRef
        
        domain_events = voiceid_events.DomainEvents.from_domain(domain_ref)
    '''

    @jsii.member(jsii_name="fromDomain")
    @builtins.classmethod
    def from_domain(
        cls,
        domain_ref: _aws_cdk_interfaces_aws_voiceid_ceddda9d.IDomainRef,
    ) -> "DomainEvents":
        '''(experimental) Create DomainEvents from a Domain reference.

        :param domain_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f136a5b85b027f97dcce5d4bbabc0519a38dbb97bb11a589a536ecbfd7c0d4)
            check_type(argname="argument domain_ref", value=domain_ref, expected_type=type_hints["domain_ref"])
        return typing.cast("DomainEvents", jsii.sinvoke(cls, "fromDomain", [domain_ref]))

    @jsii.member(jsii_name="voiceIdBatchFraudsterRegistrationActionPattern")
    def voice_id_batch_fraudster_registration_action_pattern(
        self,
        *,
        action: typing.Optional[typing.Sequence[builtins.str]] = None,
        batch_job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        data: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.Data", typing.Dict[builtins.str, typing.Any]]] = None,
        domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Domain VoiceId Batch Fraudster Registration Action.

        :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param batch_job_id: (experimental) batchJobId property. Specify an array of string values to match this event if the actual value of batchJobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param data: (experimental) data property. Specify an array of string values to match this event if the actual value of data is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
        :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DomainEvents.VoiceIdBatchFraudsterRegistrationAction.VoiceIdBatchFraudsterRegistrationActionProps(
            action=action,
            batch_job_id=batch_job_id,
            data=data,
            domain_id=domain_id,
            error_info=error_info,
            event_metadata=event_metadata,
            source_id=source_id,
            status=status,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "voiceIdBatchFraudsterRegistrationActionPattern", [options]))

    @jsii.member(jsii_name="voiceIdBatchSpeakerEnrollmentActionPattern")
    def voice_id_batch_speaker_enrollment_action_pattern(
        self,
        *,
        action: typing.Optional[typing.Sequence[builtins.str]] = None,
        batch_job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        data: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.Data", typing.Dict[builtins.str, typing.Any]]] = None,
        domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Domain VoiceId Batch Speaker Enrollment Action.

        :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param batch_job_id: (experimental) batchJobId property. Specify an array of string values to match this event if the actual value of batchJobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param data: (experimental) data property. Specify an array of string values to match this event if the actual value of data is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
        :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.VoiceIdBatchSpeakerEnrollmentActionProps(
            action=action,
            batch_job_id=batch_job_id,
            data=data,
            domain_id=domain_id,
            error_info=error_info,
            event_metadata=event_metadata,
            source_id=source_id,
            status=status,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "voiceIdBatchSpeakerEnrollmentActionPattern", [options]))

    @jsii.member(jsii_name="voiceIdEvaluateSessionActionPattern")
    def voice_id_evaluate_session_action_pattern(
        self,
        *,
        action: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdEvaluateSessionAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        session: typing.Optional[typing.Union["DomainEvents.VoiceIdEvaluateSessionAction.Session", typing.Dict[builtins.str, typing.Any]]] = None,
        source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
        system_attributes: typing.Optional[typing.Union["DomainEvents.VoiceIdEvaluateSessionAction.SystemAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Domain VoiceId Evaluate Session Action.

        :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
        :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param session: (experimental) session property. Specify an array of string values to match this event if the actual value of session is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param system_attributes: (experimental) systemAttributes property. Specify an array of string values to match this event if the actual value of systemAttributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DomainEvents.VoiceIdEvaluateSessionAction.VoiceIdEvaluateSessionActionProps(
            action=action,
            domain_id=domain_id,
            error_info=error_info,
            event_metadata=event_metadata,
            session=session,
            source_id=source_id,
            status=status,
            system_attributes=system_attributes,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "voiceIdEvaluateSessionActionPattern", [options]))

    @jsii.member(jsii_name="voiceIdFraudsterActionPattern")
    def voice_id_fraudster_action_pattern(
        self,
        *,
        action: typing.Optional[typing.Sequence[builtins.str]] = None,
        data: typing.Optional[typing.Union["DomainEvents.VoiceIdFraudsterAction.Data", typing.Dict[builtins.str, typing.Any]]] = None,
        domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdFraudsterAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        generated_fraudster_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
        watchlist_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Domain VoiceId Fraudster Action.

        :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param data: (experimental) data property. Specify an array of string values to match this event if the actual value of data is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
        :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param generated_fraudster_id: (experimental) generatedFraudsterId property. Specify an array of string values to match this event if the actual value of generatedFraudsterId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param watchlist_ids: (experimental) watchlistIds property. Specify an array of string values to match this event if the actual value of watchlistIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DomainEvents.VoiceIdFraudsterAction.VoiceIdFraudsterActionProps(
            action=action,
            data=data,
            domain_id=domain_id,
            error_info=error_info,
            event_metadata=event_metadata,
            generated_fraudster_id=generated_fraudster_id,
            source_id=source_id,
            status=status,
            watchlist_ids=watchlist_ids,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "voiceIdFraudsterActionPattern", [options]))

    @jsii.member(jsii_name="voiceIdSessionSpeakerEnrollmentActionPattern")
    def voice_id_session_speaker_enrollment_action_pattern(
        self,
        *,
        action: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        session_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
        system_attributes: typing.Optional[typing.Union["DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.SystemAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Domain VoiceId Session Speaker Enrollment Action.

        :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
        :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param session_id: (experimental) sessionId property. Specify an array of string values to match this event if the actual value of sessionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param session_name: (experimental) sessionName property. Specify an array of string values to match this event if the actual value of sessionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param system_attributes: (experimental) systemAttributes property. Specify an array of string values to match this event if the actual value of systemAttributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.VoiceIdSessionSpeakerEnrollmentActionProps(
            action=action,
            domain_id=domain_id,
            error_info=error_info,
            event_metadata=event_metadata,
            session_id=session_id,
            session_name=session_name,
            source_id=source_id,
            status=status,
            system_attributes=system_attributes,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "voiceIdSessionSpeakerEnrollmentActionPattern", [options]))

    @jsii.member(jsii_name="voiceIdSpeakerActionPattern")
    def voice_id_speaker_action_pattern(
        self,
        *,
        action: typing.Optional[typing.Sequence[builtins.str]] = None,
        data: typing.Optional[typing.Union["DomainEvents.VoiceIdSpeakerAction.Data", typing.Dict[builtins.str, typing.Any]]] = None,
        domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdSpeakerAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        generated_speaker_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
        system_attributes: typing.Optional[typing.Union["DomainEvents.VoiceIdSpeakerAction.SystemAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Domain VoiceId Speaker Action.

        :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param data: (experimental) data property. Specify an array of string values to match this event if the actual value of data is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
        :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param generated_speaker_id: (experimental) generatedSpeakerId property. Specify an array of string values to match this event if the actual value of generatedSpeakerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param system_attributes: (experimental) systemAttributes property. Specify an array of string values to match this event if the actual value of systemAttributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DomainEvents.VoiceIdSpeakerAction.VoiceIdSpeakerActionProps(
            action=action,
            data=data,
            domain_id=domain_id,
            error_info=error_info,
            event_metadata=event_metadata,
            generated_speaker_id=generated_speaker_id,
            source_id=source_id,
            status=status,
            system_attributes=system_attributes,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "voiceIdSpeakerActionPattern", [options]))

    @jsii.member(jsii_name="voiceIdStartSessionActionPattern")
    def voice_id_start_session_action_pattern(
        self,
        *,
        action: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdStartSessionAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        session: typing.Optional[typing.Union["DomainEvents.VoiceIdStartSessionAction.Session", typing.Dict[builtins.str, typing.Any]]] = None,
        source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
        system_attributes: typing.Optional[typing.Union["DomainEvents.VoiceIdStartSessionAction.SystemAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Domain VoiceId Start Session Action.

        :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
        :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param session: (experimental) session property. Specify an array of string values to match this event if the actual value of session is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param system_attributes: (experimental) systemAttributes property. Specify an array of string values to match this event if the actual value of systemAttributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DomainEvents.VoiceIdStartSessionAction.VoiceIdStartSessionActionProps(
            action=action,
            domain_id=domain_id,
            error_info=error_info,
            event_metadata=event_metadata,
            session=session,
            source_id=source_id,
            status=status,
            system_attributes=system_attributes,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "voiceIdStartSessionActionPattern", [options]))

    @jsii.member(jsii_name="voiceIdUpdateSessionActionPattern")
    def voice_id_update_session_action_pattern(
        self,
        *,
        action: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdUpdateSessionAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        session: typing.Optional[typing.Union["DomainEvents.VoiceIdUpdateSessionAction.Session", typing.Dict[builtins.str, typing.Any]]] = None,
        source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Domain VoiceId Update Session Action.

        :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
        :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param session: (experimental) session property. Specify an array of string values to match this event if the actual value of session is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DomainEvents.VoiceIdUpdateSessionAction.VoiceIdUpdateSessionActionProps(
            action=action,
            domain_id=domain_id,
            error_info=error_info,
            event_metadata=event_metadata,
            session=session,
            source_id=source_id,
            status=status,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "voiceIdUpdateSessionActionPattern", [options]))

    class VoiceIdBatchFraudsterRegistrationAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction",
    ):
        '''(experimental) aws.voiceid@VoiceIdBatchFraudsterRegistrationAction event types for Domain.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
            
            voice_id_batch_fraudster_registration_action = voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.Data",
            jsii_struct_bases=[],
            name_mapping={
                "data_access_role_arn": "dataAccessRoleArn",
                "input_data_config": "inputDataConfig",
                "output_data_config": "outputDataConfig",
                "registration_config": "registrationConfig",
            },
        )
        class Data:
            def __init__(
                self,
                *,
                data_access_role_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                input_data_config: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.InputDataConfig", typing.Dict[builtins.str, typing.Any]]] = None,
                output_data_config: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.OutputDataConfig", typing.Dict[builtins.str, typing.Any]]] = None,
                registration_config: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.RegistrationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for Data.

                :param data_access_role_arn: (experimental) dataAccessRoleArn property. Specify an array of string values to match this event if the actual value of dataAccessRoleArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param input_data_config: (experimental) inputDataConfig property. Specify an array of string values to match this event if the actual value of inputDataConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param output_data_config: (experimental) outputDataConfig property. Specify an array of string values to match this event if the actual value of outputDataConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param registration_config: (experimental) registrationConfig property. Specify an array of string values to match this event if the actual value of registrationConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    data = voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.Data(
                        data_access_role_arn=["dataAccessRoleArn"],
                        input_data_config=voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.InputDataConfig(
                            s3_uri=["s3Uri"]
                        ),
                        output_data_config=voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.OutputDataConfig(
                            kms_key_id=["kmsKeyId"],
                            s3_uri=["s3Uri"]
                        ),
                        registration_config=voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.RegistrationConfig(
                            duplicate_registration_action=["duplicateRegistrationAction"],
                            fraudster_similarity_threshold=["fraudsterSimilarityThreshold"],
                            watchlist_ids=["watchlistIds"]
                        )
                    )
                '''
                if isinstance(input_data_config, dict):
                    input_data_config = DomainEvents.VoiceIdBatchFraudsterRegistrationAction.InputDataConfig(**input_data_config)
                if isinstance(output_data_config, dict):
                    output_data_config = DomainEvents.VoiceIdBatchFraudsterRegistrationAction.OutputDataConfig(**output_data_config)
                if isinstance(registration_config, dict):
                    registration_config = DomainEvents.VoiceIdBatchFraudsterRegistrationAction.RegistrationConfig(**registration_config)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__396b26ac89eb581bd6fd72cf0e1e832a1beedc3db353c67952bbdca24be84551)
                    check_type(argname="argument data_access_role_arn", value=data_access_role_arn, expected_type=type_hints["data_access_role_arn"])
                    check_type(argname="argument input_data_config", value=input_data_config, expected_type=type_hints["input_data_config"])
                    check_type(argname="argument output_data_config", value=output_data_config, expected_type=type_hints["output_data_config"])
                    check_type(argname="argument registration_config", value=registration_config, expected_type=type_hints["registration_config"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if data_access_role_arn is not None:
                    self._values["data_access_role_arn"] = data_access_role_arn
                if input_data_config is not None:
                    self._values["input_data_config"] = input_data_config
                if output_data_config is not None:
                    self._values["output_data_config"] = output_data_config
                if registration_config is not None:
                    self._values["registration_config"] = registration_config

            @builtins.property
            def data_access_role_arn(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) dataAccessRoleArn property.

                Specify an array of string values to match this event if the actual value of dataAccessRoleArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("data_access_role_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def input_data_config(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.InputDataConfig"]:
                '''(experimental) inputDataConfig property.

                Specify an array of string values to match this event if the actual value of inputDataConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("input_data_config")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.InputDataConfig"], result)

            @builtins.property
            def output_data_config(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.OutputDataConfig"]:
                '''(experimental) outputDataConfig property.

                Specify an array of string values to match this event if the actual value of outputDataConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("output_data_config")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.OutputDataConfig"], result)

            @builtins.property
            def registration_config(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.RegistrationConfig"]:
                '''(experimental) registrationConfig property.

                Specify an array of string values to match this event if the actual value of registrationConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("registration_config")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.RegistrationConfig"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Data(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.ErrorInfo",
            jsii_struct_bases=[],
            name_mapping={
                "error_code": "errorCode",
                "error_message": "errorMessage",
                "error_type": "errorType",
            },
        )
        class ErrorInfo:
            def __init__(
                self,
                *,
                error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ErrorInfo.

                :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_type: (experimental) errorType property. Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    error_info = voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.ErrorInfo(
                        error_code=["errorCode"],
                        error_message=["errorMessage"],
                        error_type=["errorType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__47d0357b1b8c442687b26d583da68aae954cc71bc3a1edb012084848d65a24d6)
                    check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                    check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
                    check_type(argname="argument error_type", value=error_type, expected_type=type_hints["error_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if error_code is not None:
                    self._values["error_code"] = error_code
                if error_message is not None:
                    self._values["error_message"] = error_message
                if error_type is not None:
                    self._values["error_type"] = error_type

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
            def error_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorType property.

                Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ErrorInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.InputDataConfig",
            jsii_struct_bases=[],
            name_mapping={"s3_uri": "s3Uri"},
        )
        class InputDataConfig:
            def __init__(
                self,
                *,
                s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for InputDataConfig.

                :param s3_uri: (experimental) s3Uri property. Specify an array of string values to match this event if the actual value of s3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    input_data_config = voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.InputDataConfig(
                        s3_uri=["s3Uri"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__e36f15ec2c6a2d41369d9c0be8c9bee8869d412f149935ff16ad5f79a770bf21)
                    check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if s3_uri is not None:
                    self._values["s3_uri"] = s3_uri

            @builtins.property
            def s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) s3Uri property.

                Specify an array of string values to match this event if the actual value of s3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "InputDataConfig(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.OutputDataConfig",
            jsii_struct_bases=[],
            name_mapping={"kms_key_id": "kmsKeyId", "s3_uri": "s3Uri"},
        )
        class OutputDataConfig:
            def __init__(
                self,
                *,
                kms_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for OutputDataConfig.

                :param kms_key_id: (experimental) kmsKeyId property. Specify an array of string values to match this event if the actual value of kmsKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_uri: (experimental) s3Uri property. Specify an array of string values to match this event if the actual value of s3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    output_data_config = voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.OutputDataConfig(
                        kms_key_id=["kmsKeyId"],
                        s3_uri=["s3Uri"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cc6237ab3ffe7bceabaece456aae247052cf26a52e017e3c61727438b7103f88)
                    check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                    check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if kms_key_id is not None:
                    self._values["kms_key_id"] = kms_key_id
                if s3_uri is not None:
                    self._values["s3_uri"] = s3_uri

            @builtins.property
            def kms_key_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) kmsKeyId property.

                Specify an array of string values to match this event if the actual value of kmsKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("kms_key_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) s3Uri property.

                Specify an array of string values to match this event if the actual value of s3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "OutputDataConfig(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.RegistrationConfig",
            jsii_struct_bases=[],
            name_mapping={
                "duplicate_registration_action": "duplicateRegistrationAction",
                "fraudster_similarity_threshold": "fraudsterSimilarityThreshold",
                "watchlist_ids": "watchlistIds",
            },
        )
        class RegistrationConfig:
            def __init__(
                self,
                *,
                duplicate_registration_action: typing.Optional[typing.Sequence[builtins.str]] = None,
                fraudster_similarity_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
                watchlist_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RegistrationConfig.

                :param duplicate_registration_action: (experimental) duplicateRegistrationAction property. Specify an array of string values to match this event if the actual value of duplicateRegistrationAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param fraudster_similarity_threshold: (experimental) fraudsterSimilarityThreshold property. Specify an array of string values to match this event if the actual value of fraudsterSimilarityThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param watchlist_ids: (experimental) watchlistIds property. Specify an array of string values to match this event if the actual value of watchlistIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    registration_config = voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.RegistrationConfig(
                        duplicate_registration_action=["duplicateRegistrationAction"],
                        fraudster_similarity_threshold=["fraudsterSimilarityThreshold"],
                        watchlist_ids=["watchlistIds"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8277cda7c5c958dba46f0c7cf2b21ab830ae6e9c3f8f1787303396d88554bccd)
                    check_type(argname="argument duplicate_registration_action", value=duplicate_registration_action, expected_type=type_hints["duplicate_registration_action"])
                    check_type(argname="argument fraudster_similarity_threshold", value=fraudster_similarity_threshold, expected_type=type_hints["fraudster_similarity_threshold"])
                    check_type(argname="argument watchlist_ids", value=watchlist_ids, expected_type=type_hints["watchlist_ids"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if duplicate_registration_action is not None:
                    self._values["duplicate_registration_action"] = duplicate_registration_action
                if fraudster_similarity_threshold is not None:
                    self._values["fraudster_similarity_threshold"] = fraudster_similarity_threshold
                if watchlist_ids is not None:
                    self._values["watchlist_ids"] = watchlist_ids

            @builtins.property
            def duplicate_registration_action(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) duplicateRegistrationAction property.

                Specify an array of string values to match this event if the actual value of duplicateRegistrationAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("duplicate_registration_action")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def fraudster_similarity_threshold(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) fraudsterSimilarityThreshold property.

                Specify an array of string values to match this event if the actual value of fraudsterSimilarityThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("fraudster_similarity_threshold")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def watchlist_ids(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) watchlistIds property.

                Specify an array of string values to match this event if the actual value of watchlistIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("watchlist_ids")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RegistrationConfig(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.VoiceIdBatchFraudsterRegistrationActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "action": "action",
                "batch_job_id": "batchJobId",
                "data": "data",
                "domain_id": "domainId",
                "error_info": "errorInfo",
                "event_metadata": "eventMetadata",
                "source_id": "sourceId",
                "status": "status",
            },
        )
        class VoiceIdBatchFraudsterRegistrationActionProps:
            def __init__(
                self,
                *,
                action: typing.Optional[typing.Sequence[builtins.str]] = None,
                batch_job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                data: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.Data", typing.Dict[builtins.str, typing.Any]]] = None,
                domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Domain aws.voiceid@VoiceIdBatchFraudsterRegistrationAction event.

                :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param batch_job_id: (experimental) batchJobId property. Specify an array of string values to match this event if the actual value of batchJobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param data: (experimental) data property. Specify an array of string values to match this event if the actual value of data is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
                :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    voice_id_batch_fraudster_registration_action_props = voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.VoiceIdBatchFraudsterRegistrationActionProps(
                        action=["action"],
                        batch_job_id=["batchJobId"],
                        data=voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.Data(
                            data_access_role_arn=["dataAccessRoleArn"],
                            input_data_config=voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.InputDataConfig(
                                s3_uri=["s3Uri"]
                            ),
                            output_data_config=voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.OutputDataConfig(
                                kms_key_id=["kmsKeyId"],
                                s3_uri=["s3Uri"]
                            ),
                            registration_config=voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.RegistrationConfig(
                                duplicate_registration_action=["duplicateRegistrationAction"],
                                fraudster_similarity_threshold=["fraudsterSimilarityThreshold"],
                                watchlist_ids=["watchlistIds"]
                            )
                        ),
                        domain_id=["domainId"],
                        error_info=voiceid_events.DomainEvents.VoiceIdBatchFraudsterRegistrationAction.ErrorInfo(
                            error_code=["errorCode"],
                            error_message=["errorMessage"],
                            error_type=["errorType"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        source_id=["sourceId"],
                        status=["status"]
                    )
                '''
                if isinstance(data, dict):
                    data = DomainEvents.VoiceIdBatchFraudsterRegistrationAction.Data(**data)
                if isinstance(error_info, dict):
                    error_info = DomainEvents.VoiceIdBatchFraudsterRegistrationAction.ErrorInfo(**error_info)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ded054e2738839ba6b4e9b215aa52ac626ce97a6a6fa39b279cbfb095967f047)
                    check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                    check_type(argname="argument batch_job_id", value=batch_job_id, expected_type=type_hints["batch_job_id"])
                    check_type(argname="argument data", value=data, expected_type=type_hints["data"])
                    check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
                    check_type(argname="argument error_info", value=error_info, expected_type=type_hints["error_info"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action is not None:
                    self._values["action"] = action
                if batch_job_id is not None:
                    self._values["batch_job_id"] = batch_job_id
                if data is not None:
                    self._values["data"] = data
                if domain_id is not None:
                    self._values["domain_id"] = domain_id
                if error_info is not None:
                    self._values["error_info"] = error_info
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if source_id is not None:
                    self._values["source_id"] = source_id
                if status is not None:
                    self._values["status"] = status

            @builtins.property
            def action(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) action property.

                Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def batch_job_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) batchJobId property.

                Specify an array of string values to match this event if the actual value of batchJobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("batch_job_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def data(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.Data"]:
                '''(experimental) data property.

                Specify an array of string values to match this event if the actual value of data is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("data")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.Data"], result)

            @builtins.property
            def domain_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domainId property.

                Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Domain reference

                :stability: experimental
                '''
                result = self._values.get("domain_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_info(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.ErrorInfo"]:
                '''(experimental) errorInfo property.

                Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_info")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdBatchFraudsterRegistrationAction.ErrorInfo"], result)

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
            def source_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceId property.

                Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_id")
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
                return "VoiceIdBatchFraudsterRegistrationActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class VoiceIdBatchSpeakerEnrollmentAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction",
    ):
        '''(experimental) aws.voiceid@VoiceIdBatchSpeakerEnrollmentAction event types for Domain.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
            
            voice_id_batch_speaker_enrollment_action = voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.Data",
            jsii_struct_bases=[],
            name_mapping={
                "data_access_role_arn": "dataAccessRoleArn",
                "enrollment_config": "enrollmentConfig",
                "input_data_config": "inputDataConfig",
                "output_data_config": "outputDataConfig",
            },
        )
        class Data:
            def __init__(
                self,
                *,
                data_access_role_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                enrollment_config: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.EnrollmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
                input_data_config: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.InputDataConfig", typing.Dict[builtins.str, typing.Any]]] = None,
                output_data_config: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.OutputDataConfig", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for Data.

                :param data_access_role_arn: (experimental) dataAccessRoleArn property. Specify an array of string values to match this event if the actual value of dataAccessRoleArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param enrollment_config: (experimental) enrollmentConfig property. Specify an array of string values to match this event if the actual value of enrollmentConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param input_data_config: (experimental) inputDataConfig property. Specify an array of string values to match this event if the actual value of inputDataConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param output_data_config: (experimental) outputDataConfig property. Specify an array of string values to match this event if the actual value of outputDataConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    data = voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.Data(
                        data_access_role_arn=["dataAccessRoleArn"],
                        enrollment_config=voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.EnrollmentConfig(
                            existing_enrollment_action=["existingEnrollmentAction"],
                            fraud_detection_config=voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.FraudDetectionConfig(
                                fraud_detection_action=["fraudDetectionAction"],
                                fraud_detection_threshold=["fraudDetectionThreshold"],
                                watchlist_ids=["watchlistIds"]
                            )
                        ),
                        input_data_config=voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.InputDataConfig(
                            s3_uri=["s3Uri"]
                        ),
                        output_data_config=voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.OutputDataConfig(
                            kms_key_id=["kmsKeyId"],
                            s3_uri=["s3Uri"]
                        )
                    )
                '''
                if isinstance(enrollment_config, dict):
                    enrollment_config = DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.EnrollmentConfig(**enrollment_config)
                if isinstance(input_data_config, dict):
                    input_data_config = DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.InputDataConfig(**input_data_config)
                if isinstance(output_data_config, dict):
                    output_data_config = DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.OutputDataConfig(**output_data_config)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__898854956c3e5b208c13f073ddbc897bc3b6c858a2f7eeb30b8f3dd47ad929f3)
                    check_type(argname="argument data_access_role_arn", value=data_access_role_arn, expected_type=type_hints["data_access_role_arn"])
                    check_type(argname="argument enrollment_config", value=enrollment_config, expected_type=type_hints["enrollment_config"])
                    check_type(argname="argument input_data_config", value=input_data_config, expected_type=type_hints["input_data_config"])
                    check_type(argname="argument output_data_config", value=output_data_config, expected_type=type_hints["output_data_config"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if data_access_role_arn is not None:
                    self._values["data_access_role_arn"] = data_access_role_arn
                if enrollment_config is not None:
                    self._values["enrollment_config"] = enrollment_config
                if input_data_config is not None:
                    self._values["input_data_config"] = input_data_config
                if output_data_config is not None:
                    self._values["output_data_config"] = output_data_config

            @builtins.property
            def data_access_role_arn(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) dataAccessRoleArn property.

                Specify an array of string values to match this event if the actual value of dataAccessRoleArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("data_access_role_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def enrollment_config(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.EnrollmentConfig"]:
                '''(experimental) enrollmentConfig property.

                Specify an array of string values to match this event if the actual value of enrollmentConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("enrollment_config")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.EnrollmentConfig"], result)

            @builtins.property
            def input_data_config(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.InputDataConfig"]:
                '''(experimental) inputDataConfig property.

                Specify an array of string values to match this event if the actual value of inputDataConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("input_data_config")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.InputDataConfig"], result)

            @builtins.property
            def output_data_config(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.OutputDataConfig"]:
                '''(experimental) outputDataConfig property.

                Specify an array of string values to match this event if the actual value of outputDataConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("output_data_config")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.OutputDataConfig"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Data(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.EnrollmentConfig",
            jsii_struct_bases=[],
            name_mapping={
                "existing_enrollment_action": "existingEnrollmentAction",
                "fraud_detection_config": "fraudDetectionConfig",
            },
        )
        class EnrollmentConfig:
            def __init__(
                self,
                *,
                existing_enrollment_action: typing.Optional[typing.Sequence[builtins.str]] = None,
                fraud_detection_config: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.FraudDetectionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for EnrollmentConfig.

                :param existing_enrollment_action: (experimental) existingEnrollmentAction property. Specify an array of string values to match this event if the actual value of existingEnrollmentAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param fraud_detection_config: (experimental) fraudDetectionConfig property. Specify an array of string values to match this event if the actual value of fraudDetectionConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    enrollment_config = voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.EnrollmentConfig(
                        existing_enrollment_action=["existingEnrollmentAction"],
                        fraud_detection_config=voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.FraudDetectionConfig(
                            fraud_detection_action=["fraudDetectionAction"],
                            fraud_detection_threshold=["fraudDetectionThreshold"],
                            watchlist_ids=["watchlistIds"]
                        )
                    )
                '''
                if isinstance(fraud_detection_config, dict):
                    fraud_detection_config = DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.FraudDetectionConfig(**fraud_detection_config)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__df7e209f5b317b7d4f1827c5a3ce101959046a79f5751d313fb6056f711ed8f2)
                    check_type(argname="argument existing_enrollment_action", value=existing_enrollment_action, expected_type=type_hints["existing_enrollment_action"])
                    check_type(argname="argument fraud_detection_config", value=fraud_detection_config, expected_type=type_hints["fraud_detection_config"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if existing_enrollment_action is not None:
                    self._values["existing_enrollment_action"] = existing_enrollment_action
                if fraud_detection_config is not None:
                    self._values["fraud_detection_config"] = fraud_detection_config

            @builtins.property
            def existing_enrollment_action(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) existingEnrollmentAction property.

                Specify an array of string values to match this event if the actual value of existingEnrollmentAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("existing_enrollment_action")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def fraud_detection_config(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.FraudDetectionConfig"]:
                '''(experimental) fraudDetectionConfig property.

                Specify an array of string values to match this event if the actual value of fraudDetectionConfig is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("fraud_detection_config")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.FraudDetectionConfig"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EnrollmentConfig(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.ErrorInfo",
            jsii_struct_bases=[],
            name_mapping={
                "error_code": "errorCode",
                "error_message": "errorMessage",
                "error_type": "errorType",
            },
        )
        class ErrorInfo:
            def __init__(
                self,
                *,
                error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ErrorInfo.

                :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_type: (experimental) errorType property. Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    error_info = voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.ErrorInfo(
                        error_code=["errorCode"],
                        error_message=["errorMessage"],
                        error_type=["errorType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3c88f011606b046dc56c3a19138ca2a5f575b41ea5e785446a42de9df6912962)
                    check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                    check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
                    check_type(argname="argument error_type", value=error_type, expected_type=type_hints["error_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if error_code is not None:
                    self._values["error_code"] = error_code
                if error_message is not None:
                    self._values["error_message"] = error_message
                if error_type is not None:
                    self._values["error_type"] = error_type

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
            def error_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorType property.

                Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ErrorInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.FraudDetectionConfig",
            jsii_struct_bases=[],
            name_mapping={
                "fraud_detection_action": "fraudDetectionAction",
                "fraud_detection_threshold": "fraudDetectionThreshold",
                "watchlist_ids": "watchlistIds",
            },
        )
        class FraudDetectionConfig:
            def __init__(
                self,
                *,
                fraud_detection_action: typing.Optional[typing.Sequence[builtins.str]] = None,
                fraud_detection_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
                watchlist_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for FraudDetectionConfig.

                :param fraud_detection_action: (experimental) fraudDetectionAction property. Specify an array of string values to match this event if the actual value of fraudDetectionAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param fraud_detection_threshold: (experimental) fraudDetectionThreshold property. Specify an array of string values to match this event if the actual value of fraudDetectionThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param watchlist_ids: (experimental) watchlistIds property. Specify an array of string values to match this event if the actual value of watchlistIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    fraud_detection_config = voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.FraudDetectionConfig(
                        fraud_detection_action=["fraudDetectionAction"],
                        fraud_detection_threshold=["fraudDetectionThreshold"],
                        watchlist_ids=["watchlistIds"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__565ba5678237094adc99f04a7294a5fdc3f527212f1211fc605597bb639738d6)
                    check_type(argname="argument fraud_detection_action", value=fraud_detection_action, expected_type=type_hints["fraud_detection_action"])
                    check_type(argname="argument fraud_detection_threshold", value=fraud_detection_threshold, expected_type=type_hints["fraud_detection_threshold"])
                    check_type(argname="argument watchlist_ids", value=watchlist_ids, expected_type=type_hints["watchlist_ids"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if fraud_detection_action is not None:
                    self._values["fraud_detection_action"] = fraud_detection_action
                if fraud_detection_threshold is not None:
                    self._values["fraud_detection_threshold"] = fraud_detection_threshold
                if watchlist_ids is not None:
                    self._values["watchlist_ids"] = watchlist_ids

            @builtins.property
            def fraud_detection_action(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) fraudDetectionAction property.

                Specify an array of string values to match this event if the actual value of fraudDetectionAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("fraud_detection_action")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def fraud_detection_threshold(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) fraudDetectionThreshold property.

                Specify an array of string values to match this event if the actual value of fraudDetectionThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("fraud_detection_threshold")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def watchlist_ids(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) watchlistIds property.

                Specify an array of string values to match this event if the actual value of watchlistIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("watchlist_ids")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "FraudDetectionConfig(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.InputDataConfig",
            jsii_struct_bases=[],
            name_mapping={"s3_uri": "s3Uri"},
        )
        class InputDataConfig:
            def __init__(
                self,
                *,
                s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for InputDataConfig.

                :param s3_uri: (experimental) s3Uri property. Specify an array of string values to match this event if the actual value of s3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    input_data_config = voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.InputDataConfig(
                        s3_uri=["s3Uri"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__86647f20f73b902c89c2051cba3d3f49fa234c2f21926a48f59175155b375bf5)
                    check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if s3_uri is not None:
                    self._values["s3_uri"] = s3_uri

            @builtins.property
            def s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) s3Uri property.

                Specify an array of string values to match this event if the actual value of s3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "InputDataConfig(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.OutputDataConfig",
            jsii_struct_bases=[],
            name_mapping={"kms_key_id": "kmsKeyId", "s3_uri": "s3Uri"},
        )
        class OutputDataConfig:
            def __init__(
                self,
                *,
                kms_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for OutputDataConfig.

                :param kms_key_id: (experimental) kmsKeyId property. Specify an array of string values to match this event if the actual value of kmsKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_uri: (experimental) s3Uri property. Specify an array of string values to match this event if the actual value of s3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    output_data_config = voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.OutputDataConfig(
                        kms_key_id=["kmsKeyId"],
                        s3_uri=["s3Uri"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cb8eb5564ddc059df5992f642ca913df50de24d973742d0824c12dc25fde5732)
                    check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                    check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if kms_key_id is not None:
                    self._values["kms_key_id"] = kms_key_id
                if s3_uri is not None:
                    self._values["s3_uri"] = s3_uri

            @builtins.property
            def kms_key_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) kmsKeyId property.

                Specify an array of string values to match this event if the actual value of kmsKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("kms_key_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) s3Uri property.

                Specify an array of string values to match this event if the actual value of s3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "OutputDataConfig(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.VoiceIdBatchSpeakerEnrollmentActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "action": "action",
                "batch_job_id": "batchJobId",
                "data": "data",
                "domain_id": "domainId",
                "error_info": "errorInfo",
                "event_metadata": "eventMetadata",
                "source_id": "sourceId",
                "status": "status",
            },
        )
        class VoiceIdBatchSpeakerEnrollmentActionProps:
            def __init__(
                self,
                *,
                action: typing.Optional[typing.Sequence[builtins.str]] = None,
                batch_job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                data: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.Data", typing.Dict[builtins.str, typing.Any]]] = None,
                domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Domain aws.voiceid@VoiceIdBatchSpeakerEnrollmentAction event.

                :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param batch_job_id: (experimental) batchJobId property. Specify an array of string values to match this event if the actual value of batchJobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param data: (experimental) data property. Specify an array of string values to match this event if the actual value of data is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
                :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    voice_id_batch_speaker_enrollment_action_props = voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.VoiceIdBatchSpeakerEnrollmentActionProps(
                        action=["action"],
                        batch_job_id=["batchJobId"],
                        data=voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.Data(
                            data_access_role_arn=["dataAccessRoleArn"],
                            enrollment_config=voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.EnrollmentConfig(
                                existing_enrollment_action=["existingEnrollmentAction"],
                                fraud_detection_config=voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.FraudDetectionConfig(
                                    fraud_detection_action=["fraudDetectionAction"],
                                    fraud_detection_threshold=["fraudDetectionThreshold"],
                                    watchlist_ids=["watchlistIds"]
                                )
                            ),
                            input_data_config=voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.InputDataConfig(
                                s3_uri=["s3Uri"]
                            ),
                            output_data_config=voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.OutputDataConfig(
                                kms_key_id=["kmsKeyId"],
                                s3_uri=["s3Uri"]
                            )
                        ),
                        domain_id=["domainId"],
                        error_info=voiceid_events.DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.ErrorInfo(
                            error_code=["errorCode"],
                            error_message=["errorMessage"],
                            error_type=["errorType"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        source_id=["sourceId"],
                        status=["status"]
                    )
                '''
                if isinstance(data, dict):
                    data = DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.Data(**data)
                if isinstance(error_info, dict):
                    error_info = DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.ErrorInfo(**error_info)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4f028e5d964df2da6b91956836b1ece90266d2f6dea91353ec38cb4ffb62fba8)
                    check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                    check_type(argname="argument batch_job_id", value=batch_job_id, expected_type=type_hints["batch_job_id"])
                    check_type(argname="argument data", value=data, expected_type=type_hints["data"])
                    check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
                    check_type(argname="argument error_info", value=error_info, expected_type=type_hints["error_info"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action is not None:
                    self._values["action"] = action
                if batch_job_id is not None:
                    self._values["batch_job_id"] = batch_job_id
                if data is not None:
                    self._values["data"] = data
                if domain_id is not None:
                    self._values["domain_id"] = domain_id
                if error_info is not None:
                    self._values["error_info"] = error_info
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if source_id is not None:
                    self._values["source_id"] = source_id
                if status is not None:
                    self._values["status"] = status

            @builtins.property
            def action(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) action property.

                Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def batch_job_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) batchJobId property.

                Specify an array of string values to match this event if the actual value of batchJobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("batch_job_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def data(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.Data"]:
                '''(experimental) data property.

                Specify an array of string values to match this event if the actual value of data is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("data")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.Data"], result)

            @builtins.property
            def domain_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domainId property.

                Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Domain reference

                :stability: experimental
                '''
                result = self._values.get("domain_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_info(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.ErrorInfo"]:
                '''(experimental) errorInfo property.

                Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_info")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.ErrorInfo"], result)

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
            def source_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceId property.

                Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_id")
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
                return "VoiceIdBatchSpeakerEnrollmentActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class VoiceIdEvaluateSessionAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdEvaluateSessionAction",
    ):
        '''(experimental) aws.voiceid@VoiceIdEvaluateSessionAction event types for Domain.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
            
            voice_id_evaluate_session_action = voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdEvaluateSessionAction.AuthenticationResult",
            jsii_struct_bases=[],
            name_mapping={
                "audio_aggregation_ended_at": "audioAggregationEndedAt",
                "audio_aggregation_started_at": "audioAggregationStartedAt",
                "authentication_result_id": "authenticationResultId",
                "configuration": "configuration",
                "decision": "decision",
                "score": "score",
            },
        )
        class AuthenticationResult:
            def __init__(
                self,
                *,
                audio_aggregation_ended_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                audio_aggregation_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                authentication_result_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                configuration: typing.Optional[typing.Union["DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
                decision: typing.Optional[typing.Sequence[builtins.str]] = None,
                score: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AuthenticationResult.

                :param audio_aggregation_ended_at: (experimental) audioAggregationEndedAt property. Specify an array of string values to match this event if the actual value of audioAggregationEndedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param audio_aggregation_started_at: (experimental) audioAggregationStartedAt property. Specify an array of string values to match this event if the actual value of audioAggregationStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param authentication_result_id: (experimental) authenticationResultId property. Specify an array of string values to match this event if the actual value of authenticationResultId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param configuration: (experimental) configuration property. Specify an array of string values to match this event if the actual value of configuration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param decision: (experimental) decision property. Specify an array of string values to match this event if the actual value of decision is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param score: (experimental) score property. Specify an array of string values to match this event if the actual value of score is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    authentication_result = voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.AuthenticationResult(
                        audio_aggregation_ended_at=["audioAggregationEndedAt"],
                        audio_aggregation_started_at=["audioAggregationStartedAt"],
                        authentication_result_id=["authenticationResultId"],
                        configuration=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationAuthentication(
                            acceptance_threshold=["acceptanceThreshold"]
                        ),
                        decision=["decision"],
                        score=["score"]
                    )
                '''
                if isinstance(configuration, dict):
                    configuration = DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationAuthentication(**configuration)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__67188cfbeeb840b4474b04ec656ee44e0d3131669c5354837582a96a5dc3de36)
                    check_type(argname="argument audio_aggregation_ended_at", value=audio_aggregation_ended_at, expected_type=type_hints["audio_aggregation_ended_at"])
                    check_type(argname="argument audio_aggregation_started_at", value=audio_aggregation_started_at, expected_type=type_hints["audio_aggregation_started_at"])
                    check_type(argname="argument authentication_result_id", value=authentication_result_id, expected_type=type_hints["authentication_result_id"])
                    check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
                    check_type(argname="argument decision", value=decision, expected_type=type_hints["decision"])
                    check_type(argname="argument score", value=score, expected_type=type_hints["score"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if audio_aggregation_ended_at is not None:
                    self._values["audio_aggregation_ended_at"] = audio_aggregation_ended_at
                if audio_aggregation_started_at is not None:
                    self._values["audio_aggregation_started_at"] = audio_aggregation_started_at
                if authentication_result_id is not None:
                    self._values["authentication_result_id"] = authentication_result_id
                if configuration is not None:
                    self._values["configuration"] = configuration
                if decision is not None:
                    self._values["decision"] = decision
                if score is not None:
                    self._values["score"] = score

            @builtins.property
            def audio_aggregation_ended_at(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) audioAggregationEndedAt property.

                Specify an array of string values to match this event if the actual value of audioAggregationEndedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("audio_aggregation_ended_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def audio_aggregation_started_at(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) audioAggregationStartedAt property.

                Specify an array of string values to match this event if the actual value of audioAggregationStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("audio_aggregation_started_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def authentication_result_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) authenticationResultId property.

                Specify an array of string values to match this event if the actual value of authenticationResultId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("authentication_result_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def configuration(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationAuthentication"]:
                '''(experimental) configuration property.

                Specify an array of string values to match this event if the actual value of configuration is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("configuration")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationAuthentication"], result)

            @builtins.property
            def decision(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) decision property.

                Specify an array of string values to match this event if the actual value of decision is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("decision")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def score(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) score property.

                Specify an array of string values to match this event if the actual value of score is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("score")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AuthenticationResult(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationAuthentication",
            jsii_struct_bases=[],
            name_mapping={"acceptance_threshold": "acceptanceThreshold"},
        )
        class ConfigurationAuthentication:
            def __init__(
                self,
                *,
                acceptance_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Configuration_Authentication.

                :param acceptance_threshold: (experimental) acceptanceThreshold property. Specify an array of string values to match this event if the actual value of acceptanceThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    configuration_authentication = voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationAuthentication(
                        acceptance_threshold=["acceptanceThreshold"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__60a593346645d3529049eab0c6b758c62a52d1430c031ff7a991aab8e9ec5919)
                    check_type(argname="argument acceptance_threshold", value=acceptance_threshold, expected_type=type_hints["acceptance_threshold"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if acceptance_threshold is not None:
                    self._values["acceptance_threshold"] = acceptance_threshold

            @builtins.property
            def acceptance_threshold(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) acceptanceThreshold property.

                Specify an array of string values to match this event if the actual value of acceptanceThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("acceptance_threshold")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ConfigurationAuthentication(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationFraud",
            jsii_struct_bases=[],
            name_mapping={
                "risk_threshold": "riskThreshold",
                "watchlist_id": "watchlistId",
            },
        )
        class ConfigurationFraud:
            def __init__(
                self,
                *,
                risk_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
                watchlist_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Configuration_Fraud.

                :param risk_threshold: (experimental) riskThreshold property. Specify an array of string values to match this event if the actual value of riskThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param watchlist_id: (experimental) watchlistId property. Specify an array of string values to match this event if the actual value of watchlistId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    configuration_fraud = voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationFraud(
                        risk_threshold=["riskThreshold"],
                        watchlist_id=["watchlistId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__42f3b55cba72b1854030dffc86930f781d130f44a2c137acef39c51231b5edee)
                    check_type(argname="argument risk_threshold", value=risk_threshold, expected_type=type_hints["risk_threshold"])
                    check_type(argname="argument watchlist_id", value=watchlist_id, expected_type=type_hints["watchlist_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if risk_threshold is not None:
                    self._values["risk_threshold"] = risk_threshold
                if watchlist_id is not None:
                    self._values["watchlist_id"] = watchlist_id

            @builtins.property
            def risk_threshold(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) riskThreshold property.

                Specify an array of string values to match this event if the actual value of riskThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("risk_threshold")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def watchlist_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) watchlistId property.

                Specify an array of string values to match this event if the actual value of watchlistId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("watchlist_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ConfigurationFraud(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdEvaluateSessionAction.ErrorInfo",
            jsii_struct_bases=[],
            name_mapping={
                "error_code": "errorCode",
                "error_message": "errorMessage",
                "error_type": "errorType",
            },
        )
        class ErrorInfo:
            def __init__(
                self,
                *,
                error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ErrorInfo.

                :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_type: (experimental) errorType property. Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    error_info = voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.ErrorInfo(
                        error_code=["errorCode"],
                        error_message=["errorMessage"],
                        error_type=["errorType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__2898696b3a473bf2616e1cb58cacec8207f14ff4e6343f8720d46b818bbee07f)
                    check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                    check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
                    check_type(argname="argument error_type", value=error_type, expected_type=type_hints["error_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if error_code is not None:
                    self._values["error_code"] = error_code
                if error_message is not None:
                    self._values["error_message"] = error_message
                if error_type is not None:
                    self._values["error_type"] = error_type

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
            def error_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorType property.

                Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ErrorInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdEvaluateSessionAction.FraudDetectionResult",
            jsii_struct_bases=[],
            name_mapping={
                "audio_aggregation_ended_at": "audioAggregationEndedAt",
                "audio_aggregation_started_at": "audioAggregationStartedAt",
                "configuration": "configuration",
                "decision": "decision",
                "fraud_detection_result_id": "fraudDetectionResultId",
                "reasons": "reasons",
                "risk_details": "riskDetails",
            },
        )
        class FraudDetectionResult:
            def __init__(
                self,
                *,
                audio_aggregation_ended_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                audio_aggregation_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                configuration: typing.Optional[typing.Union["DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationFraud", typing.Dict[builtins.str, typing.Any]]] = None,
                decision: typing.Optional[typing.Sequence[builtins.str]] = None,
                fraud_detection_result_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
                risk_details: typing.Optional[typing.Union["DomainEvents.VoiceIdEvaluateSessionAction.RiskDetails", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for FraudDetectionResult.

                :param audio_aggregation_ended_at: (experimental) audioAggregationEndedAt property. Specify an array of string values to match this event if the actual value of audioAggregationEndedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param audio_aggregation_started_at: (experimental) audioAggregationStartedAt property. Specify an array of string values to match this event if the actual value of audioAggregationStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param configuration: (experimental) configuration property. Specify an array of string values to match this event if the actual value of configuration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param decision: (experimental) decision property. Specify an array of string values to match this event if the actual value of decision is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param fraud_detection_result_id: (experimental) fraudDetectionResultId property. Specify an array of string values to match this event if the actual value of fraudDetectionResultId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reasons: (experimental) reasons property. Specify an array of string values to match this event if the actual value of reasons is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param risk_details: (experimental) riskDetails property. Specify an array of string values to match this event if the actual value of riskDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    fraud_detection_result = voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.FraudDetectionResult(
                        audio_aggregation_ended_at=["audioAggregationEndedAt"],
                        audio_aggregation_started_at=["audioAggregationStartedAt"],
                        configuration=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationFraud(
                            risk_threshold=["riskThreshold"],
                            watchlist_id=["watchlistId"]
                        ),
                        decision=["decision"],
                        fraud_detection_result_id=["fraudDetectionResultId"],
                        reasons=["reasons"],
                        risk_details=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.RiskDetails(
                            known_fraudster_risk=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.KnownFraudsterRisk(
                                generated_fraudster_id=["generatedFraudsterId"],
                                risk_score=["riskScore"]
                            ),
                            voice_spoofing_risk=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.VoiceSpoofingRisk(
                                risk_score=["riskScore"]
                            )
                        )
                    )
                '''
                if isinstance(configuration, dict):
                    configuration = DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationFraud(**configuration)
                if isinstance(risk_details, dict):
                    risk_details = DomainEvents.VoiceIdEvaluateSessionAction.RiskDetails(**risk_details)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__d0cc8d92394c25c063e5356e76f1fff762db2a8afc245afb5d92f234b9dba576)
                    check_type(argname="argument audio_aggregation_ended_at", value=audio_aggregation_ended_at, expected_type=type_hints["audio_aggregation_ended_at"])
                    check_type(argname="argument audio_aggregation_started_at", value=audio_aggregation_started_at, expected_type=type_hints["audio_aggregation_started_at"])
                    check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
                    check_type(argname="argument decision", value=decision, expected_type=type_hints["decision"])
                    check_type(argname="argument fraud_detection_result_id", value=fraud_detection_result_id, expected_type=type_hints["fraud_detection_result_id"])
                    check_type(argname="argument reasons", value=reasons, expected_type=type_hints["reasons"])
                    check_type(argname="argument risk_details", value=risk_details, expected_type=type_hints["risk_details"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if audio_aggregation_ended_at is not None:
                    self._values["audio_aggregation_ended_at"] = audio_aggregation_ended_at
                if audio_aggregation_started_at is not None:
                    self._values["audio_aggregation_started_at"] = audio_aggregation_started_at
                if configuration is not None:
                    self._values["configuration"] = configuration
                if decision is not None:
                    self._values["decision"] = decision
                if fraud_detection_result_id is not None:
                    self._values["fraud_detection_result_id"] = fraud_detection_result_id
                if reasons is not None:
                    self._values["reasons"] = reasons
                if risk_details is not None:
                    self._values["risk_details"] = risk_details

            @builtins.property
            def audio_aggregation_ended_at(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) audioAggregationEndedAt property.

                Specify an array of string values to match this event if the actual value of audioAggregationEndedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("audio_aggregation_ended_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def audio_aggregation_started_at(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) audioAggregationStartedAt property.

                Specify an array of string values to match this event if the actual value of audioAggregationStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("audio_aggregation_started_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def configuration(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationFraud"]:
                '''(experimental) configuration property.

                Specify an array of string values to match this event if the actual value of configuration is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("configuration")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationFraud"], result)

            @builtins.property
            def decision(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) decision property.

                Specify an array of string values to match this event if the actual value of decision is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("decision")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def fraud_detection_result_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) fraudDetectionResultId property.

                Specify an array of string values to match this event if the actual value of fraudDetectionResultId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("fraud_detection_result_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def reasons(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) reasons property.

                Specify an array of string values to match this event if the actual value of reasons is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("reasons")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def risk_details(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.RiskDetails"]:
                '''(experimental) riskDetails property.

                Specify an array of string values to match this event if the actual value of riskDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("risk_details")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.RiskDetails"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "FraudDetectionResult(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdEvaluateSessionAction.KnownFraudsterRisk",
            jsii_struct_bases=[],
            name_mapping={
                "generated_fraudster_id": "generatedFraudsterId",
                "risk_score": "riskScore",
            },
        )
        class KnownFraudsterRisk:
            def __init__(
                self,
                *,
                generated_fraudster_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                risk_score: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for KnownFraudsterRisk.

                :param generated_fraudster_id: (experimental) generatedFraudsterId property. Specify an array of string values to match this event if the actual value of generatedFraudsterId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param risk_score: (experimental) riskScore property. Specify an array of string values to match this event if the actual value of riskScore is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    known_fraudster_risk = voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.KnownFraudsterRisk(
                        generated_fraudster_id=["generatedFraudsterId"],
                        risk_score=["riskScore"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__c3f9fbee09c684260a473955f91fc805aaf51e26e9f70ab04ae1db41ccdeb803)
                    check_type(argname="argument generated_fraudster_id", value=generated_fraudster_id, expected_type=type_hints["generated_fraudster_id"])
                    check_type(argname="argument risk_score", value=risk_score, expected_type=type_hints["risk_score"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if generated_fraudster_id is not None:
                    self._values["generated_fraudster_id"] = generated_fraudster_id
                if risk_score is not None:
                    self._values["risk_score"] = risk_score

            @builtins.property
            def generated_fraudster_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) generatedFraudsterId property.

                Specify an array of string values to match this event if the actual value of generatedFraudsterId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("generated_fraudster_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def risk_score(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) riskScore property.

                Specify an array of string values to match this event if the actual value of riskScore is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("risk_score")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "KnownFraudsterRisk(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdEvaluateSessionAction.RiskDetails",
            jsii_struct_bases=[],
            name_mapping={
                "known_fraudster_risk": "knownFraudsterRisk",
                "voice_spoofing_risk": "voiceSpoofingRisk",
            },
        )
        class RiskDetails:
            def __init__(
                self,
                *,
                known_fraudster_risk: typing.Optional[typing.Union["DomainEvents.VoiceIdEvaluateSessionAction.KnownFraudsterRisk", typing.Dict[builtins.str, typing.Any]]] = None,
                voice_spoofing_risk: typing.Optional[typing.Union["DomainEvents.VoiceIdEvaluateSessionAction.VoiceSpoofingRisk", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for RiskDetails.

                :param known_fraudster_risk: (experimental) knownFraudsterRisk property. Specify an array of string values to match this event if the actual value of knownFraudsterRisk is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param voice_spoofing_risk: (experimental) voiceSpoofingRisk property. Specify an array of string values to match this event if the actual value of voiceSpoofingRisk is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    risk_details = voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.RiskDetails(
                        known_fraudster_risk=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.KnownFraudsterRisk(
                            generated_fraudster_id=["generatedFraudsterId"],
                            risk_score=["riskScore"]
                        ),
                        voice_spoofing_risk=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.VoiceSpoofingRisk(
                            risk_score=["riskScore"]
                        )
                    )
                '''
                if isinstance(known_fraudster_risk, dict):
                    known_fraudster_risk = DomainEvents.VoiceIdEvaluateSessionAction.KnownFraudsterRisk(**known_fraudster_risk)
                if isinstance(voice_spoofing_risk, dict):
                    voice_spoofing_risk = DomainEvents.VoiceIdEvaluateSessionAction.VoiceSpoofingRisk(**voice_spoofing_risk)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__e3eeac636e4c4abe2189bf57c6a46b05930c443bc94c10c4cd0e44538ac7936e)
                    check_type(argname="argument known_fraudster_risk", value=known_fraudster_risk, expected_type=type_hints["known_fraudster_risk"])
                    check_type(argname="argument voice_spoofing_risk", value=voice_spoofing_risk, expected_type=type_hints["voice_spoofing_risk"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if known_fraudster_risk is not None:
                    self._values["known_fraudster_risk"] = known_fraudster_risk
                if voice_spoofing_risk is not None:
                    self._values["voice_spoofing_risk"] = voice_spoofing_risk

            @builtins.property
            def known_fraudster_risk(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.KnownFraudsterRisk"]:
                '''(experimental) knownFraudsterRisk property.

                Specify an array of string values to match this event if the actual value of knownFraudsterRisk is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("known_fraudster_risk")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.KnownFraudsterRisk"], result)

            @builtins.property
            def voice_spoofing_risk(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.VoiceSpoofingRisk"]:
                '''(experimental) voiceSpoofingRisk property.

                Specify an array of string values to match this event if the actual value of voiceSpoofingRisk is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("voice_spoofing_risk")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.VoiceSpoofingRisk"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RiskDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdEvaluateSessionAction.Session",
            jsii_struct_bases=[],
            name_mapping={
                "authentication_result": "authenticationResult",
                "fraud_detection_result": "fraudDetectionResult",
                "generated_speaker_id": "generatedSpeakerId",
                "session_id": "sessionId",
                "session_name": "sessionName",
                "streaming_status": "streamingStatus",
            },
        )
        class Session:
            def __init__(
                self,
                *,
                authentication_result: typing.Optional[typing.Union["DomainEvents.VoiceIdEvaluateSessionAction.AuthenticationResult", typing.Dict[builtins.str, typing.Any]]] = None,
                fraud_detection_result: typing.Optional[typing.Union["DomainEvents.VoiceIdEvaluateSessionAction.FraudDetectionResult", typing.Dict[builtins.str, typing.Any]]] = None,
                generated_speaker_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                session_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                session_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                streaming_status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Session.

                :param authentication_result: (experimental) authenticationResult property. Specify an array of string values to match this event if the actual value of authenticationResult is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param fraud_detection_result: (experimental) fraudDetectionResult property. Specify an array of string values to match this event if the actual value of fraudDetectionResult is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param generated_speaker_id: (experimental) generatedSpeakerId property. Specify an array of string values to match this event if the actual value of generatedSpeakerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_id: (experimental) sessionId property. Specify an array of string values to match this event if the actual value of sessionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_name: (experimental) sessionName property. Specify an array of string values to match this event if the actual value of sessionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param streaming_status: (experimental) streamingStatus property. Specify an array of string values to match this event if the actual value of streamingStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    session = voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.Session(
                        authentication_result=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.AuthenticationResult(
                            audio_aggregation_ended_at=["audioAggregationEndedAt"],
                            audio_aggregation_started_at=["audioAggregationStartedAt"],
                            authentication_result_id=["authenticationResultId"],
                            configuration=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationAuthentication(
                                acceptance_threshold=["acceptanceThreshold"]
                            ),
                            decision=["decision"],
                            score=["score"]
                        ),
                        fraud_detection_result=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.FraudDetectionResult(
                            audio_aggregation_ended_at=["audioAggregationEndedAt"],
                            audio_aggregation_started_at=["audioAggregationStartedAt"],
                            configuration=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationFraud(
                                risk_threshold=["riskThreshold"],
                                watchlist_id=["watchlistId"]
                            ),
                            decision=["decision"],
                            fraud_detection_result_id=["fraudDetectionResultId"],
                            reasons=["reasons"],
                            risk_details=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.RiskDetails(
                                known_fraudster_risk=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.KnownFraudsterRisk(
                                    generated_fraudster_id=["generatedFraudsterId"],
                                    risk_score=["riskScore"]
                                ),
                                voice_spoofing_risk=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.VoiceSpoofingRisk(
                                    risk_score=["riskScore"]
                                )
                            )
                        ),
                        generated_speaker_id=["generatedSpeakerId"],
                        session_id=["sessionId"],
                        session_name=["sessionName"],
                        streaming_status=["streamingStatus"]
                    )
                '''
                if isinstance(authentication_result, dict):
                    authentication_result = DomainEvents.VoiceIdEvaluateSessionAction.AuthenticationResult(**authentication_result)
                if isinstance(fraud_detection_result, dict):
                    fraud_detection_result = DomainEvents.VoiceIdEvaluateSessionAction.FraudDetectionResult(**fraud_detection_result)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__9ecc91c62c3c9d2945105c3872626fb5731362acf2af61c26520794773f04421)
                    check_type(argname="argument authentication_result", value=authentication_result, expected_type=type_hints["authentication_result"])
                    check_type(argname="argument fraud_detection_result", value=fraud_detection_result, expected_type=type_hints["fraud_detection_result"])
                    check_type(argname="argument generated_speaker_id", value=generated_speaker_id, expected_type=type_hints["generated_speaker_id"])
                    check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
                    check_type(argname="argument session_name", value=session_name, expected_type=type_hints["session_name"])
                    check_type(argname="argument streaming_status", value=streaming_status, expected_type=type_hints["streaming_status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if authentication_result is not None:
                    self._values["authentication_result"] = authentication_result
                if fraud_detection_result is not None:
                    self._values["fraud_detection_result"] = fraud_detection_result
                if generated_speaker_id is not None:
                    self._values["generated_speaker_id"] = generated_speaker_id
                if session_id is not None:
                    self._values["session_id"] = session_id
                if session_name is not None:
                    self._values["session_name"] = session_name
                if streaming_status is not None:
                    self._values["streaming_status"] = streaming_status

            @builtins.property
            def authentication_result(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.AuthenticationResult"]:
                '''(experimental) authenticationResult property.

                Specify an array of string values to match this event if the actual value of authenticationResult is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("authentication_result")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.AuthenticationResult"], result)

            @builtins.property
            def fraud_detection_result(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.FraudDetectionResult"]:
                '''(experimental) fraudDetectionResult property.

                Specify an array of string values to match this event if the actual value of fraudDetectionResult is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("fraud_detection_result")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.FraudDetectionResult"], result)

            @builtins.property
            def generated_speaker_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) generatedSpeakerId property.

                Specify an array of string values to match this event if the actual value of generatedSpeakerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("generated_speaker_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def session_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sessionId property.

                Specify an array of string values to match this event if the actual value of sessionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def session_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sessionName property.

                Specify an array of string values to match this event if the actual value of sessionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def streaming_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) streamingStatus property.

                Specify an array of string values to match this event if the actual value of streamingStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("streaming_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Session(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdEvaluateSessionAction.SystemAttributes",
            jsii_struct_bases=[],
            name_mapping={
                "aws_connect_original_contact_arn": "awsConnectOriginalContactArn",
            },
        )
        class SystemAttributes:
            def __init__(
                self,
                *,
                aws_connect_original_contact_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SystemAttributes.

                :param aws_connect_original_contact_arn: (experimental) aws-connect-OriginalContactArn property. Specify an array of string values to match this event if the actual value of aws-connect-OriginalContactArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    system_attributes = voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.SystemAttributes(
                        aws_connect_original_contact_arn=["awsConnectOriginalContactArn"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__43fa76ae5e2ee85491a3bbe02c41cb048f2c9a60e20c587681cd0eb7adb7adbd)
                    check_type(argname="argument aws_connect_original_contact_arn", value=aws_connect_original_contact_arn, expected_type=type_hints["aws_connect_original_contact_arn"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if aws_connect_original_contact_arn is not None:
                    self._values["aws_connect_original_contact_arn"] = aws_connect_original_contact_arn

            @builtins.property
            def aws_connect_original_contact_arn(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) aws-connect-OriginalContactArn property.

                Specify an array of string values to match this event if the actual value of aws-connect-OriginalContactArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("aws_connect_original_contact_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SystemAttributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdEvaluateSessionAction.VoiceIdEvaluateSessionActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "action": "action",
                "domain_id": "domainId",
                "error_info": "errorInfo",
                "event_metadata": "eventMetadata",
                "session": "session",
                "source_id": "sourceId",
                "status": "status",
                "system_attributes": "systemAttributes",
            },
        )
        class VoiceIdEvaluateSessionActionProps:
            def __init__(
                self,
                *,
                action: typing.Optional[typing.Sequence[builtins.str]] = None,
                domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdEvaluateSessionAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                session: typing.Optional[typing.Union["DomainEvents.VoiceIdEvaluateSessionAction.Session", typing.Dict[builtins.str, typing.Any]]] = None,
                source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                system_attributes: typing.Optional[typing.Union["DomainEvents.VoiceIdEvaluateSessionAction.SystemAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Domain aws.voiceid@VoiceIdEvaluateSessionAction event.

                :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
                :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param session: (experimental) session property. Specify an array of string values to match this event if the actual value of session is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param system_attributes: (experimental) systemAttributes property. Specify an array of string values to match this event if the actual value of systemAttributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    voice_id_evaluate_session_action_props = voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.VoiceIdEvaluateSessionActionProps(
                        action=["action"],
                        domain_id=["domainId"],
                        error_info=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.ErrorInfo(
                            error_code=["errorCode"],
                            error_message=["errorMessage"],
                            error_type=["errorType"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        session=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.Session(
                            authentication_result=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.AuthenticationResult(
                                audio_aggregation_ended_at=["audioAggregationEndedAt"],
                                audio_aggregation_started_at=["audioAggregationStartedAt"],
                                authentication_result_id=["authenticationResultId"],
                                configuration=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationAuthentication(
                                    acceptance_threshold=["acceptanceThreshold"]
                                ),
                                decision=["decision"],
                                score=["score"]
                            ),
                            fraud_detection_result=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.FraudDetectionResult(
                                audio_aggregation_ended_at=["audioAggregationEndedAt"],
                                audio_aggregation_started_at=["audioAggregationStartedAt"],
                                configuration=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationFraud(
                                    risk_threshold=["riskThreshold"],
                                    watchlist_id=["watchlistId"]
                                ),
                                decision=["decision"],
                                fraud_detection_result_id=["fraudDetectionResultId"],
                                reasons=["reasons"],
                                risk_details=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.RiskDetails(
                                    known_fraudster_risk=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.KnownFraudsterRisk(
                                        generated_fraudster_id=["generatedFraudsterId"],
                                        risk_score=["riskScore"]
                                    ),
                                    voice_spoofing_risk=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.VoiceSpoofingRisk(
                                        risk_score=["riskScore"]
                                    )
                                )
                            ),
                            generated_speaker_id=["generatedSpeakerId"],
                            session_id=["sessionId"],
                            session_name=["sessionName"],
                            streaming_status=["streamingStatus"]
                        ),
                        source_id=["sourceId"],
                        status=["status"],
                        system_attributes=voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.SystemAttributes(
                            aws_connect_original_contact_arn=["awsConnectOriginalContactArn"]
                        )
                    )
                '''
                if isinstance(error_info, dict):
                    error_info = DomainEvents.VoiceIdEvaluateSessionAction.ErrorInfo(**error_info)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(session, dict):
                    session = DomainEvents.VoiceIdEvaluateSessionAction.Session(**session)
                if isinstance(system_attributes, dict):
                    system_attributes = DomainEvents.VoiceIdEvaluateSessionAction.SystemAttributes(**system_attributes)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__188a0c8535858a82e2b77f02385245924a66627388d405c5734e732cbc32844c)
                    check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                    check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
                    check_type(argname="argument error_info", value=error_info, expected_type=type_hints["error_info"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument session", value=session, expected_type=type_hints["session"])
                    check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument system_attributes", value=system_attributes, expected_type=type_hints["system_attributes"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action is not None:
                    self._values["action"] = action
                if domain_id is not None:
                    self._values["domain_id"] = domain_id
                if error_info is not None:
                    self._values["error_info"] = error_info
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if session is not None:
                    self._values["session"] = session
                if source_id is not None:
                    self._values["source_id"] = source_id
                if status is not None:
                    self._values["status"] = status
                if system_attributes is not None:
                    self._values["system_attributes"] = system_attributes

            @builtins.property
            def action(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) action property.

                Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def domain_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domainId property.

                Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Domain reference

                :stability: experimental
                '''
                result = self._values.get("domain_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_info(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.ErrorInfo"]:
                '''(experimental) errorInfo property.

                Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_info")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.ErrorInfo"], result)

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
            def session(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.Session"]:
                '''(experimental) session property.

                Specify an array of string values to match this event if the actual value of session is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.Session"], result)

            @builtins.property
            def source_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceId property.

                Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_id")
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
            def system_attributes(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.SystemAttributes"]:
                '''(experimental) systemAttributes property.

                Specify an array of string values to match this event if the actual value of systemAttributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("system_attributes")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdEvaluateSessionAction.SystemAttributes"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "VoiceIdEvaluateSessionActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdEvaluateSessionAction.VoiceSpoofingRisk",
            jsii_struct_bases=[],
            name_mapping={"risk_score": "riskScore"},
        )
        class VoiceSpoofingRisk:
            def __init__(
                self,
                *,
                risk_score: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for VoiceSpoofingRisk.

                :param risk_score: (experimental) riskScore property. Specify an array of string values to match this event if the actual value of riskScore is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    voice_spoofing_risk = voiceid_events.DomainEvents.VoiceIdEvaluateSessionAction.VoiceSpoofingRisk(
                        risk_score=["riskScore"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__e9c6b96b5dcb6abd3e7ddbfc825b1390dd4f2263577487649da573f3fa52bf5d)
                    check_type(argname="argument risk_score", value=risk_score, expected_type=type_hints["risk_score"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if risk_score is not None:
                    self._values["risk_score"] = risk_score

            @builtins.property
            def risk_score(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) riskScore property.

                Specify an array of string values to match this event if the actual value of riskScore is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("risk_score")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "VoiceSpoofingRisk(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class VoiceIdFraudsterAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdFraudsterAction",
    ):
        '''(experimental) aws.voiceid@VoiceIdFraudsterAction event types for Domain.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
            
            voice_id_fraudster_action = voiceid_events.DomainEvents.VoiceIdFraudsterAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdFraudsterAction.Data",
            jsii_struct_bases=[],
            name_mapping={
                "registration_source": "registrationSource",
                "registration_source_id": "registrationSourceId",
                "registration_status": "registrationStatus",
            },
        )
        class Data:
            def __init__(
                self,
                *,
                registration_source: typing.Optional[typing.Sequence[builtins.str]] = None,
                registration_source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                registration_status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Data.

                :param registration_source: (experimental) registrationSource property. Specify an array of string values to match this event if the actual value of registrationSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param registration_source_id: (experimental) registrationSourceId property. Specify an array of string values to match this event if the actual value of registrationSourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param registration_status: (experimental) registrationStatus property. Specify an array of string values to match this event if the actual value of registrationStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    data = voiceid_events.DomainEvents.VoiceIdFraudsterAction.Data(
                        registration_source=["registrationSource"],
                        registration_source_id=["registrationSourceId"],
                        registration_status=["registrationStatus"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f1196e98eb4556a66a8c1b94493cda94ef144e7b3ecd684ce68b0ce556d5c66d)
                    check_type(argname="argument registration_source", value=registration_source, expected_type=type_hints["registration_source"])
                    check_type(argname="argument registration_source_id", value=registration_source_id, expected_type=type_hints["registration_source_id"])
                    check_type(argname="argument registration_status", value=registration_status, expected_type=type_hints["registration_status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if registration_source is not None:
                    self._values["registration_source"] = registration_source
                if registration_source_id is not None:
                    self._values["registration_source_id"] = registration_source_id
                if registration_status is not None:
                    self._values["registration_status"] = registration_status

            @builtins.property
            def registration_source(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) registrationSource property.

                Specify an array of string values to match this event if the actual value of registrationSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("registration_source")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def registration_source_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) registrationSourceId property.

                Specify an array of string values to match this event if the actual value of registrationSourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("registration_source_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def registration_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) registrationStatus property.

                Specify an array of string values to match this event if the actual value of registrationStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("registration_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Data(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdFraudsterAction.ErrorInfo",
            jsii_struct_bases=[],
            name_mapping={
                "error_code": "errorCode",
                "error_message": "errorMessage",
                "error_type": "errorType",
            },
        )
        class ErrorInfo:
            def __init__(
                self,
                *,
                error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ErrorInfo.

                :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_type: (experimental) errorType property. Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    error_info = voiceid_events.DomainEvents.VoiceIdFraudsterAction.ErrorInfo(
                        error_code=["errorCode"],
                        error_message=["errorMessage"],
                        error_type=["errorType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__c5d56ee588eeb39fe7f57709c30db1774ae31a617de3fe0849152d250af9412e)
                    check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                    check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
                    check_type(argname="argument error_type", value=error_type, expected_type=type_hints["error_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if error_code is not None:
                    self._values["error_code"] = error_code
                if error_message is not None:
                    self._values["error_message"] = error_message
                if error_type is not None:
                    self._values["error_type"] = error_type

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
            def error_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorType property.

                Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ErrorInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdFraudsterAction.VoiceIdFraudsterActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "action": "action",
                "data": "data",
                "domain_id": "domainId",
                "error_info": "errorInfo",
                "event_metadata": "eventMetadata",
                "generated_fraudster_id": "generatedFraudsterId",
                "source_id": "sourceId",
                "status": "status",
                "watchlist_ids": "watchlistIds",
            },
        )
        class VoiceIdFraudsterActionProps:
            def __init__(
                self,
                *,
                action: typing.Optional[typing.Sequence[builtins.str]] = None,
                data: typing.Optional[typing.Union["DomainEvents.VoiceIdFraudsterAction.Data", typing.Dict[builtins.str, typing.Any]]] = None,
                domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdFraudsterAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                generated_fraudster_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                watchlist_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Domain aws.voiceid@VoiceIdFraudsterAction event.

                :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param data: (experimental) data property. Specify an array of string values to match this event if the actual value of data is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
                :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param generated_fraudster_id: (experimental) generatedFraudsterId property. Specify an array of string values to match this event if the actual value of generatedFraudsterId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param watchlist_ids: (experimental) watchlistIds property. Specify an array of string values to match this event if the actual value of watchlistIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    voice_id_fraudster_action_props = voiceid_events.DomainEvents.VoiceIdFraudsterAction.VoiceIdFraudsterActionProps(
                        action=["action"],
                        data=voiceid_events.DomainEvents.VoiceIdFraudsterAction.Data(
                            registration_source=["registrationSource"],
                            registration_source_id=["registrationSourceId"],
                            registration_status=["registrationStatus"]
                        ),
                        domain_id=["domainId"],
                        error_info=voiceid_events.DomainEvents.VoiceIdFraudsterAction.ErrorInfo(
                            error_code=["errorCode"],
                            error_message=["errorMessage"],
                            error_type=["errorType"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        generated_fraudster_id=["generatedFraudsterId"],
                        source_id=["sourceId"],
                        status=["status"],
                        watchlist_ids=["watchlistIds"]
                    )
                '''
                if isinstance(data, dict):
                    data = DomainEvents.VoiceIdFraudsterAction.Data(**data)
                if isinstance(error_info, dict):
                    error_info = DomainEvents.VoiceIdFraudsterAction.ErrorInfo(**error_info)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7a6c8efcc3231771e5a8785a4b46e58f525e2706cc8a07bf13f48cc5ac646e41)
                    check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                    check_type(argname="argument data", value=data, expected_type=type_hints["data"])
                    check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
                    check_type(argname="argument error_info", value=error_info, expected_type=type_hints["error_info"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument generated_fraudster_id", value=generated_fraudster_id, expected_type=type_hints["generated_fraudster_id"])
                    check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument watchlist_ids", value=watchlist_ids, expected_type=type_hints["watchlist_ids"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action is not None:
                    self._values["action"] = action
                if data is not None:
                    self._values["data"] = data
                if domain_id is not None:
                    self._values["domain_id"] = domain_id
                if error_info is not None:
                    self._values["error_info"] = error_info
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if generated_fraudster_id is not None:
                    self._values["generated_fraudster_id"] = generated_fraudster_id
                if source_id is not None:
                    self._values["source_id"] = source_id
                if status is not None:
                    self._values["status"] = status
                if watchlist_ids is not None:
                    self._values["watchlist_ids"] = watchlist_ids

            @builtins.property
            def action(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) action property.

                Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def data(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdFraudsterAction.Data"]:
                '''(experimental) data property.

                Specify an array of string values to match this event if the actual value of data is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("data")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdFraudsterAction.Data"], result)

            @builtins.property
            def domain_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domainId property.

                Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Domain reference

                :stability: experimental
                '''
                result = self._values.get("domain_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_info(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdFraudsterAction.ErrorInfo"]:
                '''(experimental) errorInfo property.

                Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_info")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdFraudsterAction.ErrorInfo"], result)

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
            def generated_fraudster_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) generatedFraudsterId property.

                Specify an array of string values to match this event if the actual value of generatedFraudsterId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("generated_fraudster_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceId property.

                Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_id")
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
            def watchlist_ids(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) watchlistIds property.

                Specify an array of string values to match this event if the actual value of watchlistIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("watchlist_ids")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "VoiceIdFraudsterActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class VoiceIdSessionSpeakerEnrollmentAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdSessionSpeakerEnrollmentAction",
    ):
        '''(experimental) aws.voiceid@VoiceIdSessionSpeakerEnrollmentAction event types for Domain.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
            
            voice_id_session_speaker_enrollment_action = voiceid_events.DomainEvents.VoiceIdSessionSpeakerEnrollmentAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.ErrorInfo",
            jsii_struct_bases=[],
            name_mapping={
                "error_code": "errorCode",
                "error_message": "errorMessage",
                "error_type": "errorType",
            },
        )
        class ErrorInfo:
            def __init__(
                self,
                *,
                error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ErrorInfo.

                :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_type: (experimental) errorType property. Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    error_info = voiceid_events.DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.ErrorInfo(
                        error_code=["errorCode"],
                        error_message=["errorMessage"],
                        error_type=["errorType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1d67418843d23793653f5cebf9e1909b2c1dc63c7d04589db171eb0b426d3c61)
                    check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                    check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
                    check_type(argname="argument error_type", value=error_type, expected_type=type_hints["error_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if error_code is not None:
                    self._values["error_code"] = error_code
                if error_message is not None:
                    self._values["error_message"] = error_message
                if error_type is not None:
                    self._values["error_type"] = error_type

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
            def error_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorType property.

                Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ErrorInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.SystemAttributes",
            jsii_struct_bases=[],
            name_mapping={
                "aws_connect_original_contact_arn": "awsConnectOriginalContactArn",
            },
        )
        class SystemAttributes:
            def __init__(
                self,
                *,
                aws_connect_original_contact_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SystemAttributes.

                :param aws_connect_original_contact_arn: (experimental) aws-connect-OriginalContactArn property. Specify an array of string values to match this event if the actual value of aws-connect-OriginalContactArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    system_attributes = voiceid_events.DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.SystemAttributes(
                        aws_connect_original_contact_arn=["awsConnectOriginalContactArn"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__fe12c7f19f688dc43f12dad9cd110421674ba603447af542ff5c127baed6d2af)
                    check_type(argname="argument aws_connect_original_contact_arn", value=aws_connect_original_contact_arn, expected_type=type_hints["aws_connect_original_contact_arn"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if aws_connect_original_contact_arn is not None:
                    self._values["aws_connect_original_contact_arn"] = aws_connect_original_contact_arn

            @builtins.property
            def aws_connect_original_contact_arn(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) aws-connect-OriginalContactArn property.

                Specify an array of string values to match this event if the actual value of aws-connect-OriginalContactArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("aws_connect_original_contact_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SystemAttributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.VoiceIdSessionSpeakerEnrollmentActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "action": "action",
                "domain_id": "domainId",
                "error_info": "errorInfo",
                "event_metadata": "eventMetadata",
                "session_id": "sessionId",
                "session_name": "sessionName",
                "source_id": "sourceId",
                "status": "status",
                "system_attributes": "systemAttributes",
            },
        )
        class VoiceIdSessionSpeakerEnrollmentActionProps:
            def __init__(
                self,
                *,
                action: typing.Optional[typing.Sequence[builtins.str]] = None,
                domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                session_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                session_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                system_attributes: typing.Optional[typing.Union["DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.SystemAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Domain aws.voiceid@VoiceIdSessionSpeakerEnrollmentAction event.

                :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
                :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param session_id: (experimental) sessionId property. Specify an array of string values to match this event if the actual value of sessionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_name: (experimental) sessionName property. Specify an array of string values to match this event if the actual value of sessionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param system_attributes: (experimental) systemAttributes property. Specify an array of string values to match this event if the actual value of systemAttributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    voice_id_session_speaker_enrollment_action_props = voiceid_events.DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.VoiceIdSessionSpeakerEnrollmentActionProps(
                        action=["action"],
                        domain_id=["domainId"],
                        error_info=voiceid_events.DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.ErrorInfo(
                            error_code=["errorCode"],
                            error_message=["errorMessage"],
                            error_type=["errorType"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        session_id=["sessionId"],
                        session_name=["sessionName"],
                        source_id=["sourceId"],
                        status=["status"],
                        system_attributes=voiceid_events.DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.SystemAttributes(
                            aws_connect_original_contact_arn=["awsConnectOriginalContactArn"]
                        )
                    )
                '''
                if isinstance(error_info, dict):
                    error_info = DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.ErrorInfo(**error_info)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(system_attributes, dict):
                    system_attributes = DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.SystemAttributes(**system_attributes)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cfe646d8f97550f2115c0d38ac6fb9f06b8ce7474a324d721277697e2facbe62)
                    check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                    check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
                    check_type(argname="argument error_info", value=error_info, expected_type=type_hints["error_info"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
                    check_type(argname="argument session_name", value=session_name, expected_type=type_hints["session_name"])
                    check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument system_attributes", value=system_attributes, expected_type=type_hints["system_attributes"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action is not None:
                    self._values["action"] = action
                if domain_id is not None:
                    self._values["domain_id"] = domain_id
                if error_info is not None:
                    self._values["error_info"] = error_info
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if session_id is not None:
                    self._values["session_id"] = session_id
                if session_name is not None:
                    self._values["session_name"] = session_name
                if source_id is not None:
                    self._values["source_id"] = source_id
                if status is not None:
                    self._values["status"] = status
                if system_attributes is not None:
                    self._values["system_attributes"] = system_attributes

            @builtins.property
            def action(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) action property.

                Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def domain_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domainId property.

                Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Domain reference

                :stability: experimental
                '''
                result = self._values.get("domain_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_info(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.ErrorInfo"]:
                '''(experimental) errorInfo property.

                Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_info")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.ErrorInfo"], result)

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
            def session_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sessionId property.

                Specify an array of string values to match this event if the actual value of sessionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def session_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sessionName property.

                Specify an array of string values to match this event if the actual value of sessionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceId property.

                Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_id")
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
            def system_attributes(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.SystemAttributes"]:
                '''(experimental) systemAttributes property.

                Specify an array of string values to match this event if the actual value of systemAttributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("system_attributes")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.SystemAttributes"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "VoiceIdSessionSpeakerEnrollmentActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class VoiceIdSpeakerAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdSpeakerAction",
    ):
        '''(experimental) aws.voiceid@VoiceIdSpeakerAction event types for Domain.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
            
            voice_id_speaker_action = voiceid_events.DomainEvents.VoiceIdSpeakerAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdSpeakerAction.Data",
            jsii_struct_bases=[],
            name_mapping={
                "enrollment_source": "enrollmentSource",
                "enrollment_source_id": "enrollmentSourceId",
                "enrollment_status": "enrollmentStatus",
            },
        )
        class Data:
            def __init__(
                self,
                *,
                enrollment_source: typing.Optional[typing.Sequence[builtins.str]] = None,
                enrollment_source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                enrollment_status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Data.

                :param enrollment_source: (experimental) enrollmentSource property. Specify an array of string values to match this event if the actual value of enrollmentSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param enrollment_source_id: (experimental) enrollmentSourceId property. Specify an array of string values to match this event if the actual value of enrollmentSourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param enrollment_status: (experimental) enrollmentStatus property. Specify an array of string values to match this event if the actual value of enrollmentStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    data = voiceid_events.DomainEvents.VoiceIdSpeakerAction.Data(
                        enrollment_source=["enrollmentSource"],
                        enrollment_source_id=["enrollmentSourceId"],
                        enrollment_status=["enrollmentStatus"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8d9bf1d22ac92cf1abf9e4a2494a44b594474e2a01cdb4c022483d2b606be3e2)
                    check_type(argname="argument enrollment_source", value=enrollment_source, expected_type=type_hints["enrollment_source"])
                    check_type(argname="argument enrollment_source_id", value=enrollment_source_id, expected_type=type_hints["enrollment_source_id"])
                    check_type(argname="argument enrollment_status", value=enrollment_status, expected_type=type_hints["enrollment_status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if enrollment_source is not None:
                    self._values["enrollment_source"] = enrollment_source
                if enrollment_source_id is not None:
                    self._values["enrollment_source_id"] = enrollment_source_id
                if enrollment_status is not None:
                    self._values["enrollment_status"] = enrollment_status

            @builtins.property
            def enrollment_source(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) enrollmentSource property.

                Specify an array of string values to match this event if the actual value of enrollmentSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("enrollment_source")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def enrollment_source_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) enrollmentSourceId property.

                Specify an array of string values to match this event if the actual value of enrollmentSourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("enrollment_source_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def enrollment_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) enrollmentStatus property.

                Specify an array of string values to match this event if the actual value of enrollmentStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("enrollment_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Data(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdSpeakerAction.ErrorInfo",
            jsii_struct_bases=[],
            name_mapping={
                "error_code": "errorCode",
                "error_message": "errorMessage",
                "error_type": "errorType",
            },
        )
        class ErrorInfo:
            def __init__(
                self,
                *,
                error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ErrorInfo.

                :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_type: (experimental) errorType property. Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    error_info = voiceid_events.DomainEvents.VoiceIdSpeakerAction.ErrorInfo(
                        error_code=["errorCode"],
                        error_message=["errorMessage"],
                        error_type=["errorType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__62c1377d499a281b526b6167115fdc0766eee9edac8895e0f22b43d8516fa8d7)
                    check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                    check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
                    check_type(argname="argument error_type", value=error_type, expected_type=type_hints["error_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if error_code is not None:
                    self._values["error_code"] = error_code
                if error_message is not None:
                    self._values["error_message"] = error_message
                if error_type is not None:
                    self._values["error_type"] = error_type

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
            def error_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorType property.

                Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ErrorInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdSpeakerAction.SystemAttributes",
            jsii_struct_bases=[],
            name_mapping={
                "aws_connect_original_contact_arn": "awsConnectOriginalContactArn",
            },
        )
        class SystemAttributes:
            def __init__(
                self,
                *,
                aws_connect_original_contact_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SystemAttributes.

                :param aws_connect_original_contact_arn: (experimental) aws-connect-OriginalContactArn property. Specify an array of string values to match this event if the actual value of aws-connect-OriginalContactArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    system_attributes = voiceid_events.DomainEvents.VoiceIdSpeakerAction.SystemAttributes(
                        aws_connect_original_contact_arn=["awsConnectOriginalContactArn"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__bd1af6060a30dfe851d2d68dbd4e03aaa97919a3c66c83b229956d0d82bca189)
                    check_type(argname="argument aws_connect_original_contact_arn", value=aws_connect_original_contact_arn, expected_type=type_hints["aws_connect_original_contact_arn"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if aws_connect_original_contact_arn is not None:
                    self._values["aws_connect_original_contact_arn"] = aws_connect_original_contact_arn

            @builtins.property
            def aws_connect_original_contact_arn(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) aws-connect-OriginalContactArn property.

                Specify an array of string values to match this event if the actual value of aws-connect-OriginalContactArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("aws_connect_original_contact_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SystemAttributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdSpeakerAction.VoiceIdSpeakerActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "action": "action",
                "data": "data",
                "domain_id": "domainId",
                "error_info": "errorInfo",
                "event_metadata": "eventMetadata",
                "generated_speaker_id": "generatedSpeakerId",
                "source_id": "sourceId",
                "status": "status",
                "system_attributes": "systemAttributes",
            },
        )
        class VoiceIdSpeakerActionProps:
            def __init__(
                self,
                *,
                action: typing.Optional[typing.Sequence[builtins.str]] = None,
                data: typing.Optional[typing.Union["DomainEvents.VoiceIdSpeakerAction.Data", typing.Dict[builtins.str, typing.Any]]] = None,
                domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdSpeakerAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                generated_speaker_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                system_attributes: typing.Optional[typing.Union["DomainEvents.VoiceIdSpeakerAction.SystemAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Domain aws.voiceid@VoiceIdSpeakerAction event.

                :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param data: (experimental) data property. Specify an array of string values to match this event if the actual value of data is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
                :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param generated_speaker_id: (experimental) generatedSpeakerId property. Specify an array of string values to match this event if the actual value of generatedSpeakerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param system_attributes: (experimental) systemAttributes property. Specify an array of string values to match this event if the actual value of systemAttributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    voice_id_speaker_action_props = voiceid_events.DomainEvents.VoiceIdSpeakerAction.VoiceIdSpeakerActionProps(
                        action=["action"],
                        data=voiceid_events.DomainEvents.VoiceIdSpeakerAction.Data(
                            enrollment_source=["enrollmentSource"],
                            enrollment_source_id=["enrollmentSourceId"],
                            enrollment_status=["enrollmentStatus"]
                        ),
                        domain_id=["domainId"],
                        error_info=voiceid_events.DomainEvents.VoiceIdSpeakerAction.ErrorInfo(
                            error_code=["errorCode"],
                            error_message=["errorMessage"],
                            error_type=["errorType"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        generated_speaker_id=["generatedSpeakerId"],
                        source_id=["sourceId"],
                        status=["status"],
                        system_attributes=voiceid_events.DomainEvents.VoiceIdSpeakerAction.SystemAttributes(
                            aws_connect_original_contact_arn=["awsConnectOriginalContactArn"]
                        )
                    )
                '''
                if isinstance(data, dict):
                    data = DomainEvents.VoiceIdSpeakerAction.Data(**data)
                if isinstance(error_info, dict):
                    error_info = DomainEvents.VoiceIdSpeakerAction.ErrorInfo(**error_info)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(system_attributes, dict):
                    system_attributes = DomainEvents.VoiceIdSpeakerAction.SystemAttributes(**system_attributes)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__d08c14b97468d7b8ab1374a8202031cd8d24623c6af62ec89156ed96d66b3a44)
                    check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                    check_type(argname="argument data", value=data, expected_type=type_hints["data"])
                    check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
                    check_type(argname="argument error_info", value=error_info, expected_type=type_hints["error_info"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument generated_speaker_id", value=generated_speaker_id, expected_type=type_hints["generated_speaker_id"])
                    check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument system_attributes", value=system_attributes, expected_type=type_hints["system_attributes"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action is not None:
                    self._values["action"] = action
                if data is not None:
                    self._values["data"] = data
                if domain_id is not None:
                    self._values["domain_id"] = domain_id
                if error_info is not None:
                    self._values["error_info"] = error_info
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if generated_speaker_id is not None:
                    self._values["generated_speaker_id"] = generated_speaker_id
                if source_id is not None:
                    self._values["source_id"] = source_id
                if status is not None:
                    self._values["status"] = status
                if system_attributes is not None:
                    self._values["system_attributes"] = system_attributes

            @builtins.property
            def action(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) action property.

                Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def data(self) -> typing.Optional["DomainEvents.VoiceIdSpeakerAction.Data"]:
                '''(experimental) data property.

                Specify an array of string values to match this event if the actual value of data is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("data")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdSpeakerAction.Data"], result)

            @builtins.property
            def domain_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domainId property.

                Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Domain reference

                :stability: experimental
                '''
                result = self._values.get("domain_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_info(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdSpeakerAction.ErrorInfo"]:
                '''(experimental) errorInfo property.

                Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_info")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdSpeakerAction.ErrorInfo"], result)

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
            def generated_speaker_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) generatedSpeakerId property.

                Specify an array of string values to match this event if the actual value of generatedSpeakerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("generated_speaker_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceId property.

                Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_id")
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
            def system_attributes(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdSpeakerAction.SystemAttributes"]:
                '''(experimental) systemAttributes property.

                Specify an array of string values to match this event if the actual value of systemAttributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("system_attributes")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdSpeakerAction.SystemAttributes"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "VoiceIdSpeakerActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class VoiceIdStartSessionAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdStartSessionAction",
    ):
        '''(experimental) aws.voiceid@VoiceIdStartSessionAction event types for Domain.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
            
            voice_id_start_session_action = voiceid_events.DomainEvents.VoiceIdStartSessionAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress",
            jsii_struct_bases=[],
            name_mapping={
                "audio_aggregation_ended_at": "audioAggregationEndedAt",
                "audio_aggregation_started_at": "audioAggregationStartedAt",
            },
        )
        class AuthenticationAudioProgress:
            def __init__(
                self,
                *,
                audio_aggregation_ended_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                audio_aggregation_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AuthenticationAudioProgress.

                :param audio_aggregation_ended_at: (experimental) audioAggregationEndedAt property. Specify an array of string values to match this event if the actual value of audioAggregationEndedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param audio_aggregation_started_at: (experimental) audioAggregationStartedAt property. Specify an array of string values to match this event if the actual value of audioAggregationStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    authentication_audio_progress = voiceid_events.DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress(
                        audio_aggregation_ended_at=["audioAggregationEndedAt"],
                        audio_aggregation_started_at=["audioAggregationStartedAt"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cf083acb72b298a9d2cfaa479e77bbe43d50e95c2dc27cbb83f7d2db05ba61e8)
                    check_type(argname="argument audio_aggregation_ended_at", value=audio_aggregation_ended_at, expected_type=type_hints["audio_aggregation_ended_at"])
                    check_type(argname="argument audio_aggregation_started_at", value=audio_aggregation_started_at, expected_type=type_hints["audio_aggregation_started_at"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if audio_aggregation_ended_at is not None:
                    self._values["audio_aggregation_ended_at"] = audio_aggregation_ended_at
                if audio_aggregation_started_at is not None:
                    self._values["audio_aggregation_started_at"] = audio_aggregation_started_at

            @builtins.property
            def audio_aggregation_ended_at(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) audioAggregationEndedAt property.

                Specify an array of string values to match this event if the actual value of audioAggregationEndedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("audio_aggregation_ended_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def audio_aggregation_started_at(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) audioAggregationStartedAt property.

                Specify an array of string values to match this event if the actual value of audioAggregationStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("audio_aggregation_started_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AuthenticationAudioProgress(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdStartSessionAction.AuthenticationConfiguration",
            jsii_struct_bases=[],
            name_mapping={"acceptance_threshold": "acceptanceThreshold"},
        )
        class AuthenticationConfiguration:
            def __init__(
                self,
                *,
                acceptance_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AuthenticationConfiguration.

                :param acceptance_threshold: (experimental) acceptanceThreshold property. Specify an array of string values to match this event if the actual value of acceptanceThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    authentication_configuration = voiceid_events.DomainEvents.VoiceIdStartSessionAction.AuthenticationConfiguration(
                        acceptance_threshold=["acceptanceThreshold"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f30538e9979097eeca9d1d5f45ecef9c34abca8f491f8a6b0f96d34a933fd1ac)
                    check_type(argname="argument acceptance_threshold", value=acceptance_threshold, expected_type=type_hints["acceptance_threshold"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if acceptance_threshold is not None:
                    self._values["acceptance_threshold"] = acceptance_threshold

            @builtins.property
            def acceptance_threshold(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) acceptanceThreshold property.

                Specify an array of string values to match this event if the actual value of acceptanceThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("acceptance_threshold")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AuthenticationConfiguration(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdStartSessionAction.EnrollmentAudioProgress",
            jsii_struct_bases=[],
            name_mapping={
                "audio_aggregation_ended_at": "audioAggregationEndedAt",
                "audio_aggregation_started_at": "audioAggregationStartedAt",
                "audio_aggregation_status": "audioAggregationStatus",
            },
        )
        class EnrollmentAudioProgress:
            def __init__(
                self,
                *,
                audio_aggregation_ended_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                audio_aggregation_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                audio_aggregation_status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for EnrollmentAudioProgress.

                :param audio_aggregation_ended_at: (experimental) audioAggregationEndedAt property. Specify an array of string values to match this event if the actual value of audioAggregationEndedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param audio_aggregation_started_at: (experimental) audioAggregationStartedAt property. Specify an array of string values to match this event if the actual value of audioAggregationStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param audio_aggregation_status: (experimental) audioAggregationStatus property. Specify an array of string values to match this event if the actual value of audioAggregationStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    enrollment_audio_progress = voiceid_events.DomainEvents.VoiceIdStartSessionAction.EnrollmentAudioProgress(
                        audio_aggregation_ended_at=["audioAggregationEndedAt"],
                        audio_aggregation_started_at=["audioAggregationStartedAt"],
                        audio_aggregation_status=["audioAggregationStatus"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ec4ec0c32df4be058bf2c8820b15271e96c1ecdc53a5de64a11a884f57b32c71)
                    check_type(argname="argument audio_aggregation_ended_at", value=audio_aggregation_ended_at, expected_type=type_hints["audio_aggregation_ended_at"])
                    check_type(argname="argument audio_aggregation_started_at", value=audio_aggregation_started_at, expected_type=type_hints["audio_aggregation_started_at"])
                    check_type(argname="argument audio_aggregation_status", value=audio_aggregation_status, expected_type=type_hints["audio_aggregation_status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if audio_aggregation_ended_at is not None:
                    self._values["audio_aggregation_ended_at"] = audio_aggregation_ended_at
                if audio_aggregation_started_at is not None:
                    self._values["audio_aggregation_started_at"] = audio_aggregation_started_at
                if audio_aggregation_status is not None:
                    self._values["audio_aggregation_status"] = audio_aggregation_status

            @builtins.property
            def audio_aggregation_ended_at(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) audioAggregationEndedAt property.

                Specify an array of string values to match this event if the actual value of audioAggregationEndedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("audio_aggregation_ended_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def audio_aggregation_started_at(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) audioAggregationStartedAt property.

                Specify an array of string values to match this event if the actual value of audioAggregationStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("audio_aggregation_started_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def audio_aggregation_status(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) audioAggregationStatus property.

                Specify an array of string values to match this event if the actual value of audioAggregationStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("audio_aggregation_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EnrollmentAudioProgress(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdStartSessionAction.ErrorInfo",
            jsii_struct_bases=[],
            name_mapping={
                "error_code": "errorCode",
                "error_message": "errorMessage",
                "error_type": "errorType",
            },
        )
        class ErrorInfo:
            def __init__(
                self,
                *,
                error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ErrorInfo.

                :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_type: (experimental) errorType property. Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    error_info = voiceid_events.DomainEvents.VoiceIdStartSessionAction.ErrorInfo(
                        error_code=["errorCode"],
                        error_message=["errorMessage"],
                        error_type=["errorType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__2e19b21f7f0c51a914c2975036d4a91547c22f800a98dcac37159cf18ecec5e3)
                    check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                    check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
                    check_type(argname="argument error_type", value=error_type, expected_type=type_hints["error_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if error_code is not None:
                    self._values["error_code"] = error_code
                if error_message is not None:
                    self._values["error_message"] = error_message
                if error_type is not None:
                    self._values["error_type"] = error_type

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
            def error_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorType property.

                Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ErrorInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdStartSessionAction.FraudDetectionConfiguration",
            jsii_struct_bases=[],
            name_mapping={
                "risk_threshold": "riskThreshold",
                "watchlist_id": "watchlistId",
            },
        )
        class FraudDetectionConfiguration:
            def __init__(
                self,
                *,
                risk_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
                watchlist_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for FraudDetectionConfiguration.

                :param risk_threshold: (experimental) riskThreshold property. Specify an array of string values to match this event if the actual value of riskThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param watchlist_id: (experimental) watchlistId property. Specify an array of string values to match this event if the actual value of watchlistId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    fraud_detection_configuration = voiceid_events.DomainEvents.VoiceIdStartSessionAction.FraudDetectionConfiguration(
                        risk_threshold=["riskThreshold"],
                        watchlist_id=["watchlistId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8dd24420ad562cc233a6b7a03d87854a1f80438b0921dc981a95c01142eee9e1)
                    check_type(argname="argument risk_threshold", value=risk_threshold, expected_type=type_hints["risk_threshold"])
                    check_type(argname="argument watchlist_id", value=watchlist_id, expected_type=type_hints["watchlist_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if risk_threshold is not None:
                    self._values["risk_threshold"] = risk_threshold
                if watchlist_id is not None:
                    self._values["watchlist_id"] = watchlist_id

            @builtins.property
            def risk_threshold(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) riskThreshold property.

                Specify an array of string values to match this event if the actual value of riskThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("risk_threshold")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def watchlist_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) watchlistId property.

                Specify an array of string values to match this event if the actual value of watchlistId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("watchlist_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "FraudDetectionConfiguration(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdStartSessionAction.Session",
            jsii_struct_bases=[],
            name_mapping={
                "authentication_audio_progress": "authenticationAudioProgress",
                "authentication_configuration": "authenticationConfiguration",
                "enrollment_audio_progress": "enrollmentAudioProgress",
                "fraud_detection_audio_progress": "fraudDetectionAudioProgress",
                "fraud_detection_configuration": "fraudDetectionConfiguration",
                "generated_speaker_id": "generatedSpeakerId",
                "session_id": "sessionId",
                "session_name": "sessionName",
                "streaming_configuration": "streamingConfiguration",
            },
        )
        class Session:
            def __init__(
                self,
                *,
                authentication_audio_progress: typing.Optional[typing.Union["DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress", typing.Dict[builtins.str, typing.Any]]] = None,
                authentication_configuration: typing.Optional[typing.Union["DomainEvents.VoiceIdStartSessionAction.AuthenticationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
                enrollment_audio_progress: typing.Optional[typing.Union["DomainEvents.VoiceIdStartSessionAction.EnrollmentAudioProgress", typing.Dict[builtins.str, typing.Any]]] = None,
                fraud_detection_audio_progress: typing.Optional[typing.Union["DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress", typing.Dict[builtins.str, typing.Any]]] = None,
                fraud_detection_configuration: typing.Optional[typing.Union["DomainEvents.VoiceIdStartSessionAction.FraudDetectionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
                generated_speaker_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                session_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                session_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                streaming_configuration: typing.Optional[typing.Union["DomainEvents.VoiceIdStartSessionAction.StreamingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for Session.

                :param authentication_audio_progress: (experimental) authenticationAudioProgress property. Specify an array of string values to match this event if the actual value of authenticationAudioProgress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param authentication_configuration: (experimental) authenticationConfiguration property. Specify an array of string values to match this event if the actual value of authenticationConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param enrollment_audio_progress: (experimental) enrollmentAudioProgress property. Specify an array of string values to match this event if the actual value of enrollmentAudioProgress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param fraud_detection_audio_progress: (experimental) fraudDetectionAudioProgress property. Specify an array of string values to match this event if the actual value of fraudDetectionAudioProgress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param fraud_detection_configuration: (experimental) fraudDetectionConfiguration property. Specify an array of string values to match this event if the actual value of fraudDetectionConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param generated_speaker_id: (experimental) generatedSpeakerId property. Specify an array of string values to match this event if the actual value of generatedSpeakerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_id: (experimental) sessionId property. Specify an array of string values to match this event if the actual value of sessionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_name: (experimental) sessionName property. Specify an array of string values to match this event if the actual value of sessionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param streaming_configuration: (experimental) streamingConfiguration property. Specify an array of string values to match this event if the actual value of streamingConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    session = voiceid_events.DomainEvents.VoiceIdStartSessionAction.Session(
                        authentication_audio_progress=voiceid_events.DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress(
                            audio_aggregation_ended_at=["audioAggregationEndedAt"],
                            audio_aggregation_started_at=["audioAggregationStartedAt"]
                        ),
                        authentication_configuration=voiceid_events.DomainEvents.VoiceIdStartSessionAction.AuthenticationConfiguration(
                            acceptance_threshold=["acceptanceThreshold"]
                        ),
                        enrollment_audio_progress=voiceid_events.DomainEvents.VoiceIdStartSessionAction.EnrollmentAudioProgress(
                            audio_aggregation_ended_at=["audioAggregationEndedAt"],
                            audio_aggregation_started_at=["audioAggregationStartedAt"],
                            audio_aggregation_status=["audioAggregationStatus"]
                        ),
                        fraud_detection_audio_progress=voiceid_events.DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress(
                            audio_aggregation_ended_at=["audioAggregationEndedAt"],
                            audio_aggregation_started_at=["audioAggregationStartedAt"]
                        ),
                        fraud_detection_configuration=voiceid_events.DomainEvents.VoiceIdStartSessionAction.FraudDetectionConfiguration(
                            risk_threshold=["riskThreshold"],
                            watchlist_id=["watchlistId"]
                        ),
                        generated_speaker_id=["generatedSpeakerId"],
                        session_id=["sessionId"],
                        session_name=["sessionName"],
                        streaming_configuration=voiceid_events.DomainEvents.VoiceIdStartSessionAction.StreamingConfiguration(
                            authentication_minimum_speech_in_seconds=["authenticationMinimumSpeechInSeconds"]
                        )
                    )
                '''
                if isinstance(authentication_audio_progress, dict):
                    authentication_audio_progress = DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress(**authentication_audio_progress)
                if isinstance(authentication_configuration, dict):
                    authentication_configuration = DomainEvents.VoiceIdStartSessionAction.AuthenticationConfiguration(**authentication_configuration)
                if isinstance(enrollment_audio_progress, dict):
                    enrollment_audio_progress = DomainEvents.VoiceIdStartSessionAction.EnrollmentAudioProgress(**enrollment_audio_progress)
                if isinstance(fraud_detection_audio_progress, dict):
                    fraud_detection_audio_progress = DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress(**fraud_detection_audio_progress)
                if isinstance(fraud_detection_configuration, dict):
                    fraud_detection_configuration = DomainEvents.VoiceIdStartSessionAction.FraudDetectionConfiguration(**fraud_detection_configuration)
                if isinstance(streaming_configuration, dict):
                    streaming_configuration = DomainEvents.VoiceIdStartSessionAction.StreamingConfiguration(**streaming_configuration)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a2ff184270a984b38b3260fd63b96c648f6d262c499492b894cc2fc6ef235d6b)
                    check_type(argname="argument authentication_audio_progress", value=authentication_audio_progress, expected_type=type_hints["authentication_audio_progress"])
                    check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
                    check_type(argname="argument enrollment_audio_progress", value=enrollment_audio_progress, expected_type=type_hints["enrollment_audio_progress"])
                    check_type(argname="argument fraud_detection_audio_progress", value=fraud_detection_audio_progress, expected_type=type_hints["fraud_detection_audio_progress"])
                    check_type(argname="argument fraud_detection_configuration", value=fraud_detection_configuration, expected_type=type_hints["fraud_detection_configuration"])
                    check_type(argname="argument generated_speaker_id", value=generated_speaker_id, expected_type=type_hints["generated_speaker_id"])
                    check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
                    check_type(argname="argument session_name", value=session_name, expected_type=type_hints["session_name"])
                    check_type(argname="argument streaming_configuration", value=streaming_configuration, expected_type=type_hints["streaming_configuration"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if authentication_audio_progress is not None:
                    self._values["authentication_audio_progress"] = authentication_audio_progress
                if authentication_configuration is not None:
                    self._values["authentication_configuration"] = authentication_configuration
                if enrollment_audio_progress is not None:
                    self._values["enrollment_audio_progress"] = enrollment_audio_progress
                if fraud_detection_audio_progress is not None:
                    self._values["fraud_detection_audio_progress"] = fraud_detection_audio_progress
                if fraud_detection_configuration is not None:
                    self._values["fraud_detection_configuration"] = fraud_detection_configuration
                if generated_speaker_id is not None:
                    self._values["generated_speaker_id"] = generated_speaker_id
                if session_id is not None:
                    self._values["session_id"] = session_id
                if session_name is not None:
                    self._values["session_name"] = session_name
                if streaming_configuration is not None:
                    self._values["streaming_configuration"] = streaming_configuration

            @builtins.property
            def authentication_audio_progress(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress"]:
                '''(experimental) authenticationAudioProgress property.

                Specify an array of string values to match this event if the actual value of authenticationAudioProgress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("authentication_audio_progress")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress"], result)

            @builtins.property
            def authentication_configuration(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdStartSessionAction.AuthenticationConfiguration"]:
                '''(experimental) authenticationConfiguration property.

                Specify an array of string values to match this event if the actual value of authenticationConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("authentication_configuration")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdStartSessionAction.AuthenticationConfiguration"], result)

            @builtins.property
            def enrollment_audio_progress(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdStartSessionAction.EnrollmentAudioProgress"]:
                '''(experimental) enrollmentAudioProgress property.

                Specify an array of string values to match this event if the actual value of enrollmentAudioProgress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("enrollment_audio_progress")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdStartSessionAction.EnrollmentAudioProgress"], result)

            @builtins.property
            def fraud_detection_audio_progress(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress"]:
                '''(experimental) fraudDetectionAudioProgress property.

                Specify an array of string values to match this event if the actual value of fraudDetectionAudioProgress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("fraud_detection_audio_progress")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress"], result)

            @builtins.property
            def fraud_detection_configuration(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdStartSessionAction.FraudDetectionConfiguration"]:
                '''(experimental) fraudDetectionConfiguration property.

                Specify an array of string values to match this event if the actual value of fraudDetectionConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("fraud_detection_configuration")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdStartSessionAction.FraudDetectionConfiguration"], result)

            @builtins.property
            def generated_speaker_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) generatedSpeakerId property.

                Specify an array of string values to match this event if the actual value of generatedSpeakerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("generated_speaker_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def session_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sessionId property.

                Specify an array of string values to match this event if the actual value of sessionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def session_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sessionName property.

                Specify an array of string values to match this event if the actual value of sessionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def streaming_configuration(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdStartSessionAction.StreamingConfiguration"]:
                '''(experimental) streamingConfiguration property.

                Specify an array of string values to match this event if the actual value of streamingConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("streaming_configuration")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdStartSessionAction.StreamingConfiguration"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Session(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdStartSessionAction.StreamingConfiguration",
            jsii_struct_bases=[],
            name_mapping={
                "authentication_minimum_speech_in_seconds": "authenticationMinimumSpeechInSeconds",
            },
        )
        class StreamingConfiguration:
            def __init__(
                self,
                *,
                authentication_minimum_speech_in_seconds: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for StreamingConfiguration.

                :param authentication_minimum_speech_in_seconds: (experimental) authenticationMinimumSpeechInSeconds property. Specify an array of string values to match this event if the actual value of authenticationMinimumSpeechInSeconds is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    streaming_configuration = voiceid_events.DomainEvents.VoiceIdStartSessionAction.StreamingConfiguration(
                        authentication_minimum_speech_in_seconds=["authenticationMinimumSpeechInSeconds"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ad4245f00f7bf7ad96d3332dc49fc0cff3d6707431abb7a3848cdaff6c4e85a0)
                    check_type(argname="argument authentication_minimum_speech_in_seconds", value=authentication_minimum_speech_in_seconds, expected_type=type_hints["authentication_minimum_speech_in_seconds"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if authentication_minimum_speech_in_seconds is not None:
                    self._values["authentication_minimum_speech_in_seconds"] = authentication_minimum_speech_in_seconds

            @builtins.property
            def authentication_minimum_speech_in_seconds(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) authenticationMinimumSpeechInSeconds property.

                Specify an array of string values to match this event if the actual value of authenticationMinimumSpeechInSeconds is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("authentication_minimum_speech_in_seconds")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "StreamingConfiguration(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdStartSessionAction.SystemAttributes",
            jsii_struct_bases=[],
            name_mapping={
                "aws_connect_original_contact_arn": "awsConnectOriginalContactArn",
            },
        )
        class SystemAttributes:
            def __init__(
                self,
                *,
                aws_connect_original_contact_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SystemAttributes.

                :param aws_connect_original_contact_arn: (experimental) aws-connect-OriginalContactArn property. Specify an array of string values to match this event if the actual value of aws-connect-OriginalContactArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    system_attributes = voiceid_events.DomainEvents.VoiceIdStartSessionAction.SystemAttributes(
                        aws_connect_original_contact_arn=["awsConnectOriginalContactArn"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__fc5dff58538b4b312e6e9d5f0ae9d32d38029b0aad0b132be56ea1f9e18207e4)
                    check_type(argname="argument aws_connect_original_contact_arn", value=aws_connect_original_contact_arn, expected_type=type_hints["aws_connect_original_contact_arn"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if aws_connect_original_contact_arn is not None:
                    self._values["aws_connect_original_contact_arn"] = aws_connect_original_contact_arn

            @builtins.property
            def aws_connect_original_contact_arn(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) aws-connect-OriginalContactArn property.

                Specify an array of string values to match this event if the actual value of aws-connect-OriginalContactArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("aws_connect_original_contact_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SystemAttributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdStartSessionAction.VoiceIdStartSessionActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "action": "action",
                "domain_id": "domainId",
                "error_info": "errorInfo",
                "event_metadata": "eventMetadata",
                "session": "session",
                "source_id": "sourceId",
                "status": "status",
                "system_attributes": "systemAttributes",
            },
        )
        class VoiceIdStartSessionActionProps:
            def __init__(
                self,
                *,
                action: typing.Optional[typing.Sequence[builtins.str]] = None,
                domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdStartSessionAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                session: typing.Optional[typing.Union["DomainEvents.VoiceIdStartSessionAction.Session", typing.Dict[builtins.str, typing.Any]]] = None,
                source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                system_attributes: typing.Optional[typing.Union["DomainEvents.VoiceIdStartSessionAction.SystemAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Domain aws.voiceid@VoiceIdStartSessionAction event.

                :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
                :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param session: (experimental) session property. Specify an array of string values to match this event if the actual value of session is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param system_attributes: (experimental) systemAttributes property. Specify an array of string values to match this event if the actual value of systemAttributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    voice_id_start_session_action_props = voiceid_events.DomainEvents.VoiceIdStartSessionAction.VoiceIdStartSessionActionProps(
                        action=["action"],
                        domain_id=["domainId"],
                        error_info=voiceid_events.DomainEvents.VoiceIdStartSessionAction.ErrorInfo(
                            error_code=["errorCode"],
                            error_message=["errorMessage"],
                            error_type=["errorType"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        session=voiceid_events.DomainEvents.VoiceIdStartSessionAction.Session(
                            authentication_audio_progress=voiceid_events.DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress(
                                audio_aggregation_ended_at=["audioAggregationEndedAt"],
                                audio_aggregation_started_at=["audioAggregationStartedAt"]
                            ),
                            authentication_configuration=voiceid_events.DomainEvents.VoiceIdStartSessionAction.AuthenticationConfiguration(
                                acceptance_threshold=["acceptanceThreshold"]
                            ),
                            enrollment_audio_progress=voiceid_events.DomainEvents.VoiceIdStartSessionAction.EnrollmentAudioProgress(
                                audio_aggregation_ended_at=["audioAggregationEndedAt"],
                                audio_aggregation_started_at=["audioAggregationStartedAt"],
                                audio_aggregation_status=["audioAggregationStatus"]
                            ),
                            fraud_detection_audio_progress=voiceid_events.DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress(
                                audio_aggregation_ended_at=["audioAggregationEndedAt"],
                                audio_aggregation_started_at=["audioAggregationStartedAt"]
                            ),
                            fraud_detection_configuration=voiceid_events.DomainEvents.VoiceIdStartSessionAction.FraudDetectionConfiguration(
                                risk_threshold=["riskThreshold"],
                                watchlist_id=["watchlistId"]
                            ),
                            generated_speaker_id=["generatedSpeakerId"],
                            session_id=["sessionId"],
                            session_name=["sessionName"],
                            streaming_configuration=voiceid_events.DomainEvents.VoiceIdStartSessionAction.StreamingConfiguration(
                                authentication_minimum_speech_in_seconds=["authenticationMinimumSpeechInSeconds"]
                            )
                        ),
                        source_id=["sourceId"],
                        status=["status"],
                        system_attributes=voiceid_events.DomainEvents.VoiceIdStartSessionAction.SystemAttributes(
                            aws_connect_original_contact_arn=["awsConnectOriginalContactArn"]
                        )
                    )
                '''
                if isinstance(error_info, dict):
                    error_info = DomainEvents.VoiceIdStartSessionAction.ErrorInfo(**error_info)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(session, dict):
                    session = DomainEvents.VoiceIdStartSessionAction.Session(**session)
                if isinstance(system_attributes, dict):
                    system_attributes = DomainEvents.VoiceIdStartSessionAction.SystemAttributes(**system_attributes)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__13ccf6196b3dd1015b3181c6f264b6b21ac25355986c764ff13037eb7c9d88db)
                    check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                    check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
                    check_type(argname="argument error_info", value=error_info, expected_type=type_hints["error_info"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument session", value=session, expected_type=type_hints["session"])
                    check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument system_attributes", value=system_attributes, expected_type=type_hints["system_attributes"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action is not None:
                    self._values["action"] = action
                if domain_id is not None:
                    self._values["domain_id"] = domain_id
                if error_info is not None:
                    self._values["error_info"] = error_info
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if session is not None:
                    self._values["session"] = session
                if source_id is not None:
                    self._values["source_id"] = source_id
                if status is not None:
                    self._values["status"] = status
                if system_attributes is not None:
                    self._values["system_attributes"] = system_attributes

            @builtins.property
            def action(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) action property.

                Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def domain_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domainId property.

                Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Domain reference

                :stability: experimental
                '''
                result = self._values.get("domain_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_info(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdStartSessionAction.ErrorInfo"]:
                '''(experimental) errorInfo property.

                Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_info")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdStartSessionAction.ErrorInfo"], result)

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
            def session(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdStartSessionAction.Session"]:
                '''(experimental) session property.

                Specify an array of string values to match this event if the actual value of session is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdStartSessionAction.Session"], result)

            @builtins.property
            def source_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceId property.

                Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_id")
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
            def system_attributes(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdStartSessionAction.SystemAttributes"]:
                '''(experimental) systemAttributes property.

                Specify an array of string values to match this event if the actual value of systemAttributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("system_attributes")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdStartSessionAction.SystemAttributes"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "VoiceIdStartSessionActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class VoiceIdUpdateSessionAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdUpdateSessionAction",
    ):
        '''(experimental) aws.voiceid@VoiceIdUpdateSessionAction event types for Domain.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
            
            voice_id_update_session_action = voiceid_events.DomainEvents.VoiceIdUpdateSessionAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdUpdateSessionAction.AuthenticationConfiguration",
            jsii_struct_bases=[],
            name_mapping={"acceptance_threshold": "acceptanceThreshold"},
        )
        class AuthenticationConfiguration:
            def __init__(
                self,
                *,
                acceptance_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AuthenticationConfiguration.

                :param acceptance_threshold: (experimental) acceptanceThreshold property. Specify an array of string values to match this event if the actual value of acceptanceThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    authentication_configuration = voiceid_events.DomainEvents.VoiceIdUpdateSessionAction.AuthenticationConfiguration(
                        acceptance_threshold=["acceptanceThreshold"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__401384b4c88c000a907af2ab3b5cb4036f17b318d4819f7398d61d55c2441ee9)
                    check_type(argname="argument acceptance_threshold", value=acceptance_threshold, expected_type=type_hints["acceptance_threshold"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if acceptance_threshold is not None:
                    self._values["acceptance_threshold"] = acceptance_threshold

            @builtins.property
            def acceptance_threshold(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) acceptanceThreshold property.

                Specify an array of string values to match this event if the actual value of acceptanceThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("acceptance_threshold")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AuthenticationConfiguration(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdUpdateSessionAction.ErrorInfo",
            jsii_struct_bases=[],
            name_mapping={
                "error_code": "errorCode",
                "error_message": "errorMessage",
                "error_type": "errorType",
            },
        )
        class ErrorInfo:
            def __init__(
                self,
                *,
                error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ErrorInfo.

                :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_type: (experimental) errorType property. Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    error_info = voiceid_events.DomainEvents.VoiceIdUpdateSessionAction.ErrorInfo(
                        error_code=["errorCode"],
                        error_message=["errorMessage"],
                        error_type=["errorType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__94dfe63b7d17df027f513bfaa8525522b1424ba4747e8f66163639a4d1f72b77)
                    check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                    check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
                    check_type(argname="argument error_type", value=error_type, expected_type=type_hints["error_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if error_code is not None:
                    self._values["error_code"] = error_code
                if error_message is not None:
                    self._values["error_message"] = error_message
                if error_type is not None:
                    self._values["error_type"] = error_type

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
            def error_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorType property.

                Specify an array of string values to match this event if the actual value of errorType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ErrorInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdUpdateSessionAction.FraudDetectionConfiguration",
            jsii_struct_bases=[],
            name_mapping={
                "risk_threshold": "riskThreshold",
                "watchlist_id": "watchlistId",
            },
        )
        class FraudDetectionConfiguration:
            def __init__(
                self,
                *,
                risk_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
                watchlist_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for FraudDetectionConfiguration.

                :param risk_threshold: (experimental) riskThreshold property. Specify an array of string values to match this event if the actual value of riskThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param watchlist_id: (experimental) watchlistId property. Specify an array of string values to match this event if the actual value of watchlistId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    fraud_detection_configuration = voiceid_events.DomainEvents.VoiceIdUpdateSessionAction.FraudDetectionConfiguration(
                        risk_threshold=["riskThreshold"],
                        watchlist_id=["watchlistId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__5d55bf77bdc4d66799343d1f9b22b344c2a23bda4d303373151080939676e900)
                    check_type(argname="argument risk_threshold", value=risk_threshold, expected_type=type_hints["risk_threshold"])
                    check_type(argname="argument watchlist_id", value=watchlist_id, expected_type=type_hints["watchlist_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if risk_threshold is not None:
                    self._values["risk_threshold"] = risk_threshold
                if watchlist_id is not None:
                    self._values["watchlist_id"] = watchlist_id

            @builtins.property
            def risk_threshold(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) riskThreshold property.

                Specify an array of string values to match this event if the actual value of riskThreshold is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("risk_threshold")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def watchlist_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) watchlistId property.

                Specify an array of string values to match this event if the actual value of watchlistId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("watchlist_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "FraudDetectionConfiguration(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdUpdateSessionAction.Session",
            jsii_struct_bases=[],
            name_mapping={
                "authentication_configuration": "authenticationConfiguration",
                "fraud_detection_configuration": "fraudDetectionConfiguration",
                "generated_speaker_id": "generatedSpeakerId",
                "session_id": "sessionId",
                "session_name": "sessionName",
            },
        )
        class Session:
            def __init__(
                self,
                *,
                authentication_configuration: typing.Optional[typing.Union["DomainEvents.VoiceIdUpdateSessionAction.AuthenticationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
                fraud_detection_configuration: typing.Optional[typing.Union["DomainEvents.VoiceIdUpdateSessionAction.FraudDetectionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
                generated_speaker_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                session_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                session_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Session.

                :param authentication_configuration: (experimental) authenticationConfiguration property. Specify an array of string values to match this event if the actual value of authenticationConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param fraud_detection_configuration: (experimental) fraudDetectionConfiguration property. Specify an array of string values to match this event if the actual value of fraudDetectionConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param generated_speaker_id: (experimental) generatedSpeakerId property. Specify an array of string values to match this event if the actual value of generatedSpeakerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_id: (experimental) sessionId property. Specify an array of string values to match this event if the actual value of sessionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_name: (experimental) sessionName property. Specify an array of string values to match this event if the actual value of sessionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    session = voiceid_events.DomainEvents.VoiceIdUpdateSessionAction.Session(
                        authentication_configuration=voiceid_events.DomainEvents.VoiceIdUpdateSessionAction.AuthenticationConfiguration(
                            acceptance_threshold=["acceptanceThreshold"]
                        ),
                        fraud_detection_configuration=voiceid_events.DomainEvents.VoiceIdUpdateSessionAction.FraudDetectionConfiguration(
                            risk_threshold=["riskThreshold"],
                            watchlist_id=["watchlistId"]
                        ),
                        generated_speaker_id=["generatedSpeakerId"],
                        session_id=["sessionId"],
                        session_name=["sessionName"]
                    )
                '''
                if isinstance(authentication_configuration, dict):
                    authentication_configuration = DomainEvents.VoiceIdUpdateSessionAction.AuthenticationConfiguration(**authentication_configuration)
                if isinstance(fraud_detection_configuration, dict):
                    fraud_detection_configuration = DomainEvents.VoiceIdUpdateSessionAction.FraudDetectionConfiguration(**fraud_detection_configuration)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__43cb56cb2eaee0eb2ccf5546bc65b59e62256aa524fa78d42c95c878f6576ebb)
                    check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
                    check_type(argname="argument fraud_detection_configuration", value=fraud_detection_configuration, expected_type=type_hints["fraud_detection_configuration"])
                    check_type(argname="argument generated_speaker_id", value=generated_speaker_id, expected_type=type_hints["generated_speaker_id"])
                    check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
                    check_type(argname="argument session_name", value=session_name, expected_type=type_hints["session_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if authentication_configuration is not None:
                    self._values["authentication_configuration"] = authentication_configuration
                if fraud_detection_configuration is not None:
                    self._values["fraud_detection_configuration"] = fraud_detection_configuration
                if generated_speaker_id is not None:
                    self._values["generated_speaker_id"] = generated_speaker_id
                if session_id is not None:
                    self._values["session_id"] = session_id
                if session_name is not None:
                    self._values["session_name"] = session_name

            @builtins.property
            def authentication_configuration(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdUpdateSessionAction.AuthenticationConfiguration"]:
                '''(experimental) authenticationConfiguration property.

                Specify an array of string values to match this event if the actual value of authenticationConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("authentication_configuration")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdUpdateSessionAction.AuthenticationConfiguration"], result)

            @builtins.property
            def fraud_detection_configuration(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdUpdateSessionAction.FraudDetectionConfiguration"]:
                '''(experimental) fraudDetectionConfiguration property.

                Specify an array of string values to match this event if the actual value of fraudDetectionConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("fraud_detection_configuration")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdUpdateSessionAction.FraudDetectionConfiguration"], result)

            @builtins.property
            def generated_speaker_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) generatedSpeakerId property.

                Specify an array of string values to match this event if the actual value of generatedSpeakerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("generated_speaker_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def session_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sessionId property.

                Specify an array of string values to match this event if the actual value of sessionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def session_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sessionName property.

                Specify an array of string values to match this event if the actual value of sessionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Session(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_voiceid.events.DomainEvents.VoiceIdUpdateSessionAction.VoiceIdUpdateSessionActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "action": "action",
                "domain_id": "domainId",
                "error_info": "errorInfo",
                "event_metadata": "eventMetadata",
                "session": "session",
                "source_id": "sourceId",
                "status": "status",
            },
        )
        class VoiceIdUpdateSessionActionProps:
            def __init__(
                self,
                *,
                action: typing.Optional[typing.Sequence[builtins.str]] = None,
                domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_info: typing.Optional[typing.Union["DomainEvents.VoiceIdUpdateSessionAction.ErrorInfo", typing.Dict[builtins.str, typing.Any]]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                session: typing.Optional[typing.Union["DomainEvents.VoiceIdUpdateSessionAction.Session", typing.Dict[builtins.str, typing.Any]]] = None,
                source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Domain aws.voiceid@VoiceIdUpdateSessionAction event.

                :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain_id: (experimental) domainId property. Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Domain reference
                :param error_info: (experimental) errorInfo property. Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param session: (experimental) session property. Specify an array of string values to match this event if the actual value of session is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_id: (experimental) sourceId property. Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_voiceid import events as voiceid_events
                    
                    voice_id_update_session_action_props = voiceid_events.DomainEvents.VoiceIdUpdateSessionAction.VoiceIdUpdateSessionActionProps(
                        action=["action"],
                        domain_id=["domainId"],
                        error_info=voiceid_events.DomainEvents.VoiceIdUpdateSessionAction.ErrorInfo(
                            error_code=["errorCode"],
                            error_message=["errorMessage"],
                            error_type=["errorType"]
                        ),
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        session=voiceid_events.DomainEvents.VoiceIdUpdateSessionAction.Session(
                            authentication_configuration=voiceid_events.DomainEvents.VoiceIdUpdateSessionAction.AuthenticationConfiguration(
                                acceptance_threshold=["acceptanceThreshold"]
                            ),
                            fraud_detection_configuration=voiceid_events.DomainEvents.VoiceIdUpdateSessionAction.FraudDetectionConfiguration(
                                risk_threshold=["riskThreshold"],
                                watchlist_id=["watchlistId"]
                            ),
                            generated_speaker_id=["generatedSpeakerId"],
                            session_id=["sessionId"],
                            session_name=["sessionName"]
                        ),
                        source_id=["sourceId"],
                        status=["status"]
                    )
                '''
                if isinstance(error_info, dict):
                    error_info = DomainEvents.VoiceIdUpdateSessionAction.ErrorInfo(**error_info)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(session, dict):
                    session = DomainEvents.VoiceIdUpdateSessionAction.Session(**session)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__82a142eef5dae115926fd9065654237e4abe1c7bd036c3708d157edbf2696e9f)
                    check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                    check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
                    check_type(argname="argument error_info", value=error_info, expected_type=type_hints["error_info"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument session", value=session, expected_type=type_hints["session"])
                    check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action is not None:
                    self._values["action"] = action
                if domain_id is not None:
                    self._values["domain_id"] = domain_id
                if error_info is not None:
                    self._values["error_info"] = error_info
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if session is not None:
                    self._values["session"] = session
                if source_id is not None:
                    self._values["source_id"] = source_id
                if status is not None:
                    self._values["status"] = status

            @builtins.property
            def action(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) action property.

                Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def domain_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domainId property.

                Specify an array of string values to match this event if the actual value of domainId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Domain reference

                :stability: experimental
                '''
                result = self._values.get("domain_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_info(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdUpdateSessionAction.ErrorInfo"]:
                '''(experimental) errorInfo property.

                Specify an array of string values to match this event if the actual value of errorInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_info")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdUpdateSessionAction.ErrorInfo"], result)

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
            def session(
                self,
            ) -> typing.Optional["DomainEvents.VoiceIdUpdateSessionAction.Session"]:
                '''(experimental) session property.

                Specify an array of string values to match this event if the actual value of session is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session")
                return typing.cast(typing.Optional["DomainEvents.VoiceIdUpdateSessionAction.Session"], result)

            @builtins.property
            def source_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceId property.

                Specify an array of string values to match this event if the actual value of sourceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_id")
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
                return "VoiceIdUpdateSessionActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "DomainEvents",
]

publication.publish()

def _typecheckingstub__33f136a5b85b027f97dcce5d4bbabc0519a38dbb97bb11a589a536ecbfd7c0d4(
    domain_ref: _aws_cdk_interfaces_aws_voiceid_ceddda9d.IDomainRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396b26ac89eb581bd6fd72cf0e1e832a1beedc3db353c67952bbdca24be84551(
    *,
    data_access_role_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    input_data_config: typing.Optional[typing.Union[DomainEvents.VoiceIdBatchFraudsterRegistrationAction.InputDataConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    output_data_config: typing.Optional[typing.Union[DomainEvents.VoiceIdBatchFraudsterRegistrationAction.OutputDataConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    registration_config: typing.Optional[typing.Union[DomainEvents.VoiceIdBatchFraudsterRegistrationAction.RegistrationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d0357b1b8c442687b26d583da68aae954cc71bc3a1edb012084848d65a24d6(
    *,
    error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36f15ec2c6a2d41369d9c0be8c9bee8869d412f149935ff16ad5f79a770bf21(
    *,
    s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6237ab3ffe7bceabaece456aae247052cf26a52e017e3c61727438b7103f88(
    *,
    kms_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8277cda7c5c958dba46f0c7cf2b21ab830ae6e9c3f8f1787303396d88554bccd(
    *,
    duplicate_registration_action: typing.Optional[typing.Sequence[builtins.str]] = None,
    fraudster_similarity_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
    watchlist_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded054e2738839ba6b4e9b215aa52ac626ce97a6a6fa39b279cbfb095967f047(
    *,
    action: typing.Optional[typing.Sequence[builtins.str]] = None,
    batch_job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    data: typing.Optional[typing.Union[DomainEvents.VoiceIdBatchFraudsterRegistrationAction.Data, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_info: typing.Optional[typing.Union[DomainEvents.VoiceIdBatchFraudsterRegistrationAction.ErrorInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898854956c3e5b208c13f073ddbc897bc3b6c858a2f7eeb30b8f3dd47ad929f3(
    *,
    data_access_role_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    enrollment_config: typing.Optional[typing.Union[DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.EnrollmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    input_data_config: typing.Optional[typing.Union[DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.InputDataConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    output_data_config: typing.Optional[typing.Union[DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.OutputDataConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7e209f5b317b7d4f1827c5a3ce101959046a79f5751d313fb6056f711ed8f2(
    *,
    existing_enrollment_action: typing.Optional[typing.Sequence[builtins.str]] = None,
    fraud_detection_config: typing.Optional[typing.Union[DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.FraudDetectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c88f011606b046dc56c3a19138ca2a5f575b41ea5e785446a42de9df6912962(
    *,
    error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__565ba5678237094adc99f04a7294a5fdc3f527212f1211fc605597bb639738d6(
    *,
    fraud_detection_action: typing.Optional[typing.Sequence[builtins.str]] = None,
    fraud_detection_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
    watchlist_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86647f20f73b902c89c2051cba3d3f49fa234c2f21926a48f59175155b375bf5(
    *,
    s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb8eb5564ddc059df5992f642ca913df50de24d973742d0824c12dc25fde5732(
    *,
    kms_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f028e5d964df2da6b91956836b1ece90266d2f6dea91353ec38cb4ffb62fba8(
    *,
    action: typing.Optional[typing.Sequence[builtins.str]] = None,
    batch_job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    data: typing.Optional[typing.Union[DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.Data, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_info: typing.Optional[typing.Union[DomainEvents.VoiceIdBatchSpeakerEnrollmentAction.ErrorInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67188cfbeeb840b4474b04ec656ee44e0d3131669c5354837582a96a5dc3de36(
    *,
    audio_aggregation_ended_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    audio_aggregation_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    authentication_result_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    configuration: typing.Optional[typing.Union[DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    decision: typing.Optional[typing.Sequence[builtins.str]] = None,
    score: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a593346645d3529049eab0c6b758c62a52d1430c031ff7a991aab8e9ec5919(
    *,
    acceptance_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f3b55cba72b1854030dffc86930f781d130f44a2c137acef39c51231b5edee(
    *,
    risk_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
    watchlist_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2898696b3a473bf2616e1cb58cacec8207f14ff4e6343f8720d46b818bbee07f(
    *,
    error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0cc8d92394c25c063e5356e76f1fff762db2a8afc245afb5d92f234b9dba576(
    *,
    audio_aggregation_ended_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    audio_aggregation_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    configuration: typing.Optional[typing.Union[DomainEvents.VoiceIdEvaluateSessionAction.ConfigurationFraud, typing.Dict[builtins.str, typing.Any]]] = None,
    decision: typing.Optional[typing.Sequence[builtins.str]] = None,
    fraud_detection_result_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
    risk_details: typing.Optional[typing.Union[DomainEvents.VoiceIdEvaluateSessionAction.RiskDetails, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f9fbee09c684260a473955f91fc805aaf51e26e9f70ab04ae1db41ccdeb803(
    *,
    generated_fraudster_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    risk_score: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3eeac636e4c4abe2189bf57c6a46b05930c443bc94c10c4cd0e44538ac7936e(
    *,
    known_fraudster_risk: typing.Optional[typing.Union[DomainEvents.VoiceIdEvaluateSessionAction.KnownFraudsterRisk, typing.Dict[builtins.str, typing.Any]]] = None,
    voice_spoofing_risk: typing.Optional[typing.Union[DomainEvents.VoiceIdEvaluateSessionAction.VoiceSpoofingRisk, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecc91c62c3c9d2945105c3872626fb5731362acf2af61c26520794773f04421(
    *,
    authentication_result: typing.Optional[typing.Union[DomainEvents.VoiceIdEvaluateSessionAction.AuthenticationResult, typing.Dict[builtins.str, typing.Any]]] = None,
    fraud_detection_result: typing.Optional[typing.Union[DomainEvents.VoiceIdEvaluateSessionAction.FraudDetectionResult, typing.Dict[builtins.str, typing.Any]]] = None,
    generated_speaker_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    streaming_status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fa76ae5e2ee85491a3bbe02c41cb048f2c9a60e20c587681cd0eb7adb7adbd(
    *,
    aws_connect_original_contact_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188a0c8535858a82e2b77f02385245924a66627388d405c5734e732cbc32844c(
    *,
    action: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_info: typing.Optional[typing.Union[DomainEvents.VoiceIdEvaluateSessionAction.ErrorInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    session: typing.Optional[typing.Union[DomainEvents.VoiceIdEvaluateSessionAction.Session, typing.Dict[builtins.str, typing.Any]]] = None,
    source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    system_attributes: typing.Optional[typing.Union[DomainEvents.VoiceIdEvaluateSessionAction.SystemAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c6b96b5dcb6abd3e7ddbfc825b1390dd4f2263577487649da573f3fa52bf5d(
    *,
    risk_score: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1196e98eb4556a66a8c1b94493cda94ef144e7b3ecd684ce68b0ce556d5c66d(
    *,
    registration_source: typing.Optional[typing.Sequence[builtins.str]] = None,
    registration_source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    registration_status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5d56ee588eeb39fe7f57709c30db1774ae31a617de3fe0849152d250af9412e(
    *,
    error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6c8efcc3231771e5a8785a4b46e58f525e2706cc8a07bf13f48cc5ac646e41(
    *,
    action: typing.Optional[typing.Sequence[builtins.str]] = None,
    data: typing.Optional[typing.Union[DomainEvents.VoiceIdFraudsterAction.Data, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_info: typing.Optional[typing.Union[DomainEvents.VoiceIdFraudsterAction.ErrorInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    generated_fraudster_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    watchlist_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d67418843d23793653f5cebf9e1909b2c1dc63c7d04589db171eb0b426d3c61(
    *,
    error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe12c7f19f688dc43f12dad9cd110421674ba603447af542ff5c127baed6d2af(
    *,
    aws_connect_original_contact_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe646d8f97550f2115c0d38ac6fb9f06b8ce7474a324d721277697e2facbe62(
    *,
    action: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_info: typing.Optional[typing.Union[DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.ErrorInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    session_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    system_attributes: typing.Optional[typing.Union[DomainEvents.VoiceIdSessionSpeakerEnrollmentAction.SystemAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d9bf1d22ac92cf1abf9e4a2494a44b594474e2a01cdb4c022483d2b606be3e2(
    *,
    enrollment_source: typing.Optional[typing.Sequence[builtins.str]] = None,
    enrollment_source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    enrollment_status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c1377d499a281b526b6167115fdc0766eee9edac8895e0f22b43d8516fa8d7(
    *,
    error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1af6060a30dfe851d2d68dbd4e03aaa97919a3c66c83b229956d0d82bca189(
    *,
    aws_connect_original_contact_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08c14b97468d7b8ab1374a8202031cd8d24623c6af62ec89156ed96d66b3a44(
    *,
    action: typing.Optional[typing.Sequence[builtins.str]] = None,
    data: typing.Optional[typing.Union[DomainEvents.VoiceIdSpeakerAction.Data, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_info: typing.Optional[typing.Union[DomainEvents.VoiceIdSpeakerAction.ErrorInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    generated_speaker_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    system_attributes: typing.Optional[typing.Union[DomainEvents.VoiceIdSpeakerAction.SystemAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf083acb72b298a9d2cfaa479e77bbe43d50e95c2dc27cbb83f7d2db05ba61e8(
    *,
    audio_aggregation_ended_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    audio_aggregation_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30538e9979097eeca9d1d5f45ecef9c34abca8f491f8a6b0f96d34a933fd1ac(
    *,
    acceptance_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4ec0c32df4be058bf2c8820b15271e96c1ecdc53a5de64a11a884f57b32c71(
    *,
    audio_aggregation_ended_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    audio_aggregation_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    audio_aggregation_status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e19b21f7f0c51a914c2975036d4a91547c22f800a98dcac37159cf18ecec5e3(
    *,
    error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd24420ad562cc233a6b7a03d87854a1f80438b0921dc981a95c01142eee9e1(
    *,
    risk_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
    watchlist_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ff184270a984b38b3260fd63b96c648f6d262c499492b894cc2fc6ef235d6b(
    *,
    authentication_audio_progress: typing.Optional[typing.Union[DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress, typing.Dict[builtins.str, typing.Any]]] = None,
    authentication_configuration: typing.Optional[typing.Union[DomainEvents.VoiceIdStartSessionAction.AuthenticationConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    enrollment_audio_progress: typing.Optional[typing.Union[DomainEvents.VoiceIdStartSessionAction.EnrollmentAudioProgress, typing.Dict[builtins.str, typing.Any]]] = None,
    fraud_detection_audio_progress: typing.Optional[typing.Union[DomainEvents.VoiceIdStartSessionAction.AuthenticationAudioProgress, typing.Dict[builtins.str, typing.Any]]] = None,
    fraud_detection_configuration: typing.Optional[typing.Union[DomainEvents.VoiceIdStartSessionAction.FraudDetectionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    generated_speaker_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    streaming_configuration: typing.Optional[typing.Union[DomainEvents.VoiceIdStartSessionAction.StreamingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4245f00f7bf7ad96d3332dc49fc0cff3d6707431abb7a3848cdaff6c4e85a0(
    *,
    authentication_minimum_speech_in_seconds: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5dff58538b4b312e6e9d5f0ae9d32d38029b0aad0b132be56ea1f9e18207e4(
    *,
    aws_connect_original_contact_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ccf6196b3dd1015b3181c6f264b6b21ac25355986c764ff13037eb7c9d88db(
    *,
    action: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_info: typing.Optional[typing.Union[DomainEvents.VoiceIdStartSessionAction.ErrorInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    session: typing.Optional[typing.Union[DomainEvents.VoiceIdStartSessionAction.Session, typing.Dict[builtins.str, typing.Any]]] = None,
    source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    system_attributes: typing.Optional[typing.Union[DomainEvents.VoiceIdStartSessionAction.SystemAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__401384b4c88c000a907af2ab3b5cb4036f17b318d4819f7398d61d55c2441ee9(
    *,
    acceptance_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94dfe63b7d17df027f513bfaa8525522b1424ba4747e8f66163639a4d1f72b77(
    *,
    error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d55bf77bdc4d66799343d1f9b22b344c2a23bda4d303373151080939676e900(
    *,
    risk_threshold: typing.Optional[typing.Sequence[builtins.str]] = None,
    watchlist_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43cb56cb2eaee0eb2ccf5546bc65b59e62256aa524fa78d42c95c878f6576ebb(
    *,
    authentication_configuration: typing.Optional[typing.Union[DomainEvents.VoiceIdUpdateSessionAction.AuthenticationConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    fraud_detection_configuration: typing.Optional[typing.Union[DomainEvents.VoiceIdUpdateSessionAction.FraudDetectionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    generated_speaker_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a142eef5dae115926fd9065654237e4abe1c7bd036c3708d157edbf2696e9f(
    *,
    action: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_info: typing.Optional[typing.Union[DomainEvents.VoiceIdUpdateSessionAction.ErrorInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    session: typing.Optional[typing.Union[DomainEvents.VoiceIdUpdateSessionAction.Session, typing.Dict[builtins.str, typing.Any]]] = None,
    source_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
