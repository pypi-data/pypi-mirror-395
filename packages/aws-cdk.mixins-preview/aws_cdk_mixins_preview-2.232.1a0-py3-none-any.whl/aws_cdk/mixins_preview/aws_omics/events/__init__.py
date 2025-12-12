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
import aws_cdk.interfaces.aws_omics as _aws_cdk_interfaces_aws_omics_ceddda9d


class ReferenceStoreEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_omics.events.ReferenceStoreEvents",
):
    '''(experimental) EventBridge event patterns for ReferenceStore.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_omics import events as omics_events
        from aws_cdk.interfaces import aws_omics as interfaces_omics
        
        # reference_store_ref: interfaces_omics.IReferenceStoreRef
        
        reference_store_events = omics_events.ReferenceStoreEvents.from_reference_store(reference_store_ref)
    '''

    @jsii.member(jsii_name="fromReferenceStore")
    @builtins.classmethod
    def from_reference_store(
        cls,
        reference_store_ref: _aws_cdk_interfaces_aws_omics_ceddda9d.IReferenceStoreRef,
    ) -> "ReferenceStoreEvents":
        '''(experimental) Create ReferenceStoreEvents from a ReferenceStore reference.

        :param reference_store_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3525328e1da009f9db687f5649739881ec604ae1f81b03cb7050db2bbb055432)
            check_type(argname="argument reference_store_ref", value=reference_store_ref, expected_type=type_hints["reference_store_ref"])
        return typing.cast("ReferenceStoreEvents", jsii.sinvoke(cls, "fromReferenceStore", [reference_store_ref]))

    @jsii.member(jsii_name="referenceImportJobStatusChangePattern")
    def reference_import_job_status_change_pattern(
        self,
        *,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[typing.Sequence[builtins.str]] = None,
        omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        reference_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for ReferenceStore Reference Import Job Status Change.

        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param omics_version: (experimental) omicsVersion property. Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param reference_store_id: (experimental) referenceStoreId property. Specify an array of string values to match this event if the actual value of referenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the ReferenceStore reference
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_message: (experimental) statusMessage property. Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ReferenceStoreEvents.ReferenceImportJobStatusChange.ReferenceImportJobStatusChangeProps(
            event_metadata=event_metadata,
            id=id,
            omics_version=omics_version,
            reference_store_id=reference_store_id,
            status=status,
            status_message=status_message,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "referenceImportJobStatusChangePattern", [options]))

    @jsii.member(jsii_name="referenceStatusChangePattern")
    def reference_status_change_pattern(
        self,
        *,
        arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        creation_job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[typing.Sequence[builtins.str]] = None,
        omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        reference_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for ReferenceStore Reference Status Change.

        :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param creation_job_id: (experimental) creationJobId property. Specify an array of string values to match this event if the actual value of creationJobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param omics_version: (experimental) omicsVersion property. Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param reference_store_id: (experimental) referenceStoreId property. Specify an array of string values to match this event if the actual value of referenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the ReferenceStore reference
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ReferenceStoreEvents.ReferenceStatusChange.ReferenceStatusChangeProps(
            arn=arn,
            creation_job_id=creation_job_id,
            event_metadata=event_metadata,
            id=id,
            omics_version=omics_version,
            reference_store_id=reference_store_id,
            status=status,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "referenceStatusChangePattern", [options]))

    class ReferenceImportJobStatusChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_omics.events.ReferenceStoreEvents.ReferenceImportJobStatusChange",
    ):
        '''(experimental) aws.omics@ReferenceImportJobStatusChange event types for ReferenceStore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_omics import events as omics_events
            
            reference_import_job_status_change = omics_events.ReferenceStoreEvents.ReferenceImportJobStatusChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_omics.events.ReferenceStoreEvents.ReferenceImportJobStatusChange.ReferenceImportJobStatusChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "event_metadata": "eventMetadata",
                "id": "id",
                "omics_version": "omicsVersion",
                "reference_store_id": "referenceStoreId",
                "status": "status",
                "status_message": "statusMessage",
            },
        )
        class ReferenceImportJobStatusChangeProps:
            def __init__(
                self,
                *,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                reference_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for ReferenceStore aws.omics@ReferenceImportJobStatusChange event.

                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param omics_version: (experimental) omicsVersion property. Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reference_store_id: (experimental) referenceStoreId property. Specify an array of string values to match this event if the actual value of referenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the ReferenceStore reference
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_message: (experimental) statusMessage property. Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_omics import events as omics_events
                    
                    reference_import_job_status_change_props = omics_events.ReferenceStoreEvents.ReferenceImportJobStatusChange.ReferenceImportJobStatusChangeProps(
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        id=["id"],
                        omics_version=["omicsVersion"],
                        reference_store_id=["referenceStoreId"],
                        status=["status"],
                        status_message=["statusMessage"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__c7e0d03ff254aca164417925c3bc4259fdc7403bff1ab731b4bfbcc236d373b9)
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument omics_version", value=omics_version, expected_type=type_hints["omics_version"])
                    check_type(argname="argument reference_store_id", value=reference_store_id, expected_type=type_hints["reference_store_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument status_message", value=status_message, expected_type=type_hints["status_message"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if id is not None:
                    self._values["id"] = id
                if omics_version is not None:
                    self._values["omics_version"] = omics_version
                if reference_store_id is not None:
                    self._values["reference_store_id"] = reference_store_id
                if status is not None:
                    self._values["status"] = status
                if status_message is not None:
                    self._values["status_message"] = status_message

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
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def omics_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) omicsVersion property.

                Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("omics_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def reference_store_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) referenceStoreId property.

                Specify an array of string values to match this event if the actual value of referenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the ReferenceStore reference

                :stability: experimental
                '''
                result = self._values.get("reference_store_id")
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
            def status_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) statusMessage property.

                Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ReferenceImportJobStatusChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ReferenceStatusChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_omics.events.ReferenceStoreEvents.ReferenceStatusChange",
    ):
        '''(experimental) aws.omics@ReferenceStatusChange event types for ReferenceStore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_omics import events as omics_events
            
            reference_status_change = omics_events.ReferenceStoreEvents.ReferenceStatusChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_omics.events.ReferenceStoreEvents.ReferenceStatusChange.ReferenceStatusChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "arn": "arn",
                "creation_job_id": "creationJobId",
                "event_metadata": "eventMetadata",
                "id": "id",
                "omics_version": "omicsVersion",
                "reference_store_id": "referenceStoreId",
                "status": "status",
            },
        )
        class ReferenceStatusChangeProps:
            def __init__(
                self,
                *,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                creation_job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                reference_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for ReferenceStore aws.omics@ReferenceStatusChange event.

                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param creation_job_id: (experimental) creationJobId property. Specify an array of string values to match this event if the actual value of creationJobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param omics_version: (experimental) omicsVersion property. Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reference_store_id: (experimental) referenceStoreId property. Specify an array of string values to match this event if the actual value of referenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the ReferenceStore reference
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_omics import events as omics_events
                    
                    reference_status_change_props = omics_events.ReferenceStoreEvents.ReferenceStatusChange.ReferenceStatusChangeProps(
                        arn=["arn"],
                        creation_job_id=["creationJobId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        id=["id"],
                        omics_version=["omicsVersion"],
                        reference_store_id=["referenceStoreId"],
                        status=["status"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__043c397b8923cae2e9e56a9f6c45208b140c4bc98e13514dbf5f077c1ab03ec3)
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument creation_job_id", value=creation_job_id, expected_type=type_hints["creation_job_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument omics_version", value=omics_version, expected_type=type_hints["omics_version"])
                    check_type(argname="argument reference_store_id", value=reference_store_id, expected_type=type_hints["reference_store_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if arn is not None:
                    self._values["arn"] = arn
                if creation_job_id is not None:
                    self._values["creation_job_id"] = creation_job_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if id is not None:
                    self._values["id"] = id
                if omics_version is not None:
                    self._values["omics_version"] = omics_version
                if reference_store_id is not None:
                    self._values["reference_store_id"] = reference_store_id
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
            def creation_job_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) creationJobId property.

                Specify an array of string values to match this event if the actual value of creationJobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("creation_job_id")
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
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def omics_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) omicsVersion property.

                Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("omics_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def reference_store_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) referenceStoreId property.

                Specify an array of string values to match this event if the actual value of referenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the ReferenceStore reference

                :stability: experimental
                '''
                result = self._values.get("reference_store_id")
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
                return "ReferenceStatusChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


class SequenceStoreEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_omics.events.SequenceStoreEvents",
):
    '''(experimental) EventBridge event patterns for SequenceStore.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_omics import events as omics_events
        from aws_cdk.interfaces import aws_omics as interfaces_omics
        
        # sequence_store_ref: interfaces_omics.ISequenceStoreRef
        
        sequence_store_events = omics_events.SequenceStoreEvents.from_sequence_store(sequence_store_ref)
    '''

    @jsii.member(jsii_name="fromSequenceStore")
    @builtins.classmethod
    def from_sequence_store(
        cls,
        sequence_store_ref: _aws_cdk_interfaces_aws_omics_ceddda9d.ISequenceStoreRef,
    ) -> "SequenceStoreEvents":
        '''(experimental) Create SequenceStoreEvents from a SequenceStore reference.

        :param sequence_store_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fdeb323027e6ff7c9a852433dc84cd9b3db351345a19ee02d41a5b219eb74b7)
            check_type(argname="argument sequence_store_ref", value=sequence_store_ref, expected_type=type_hints["sequence_store_ref"])
        return typing.cast("SequenceStoreEvents", jsii.sinvoke(cls, "fromSequenceStore", [sequence_store_ref]))

    @jsii.member(jsii_name="readSetActivationJobStatusChangePattern")
    def read_set_activation_job_status_change_pattern(
        self,
        *,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[typing.Sequence[builtins.str]] = None,
        omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        sequence_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for SequenceStore Read Set Activation Job Status Change.

        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param omics_version: (experimental) omicsVersion property. Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param sequence_store_id: (experimental) sequenceStoreId property. Specify an array of string values to match this event if the actual value of sequenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the SequenceStore reference
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_message: (experimental) statusMessage property. Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = SequenceStoreEvents.ReadSetActivationJobStatusChange.ReadSetActivationJobStatusChangeProps(
            event_metadata=event_metadata,
            id=id,
            omics_version=omics_version,
            sequence_store_id=sequence_store_id,
            status=status,
            status_message=status_message,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "readSetActivationJobStatusChangePattern", [options]))

    @jsii.member(jsii_name="readSetExportJobStatusChangePattern")
    def read_set_export_job_status_change_pattern(
        self,
        *,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[typing.Sequence[builtins.str]] = None,
        omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        sequence_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for SequenceStore Read Set Export Job Status Change.

        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param omics_version: (experimental) omicsVersion property. Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param sequence_store_id: (experimental) sequenceStoreId property. Specify an array of string values to match this event if the actual value of sequenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the SequenceStore reference
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_message: (experimental) statusMessage property. Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = SequenceStoreEvents.ReadSetExportJobStatusChange.ReadSetExportJobStatusChangeProps(
            event_metadata=event_metadata,
            id=id,
            omics_version=omics_version,
            sequence_store_id=sequence_store_id,
            status=status,
            status_message=status_message,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "readSetExportJobStatusChangePattern", [options]))

    @jsii.member(jsii_name="readSetImportJobStatusChangePattern")
    def read_set_import_job_status_change_pattern(
        self,
        *,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[typing.Sequence[builtins.str]] = None,
        omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        sequence_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for SequenceStore Read Set Import Job Status Change.

        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param omics_version: (experimental) omicsVersion property. Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param sequence_store_id: (experimental) sequenceStoreId property. Specify an array of string values to match this event if the actual value of sequenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the SequenceStore reference
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_message: (experimental) statusMessage property. Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = SequenceStoreEvents.ReadSetImportJobStatusChange.ReadSetImportJobStatusChangeProps(
            event_metadata=event_metadata,
            id=id,
            omics_version=omics_version,
            sequence_store_id=sequence_store_id,
            status=status,
            status_message=status_message,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "readSetImportJobStatusChangePattern", [options]))

    @jsii.member(jsii_name="readSetStatusChangePattern")
    def read_set_status_change_pattern(
        self,
        *,
        arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        creation_job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[typing.Sequence[builtins.str]] = None,
        omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        sequence_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for SequenceStore Read Set Status Change.

        :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param creation_job_id: (experimental) creationJobId property. Specify an array of string values to match this event if the actual value of creationJobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param omics_version: (experimental) omicsVersion property. Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param sequence_store_id: (experimental) sequenceStoreId property. Specify an array of string values to match this event if the actual value of sequenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the SequenceStore reference
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_message: (experimental) statusMessage property. Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = SequenceStoreEvents.ReadSetStatusChange.ReadSetStatusChangeProps(
            arn=arn,
            creation_job_id=creation_job_id,
            event_metadata=event_metadata,
            id=id,
            omics_version=omics_version,
            sequence_store_id=sequence_store_id,
            status=status,
            status_message=status_message,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "readSetStatusChangePattern", [options]))

    class ReadSetActivationJobStatusChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_omics.events.SequenceStoreEvents.ReadSetActivationJobStatusChange",
    ):
        '''(experimental) aws.omics@ReadSetActivationJobStatusChange event types for SequenceStore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_omics import events as omics_events
            
            read_set_activation_job_status_change = omics_events.SequenceStoreEvents.ReadSetActivationJobStatusChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_omics.events.SequenceStoreEvents.ReadSetActivationJobStatusChange.ReadSetActivationJobStatusChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "event_metadata": "eventMetadata",
                "id": "id",
                "omics_version": "omicsVersion",
                "sequence_store_id": "sequenceStoreId",
                "status": "status",
                "status_message": "statusMessage",
            },
        )
        class ReadSetActivationJobStatusChangeProps:
            def __init__(
                self,
                *,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                sequence_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for SequenceStore aws.omics@ReadSetActivationJobStatusChange event.

                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param omics_version: (experimental) omicsVersion property. Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param sequence_store_id: (experimental) sequenceStoreId property. Specify an array of string values to match this event if the actual value of sequenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the SequenceStore reference
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_message: (experimental) statusMessage property. Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_omics import events as omics_events
                    
                    read_set_activation_job_status_change_props = omics_events.SequenceStoreEvents.ReadSetActivationJobStatusChange.ReadSetActivationJobStatusChangeProps(
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        id=["id"],
                        omics_version=["omicsVersion"],
                        sequence_store_id=["sequenceStoreId"],
                        status=["status"],
                        status_message=["statusMessage"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__620cc01eb39cc017a9d84a6560017fad1f51b72ad5d5ab17c3e5866b22a02826)
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument omics_version", value=omics_version, expected_type=type_hints["omics_version"])
                    check_type(argname="argument sequence_store_id", value=sequence_store_id, expected_type=type_hints["sequence_store_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument status_message", value=status_message, expected_type=type_hints["status_message"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if id is not None:
                    self._values["id"] = id
                if omics_version is not None:
                    self._values["omics_version"] = omics_version
                if sequence_store_id is not None:
                    self._values["sequence_store_id"] = sequence_store_id
                if status is not None:
                    self._values["status"] = status
                if status_message is not None:
                    self._values["status_message"] = status_message

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
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def omics_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) omicsVersion property.

                Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("omics_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def sequence_store_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sequenceStoreId property.

                Specify an array of string values to match this event if the actual value of sequenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the SequenceStore reference

                :stability: experimental
                '''
                result = self._values.get("sequence_store_id")
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
            def status_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) statusMessage property.

                Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ReadSetActivationJobStatusChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ReadSetExportJobStatusChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_omics.events.SequenceStoreEvents.ReadSetExportJobStatusChange",
    ):
        '''(experimental) aws.omics@ReadSetExportJobStatusChange event types for SequenceStore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_omics import events as omics_events
            
            read_set_export_job_status_change = omics_events.SequenceStoreEvents.ReadSetExportJobStatusChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_omics.events.SequenceStoreEvents.ReadSetExportJobStatusChange.ReadSetExportJobStatusChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "event_metadata": "eventMetadata",
                "id": "id",
                "omics_version": "omicsVersion",
                "sequence_store_id": "sequenceStoreId",
                "status": "status",
                "status_message": "statusMessage",
            },
        )
        class ReadSetExportJobStatusChangeProps:
            def __init__(
                self,
                *,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                sequence_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for SequenceStore aws.omics@ReadSetExportJobStatusChange event.

                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param omics_version: (experimental) omicsVersion property. Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param sequence_store_id: (experimental) sequenceStoreId property. Specify an array of string values to match this event if the actual value of sequenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the SequenceStore reference
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_message: (experimental) statusMessage property. Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_omics import events as omics_events
                    
                    read_set_export_job_status_change_props = omics_events.SequenceStoreEvents.ReadSetExportJobStatusChange.ReadSetExportJobStatusChangeProps(
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        id=["id"],
                        omics_version=["omicsVersion"],
                        sequence_store_id=["sequenceStoreId"],
                        status=["status"],
                        status_message=["statusMessage"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__b1c4158a2a471884936f23be0a30fd1ca29fe56477733d28b9e8ad28618a44ee)
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument omics_version", value=omics_version, expected_type=type_hints["omics_version"])
                    check_type(argname="argument sequence_store_id", value=sequence_store_id, expected_type=type_hints["sequence_store_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument status_message", value=status_message, expected_type=type_hints["status_message"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if id is not None:
                    self._values["id"] = id
                if omics_version is not None:
                    self._values["omics_version"] = omics_version
                if sequence_store_id is not None:
                    self._values["sequence_store_id"] = sequence_store_id
                if status is not None:
                    self._values["status"] = status
                if status_message is not None:
                    self._values["status_message"] = status_message

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
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def omics_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) omicsVersion property.

                Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("omics_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def sequence_store_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sequenceStoreId property.

                Specify an array of string values to match this event if the actual value of sequenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the SequenceStore reference

                :stability: experimental
                '''
                result = self._values.get("sequence_store_id")
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
            def status_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) statusMessage property.

                Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ReadSetExportJobStatusChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ReadSetImportJobStatusChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_omics.events.SequenceStoreEvents.ReadSetImportJobStatusChange",
    ):
        '''(experimental) aws.omics@ReadSetImportJobStatusChange event types for SequenceStore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_omics import events as omics_events
            
            read_set_import_job_status_change = omics_events.SequenceStoreEvents.ReadSetImportJobStatusChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_omics.events.SequenceStoreEvents.ReadSetImportJobStatusChange.ReadSetImportJobStatusChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "event_metadata": "eventMetadata",
                "id": "id",
                "omics_version": "omicsVersion",
                "sequence_store_id": "sequenceStoreId",
                "status": "status",
                "status_message": "statusMessage",
            },
        )
        class ReadSetImportJobStatusChangeProps:
            def __init__(
                self,
                *,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                sequence_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for SequenceStore aws.omics@ReadSetImportJobStatusChange event.

                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param omics_version: (experimental) omicsVersion property. Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param sequence_store_id: (experimental) sequenceStoreId property. Specify an array of string values to match this event if the actual value of sequenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the SequenceStore reference
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_message: (experimental) statusMessage property. Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_omics import events as omics_events
                    
                    read_set_import_job_status_change_props = omics_events.SequenceStoreEvents.ReadSetImportJobStatusChange.ReadSetImportJobStatusChangeProps(
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        id=["id"],
                        omics_version=["omicsVersion"],
                        sequence_store_id=["sequenceStoreId"],
                        status=["status"],
                        status_message=["statusMessage"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__52e8f36ddf80b565e32279e5bfea709779e10c0122d44447f07ed0bcabc86bc6)
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument omics_version", value=omics_version, expected_type=type_hints["omics_version"])
                    check_type(argname="argument sequence_store_id", value=sequence_store_id, expected_type=type_hints["sequence_store_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument status_message", value=status_message, expected_type=type_hints["status_message"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if id is not None:
                    self._values["id"] = id
                if omics_version is not None:
                    self._values["omics_version"] = omics_version
                if sequence_store_id is not None:
                    self._values["sequence_store_id"] = sequence_store_id
                if status is not None:
                    self._values["status"] = status
                if status_message is not None:
                    self._values["status_message"] = status_message

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
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def omics_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) omicsVersion property.

                Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("omics_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def sequence_store_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sequenceStoreId property.

                Specify an array of string values to match this event if the actual value of sequenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the SequenceStore reference

                :stability: experimental
                '''
                result = self._values.get("sequence_store_id")
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
            def status_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) statusMessage property.

                Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ReadSetImportJobStatusChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ReadSetStatusChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_omics.events.SequenceStoreEvents.ReadSetStatusChange",
    ):
        '''(experimental) aws.omics@ReadSetStatusChange event types for SequenceStore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_omics import events as omics_events
            
            read_set_status_change = omics_events.SequenceStoreEvents.ReadSetStatusChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_omics.events.SequenceStoreEvents.ReadSetStatusChange.ReadSetStatusChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "arn": "arn",
                "creation_job_id": "creationJobId",
                "event_metadata": "eventMetadata",
                "id": "id",
                "omics_version": "omicsVersion",
                "sequence_store_id": "sequenceStoreId",
                "status": "status",
                "status_message": "statusMessage",
            },
        )
        class ReadSetStatusChangeProps:
            def __init__(
                self,
                *,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                creation_job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                sequence_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for SequenceStore aws.omics@ReadSetStatusChange event.

                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param creation_job_id: (experimental) creationJobId property. Specify an array of string values to match this event if the actual value of creationJobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param omics_version: (experimental) omicsVersion property. Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param sequence_store_id: (experimental) sequenceStoreId property. Specify an array of string values to match this event if the actual value of sequenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the SequenceStore reference
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_message: (experimental) statusMessage property. Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_omics import events as omics_events
                    
                    read_set_status_change_props = omics_events.SequenceStoreEvents.ReadSetStatusChange.ReadSetStatusChangeProps(
                        arn=["arn"],
                        creation_job_id=["creationJobId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        id=["id"],
                        omics_version=["omicsVersion"],
                        sequence_store_id=["sequenceStoreId"],
                        status=["status"],
                        status_message=["statusMessage"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__18e2e40603640b7d71131eccb8795e5be062dfede1bbed302acd4af637f9475b)
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument creation_job_id", value=creation_job_id, expected_type=type_hints["creation_job_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument omics_version", value=omics_version, expected_type=type_hints["omics_version"])
                    check_type(argname="argument sequence_store_id", value=sequence_store_id, expected_type=type_hints["sequence_store_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument status_message", value=status_message, expected_type=type_hints["status_message"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if arn is not None:
                    self._values["arn"] = arn
                if creation_job_id is not None:
                    self._values["creation_job_id"] = creation_job_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if id is not None:
                    self._values["id"] = id
                if omics_version is not None:
                    self._values["omics_version"] = omics_version
                if sequence_store_id is not None:
                    self._values["sequence_store_id"] = sequence_store_id
                if status is not None:
                    self._values["status"] = status
                if status_message is not None:
                    self._values["status_message"] = status_message

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
            def creation_job_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) creationJobId property.

                Specify an array of string values to match this event if the actual value of creationJobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("creation_job_id")
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
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def omics_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) omicsVersion property.

                Specify an array of string values to match this event if the actual value of omicsVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("omics_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def sequence_store_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sequenceStoreId property.

                Specify an array of string values to match this event if the actual value of sequenceStoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the SequenceStore reference

                :stability: experimental
                '''
                result = self._values.get("sequence_store_id")
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
            def status_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) statusMessage property.

                Specify an array of string values to match this event if the actual value of statusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ReadSetStatusChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "ReferenceStoreEvents",
    "SequenceStoreEvents",
]

publication.publish()

def _typecheckingstub__3525328e1da009f9db687f5649739881ec604ae1f81b03cb7050db2bbb055432(
    reference_store_ref: _aws_cdk_interfaces_aws_omics_ceddda9d.IReferenceStoreRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e0d03ff254aca164417925c3bc4259fdc7403bff1ab731b4bfbcc236d373b9(
    *,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    reference_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043c397b8923cae2e9e56a9f6c45208b140c4bc98e13514dbf5f077c1ab03ec3(
    *,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    creation_job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    reference_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fdeb323027e6ff7c9a852433dc84cd9b3db351345a19ee02d41a5b219eb74b7(
    sequence_store_ref: _aws_cdk_interfaces_aws_omics_ceddda9d.ISequenceStoreRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620cc01eb39cc017a9d84a6560017fad1f51b72ad5d5ab17c3e5866b22a02826(
    *,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    sequence_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c4158a2a471884936f23be0a30fd1ca29fe56477733d28b9e8ad28618a44ee(
    *,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    sequence_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e8f36ddf80b565e32279e5bfea709779e10c0122d44447f07ed0bcabc86bc6(
    *,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    sequence_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e2e40603640b7d71131eccb8795e5be062dfede1bbed302acd4af637f9475b(
    *,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    creation_job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    omics_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    sequence_store_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
