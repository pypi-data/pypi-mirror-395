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
import aws_cdk.interfaces.aws_athena as _aws_cdk_interfaces_aws_athena_ceddda9d


class WorkGroupEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_athena.events.WorkGroupEvents",
):
    '''(experimental) EventBridge event patterns for WorkGroup.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_athena import events as athena_events
        from aws_cdk.interfaces import aws_athena as interfaces_athena
        
        # work_group_ref: interfaces_athena.IWorkGroupRef
        
        work_group_events = athena_events.WorkGroupEvents.from_work_group(work_group_ref)
    '''

    @jsii.member(jsii_name="fromWorkGroup")
    @builtins.classmethod
    def from_work_group(
        cls,
        work_group_ref: _aws_cdk_interfaces_aws_athena_ceddda9d.IWorkGroupRef,
    ) -> "WorkGroupEvents":
        '''(experimental) Create WorkGroupEvents from a WorkGroup reference.

        :param work_group_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04261b3668d5e7e1f07542772070842eae4a8f7495954c11cc062b24fd59a7a0)
            check_type(argname="argument work_group_ref", value=work_group_ref, expected_type=type_hints["work_group_ref"])
        return typing.cast("WorkGroupEvents", jsii.sinvoke(cls, "fromWorkGroup", [work_group_ref]))

    @jsii.member(jsii_name="athenaQueryStateChangePattern")
    def athena_query_state_change_pattern(
        self,
        *,
        current_state: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        previous_state: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_execution_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        sequence_number: typing.Optional[typing.Sequence[builtins.str]] = None,
        statement_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        workgroup_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for WorkGroup Athena Query State Change.

        :param current_state: (experimental) currentState property. Specify an array of string values to match this event if the actual value of currentState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param previous_state: (experimental) previousState property. Specify an array of string values to match this event if the actual value of previousState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param query_execution_id: (experimental) queryExecutionId property. Specify an array of string values to match this event if the actual value of queryExecutionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param sequence_number: (experimental) sequenceNumber property. Specify an array of string values to match this event if the actual value of sequenceNumber is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param statement_type: (experimental) statementType property. Specify an array of string values to match this event if the actual value of statementType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version_id: (experimental) versionId property. Specify an array of string values to match this event if the actual value of versionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param workgroup_name: (experimental) workgroupName property. Specify an array of string values to match this event if the actual value of workgroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the WorkGroup reference

        :stability: experimental
        '''
        options = WorkGroupEvents.AthenaQueryStateChange.AthenaQueryStateChangeProps(
            current_state=current_state,
            event_metadata=event_metadata,
            previous_state=previous_state,
            query_execution_id=query_execution_id,
            sequence_number=sequence_number,
            statement_type=statement_type,
            version_id=version_id,
            workgroup_name=workgroup_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "athenaQueryStateChangePattern", [options]))

    class AthenaQueryStateChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_athena.events.WorkGroupEvents.AthenaQueryStateChange",
    ):
        '''(experimental) aws.athena@AthenaQueryStateChange event types for WorkGroup.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_athena import events as athena_events
            
            athena_query_state_change = athena_events.WorkGroupEvents.AthenaQueryStateChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_athena.events.WorkGroupEvents.AthenaQueryStateChange.AthenaQueryStateChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "current_state": "currentState",
                "event_metadata": "eventMetadata",
                "previous_state": "previousState",
                "query_execution_id": "queryExecutionId",
                "sequence_number": "sequenceNumber",
                "statement_type": "statementType",
                "version_id": "versionId",
                "workgroup_name": "workgroupName",
            },
        )
        class AthenaQueryStateChangeProps:
            def __init__(
                self,
                *,
                current_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                previous_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                query_execution_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                sequence_number: typing.Optional[typing.Sequence[builtins.str]] = None,
                statement_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                workgroup_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for WorkGroup aws.athena@AthenaQueryStateChange event.

                :param current_state: (experimental) currentState property. Specify an array of string values to match this event if the actual value of currentState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param previous_state: (experimental) previousState property. Specify an array of string values to match this event if the actual value of previousState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param query_execution_id: (experimental) queryExecutionId property. Specify an array of string values to match this event if the actual value of queryExecutionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param sequence_number: (experimental) sequenceNumber property. Specify an array of string values to match this event if the actual value of sequenceNumber is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param statement_type: (experimental) statementType property. Specify an array of string values to match this event if the actual value of statementType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version_id: (experimental) versionId property. Specify an array of string values to match this event if the actual value of versionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param workgroup_name: (experimental) workgroupName property. Specify an array of string values to match this event if the actual value of workgroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the WorkGroup reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_athena import events as athena_events
                    
                    athena_query_state_change_props = athena_events.WorkGroupEvents.AthenaQueryStateChange.AthenaQueryStateChangeProps(
                        current_state=["currentState"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        previous_state=["previousState"],
                        query_execution_id=["queryExecutionId"],
                        sequence_number=["sequenceNumber"],
                        statement_type=["statementType"],
                        version_id=["versionId"],
                        workgroup_name=["workgroupName"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__038a06fb0b9991f48c4e1ea77e1cc0d51d4a9675d8a99528e630f7dd9ee1c6da)
                    check_type(argname="argument current_state", value=current_state, expected_type=type_hints["current_state"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument previous_state", value=previous_state, expected_type=type_hints["previous_state"])
                    check_type(argname="argument query_execution_id", value=query_execution_id, expected_type=type_hints["query_execution_id"])
                    check_type(argname="argument sequence_number", value=sequence_number, expected_type=type_hints["sequence_number"])
                    check_type(argname="argument statement_type", value=statement_type, expected_type=type_hints["statement_type"])
                    check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
                    check_type(argname="argument workgroup_name", value=workgroup_name, expected_type=type_hints["workgroup_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if current_state is not None:
                    self._values["current_state"] = current_state
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if previous_state is not None:
                    self._values["previous_state"] = previous_state
                if query_execution_id is not None:
                    self._values["query_execution_id"] = query_execution_id
                if sequence_number is not None:
                    self._values["sequence_number"] = sequence_number
                if statement_type is not None:
                    self._values["statement_type"] = statement_type
                if version_id is not None:
                    self._values["version_id"] = version_id
                if workgroup_name is not None:
                    self._values["workgroup_name"] = workgroup_name

            @builtins.property
            def current_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) currentState property.

                Specify an array of string values to match this event if the actual value of currentState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("current_state")
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
            def previous_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) previousState property.

                Specify an array of string values to match this event if the actual value of previousState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("previous_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def query_execution_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) queryExecutionId property.

                Specify an array of string values to match this event if the actual value of queryExecutionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("query_execution_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def sequence_number(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sequenceNumber property.

                Specify an array of string values to match this event if the actual value of sequenceNumber is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("sequence_number")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def statement_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) statementType property.

                Specify an array of string values to match this event if the actual value of statementType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("statement_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) versionId property.

                Specify an array of string values to match this event if the actual value of versionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def workgroup_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) workgroupName property.

                Specify an array of string values to match this event if the actual value of workgroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the WorkGroup reference

                :stability: experimental
                '''
                result = self._values.get("workgroup_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AthenaQueryStateChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "WorkGroupEvents",
]

publication.publish()

def _typecheckingstub__04261b3668d5e7e1f07542772070842eae4a8f7495954c11cc062b24fd59a7a0(
    work_group_ref: _aws_cdk_interfaces_aws_athena_ceddda9d.IWorkGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038a06fb0b9991f48c4e1ea77e1cc0d51d4a9675d8a99528e630f7dd9ee1c6da(
    *,
    current_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    previous_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_execution_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    sequence_number: typing.Optional[typing.Sequence[builtins.str]] = None,
    statement_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    workgroup_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
