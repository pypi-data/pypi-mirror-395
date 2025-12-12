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
import aws_cdk.interfaces.aws_codecommit as _aws_cdk_interfaces_aws_codecommit_ceddda9d


class RepositoryEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents",
):
    '''(experimental) EventBridge event patterns for Repository.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
        from aws_cdk.interfaces import aws_codecommit as interfaces_codecommit
        
        # repository_ref: interfaces_codecommit.IRepositoryRef
        
        repository_events = codecommit_events.RepositoryEvents.from_repository(repository_ref)
    '''

    @jsii.member(jsii_name="fromRepository")
    @builtins.classmethod
    def from_repository(
        cls,
        repository_ref: _aws_cdk_interfaces_aws_codecommit_ceddda9d.IRepositoryRef,
    ) -> "RepositoryEvents":
        '''(experimental) Create RepositoryEvents from a Repository reference.

        :param repository_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6560e34dfd253e278bdb61eeb92735634ce46d1d78d62a7b2176036a11ef713a)
            check_type(argname="argument repository_ref", value=repository_ref, expected_type=type_hints["repository_ref"])
        return typing.cast("RepositoryEvents", jsii.sinvoke(cls, "fromRepository", [repository_ref]))

    @jsii.member(jsii_name="codeCommitCommentOnCommitPattern")
    def code_commit_comment_on_commit_pattern(
        self,
        *,
        after_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        before_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        caller_user_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        comment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        in_reply_to: typing.Optional[typing.Sequence[builtins.str]] = None,
        notification_body: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Repository CodeCommit Comment on Commit.

        :param after_commit_id: (experimental) afterCommitId property. Specify an array of string values to match this event if the actual value of afterCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param before_commit_id: (experimental) beforeCommitId property. Specify an array of string values to match this event if the actual value of beforeCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param caller_user_arn: (experimental) callerUserArn property. Specify an array of string values to match this event if the actual value of callerUserArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param comment_id: (experimental) commentId property. Specify an array of string values to match this event if the actual value of commentId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event: (experimental) event property. Specify an array of string values to match this event if the actual value of event is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param in_reply_to: (experimental) inReplyTo property. Specify an array of string values to match this event if the actual value of inReplyTo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param notification_body: (experimental) notificationBody property. Specify an array of string values to match this event if the actual value of notificationBody is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param repository_id: (experimental) repositoryId property. Specify an array of string values to match this event if the actual value of repositoryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
        :param repository_name: (experimental) repositoryName property. Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = RepositoryEvents.CodeCommitCommentOnCommit.CodeCommitCommentOnCommitProps(
            after_commit_id=after_commit_id,
            before_commit_id=before_commit_id,
            caller_user_arn=caller_user_arn,
            comment_id=comment_id,
            event=event,
            event_metadata=event_metadata,
            in_reply_to=in_reply_to,
            notification_body=notification_body,
            repository_id=repository_id,
            repository_name=repository_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "codeCommitCommentOnCommitPattern", [options]))

    @jsii.member(jsii_name="codeCommitCommentOnPullRequestPattern")
    def code_commit_comment_on_pull_request_pattern(
        self,
        *,
        after_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        before_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        caller_user_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        comment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        in_reply_to: typing.Optional[typing.Sequence[builtins.str]] = None,
        notification_body: typing.Optional[typing.Sequence[builtins.str]] = None,
        pull_request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Repository CodeCommit Comment on Pull Request.

        :param after_commit_id: (experimental) afterCommitId property. Specify an array of string values to match this event if the actual value of afterCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param before_commit_id: (experimental) beforeCommitId property. Specify an array of string values to match this event if the actual value of beforeCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param caller_user_arn: (experimental) callerUserArn property. Specify an array of string values to match this event if the actual value of callerUserArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param comment_id: (experimental) commentId property. Specify an array of string values to match this event if the actual value of commentId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event: (experimental) event property. Specify an array of string values to match this event if the actual value of event is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param in_reply_to: (experimental) inReplyTo property. Specify an array of string values to match this event if the actual value of inReplyTo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param notification_body: (experimental) notificationBody property. Specify an array of string values to match this event if the actual value of notificationBody is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param pull_request_id: (experimental) pullRequestId property. Specify an array of string values to match this event if the actual value of pullRequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param repository_id: (experimental) repositoryId property. Specify an array of string values to match this event if the actual value of repositoryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
        :param repository_name: (experimental) repositoryName property. Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = RepositoryEvents.CodeCommitCommentOnPullRequest.CodeCommitCommentOnPullRequestProps(
            after_commit_id=after_commit_id,
            before_commit_id=before_commit_id,
            caller_user_arn=caller_user_arn,
            comment_id=comment_id,
            event=event,
            event_metadata=event_metadata,
            in_reply_to=in_reply_to,
            notification_body=notification_body,
            pull_request_id=pull_request_id,
            repository_id=repository_id,
            repository_name=repository_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "codeCommitCommentOnPullRequestPattern", [options]))

    @jsii.member(jsii_name="codeCommitRepositoryStateChangePattern")
    def code_commit_repository_state_change_pattern(
        self,
        *,
        base_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        caller_user_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        conflict_detail_level: typing.Optional[typing.Sequence[builtins.str]] = None,
        conflict_details_level: typing.Optional[typing.Sequence[builtins.str]] = None,
        conflict_resolution_strategy: typing.Optional[typing.Sequence[builtins.str]] = None,
        destination_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        merge_option: typing.Optional[typing.Sequence[builtins.str]] = None,
        old_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        reference_full_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        reference_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        reference_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Repository CodeCommit Repository State Change.

        :param base_commit_id: (experimental) baseCommitId property. Specify an array of string values to match this event if the actual value of baseCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param caller_user_arn: (experimental) callerUserArn property. Specify an array of string values to match this event if the actual value of callerUserArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param commit_id: (experimental) commitId property. Specify an array of string values to match this event if the actual value of commitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param conflict_detail_level: (experimental) conflictDetailLevel property. Specify an array of string values to match this event if the actual value of conflictDetailLevel is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param conflict_details_level: (experimental) conflictDetailsLevel property. Specify an array of string values to match this event if the actual value of conflictDetailsLevel is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param conflict_resolution_strategy: (experimental) conflictResolutionStrategy property. Specify an array of string values to match this event if the actual value of conflictResolutionStrategy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param destination_commit_id: (experimental) destinationCommitId property. Specify an array of string values to match this event if the actual value of destinationCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event: (experimental) event property. Specify an array of string values to match this event if the actual value of event is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param merge_option: (experimental) mergeOption property. Specify an array of string values to match this event if the actual value of mergeOption is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param old_commit_id: (experimental) oldCommitId property. Specify an array of string values to match this event if the actual value of oldCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param reference_full_name: (experimental) referenceFullName property. Specify an array of string values to match this event if the actual value of referenceFullName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param reference_name: (experimental) referenceName property. Specify an array of string values to match this event if the actual value of referenceName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param reference_type: (experimental) referenceType property. Specify an array of string values to match this event if the actual value of referenceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param repository_id: (experimental) repositoryId property. Specify an array of string values to match this event if the actual value of repositoryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
        :param repository_name: (experimental) repositoryName property. Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_commit_id: (experimental) sourceCommitId property. Specify an array of string values to match this event if the actual value of sourceCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = RepositoryEvents.CodeCommitRepositoryStateChange.CodeCommitRepositoryStateChangeProps(
            base_commit_id=base_commit_id,
            caller_user_arn=caller_user_arn,
            commit_id=commit_id,
            conflict_detail_level=conflict_detail_level,
            conflict_details_level=conflict_details_level,
            conflict_resolution_strategy=conflict_resolution_strategy,
            destination_commit_id=destination_commit_id,
            event=event,
            event_metadata=event_metadata,
            merge_option=merge_option,
            old_commit_id=old_commit_id,
            reference_full_name=reference_full_name,
            reference_name=reference_name,
            reference_type=reference_type,
            repository_id=repository_id,
            repository_name=repository_name,
            source_commit_id=source_commit_id,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "codeCommitRepositoryStateChangePattern", [options]))

    class AWSAPICallViaCloudTrail(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents.AWSAPICallViaCloudTrail",
    ):
        '''(experimental) aws.codecommit@AWSAPICallViaCloudTrail event types for Repository.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
            
            a_wSAPICall_via_cloud_trail = codecommit_events.RepositoryEvents.AWSAPICallViaCloudTrail()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps",
            jsii_struct_bases=[],
            name_mapping={"additional_event_data": "additionalEventData"},
        )
        class AWSAPICallViaCloudTrailProps:
            def __init__(
                self,
                *,
                additional_event_data: typing.Optional[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.AdditionalEventData", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Repository aws.codecommit@AWSAPICallViaCloudTrail event.

                :param additional_event_data: (experimental) additionalEventData property. Specify an array of string values to match this event if the actual value of additionalEventData is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
                    
                    a_wSAPICall_via_cloud_trail_props = codecommit_events.RepositoryEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
                        additional_event_data=codecommit_events.RepositoryEvents.AWSAPICallViaCloudTrail.AdditionalEventData(
                            capabilities=["capabilities"],
                            clone=["clone"],
                            data_transferred=["dataTransferred"],
                            protocol=["protocol"],
                            repository_id=["repositoryId"],
                            repository_name=["repositoryName"],
                            shallow=["shallow"]
                        )
                    )
                '''
                if isinstance(additional_event_data, dict):
                    additional_event_data = RepositoryEvents.AWSAPICallViaCloudTrail.AdditionalEventData(**additional_event_data)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4b4246abfb86697a569ed4faeb2eb9d774e94b4db9bd9a4d84e3f3a9f1f1b6b0)
                    check_type(argname="argument additional_event_data", value=additional_event_data, expected_type=type_hints["additional_event_data"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if additional_event_data is not None:
                    self._values["additional_event_data"] = additional_event_data

            @builtins.property
            def additional_event_data(
                self,
            ) -> typing.Optional["RepositoryEvents.AWSAPICallViaCloudTrail.AdditionalEventData"]:
                '''(experimental) additionalEventData property.

                Specify an array of string values to match this event if the actual value of additionalEventData is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("additional_event_data")
                return typing.cast(typing.Optional["RepositoryEvents.AWSAPICallViaCloudTrail.AdditionalEventData"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AWSAPICallViaCloudTrailProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents.AWSAPICallViaCloudTrail.AdditionalEventData",
            jsii_struct_bases=[],
            name_mapping={
                "capabilities": "capabilities",
                "clone": "clone",
                "data_transferred": "dataTransferred",
                "protocol": "protocol",
                "repository_id": "repositoryId",
                "repository_name": "repositoryName",
                "shallow": "shallow",
            },
        )
        class AdditionalEventData:
            def __init__(
                self,
                *,
                capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
                clone: typing.Optional[typing.Sequence[builtins.str]] = None,
                data_transferred: typing.Optional[typing.Sequence[builtins.str]] = None,
                protocol: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                shallow: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AdditionalEventData.

                :param capabilities: (experimental) capabilities property. Specify an array of string values to match this event if the actual value of capabilities is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param clone: (experimental) clone property. Specify an array of string values to match this event if the actual value of clone is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param data_transferred: (experimental) dataTransferred property. Specify an array of string values to match this event if the actual value of dataTransferred is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param protocol: (experimental) protocol property. Specify an array of string values to match this event if the actual value of protocol is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param repository_id: (experimental) repositoryId property. Specify an array of string values to match this event if the actual value of repositoryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param repository_name: (experimental) repositoryName property. Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param shallow: (experimental) shallow property. Specify an array of string values to match this event if the actual value of shallow is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
                    
                    additional_event_data = codecommit_events.RepositoryEvents.AWSAPICallViaCloudTrail.AdditionalEventData(
                        capabilities=["capabilities"],
                        clone=["clone"],
                        data_transferred=["dataTransferred"],
                        protocol=["protocol"],
                        repository_id=["repositoryId"],
                        repository_name=["repositoryName"],
                        shallow=["shallow"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__29f2392d9ced534aa707aa78101167099c8fe25b628703c57bda93e2e5ba7a4f)
                    check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
                    check_type(argname="argument clone", value=clone, expected_type=type_hints["clone"])
                    check_type(argname="argument data_transferred", value=data_transferred, expected_type=type_hints["data_transferred"])
                    check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                    check_type(argname="argument repository_id", value=repository_id, expected_type=type_hints["repository_id"])
                    check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
                    check_type(argname="argument shallow", value=shallow, expected_type=type_hints["shallow"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if capabilities is not None:
                    self._values["capabilities"] = capabilities
                if clone is not None:
                    self._values["clone"] = clone
                if data_transferred is not None:
                    self._values["data_transferred"] = data_transferred
                if protocol is not None:
                    self._values["protocol"] = protocol
                if repository_id is not None:
                    self._values["repository_id"] = repository_id
                if repository_name is not None:
                    self._values["repository_name"] = repository_name
                if shallow is not None:
                    self._values["shallow"] = shallow

            @builtins.property
            def capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) capabilities property.

                Specify an array of string values to match this event if the actual value of capabilities is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("capabilities")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def clone(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) clone property.

                Specify an array of string values to match this event if the actual value of clone is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("clone")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def data_transferred(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) dataTransferred property.

                Specify an array of string values to match this event if the actual value of dataTransferred is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("data_transferred")
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

            @builtins.property
            def repository_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repositoryId property.

                Specify an array of string values to match this event if the actual value of repositoryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("repository_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def repository_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repositoryName property.

                Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("repository_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def shallow(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) shallow property.

                Specify an array of string values to match this event if the actual value of shallow is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("shallow")
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
            jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents.AWSAPICallViaCloudTrail.Location",
            jsii_struct_bases=[],
            name_mapping={
                "file_path": "filePath",
                "file_position": "filePosition",
                "relative_file_version": "relativeFileVersion",
            },
        )
        class Location:
            def __init__(
                self,
                *,
                file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_position: typing.Optional[typing.Sequence[builtins.str]] = None,
                relative_file_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Location.

                :param file_path: (experimental) filePath property. Specify an array of string values to match this event if the actual value of filePath is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_position: (experimental) filePosition property. Specify an array of string values to match this event if the actual value of filePosition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param relative_file_version: (experimental) relativeFileVersion property. Specify an array of string values to match this event if the actual value of relativeFileVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
                    
                    location = codecommit_events.RepositoryEvents.AWSAPICallViaCloudTrail.Location(
                        file_path=["filePath"],
                        file_position=["filePosition"],
                        relative_file_version=["relativeFileVersion"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__b48226aa69d75f46353f4b32cc793917b1729a8283352616ca7df7426af422d5)
                    check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
                    check_type(argname="argument file_position", value=file_position, expected_type=type_hints["file_position"])
                    check_type(argname="argument relative_file_version", value=relative_file_version, expected_type=type_hints["relative_file_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if file_path is not None:
                    self._values["file_path"] = file_path
                if file_position is not None:
                    self._values["file_position"] = file_position
                if relative_file_version is not None:
                    self._values["relative_file_version"] = relative_file_version

            @builtins.property
            def file_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) filePath property.

                Specify an array of string values to match this event if the actual value of filePath is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_position(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) filePosition property.

                Specify an array of string values to match this event if the actual value of filePosition is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_position")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def relative_file_version(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) relativeFileVersion property.

                Specify an array of string values to match this event if the actual value of relativeFileVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("relative_file_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Location(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParameters",
            jsii_struct_bases=[],
            name_mapping={
                "after_commit_id": "afterCommitId",
                "approval_rule_template_content": "approvalRuleTemplateContent",
                "approval_rule_template_description": "approvalRuleTemplateDescription",
                "approval_rule_template_name": "approvalRuleTemplateName",
                "approval_state": "approvalState",
                "archive_type": "archiveType",
                "before_commit_id": "beforeCommitId",
                "branch_name": "branchName",
                "client_request_token": "clientRequestToken",
                "comment_id": "commentId",
                "commit_id": "commitId",
                "commit_ids": "commitIds",
                "commit_message": "commitMessage",
                "conflict_detail_level": "conflictDetailLevel",
                "conflict_resolution_strategy": "conflictResolutionStrategy",
                "content": "content",
                "default_branch_name": "defaultBranchName",
                "delete_files": "deleteFiles",
                "description": "description",
                "destination_commit_specifier": "destinationCommitSpecifier",
                "file_mode": "fileMode",
                "file_path": "filePath",
                "file_paths": "filePaths",
                "in_reply_to": "inReplyTo",
                "keep_empty_folders": "keepEmptyFolders",
                "location": "location",
                "max_conflict_files": "maxConflictFiles",
                "max_merge_hunks": "maxMergeHunks",
                "merge_option": "mergeOption",
                "name": "name",
                "new_name": "newName",
                "old_name": "oldName",
                "parent_commit_id": "parentCommitId",
                "pull_request_id": "pullRequestId",
                "pull_request_ids": "pullRequestIds",
                "pull_request_status": "pullRequestStatus",
                "put_files": "putFiles",
                "references": "references",
                "repository_description": "repositoryDescription",
                "repository_name": "repositoryName",
                "resource_arn": "resourceArn",
                "revision_id": "revisionId",
                "s3_bucket": "s3Bucket",
                "s3_key": "s3Key",
                "source_commit_specifier": "sourceCommitSpecifier",
                "tag_keys": "tagKeys",
                "tags": "tags",
                "target_branch": "targetBranch",
            },
        )
        class RequestParameters:
            def __init__(
                self,
                *,
                after_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                approval_rule_template_content: typing.Optional[typing.Sequence[builtins.str]] = None,
                approval_rule_template_description: typing.Optional[typing.Sequence[builtins.str]] = None,
                approval_rule_template_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                approval_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                archive_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                before_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                branch_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                client_request_token: typing.Optional[typing.Sequence[builtins.str]] = None,
                comment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                commit_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
                commit_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                conflict_detail_level: typing.Optional[typing.Sequence[builtins.str]] = None,
                conflict_resolution_strategy: typing.Optional[typing.Sequence[builtins.str]] = None,
                content: typing.Optional[typing.Sequence[builtins.str]] = None,
                default_branch_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                delete_files: typing.Optional[typing.Sequence[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                description: typing.Optional[typing.Sequence[builtins.str]] = None,
                destination_commit_specifier: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_mode: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
                in_reply_to: typing.Optional[typing.Sequence[builtins.str]] = None,
                keep_empty_folders: typing.Optional[typing.Sequence[builtins.str]] = None,
                location: typing.Optional[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.Location", typing.Dict[builtins.str, typing.Any]]] = None,
                max_conflict_files: typing.Optional[typing.Sequence[builtins.str]] = None,
                max_merge_hunks: typing.Optional[typing.Sequence[builtins.str]] = None,
                merge_option: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                new_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                old_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                parent_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                pull_request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                pull_request_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
                pull_request_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                put_files: typing.Optional[typing.Sequence[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                references: typing.Optional[typing.Sequence[typing.Union["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem1", typing.Dict[builtins.str, typing.Any]]]] = None,
                repository_description: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                resource_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                revision_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_key: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_commit_specifier: typing.Optional[typing.Sequence[builtins.str]] = None,
                tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
                tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                target_branch: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParameters.

                :param after_commit_id: (experimental) afterCommitId property. Specify an array of string values to match this event if the actual value of afterCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param approval_rule_template_content: (experimental) approvalRuleTemplateContent property. Specify an array of string values to match this event if the actual value of approvalRuleTemplateContent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param approval_rule_template_description: (experimental) approvalRuleTemplateDescription property. Specify an array of string values to match this event if the actual value of approvalRuleTemplateDescription is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param approval_rule_template_name: (experimental) approvalRuleTemplateName property. Specify an array of string values to match this event if the actual value of approvalRuleTemplateName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param approval_state: (experimental) approvalState property. Specify an array of string values to match this event if the actual value of approvalState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param archive_type: (experimental) archiveType property. Specify an array of string values to match this event if the actual value of archiveType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param before_commit_id: (experimental) beforeCommitId property. Specify an array of string values to match this event if the actual value of beforeCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param branch_name: (experimental) branchName property. Specify an array of string values to match this event if the actual value of branchName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param client_request_token: (experimental) clientRequestToken property. Specify an array of string values to match this event if the actual value of clientRequestToken is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param comment_id: (experimental) commentId property. Specify an array of string values to match this event if the actual value of commentId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param commit_id: (experimental) commitId property. Specify an array of string values to match this event if the actual value of commitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param commit_ids: (experimental) commitIds property. Specify an array of string values to match this event if the actual value of commitIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param commit_message: (experimental) commitMessage property. Specify an array of string values to match this event if the actual value of commitMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param conflict_detail_level: (experimental) conflictDetailLevel property. Specify an array of string values to match this event if the actual value of conflictDetailLevel is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param conflict_resolution_strategy: (experimental) conflictResolutionStrategy property. Specify an array of string values to match this event if the actual value of conflictResolutionStrategy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param content: (experimental) content property. Specify an array of string values to match this event if the actual value of content is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param default_branch_name: (experimental) defaultBranchName property. Specify an array of string values to match this event if the actual value of defaultBranchName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param delete_files: (experimental) deleteFiles property. Specify an array of string values to match this event if the actual value of deleteFiles is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param description: (experimental) description property. Specify an array of string values to match this event if the actual value of description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param destination_commit_specifier: (experimental) destinationCommitSpecifier property. Specify an array of string values to match this event if the actual value of destinationCommitSpecifier is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_mode: (experimental) fileMode property. Specify an array of string values to match this event if the actual value of fileMode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_path: (experimental) filePath property. Specify an array of string values to match this event if the actual value of filePath is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_paths: (experimental) filePaths property. Specify an array of string values to match this event if the actual value of filePaths is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param in_reply_to: (experimental) inReplyTo property. Specify an array of string values to match this event if the actual value of inReplyTo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param keep_empty_folders: (experimental) keepEmptyFolders property. Specify an array of string values to match this event if the actual value of keepEmptyFolders is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param location: (experimental) location property. Specify an array of string values to match this event if the actual value of location is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param max_conflict_files: (experimental) maxConflictFiles property. Specify an array of string values to match this event if the actual value of maxConflictFiles is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param max_merge_hunks: (experimental) maxMergeHunks property. Specify an array of string values to match this event if the actual value of maxMergeHunks is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param merge_option: (experimental) mergeOption property. Specify an array of string values to match this event if the actual value of mergeOption is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param new_name: (experimental) newName property. Specify an array of string values to match this event if the actual value of newName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param old_name: (experimental) oldName property. Specify an array of string values to match this event if the actual value of oldName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param parent_commit_id: (experimental) parentCommitId property. Specify an array of string values to match this event if the actual value of parentCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param pull_request_id: (experimental) pullRequestId property. Specify an array of string values to match this event if the actual value of pullRequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param pull_request_ids: (experimental) pullRequestIds property. Specify an array of string values to match this event if the actual value of pullRequestIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param pull_request_status: (experimental) pullRequestStatus property. Specify an array of string values to match this event if the actual value of pullRequestStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param put_files: (experimental) putFiles property. Specify an array of string values to match this event if the actual value of putFiles is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param references: (experimental) references property. Specify an array of string values to match this event if the actual value of references is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param repository_description: (experimental) repositoryDescription property. Specify an array of string values to match this event if the actual value of repositoryDescription is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param repository_name: (experimental) repositoryName property. Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param resource_arn: (experimental) resourceArn property. Specify an array of string values to match this event if the actual value of resourceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param revision_id: (experimental) revisionId property. Specify an array of string values to match this event if the actual value of revisionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_bucket: (experimental) s3Bucket property. Specify an array of string values to match this event if the actual value of s3Bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_key: (experimental) s3Key property. Specify an array of string values to match this event if the actual value of s3Key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_commit_specifier: (experimental) sourceCommitSpecifier property. Specify an array of string values to match this event if the actual value of sourceCommitSpecifier is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tag_keys: (experimental) tagKeys property. Specify an array of string values to match this event if the actual value of tagKeys is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tags: (experimental) tags property. Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param target_branch: (experimental) targetBranch property. Specify an array of string values to match this event if the actual value of targetBranch is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
                    
                    request_parameters = codecommit_events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParameters(
                        after_commit_id=["afterCommitId"],
                        approval_rule_template_content=["approvalRuleTemplateContent"],
                        approval_rule_template_description=["approvalRuleTemplateDescription"],
                        approval_rule_template_name=["approvalRuleTemplateName"],
                        approval_state=["approvalState"],
                        archive_type=["archiveType"],
                        before_commit_id=["beforeCommitId"],
                        branch_name=["branchName"],
                        client_request_token=["clientRequestToken"],
                        comment_id=["commentId"],
                        commit_id=["commitId"],
                        commit_ids=["commitIds"],
                        commit_message=["commitMessage"],
                        conflict_detail_level=["conflictDetailLevel"],
                        conflict_resolution_strategy=["conflictResolutionStrategy"],
                        content=["content"],
                        default_branch_name=["defaultBranchName"],
                        delete_files=[codecommit_events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem(
                            file_path=["filePath"]
                        )],
                        description=["description"],
                        destination_commit_specifier=["destinationCommitSpecifier"],
                        file_mode=["fileMode"],
                        file_path=["filePath"],
                        file_paths=["filePaths"],
                        in_reply_to=["inReplyTo"],
                        keep_empty_folders=["keepEmptyFolders"],
                        location=codecommit_events.RepositoryEvents.AWSAPICallViaCloudTrail.Location(
                            file_path=["filePath"],
                            file_position=["filePosition"],
                            relative_file_version=["relativeFileVersion"]
                        ),
                        max_conflict_files=["maxConflictFiles"],
                        max_merge_hunks=["maxMergeHunks"],
                        merge_option=["mergeOption"],
                        name=["name"],
                        new_name=["newName"],
                        old_name=["oldName"],
                        parent_commit_id=["parentCommitId"],
                        pull_request_id=["pullRequestId"],
                        pull_request_ids=["pullRequestIds"],
                        pull_request_status=["pullRequestStatus"],
                        put_files=[codecommit_events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem(
                            file_path=["filePath"]
                        )],
                        references=[codecommit_events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem1(
                            commit=["commit"],
                            ref=["ref"]
                        )],
                        repository_description=["repositoryDescription"],
                        repository_name=["repositoryName"],
                        resource_arn=["resourceArn"],
                        revision_id=["revisionId"],
                        s3_bucket=["s3Bucket"],
                        s3_key=["s3Key"],
                        source_commit_specifier=["sourceCommitSpecifier"],
                        tag_keys=["tagKeys"],
                        tags={
                            "tags_key": "tags"
                        },
                        target_branch=["targetBranch"]
                    )
                '''
                if isinstance(location, dict):
                    location = RepositoryEvents.AWSAPICallViaCloudTrail.Location(**location)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__60e5e2e17b9acf4b5b69d3c473cbe51abbe0b67f2935fa2825510c405b3b3ac3)
                    check_type(argname="argument after_commit_id", value=after_commit_id, expected_type=type_hints["after_commit_id"])
                    check_type(argname="argument approval_rule_template_content", value=approval_rule_template_content, expected_type=type_hints["approval_rule_template_content"])
                    check_type(argname="argument approval_rule_template_description", value=approval_rule_template_description, expected_type=type_hints["approval_rule_template_description"])
                    check_type(argname="argument approval_rule_template_name", value=approval_rule_template_name, expected_type=type_hints["approval_rule_template_name"])
                    check_type(argname="argument approval_state", value=approval_state, expected_type=type_hints["approval_state"])
                    check_type(argname="argument archive_type", value=archive_type, expected_type=type_hints["archive_type"])
                    check_type(argname="argument before_commit_id", value=before_commit_id, expected_type=type_hints["before_commit_id"])
                    check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
                    check_type(argname="argument client_request_token", value=client_request_token, expected_type=type_hints["client_request_token"])
                    check_type(argname="argument comment_id", value=comment_id, expected_type=type_hints["comment_id"])
                    check_type(argname="argument commit_id", value=commit_id, expected_type=type_hints["commit_id"])
                    check_type(argname="argument commit_ids", value=commit_ids, expected_type=type_hints["commit_ids"])
                    check_type(argname="argument commit_message", value=commit_message, expected_type=type_hints["commit_message"])
                    check_type(argname="argument conflict_detail_level", value=conflict_detail_level, expected_type=type_hints["conflict_detail_level"])
                    check_type(argname="argument conflict_resolution_strategy", value=conflict_resolution_strategy, expected_type=type_hints["conflict_resolution_strategy"])
                    check_type(argname="argument content", value=content, expected_type=type_hints["content"])
                    check_type(argname="argument default_branch_name", value=default_branch_name, expected_type=type_hints["default_branch_name"])
                    check_type(argname="argument delete_files", value=delete_files, expected_type=type_hints["delete_files"])
                    check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                    check_type(argname="argument destination_commit_specifier", value=destination_commit_specifier, expected_type=type_hints["destination_commit_specifier"])
                    check_type(argname="argument file_mode", value=file_mode, expected_type=type_hints["file_mode"])
                    check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
                    check_type(argname="argument file_paths", value=file_paths, expected_type=type_hints["file_paths"])
                    check_type(argname="argument in_reply_to", value=in_reply_to, expected_type=type_hints["in_reply_to"])
                    check_type(argname="argument keep_empty_folders", value=keep_empty_folders, expected_type=type_hints["keep_empty_folders"])
                    check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                    check_type(argname="argument max_conflict_files", value=max_conflict_files, expected_type=type_hints["max_conflict_files"])
                    check_type(argname="argument max_merge_hunks", value=max_merge_hunks, expected_type=type_hints["max_merge_hunks"])
                    check_type(argname="argument merge_option", value=merge_option, expected_type=type_hints["merge_option"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument new_name", value=new_name, expected_type=type_hints["new_name"])
                    check_type(argname="argument old_name", value=old_name, expected_type=type_hints["old_name"])
                    check_type(argname="argument parent_commit_id", value=parent_commit_id, expected_type=type_hints["parent_commit_id"])
                    check_type(argname="argument pull_request_id", value=pull_request_id, expected_type=type_hints["pull_request_id"])
                    check_type(argname="argument pull_request_ids", value=pull_request_ids, expected_type=type_hints["pull_request_ids"])
                    check_type(argname="argument pull_request_status", value=pull_request_status, expected_type=type_hints["pull_request_status"])
                    check_type(argname="argument put_files", value=put_files, expected_type=type_hints["put_files"])
                    check_type(argname="argument references", value=references, expected_type=type_hints["references"])
                    check_type(argname="argument repository_description", value=repository_description, expected_type=type_hints["repository_description"])
                    check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
                    check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                    check_type(argname="argument revision_id", value=revision_id, expected_type=type_hints["revision_id"])
                    check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                    check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
                    check_type(argname="argument source_commit_specifier", value=source_commit_specifier, expected_type=type_hints["source_commit_specifier"])
                    check_type(argname="argument tag_keys", value=tag_keys, expected_type=type_hints["tag_keys"])
                    check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                    check_type(argname="argument target_branch", value=target_branch, expected_type=type_hints["target_branch"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if after_commit_id is not None:
                    self._values["after_commit_id"] = after_commit_id
                if approval_rule_template_content is not None:
                    self._values["approval_rule_template_content"] = approval_rule_template_content
                if approval_rule_template_description is not None:
                    self._values["approval_rule_template_description"] = approval_rule_template_description
                if approval_rule_template_name is not None:
                    self._values["approval_rule_template_name"] = approval_rule_template_name
                if approval_state is not None:
                    self._values["approval_state"] = approval_state
                if archive_type is not None:
                    self._values["archive_type"] = archive_type
                if before_commit_id is not None:
                    self._values["before_commit_id"] = before_commit_id
                if branch_name is not None:
                    self._values["branch_name"] = branch_name
                if client_request_token is not None:
                    self._values["client_request_token"] = client_request_token
                if comment_id is not None:
                    self._values["comment_id"] = comment_id
                if commit_id is not None:
                    self._values["commit_id"] = commit_id
                if commit_ids is not None:
                    self._values["commit_ids"] = commit_ids
                if commit_message is not None:
                    self._values["commit_message"] = commit_message
                if conflict_detail_level is not None:
                    self._values["conflict_detail_level"] = conflict_detail_level
                if conflict_resolution_strategy is not None:
                    self._values["conflict_resolution_strategy"] = conflict_resolution_strategy
                if content is not None:
                    self._values["content"] = content
                if default_branch_name is not None:
                    self._values["default_branch_name"] = default_branch_name
                if delete_files is not None:
                    self._values["delete_files"] = delete_files
                if description is not None:
                    self._values["description"] = description
                if destination_commit_specifier is not None:
                    self._values["destination_commit_specifier"] = destination_commit_specifier
                if file_mode is not None:
                    self._values["file_mode"] = file_mode
                if file_path is not None:
                    self._values["file_path"] = file_path
                if file_paths is not None:
                    self._values["file_paths"] = file_paths
                if in_reply_to is not None:
                    self._values["in_reply_to"] = in_reply_to
                if keep_empty_folders is not None:
                    self._values["keep_empty_folders"] = keep_empty_folders
                if location is not None:
                    self._values["location"] = location
                if max_conflict_files is not None:
                    self._values["max_conflict_files"] = max_conflict_files
                if max_merge_hunks is not None:
                    self._values["max_merge_hunks"] = max_merge_hunks
                if merge_option is not None:
                    self._values["merge_option"] = merge_option
                if name is not None:
                    self._values["name"] = name
                if new_name is not None:
                    self._values["new_name"] = new_name
                if old_name is not None:
                    self._values["old_name"] = old_name
                if parent_commit_id is not None:
                    self._values["parent_commit_id"] = parent_commit_id
                if pull_request_id is not None:
                    self._values["pull_request_id"] = pull_request_id
                if pull_request_ids is not None:
                    self._values["pull_request_ids"] = pull_request_ids
                if pull_request_status is not None:
                    self._values["pull_request_status"] = pull_request_status
                if put_files is not None:
                    self._values["put_files"] = put_files
                if references is not None:
                    self._values["references"] = references
                if repository_description is not None:
                    self._values["repository_description"] = repository_description
                if repository_name is not None:
                    self._values["repository_name"] = repository_name
                if resource_arn is not None:
                    self._values["resource_arn"] = resource_arn
                if revision_id is not None:
                    self._values["revision_id"] = revision_id
                if s3_bucket is not None:
                    self._values["s3_bucket"] = s3_bucket
                if s3_key is not None:
                    self._values["s3_key"] = s3_key
                if source_commit_specifier is not None:
                    self._values["source_commit_specifier"] = source_commit_specifier
                if tag_keys is not None:
                    self._values["tag_keys"] = tag_keys
                if tags is not None:
                    self._values["tags"] = tags
                if target_branch is not None:
                    self._values["target_branch"] = target_branch

            @builtins.property
            def after_commit_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) afterCommitId property.

                Specify an array of string values to match this event if the actual value of afterCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("after_commit_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def approval_rule_template_content(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) approvalRuleTemplateContent property.

                Specify an array of string values to match this event if the actual value of approvalRuleTemplateContent is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("approval_rule_template_content")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def approval_rule_template_description(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) approvalRuleTemplateDescription property.

                Specify an array of string values to match this event if the actual value of approvalRuleTemplateDescription is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("approval_rule_template_description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def approval_rule_template_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) approvalRuleTemplateName property.

                Specify an array of string values to match this event if the actual value of approvalRuleTemplateName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("approval_rule_template_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def approval_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) approvalState property.

                Specify an array of string values to match this event if the actual value of approvalState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("approval_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def archive_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) archiveType property.

                Specify an array of string values to match this event if the actual value of archiveType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("archive_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def before_commit_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) beforeCommitId property.

                Specify an array of string values to match this event if the actual value of beforeCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("before_commit_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def branch_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) branchName property.

                Specify an array of string values to match this event if the actual value of branchName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("branch_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def client_request_token(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) clientRequestToken property.

                Specify an array of string values to match this event if the actual value of clientRequestToken is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("client_request_token")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def comment_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) commentId property.

                Specify an array of string values to match this event if the actual value of commentId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("comment_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def commit_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) commitId property.

                Specify an array of string values to match this event if the actual value of commitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("commit_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def commit_ids(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) commitIds property.

                Specify an array of string values to match this event if the actual value of commitIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("commit_ids")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def commit_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) commitMessage property.

                Specify an array of string values to match this event if the actual value of commitMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("commit_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def conflict_detail_level(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) conflictDetailLevel property.

                Specify an array of string values to match this event if the actual value of conflictDetailLevel is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("conflict_detail_level")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def conflict_resolution_strategy(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) conflictResolutionStrategy property.

                Specify an array of string values to match this event if the actual value of conflictResolutionStrategy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("conflict_resolution_strategy")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def content(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) content property.

                Specify an array of string values to match this event if the actual value of content is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("content")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def default_branch_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) defaultBranchName property.

                Specify an array of string values to match this event if the actual value of defaultBranchName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("default_branch_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def delete_files(
                self,
            ) -> typing.Optional[typing.List["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem"]]:
                '''(experimental) deleteFiles property.

                Specify an array of string values to match this event if the actual value of deleteFiles is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("delete_files")
                return typing.cast(typing.Optional[typing.List["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem"]], result)

            @builtins.property
            def description(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) description property.

                Specify an array of string values to match this event if the actual value of description is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def destination_commit_specifier(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) destinationCommitSpecifier property.

                Specify an array of string values to match this event if the actual value of destinationCommitSpecifier is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("destination_commit_specifier")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_mode(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) fileMode property.

                Specify an array of string values to match this event if the actual value of fileMode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_mode")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) filePath property.

                Specify an array of string values to match this event if the actual value of filePath is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_paths(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) filePaths property.

                Specify an array of string values to match this event if the actual value of filePaths is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_paths")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def in_reply_to(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) inReplyTo property.

                Specify an array of string values to match this event if the actual value of inReplyTo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("in_reply_to")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def keep_empty_folders(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) keepEmptyFolders property.

                Specify an array of string values to match this event if the actual value of keepEmptyFolders is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("keep_empty_folders")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def location(
                self,
            ) -> typing.Optional["RepositoryEvents.AWSAPICallViaCloudTrail.Location"]:
                '''(experimental) location property.

                Specify an array of string values to match this event if the actual value of location is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("location")
                return typing.cast(typing.Optional["RepositoryEvents.AWSAPICallViaCloudTrail.Location"], result)

            @builtins.property
            def max_conflict_files(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) maxConflictFiles property.

                Specify an array of string values to match this event if the actual value of maxConflictFiles is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("max_conflict_files")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def max_merge_hunks(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) maxMergeHunks property.

                Specify an array of string values to match this event if the actual value of maxMergeHunks is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("max_merge_hunks")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def merge_option(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mergeOption property.

                Specify an array of string values to match this event if the actual value of mergeOption is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("merge_option")
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
            def new_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) newName property.

                Specify an array of string values to match this event if the actual value of newName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("new_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def old_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) oldName property.

                Specify an array of string values to match this event if the actual value of oldName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("old_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def parent_commit_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) parentCommitId property.

                Specify an array of string values to match this event if the actual value of parentCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("parent_commit_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def pull_request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) pullRequestId property.

                Specify an array of string values to match this event if the actual value of pullRequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("pull_request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def pull_request_ids(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) pullRequestIds property.

                Specify an array of string values to match this event if the actual value of pullRequestIds is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("pull_request_ids")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def pull_request_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) pullRequestStatus property.

                Specify an array of string values to match this event if the actual value of pullRequestStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("pull_request_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def put_files(
                self,
            ) -> typing.Optional[typing.List["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem"]]:
                '''(experimental) putFiles property.

                Specify an array of string values to match this event if the actual value of putFiles is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("put_files")
                return typing.cast(typing.Optional[typing.List["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem"]], result)

            @builtins.property
            def references(
                self,
            ) -> typing.Optional[typing.List["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem1"]]:
                '''(experimental) references property.

                Specify an array of string values to match this event if the actual value of references is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("references")
                return typing.cast(typing.Optional[typing.List["RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem1"]], result)

            @builtins.property
            def repository_description(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repositoryDescription property.

                Specify an array of string values to match this event if the actual value of repositoryDescription is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("repository_description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def repository_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repositoryName property.

                Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("repository_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def resource_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) resourceArn property.

                Specify an array of string values to match this event if the actual value of resourceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resource_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def revision_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) revisionId property.

                Specify an array of string values to match this event if the actual value of revisionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("revision_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) s3Bucket property.

                Specify an array of string values to match this event if the actual value of s3Bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) s3Key property.

                Specify an array of string values to match this event if the actual value of s3Key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_commit_specifier(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceCommitSpecifier property.

                Specify an array of string values to match this event if the actual value of sourceCommitSpecifier is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_commit_specifier")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tag_keys(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) tagKeys property.

                Specify an array of string values to match this event if the actual value of tagKeys is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tag_keys")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tags(
                self,
            ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
                '''(experimental) tags property.

                Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tags")
                return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

            @builtins.property
            def target_branch(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) targetBranch property.

                Specify an array of string values to match this event if the actual value of targetBranch is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("target_branch")
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
            jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem",
            jsii_struct_bases=[],
            name_mapping={"file_path": "filePath"},
        )
        class RequestParametersItem:
            def __init__(
                self,
                *,
                file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParametersItem.

                :param file_path: (experimental) filePath property. Specify an array of string values to match this event if the actual value of filePath is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
                    
                    request_parameters_item = codecommit_events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem(
                        file_path=["filePath"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7f5187a34d23c2e34c1bbb9b9c9d95453a48d2e902d14c1ebe839097df9e47dd)
                    check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if file_path is not None:
                    self._values["file_path"] = file_path

            @builtins.property
            def file_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) filePath property.

                Specify an array of string values to match this event if the actual value of filePath is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_path")
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
            jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem1",
            jsii_struct_bases=[],
            name_mapping={"commit": "commit", "ref": "ref"},
        )
        class RequestParametersItem1:
            def __init__(
                self,
                *,
                commit: typing.Optional[typing.Sequence[builtins.str]] = None,
                ref: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParametersItem_1.

                :param commit: (experimental) commit property. Specify an array of string values to match this event if the actual value of commit is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ref: (experimental) ref property. Specify an array of string values to match this event if the actual value of ref is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
                    
                    request_parameters_item1 = codecommit_events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem1(
                        commit=["commit"],
                        ref=["ref"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7b793d97aeb4c7ad5da984d6a16dd234afb3f6aa1022855ccebdbaca46164296)
                    check_type(argname="argument commit", value=commit, expected_type=type_hints["commit"])
                    check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if commit is not None:
                    self._values["commit"] = commit
                if ref is not None:
                    self._values["ref"] = ref

            @builtins.property
            def commit(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) commit property.

                Specify an array of string values to match this event if the actual value of commit is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("commit")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def ref(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ref property.

                Specify an array of string values to match this event if the actual value of ref is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ref")
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
            jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem2",
            jsii_struct_bases=[],
            name_mapping={"destination_reference": "destinationReference"},
        )
        class RequestParametersItem2:
            def __init__(
                self,
                *,
                destination_reference: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParametersItem_2.

                :param destination_reference: (experimental) destinationReference property. Specify an array of string values to match this event if the actual value of destinationReference is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
                    
                    request_parameters_item2 = codecommit_events.RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem2(
                        destination_reference=["destinationReference"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__0c9709f67e0a9e91e372a69067468fab9704d3ab84721640c16d678068123210)
                    check_type(argname="argument destination_reference", value=destination_reference, expected_type=type_hints["destination_reference"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if destination_reference is not None:
                    self._values["destination_reference"] = destination_reference

            @builtins.property
            def destination_reference(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) destinationReference property.

                Specify an array of string values to match this event if the actual value of destinationReference is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("destination_reference")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RequestParametersItem2(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class CodeCommitCommentOnCommit(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents.CodeCommitCommentOnCommit",
    ):
        '''(experimental) aws.codecommit@CodeCommitCommentOnCommit event types for Repository.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
            
            code_commit_comment_on_commit = codecommit_events.RepositoryEvents.CodeCommitCommentOnCommit()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents.CodeCommitCommentOnCommit.CodeCommitCommentOnCommitProps",
            jsii_struct_bases=[],
            name_mapping={
                "after_commit_id": "afterCommitId",
                "before_commit_id": "beforeCommitId",
                "caller_user_arn": "callerUserArn",
                "comment_id": "commentId",
                "event": "event",
                "event_metadata": "eventMetadata",
                "in_reply_to": "inReplyTo",
                "notification_body": "notificationBody",
                "repository_id": "repositoryId",
                "repository_name": "repositoryName",
            },
        )
        class CodeCommitCommentOnCommitProps:
            def __init__(
                self,
                *,
                after_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                before_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                caller_user_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                comment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                in_reply_to: typing.Optional[typing.Sequence[builtins.str]] = None,
                notification_body: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Repository aws.codecommit@CodeCommitCommentOnCommit event.

                :param after_commit_id: (experimental) afterCommitId property. Specify an array of string values to match this event if the actual value of afterCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param before_commit_id: (experimental) beforeCommitId property. Specify an array of string values to match this event if the actual value of beforeCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param caller_user_arn: (experimental) callerUserArn property. Specify an array of string values to match this event if the actual value of callerUserArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param comment_id: (experimental) commentId property. Specify an array of string values to match this event if the actual value of commentId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event: (experimental) event property. Specify an array of string values to match this event if the actual value of event is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param in_reply_to: (experimental) inReplyTo property. Specify an array of string values to match this event if the actual value of inReplyTo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param notification_body: (experimental) notificationBody property. Specify an array of string values to match this event if the actual value of notificationBody is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param repository_id: (experimental) repositoryId property. Specify an array of string values to match this event if the actual value of repositoryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
                :param repository_name: (experimental) repositoryName property. Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
                    
                    code_commit_comment_on_commit_props = codecommit_events.RepositoryEvents.CodeCommitCommentOnCommit.CodeCommitCommentOnCommitProps(
                        after_commit_id=["afterCommitId"],
                        before_commit_id=["beforeCommitId"],
                        caller_user_arn=["callerUserArn"],
                        comment_id=["commentId"],
                        event=["event"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        in_reply_to=["inReplyTo"],
                        notification_body=["notificationBody"],
                        repository_id=["repositoryId"],
                        repository_name=["repositoryName"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__9b31c676bb08faf80f498a3d39fcd3d9e25bfac0db35917aee995089b01d0da9)
                    check_type(argname="argument after_commit_id", value=after_commit_id, expected_type=type_hints["after_commit_id"])
                    check_type(argname="argument before_commit_id", value=before_commit_id, expected_type=type_hints["before_commit_id"])
                    check_type(argname="argument caller_user_arn", value=caller_user_arn, expected_type=type_hints["caller_user_arn"])
                    check_type(argname="argument comment_id", value=comment_id, expected_type=type_hints["comment_id"])
                    check_type(argname="argument event", value=event, expected_type=type_hints["event"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument in_reply_to", value=in_reply_to, expected_type=type_hints["in_reply_to"])
                    check_type(argname="argument notification_body", value=notification_body, expected_type=type_hints["notification_body"])
                    check_type(argname="argument repository_id", value=repository_id, expected_type=type_hints["repository_id"])
                    check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if after_commit_id is not None:
                    self._values["after_commit_id"] = after_commit_id
                if before_commit_id is not None:
                    self._values["before_commit_id"] = before_commit_id
                if caller_user_arn is not None:
                    self._values["caller_user_arn"] = caller_user_arn
                if comment_id is not None:
                    self._values["comment_id"] = comment_id
                if event is not None:
                    self._values["event"] = event
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if in_reply_to is not None:
                    self._values["in_reply_to"] = in_reply_to
                if notification_body is not None:
                    self._values["notification_body"] = notification_body
                if repository_id is not None:
                    self._values["repository_id"] = repository_id
                if repository_name is not None:
                    self._values["repository_name"] = repository_name

            @builtins.property
            def after_commit_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) afterCommitId property.

                Specify an array of string values to match this event if the actual value of afterCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("after_commit_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def before_commit_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) beforeCommitId property.

                Specify an array of string values to match this event if the actual value of beforeCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("before_commit_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def caller_user_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) callerUserArn property.

                Specify an array of string values to match this event if the actual value of callerUserArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("caller_user_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def comment_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) commentId property.

                Specify an array of string values to match this event if the actual value of commentId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("comment_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) event property.

                Specify an array of string values to match this event if the actual value of event is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event")
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
            def in_reply_to(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) inReplyTo property.

                Specify an array of string values to match this event if the actual value of inReplyTo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("in_reply_to")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def notification_body(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) notificationBody property.

                Specify an array of string values to match this event if the actual value of notificationBody is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("notification_body")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def repository_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repositoryId property.

                Specify an array of string values to match this event if the actual value of repositoryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Repository reference

                :stability: experimental
                '''
                result = self._values.get("repository_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def repository_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repositoryName property.

                Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("repository_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "CodeCommitCommentOnCommitProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class CodeCommitCommentOnPullRequest(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents.CodeCommitCommentOnPullRequest",
    ):
        '''(experimental) aws.codecommit@CodeCommitCommentOnPullRequest event types for Repository.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
            
            code_commit_comment_on_pull_request = codecommit_events.RepositoryEvents.CodeCommitCommentOnPullRequest()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents.CodeCommitCommentOnPullRequest.CodeCommitCommentOnPullRequestProps",
            jsii_struct_bases=[],
            name_mapping={
                "after_commit_id": "afterCommitId",
                "before_commit_id": "beforeCommitId",
                "caller_user_arn": "callerUserArn",
                "comment_id": "commentId",
                "event": "event",
                "event_metadata": "eventMetadata",
                "in_reply_to": "inReplyTo",
                "notification_body": "notificationBody",
                "pull_request_id": "pullRequestId",
                "repository_id": "repositoryId",
                "repository_name": "repositoryName",
            },
        )
        class CodeCommitCommentOnPullRequestProps:
            def __init__(
                self,
                *,
                after_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                before_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                caller_user_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                comment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                in_reply_to: typing.Optional[typing.Sequence[builtins.str]] = None,
                notification_body: typing.Optional[typing.Sequence[builtins.str]] = None,
                pull_request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Repository aws.codecommit@CodeCommitCommentOnPullRequest event.

                :param after_commit_id: (experimental) afterCommitId property. Specify an array of string values to match this event if the actual value of afterCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param before_commit_id: (experimental) beforeCommitId property. Specify an array of string values to match this event if the actual value of beforeCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param caller_user_arn: (experimental) callerUserArn property. Specify an array of string values to match this event if the actual value of callerUserArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param comment_id: (experimental) commentId property. Specify an array of string values to match this event if the actual value of commentId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event: (experimental) event property. Specify an array of string values to match this event if the actual value of event is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param in_reply_to: (experimental) inReplyTo property. Specify an array of string values to match this event if the actual value of inReplyTo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param notification_body: (experimental) notificationBody property. Specify an array of string values to match this event if the actual value of notificationBody is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param pull_request_id: (experimental) pullRequestId property. Specify an array of string values to match this event if the actual value of pullRequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param repository_id: (experimental) repositoryId property. Specify an array of string values to match this event if the actual value of repositoryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
                :param repository_name: (experimental) repositoryName property. Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
                    
                    code_commit_comment_on_pull_request_props = codecommit_events.RepositoryEvents.CodeCommitCommentOnPullRequest.CodeCommitCommentOnPullRequestProps(
                        after_commit_id=["afterCommitId"],
                        before_commit_id=["beforeCommitId"],
                        caller_user_arn=["callerUserArn"],
                        comment_id=["commentId"],
                        event=["event"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        in_reply_to=["inReplyTo"],
                        notification_body=["notificationBody"],
                        pull_request_id=["pullRequestId"],
                        repository_id=["repositoryId"],
                        repository_name=["repositoryName"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__75402df114cc06f722d6ce050ae80f9315150986e553be7b5d1dc9e945400953)
                    check_type(argname="argument after_commit_id", value=after_commit_id, expected_type=type_hints["after_commit_id"])
                    check_type(argname="argument before_commit_id", value=before_commit_id, expected_type=type_hints["before_commit_id"])
                    check_type(argname="argument caller_user_arn", value=caller_user_arn, expected_type=type_hints["caller_user_arn"])
                    check_type(argname="argument comment_id", value=comment_id, expected_type=type_hints["comment_id"])
                    check_type(argname="argument event", value=event, expected_type=type_hints["event"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument in_reply_to", value=in_reply_to, expected_type=type_hints["in_reply_to"])
                    check_type(argname="argument notification_body", value=notification_body, expected_type=type_hints["notification_body"])
                    check_type(argname="argument pull_request_id", value=pull_request_id, expected_type=type_hints["pull_request_id"])
                    check_type(argname="argument repository_id", value=repository_id, expected_type=type_hints["repository_id"])
                    check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if after_commit_id is not None:
                    self._values["after_commit_id"] = after_commit_id
                if before_commit_id is not None:
                    self._values["before_commit_id"] = before_commit_id
                if caller_user_arn is not None:
                    self._values["caller_user_arn"] = caller_user_arn
                if comment_id is not None:
                    self._values["comment_id"] = comment_id
                if event is not None:
                    self._values["event"] = event
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if in_reply_to is not None:
                    self._values["in_reply_to"] = in_reply_to
                if notification_body is not None:
                    self._values["notification_body"] = notification_body
                if pull_request_id is not None:
                    self._values["pull_request_id"] = pull_request_id
                if repository_id is not None:
                    self._values["repository_id"] = repository_id
                if repository_name is not None:
                    self._values["repository_name"] = repository_name

            @builtins.property
            def after_commit_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) afterCommitId property.

                Specify an array of string values to match this event if the actual value of afterCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("after_commit_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def before_commit_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) beforeCommitId property.

                Specify an array of string values to match this event if the actual value of beforeCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("before_commit_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def caller_user_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) callerUserArn property.

                Specify an array of string values to match this event if the actual value of callerUserArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("caller_user_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def comment_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) commentId property.

                Specify an array of string values to match this event if the actual value of commentId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("comment_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) event property.

                Specify an array of string values to match this event if the actual value of event is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event")
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
            def in_reply_to(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) inReplyTo property.

                Specify an array of string values to match this event if the actual value of inReplyTo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("in_reply_to")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def notification_body(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) notificationBody property.

                Specify an array of string values to match this event if the actual value of notificationBody is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("notification_body")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def pull_request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) pullRequestId property.

                Specify an array of string values to match this event if the actual value of pullRequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("pull_request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def repository_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repositoryId property.

                Specify an array of string values to match this event if the actual value of repositoryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Repository reference

                :stability: experimental
                '''
                result = self._values.get("repository_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def repository_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repositoryName property.

                Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("repository_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "CodeCommitCommentOnPullRequestProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class CodeCommitRepositoryStateChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents.CodeCommitRepositoryStateChange",
    ):
        '''(experimental) aws.codecommit@CodeCommitRepositoryStateChange event types for Repository.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
            
            code_commit_repository_state_change = codecommit_events.RepositoryEvents.CodeCommitRepositoryStateChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_codecommit.events.RepositoryEvents.CodeCommitRepositoryStateChange.CodeCommitRepositoryStateChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "base_commit_id": "baseCommitId",
                "caller_user_arn": "callerUserArn",
                "commit_id": "commitId",
                "conflict_detail_level": "conflictDetailLevel",
                "conflict_details_level": "conflictDetailsLevel",
                "conflict_resolution_strategy": "conflictResolutionStrategy",
                "destination_commit_id": "destinationCommitId",
                "event": "event",
                "event_metadata": "eventMetadata",
                "merge_option": "mergeOption",
                "old_commit_id": "oldCommitId",
                "reference_full_name": "referenceFullName",
                "reference_name": "referenceName",
                "reference_type": "referenceType",
                "repository_id": "repositoryId",
                "repository_name": "repositoryName",
                "source_commit_id": "sourceCommitId",
            },
        )
        class CodeCommitRepositoryStateChangeProps:
            def __init__(
                self,
                *,
                base_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                caller_user_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                conflict_detail_level: typing.Optional[typing.Sequence[builtins.str]] = None,
                conflict_details_level: typing.Optional[typing.Sequence[builtins.str]] = None,
                conflict_resolution_strategy: typing.Optional[typing.Sequence[builtins.str]] = None,
                destination_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                merge_option: typing.Optional[typing.Sequence[builtins.str]] = None,
                old_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                reference_full_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                reference_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                reference_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Repository aws.codecommit@CodeCommitRepositoryStateChange event.

                :param base_commit_id: (experimental) baseCommitId property. Specify an array of string values to match this event if the actual value of baseCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param caller_user_arn: (experimental) callerUserArn property. Specify an array of string values to match this event if the actual value of callerUserArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param commit_id: (experimental) commitId property. Specify an array of string values to match this event if the actual value of commitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param conflict_detail_level: (experimental) conflictDetailLevel property. Specify an array of string values to match this event if the actual value of conflictDetailLevel is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param conflict_details_level: (experimental) conflictDetailsLevel property. Specify an array of string values to match this event if the actual value of conflictDetailsLevel is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param conflict_resolution_strategy: (experimental) conflictResolutionStrategy property. Specify an array of string values to match this event if the actual value of conflictResolutionStrategy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param destination_commit_id: (experimental) destinationCommitId property. Specify an array of string values to match this event if the actual value of destinationCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event: (experimental) event property. Specify an array of string values to match this event if the actual value of event is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param merge_option: (experimental) mergeOption property. Specify an array of string values to match this event if the actual value of mergeOption is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param old_commit_id: (experimental) oldCommitId property. Specify an array of string values to match this event if the actual value of oldCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reference_full_name: (experimental) referenceFullName property. Specify an array of string values to match this event if the actual value of referenceFullName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reference_name: (experimental) referenceName property. Specify an array of string values to match this event if the actual value of referenceName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reference_type: (experimental) referenceType property. Specify an array of string values to match this event if the actual value of referenceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param repository_id: (experimental) repositoryId property. Specify an array of string values to match this event if the actual value of repositoryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Repository reference
                :param repository_name: (experimental) repositoryName property. Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_commit_id: (experimental) sourceCommitId property. Specify an array of string values to match this event if the actual value of sourceCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_codecommit import events as codecommit_events
                    
                    code_commit_repository_state_change_props = codecommit_events.RepositoryEvents.CodeCommitRepositoryStateChange.CodeCommitRepositoryStateChangeProps(
                        base_commit_id=["baseCommitId"],
                        caller_user_arn=["callerUserArn"],
                        commit_id=["commitId"],
                        conflict_detail_level=["conflictDetailLevel"],
                        conflict_details_level=["conflictDetailsLevel"],
                        conflict_resolution_strategy=["conflictResolutionStrategy"],
                        destination_commit_id=["destinationCommitId"],
                        event=["event"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        merge_option=["mergeOption"],
                        old_commit_id=["oldCommitId"],
                        reference_full_name=["referenceFullName"],
                        reference_name=["referenceName"],
                        reference_type=["referenceType"],
                        repository_id=["repositoryId"],
                        repository_name=["repositoryName"],
                        source_commit_id=["sourceCommitId"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__e539e077eac6e87e5824556e5077c30867d4095b57503f2d8f6d459e9bdcc6ea)
                    check_type(argname="argument base_commit_id", value=base_commit_id, expected_type=type_hints["base_commit_id"])
                    check_type(argname="argument caller_user_arn", value=caller_user_arn, expected_type=type_hints["caller_user_arn"])
                    check_type(argname="argument commit_id", value=commit_id, expected_type=type_hints["commit_id"])
                    check_type(argname="argument conflict_detail_level", value=conflict_detail_level, expected_type=type_hints["conflict_detail_level"])
                    check_type(argname="argument conflict_details_level", value=conflict_details_level, expected_type=type_hints["conflict_details_level"])
                    check_type(argname="argument conflict_resolution_strategy", value=conflict_resolution_strategy, expected_type=type_hints["conflict_resolution_strategy"])
                    check_type(argname="argument destination_commit_id", value=destination_commit_id, expected_type=type_hints["destination_commit_id"])
                    check_type(argname="argument event", value=event, expected_type=type_hints["event"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument merge_option", value=merge_option, expected_type=type_hints["merge_option"])
                    check_type(argname="argument old_commit_id", value=old_commit_id, expected_type=type_hints["old_commit_id"])
                    check_type(argname="argument reference_full_name", value=reference_full_name, expected_type=type_hints["reference_full_name"])
                    check_type(argname="argument reference_name", value=reference_name, expected_type=type_hints["reference_name"])
                    check_type(argname="argument reference_type", value=reference_type, expected_type=type_hints["reference_type"])
                    check_type(argname="argument repository_id", value=repository_id, expected_type=type_hints["repository_id"])
                    check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
                    check_type(argname="argument source_commit_id", value=source_commit_id, expected_type=type_hints["source_commit_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if base_commit_id is not None:
                    self._values["base_commit_id"] = base_commit_id
                if caller_user_arn is not None:
                    self._values["caller_user_arn"] = caller_user_arn
                if commit_id is not None:
                    self._values["commit_id"] = commit_id
                if conflict_detail_level is not None:
                    self._values["conflict_detail_level"] = conflict_detail_level
                if conflict_details_level is not None:
                    self._values["conflict_details_level"] = conflict_details_level
                if conflict_resolution_strategy is not None:
                    self._values["conflict_resolution_strategy"] = conflict_resolution_strategy
                if destination_commit_id is not None:
                    self._values["destination_commit_id"] = destination_commit_id
                if event is not None:
                    self._values["event"] = event
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if merge_option is not None:
                    self._values["merge_option"] = merge_option
                if old_commit_id is not None:
                    self._values["old_commit_id"] = old_commit_id
                if reference_full_name is not None:
                    self._values["reference_full_name"] = reference_full_name
                if reference_name is not None:
                    self._values["reference_name"] = reference_name
                if reference_type is not None:
                    self._values["reference_type"] = reference_type
                if repository_id is not None:
                    self._values["repository_id"] = repository_id
                if repository_name is not None:
                    self._values["repository_name"] = repository_name
                if source_commit_id is not None:
                    self._values["source_commit_id"] = source_commit_id

            @builtins.property
            def base_commit_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) baseCommitId property.

                Specify an array of string values to match this event if the actual value of baseCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("base_commit_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def caller_user_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) callerUserArn property.

                Specify an array of string values to match this event if the actual value of callerUserArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("caller_user_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def commit_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) commitId property.

                Specify an array of string values to match this event if the actual value of commitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("commit_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def conflict_detail_level(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) conflictDetailLevel property.

                Specify an array of string values to match this event if the actual value of conflictDetailLevel is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("conflict_detail_level")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def conflict_details_level(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) conflictDetailsLevel property.

                Specify an array of string values to match this event if the actual value of conflictDetailsLevel is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("conflict_details_level")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def conflict_resolution_strategy(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) conflictResolutionStrategy property.

                Specify an array of string values to match this event if the actual value of conflictResolutionStrategy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("conflict_resolution_strategy")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def destination_commit_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) destinationCommitId property.

                Specify an array of string values to match this event if the actual value of destinationCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("destination_commit_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) event property.

                Specify an array of string values to match this event if the actual value of event is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event")
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
            def merge_option(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mergeOption property.

                Specify an array of string values to match this event if the actual value of mergeOption is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("merge_option")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def old_commit_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) oldCommitId property.

                Specify an array of string values to match this event if the actual value of oldCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("old_commit_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def reference_full_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) referenceFullName property.

                Specify an array of string values to match this event if the actual value of referenceFullName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("reference_full_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def reference_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) referenceName property.

                Specify an array of string values to match this event if the actual value of referenceName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("reference_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def reference_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) referenceType property.

                Specify an array of string values to match this event if the actual value of referenceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("reference_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def repository_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repositoryId property.

                Specify an array of string values to match this event if the actual value of repositoryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Repository reference

                :stability: experimental
                '''
                result = self._values.get("repository_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def repository_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) repositoryName property.

                Specify an array of string values to match this event if the actual value of repositoryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("repository_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_commit_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceCommitId property.

                Specify an array of string values to match this event if the actual value of sourceCommitId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_commit_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "CodeCommitRepositoryStateChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "RepositoryEvents",
]

publication.publish()

def _typecheckingstub__6560e34dfd253e278bdb61eeb92735634ce46d1d78d62a7b2176036a11ef713a(
    repository_ref: _aws_cdk_interfaces_aws_codecommit_ceddda9d.IRepositoryRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4246abfb86697a569ed4faeb2eb9d774e94b4db9bd9a4d84e3f3a9f1f1b6b0(
    *,
    additional_event_data: typing.Optional[typing.Union[RepositoryEvents.AWSAPICallViaCloudTrail.AdditionalEventData, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f2392d9ced534aa707aa78101167099c8fe25b628703c57bda93e2e5ba7a4f(
    *,
    capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    clone: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_transferred: typing.Optional[typing.Sequence[builtins.str]] = None,
    protocol: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    shallow: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48226aa69d75f46353f4b32cc793917b1729a8283352616ca7df7426af422d5(
    *,
    file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_position: typing.Optional[typing.Sequence[builtins.str]] = None,
    relative_file_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e5e2e17b9acf4b5b69d3c473cbe51abbe0b67f2935fa2825510c405b3b3ac3(
    *,
    after_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    approval_rule_template_content: typing.Optional[typing.Sequence[builtins.str]] = None,
    approval_rule_template_description: typing.Optional[typing.Sequence[builtins.str]] = None,
    approval_rule_template_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    approval_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    archive_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    before_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    branch_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_request_token: typing.Optional[typing.Sequence[builtins.str]] = None,
    comment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    commit_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    commit_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    conflict_detail_level: typing.Optional[typing.Sequence[builtins.str]] = None,
    conflict_resolution_strategy: typing.Optional[typing.Sequence[builtins.str]] = None,
    content: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_branch_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    delete_files: typing.Optional[typing.Sequence[typing.Union[RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[typing.Sequence[builtins.str]] = None,
    destination_commit_specifier: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_mode: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    in_reply_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    keep_empty_folders: typing.Optional[typing.Sequence[builtins.str]] = None,
    location: typing.Optional[typing.Union[RepositoryEvents.AWSAPICallViaCloudTrail.Location, typing.Dict[builtins.str, typing.Any]]] = None,
    max_conflict_files: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_merge_hunks: typing.Optional[typing.Sequence[builtins.str]] = None,
    merge_option: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    new_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    old_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    parent_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    pull_request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    pull_request_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    pull_request_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    put_files: typing.Optional[typing.Sequence[typing.Union[RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    references: typing.Optional[typing.Sequence[typing.Union[RepositoryEvents.AWSAPICallViaCloudTrail.RequestParametersItem1, typing.Dict[builtins.str, typing.Any]]]] = None,
    repository_description: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    revision_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_commit_specifier: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target_branch: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5187a34d23c2e34c1bbb9b9c9d95453a48d2e902d14c1ebe839097df9e47dd(
    *,
    file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b793d97aeb4c7ad5da984d6a16dd234afb3f6aa1022855ccebdbaca46164296(
    *,
    commit: typing.Optional[typing.Sequence[builtins.str]] = None,
    ref: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9709f67e0a9e91e372a69067468fab9704d3ab84721640c16d678068123210(
    *,
    destination_reference: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b31c676bb08faf80f498a3d39fcd3d9e25bfac0db35917aee995089b01d0da9(
    *,
    after_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    before_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    caller_user_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    comment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    in_reply_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    notification_body: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75402df114cc06f722d6ce050ae80f9315150986e553be7b5d1dc9e945400953(
    *,
    after_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    before_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    caller_user_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    comment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    in_reply_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    notification_body: typing.Optional[typing.Sequence[builtins.str]] = None,
    pull_request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e539e077eac6e87e5824556e5077c30867d4095b57503f2d8f6d459e9bdcc6ea(
    *,
    base_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    caller_user_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    conflict_detail_level: typing.Optional[typing.Sequence[builtins.str]] = None,
    conflict_details_level: typing.Optional[typing.Sequence[builtins.str]] = None,
    conflict_resolution_strategy: typing.Optional[typing.Sequence[builtins.str]] = None,
    destination_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    merge_option: typing.Optional[typing.Sequence[builtins.str]] = None,
    old_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    reference_full_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    reference_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    reference_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_commit_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
