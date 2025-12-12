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
import aws_cdk.interfaces.aws_healthimaging as _aws_cdk_interfaces_aws_healthimaging_ceddda9d


class DatastoreEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents",
):
    '''(experimental) EventBridge event patterns for Datastore.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
        from aws_cdk.interfaces import aws_healthimaging as interfaces_healthimaging
        
        # datastore_ref: interfaces_healthimaging.IDatastoreRef
        
        datastore_events = healthimaging_events.DatastoreEvents.from_datastore(datastore_ref)
    '''

    @jsii.member(jsii_name="fromDatastore")
    @builtins.classmethod
    def from_datastore(
        cls,
        datastore_ref: _aws_cdk_interfaces_aws_healthimaging_ceddda9d.IDatastoreRef,
    ) -> "DatastoreEvents":
        '''(experimental) Create DatastoreEvents from a Datastore reference.

        :param datastore_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca879ca9e80089c19b1c74410be72304e565fe5c3eb228c8d71887426e98d3d)
            check_type(argname="argument datastore_ref", value=datastore_ref, expected_type=type_hints["datastore_ref"])
        return typing.cast("DatastoreEvents", jsii.sinvoke(cls, "fromDatastore", [datastore_ref]))

    @jsii.member(jsii_name="dataStoreCreatedPattern")
    def data_store_created_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Data Store Created.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param datastore_name: (experimental) datastoreName property. Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param datastore_status: (experimental) datastoreStatus property. Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.DataStoreCreated.DataStoreCreatedProps(
            datastore_id=datastore_id,
            datastore_name=datastore_name,
            datastore_status=datastore_status,
            event_metadata=event_metadata,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "dataStoreCreatedPattern", [options]))

    @jsii.member(jsii_name="dataStoreCreatingPattern")
    def data_store_creating_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Data Store Creating.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param datastore_name: (experimental) datastoreName property. Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param datastore_status: (experimental) datastoreStatus property. Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.DataStoreCreating.DataStoreCreatingProps(
            datastore_id=datastore_id,
            datastore_name=datastore_name,
            datastore_status=datastore_status,
            event_metadata=event_metadata,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "dataStoreCreatingPattern", [options]))

    @jsii.member(jsii_name="dataStoreCreationFailedPattern")
    def data_store_creation_failed_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Data Store Creation Failed.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param datastore_name: (experimental) datastoreName property. Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param datastore_status: (experimental) datastoreStatus property. Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.DataStoreCreationFailed.DataStoreCreationFailedProps(
            datastore_id=datastore_id,
            datastore_name=datastore_name,
            datastore_status=datastore_status,
            event_metadata=event_metadata,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "dataStoreCreationFailedPattern", [options]))

    @jsii.member(jsii_name="dataStoreDeletedPattern")
    def data_store_deleted_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Data Store Deleted.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param datastore_name: (experimental) datastoreName property. Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param datastore_status: (experimental) datastoreStatus property. Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.DataStoreDeleted.DataStoreDeletedProps(
            datastore_id=datastore_id,
            datastore_name=datastore_name,
            datastore_status=datastore_status,
            event_metadata=event_metadata,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "dataStoreDeletedPattern", [options]))

    @jsii.member(jsii_name="dataStoreDeletingPattern")
    def data_store_deleting_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Data Store Deleting.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param datastore_name: (experimental) datastoreName property. Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param datastore_status: (experimental) datastoreStatus property. Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.DataStoreDeleting.DataStoreDeletingProps(
            datastore_id=datastore_id,
            datastore_name=datastore_name,
            datastore_status=datastore_status,
            event_metadata=event_metadata,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "dataStoreDeletingPattern", [options]))

    @jsii.member(jsii_name="imageSetCopiedPattern")
    def image_set_copied_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Image Set Copied.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.ImageSetCopied.ImageSetCopiedProps(
            datastore_id=datastore_id,
            event_metadata=event_metadata,
            image_set_id=image_set_id,
            image_set_state=image_set_state,
            image_set_workflow_status=image_set_workflow_status,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "imageSetCopiedPattern", [options]))

    @jsii.member(jsii_name="imageSetCopyFailedPattern")
    def image_set_copy_failed_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Image Set Copy Failed.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.ImageSetCopyFailed.ImageSetCopyFailedProps(
            datastore_id=datastore_id,
            event_metadata=event_metadata,
            image_set_id=image_set_id,
            image_set_state=image_set_state,
            image_set_workflow_status=image_set_workflow_status,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "imageSetCopyFailedPattern", [options]))

    @jsii.member(jsii_name="imageSetCopyingPattern")
    def image_set_copying_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Image Set Copying.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.ImageSetCopying.ImageSetCopyingProps(
            datastore_id=datastore_id,
            event_metadata=event_metadata,
            image_set_id=image_set_id,
            image_set_state=image_set_state,
            image_set_workflow_status=image_set_workflow_status,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "imageSetCopyingPattern", [options]))

    @jsii.member(jsii_name="imageSetCopyingWithReadOnlyAccessPattern")
    def image_set_copying_with_read_only_access_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Image Set Copying With Read Only Access.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.ImageSetCopyingWithReadOnlyAccess.ImageSetCopyingWithReadOnlyAccessProps(
            datastore_id=datastore_id,
            event_metadata=event_metadata,
            image_set_id=image_set_id,
            image_set_state=image_set_state,
            image_set_workflow_status=image_set_workflow_status,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "imageSetCopyingWithReadOnlyAccessPattern", [options]))

    @jsii.member(jsii_name="imageSetCreatedPattern")
    def image_set_created_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Image Set Created.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.ImageSetCreated.ImageSetCreatedProps(
            datastore_id=datastore_id,
            event_metadata=event_metadata,
            image_set_id=image_set_id,
            image_set_state=image_set_state,
            image_set_workflow_status=image_set_workflow_status,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "imageSetCreatedPattern", [options]))

    @jsii.member(jsii_name="imageSetDeletedPattern")
    def image_set_deleted_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Image Set Deleted.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.ImageSetDeleted.ImageSetDeletedProps(
            datastore_id=datastore_id,
            event_metadata=event_metadata,
            image_set_id=image_set_id,
            image_set_state=image_set_state,
            image_set_workflow_status=image_set_workflow_status,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "imageSetDeletedPattern", [options]))

    @jsii.member(jsii_name="imageSetDeletingPattern")
    def image_set_deleting_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Image Set Deleting.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.ImageSetDeleting.ImageSetDeletingProps(
            datastore_id=datastore_id,
            event_metadata=event_metadata,
            image_set_id=image_set_id,
            image_set_state=image_set_state,
            image_set_workflow_status=image_set_workflow_status,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "imageSetDeletingPattern", [options]))

    @jsii.member(jsii_name="imageSetUpdatedPattern")
    def image_set_updated_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Image Set Updated.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.ImageSetUpdated.ImageSetUpdatedProps(
            datastore_id=datastore_id,
            event_metadata=event_metadata,
            image_set_id=image_set_id,
            image_set_state=image_set_state,
            image_set_workflow_status=image_set_workflow_status,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "imageSetUpdatedPattern", [options]))

    @jsii.member(jsii_name="imageSetUpdateFailedPattern")
    def image_set_update_failed_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Image Set Update Failed.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.ImageSetUpdateFailed.ImageSetUpdateFailedProps(
            datastore_id=datastore_id,
            event_metadata=event_metadata,
            image_set_id=image_set_id,
            image_set_state=image_set_state,
            image_set_workflow_status=image_set_workflow_status,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "imageSetUpdateFailedPattern", [options]))

    @jsii.member(jsii_name="imageSetUpdatingPattern")
    def image_set_updating_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
        image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Image Set Updating.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.ImageSetUpdating.ImageSetUpdatingProps(
            datastore_id=datastore_id,
            event_metadata=event_metadata,
            image_set_id=image_set_id,
            image_set_state=image_set_state,
            image_set_workflow_status=image_set_workflow_status,
            imaging_version=imaging_version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "imageSetUpdatingPattern", [options]))

    @jsii.member(jsii_name="importJobCompletedPattern")
    def import_job_completed_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        input_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
        job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        output_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Import Job Completed.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param input_s3_uri: (experimental) inputS3Uri property. Specify an array of string values to match this event if the actual value of inputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param job_id: (experimental) jobId property. Specify an array of string values to match this event if the actual value of jobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param job_name: (experimental) jobName property. Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param job_status: (experimental) jobStatus property. Specify an array of string values to match this event if the actual value of jobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param output_s3_uri: (experimental) outputS3Uri property. Specify an array of string values to match this event if the actual value of outputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.ImportJobCompleted.ImportJobCompletedProps(
            datastore_id=datastore_id,
            event_metadata=event_metadata,
            imaging_version=imaging_version,
            input_s3_uri=input_s3_uri,
            job_id=job_id,
            job_name=job_name,
            job_status=job_status,
            output_s3_uri=output_s3_uri,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "importJobCompletedPattern", [options]))

    @jsii.member(jsii_name="importJobFailedPattern")
    def import_job_failed_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        input_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
        job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        output_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Import Job Failed.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param input_s3_uri: (experimental) inputS3Uri property. Specify an array of string values to match this event if the actual value of inputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param job_id: (experimental) jobId property. Specify an array of string values to match this event if the actual value of jobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param job_name: (experimental) jobName property. Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param job_status: (experimental) jobStatus property. Specify an array of string values to match this event if the actual value of jobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param output_s3_uri: (experimental) outputS3Uri property. Specify an array of string values to match this event if the actual value of outputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.ImportJobFailed.ImportJobFailedProps(
            datastore_id=datastore_id,
            event_metadata=event_metadata,
            imaging_version=imaging_version,
            input_s3_uri=input_s3_uri,
            job_id=job_id,
            job_name=job_name,
            job_status=job_status,
            output_s3_uri=output_s3_uri,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "importJobFailedPattern", [options]))

    @jsii.member(jsii_name="importJobInProgressPattern")
    def import_job_in_progress_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        input_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
        job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        output_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Import Job In Progress.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param input_s3_uri: (experimental) inputS3Uri property. Specify an array of string values to match this event if the actual value of inputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param job_id: (experimental) jobId property. Specify an array of string values to match this event if the actual value of jobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param job_name: (experimental) jobName property. Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param job_status: (experimental) jobStatus property. Specify an array of string values to match this event if the actual value of jobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param output_s3_uri: (experimental) outputS3Uri property. Specify an array of string values to match this event if the actual value of outputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.ImportJobInProgress.ImportJobInProgressProps(
            datastore_id=datastore_id,
            event_metadata=event_metadata,
            imaging_version=imaging_version,
            input_s3_uri=input_s3_uri,
            job_id=job_id,
            job_name=job_name,
            job_status=job_status,
            output_s3_uri=output_s3_uri,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "importJobInProgressPattern", [options]))

    @jsii.member(jsii_name="importJobSubmittedPattern")
    def import_job_submitted_pattern(
        self,
        *,
        datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        input_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
        job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
        output_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Datastore Import Job Submitted.

        :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param input_s3_uri: (experimental) inputS3Uri property. Specify an array of string values to match this event if the actual value of inputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param job_id: (experimental) jobId property. Specify an array of string values to match this event if the actual value of jobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param job_name: (experimental) jobName property. Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param job_status: (experimental) jobStatus property. Specify an array of string values to match this event if the actual value of jobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param output_s3_uri: (experimental) outputS3Uri property. Specify an array of string values to match this event if the actual value of outputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatastoreEvents.ImportJobSubmitted.ImportJobSubmittedProps(
            datastore_id=datastore_id,
            event_metadata=event_metadata,
            imaging_version=imaging_version,
            input_s3_uri=input_s3_uri,
            job_id=job_id,
            job_name=job_name,
            job_status=job_status,
            output_s3_uri=output_s3_uri,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "importJobSubmittedPattern", [options]))

    class DataStoreCreated(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.DataStoreCreated",
    ):
        '''(experimental) aws.healthimaging@DataStoreCreated event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            data_store_created = healthimaging_events.DatastoreEvents.DataStoreCreated()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.DataStoreCreated.DataStoreCreatedProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "datastore_name": "datastoreName",
                "datastore_status": "datastoreStatus",
                "event_metadata": "eventMetadata",
                "imaging_version": "imagingVersion",
            },
        )
        class DataStoreCreatedProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@DataStoreCreated event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param datastore_name: (experimental) datastoreName property. Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param datastore_status: (experimental) datastoreStatus property. Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    data_store_created_props = healthimaging_events.DatastoreEvents.DataStoreCreated.DataStoreCreatedProps(
                        datastore_id=["datastoreId"],
                        datastore_name=["datastoreName"],
                        datastore_status=["datastoreStatus"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ab19a59976c7256f7d655e05796472951d856031fd8249b48b921a52f67eaebd)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument datastore_name", value=datastore_name, expected_type=type_hints["datastore_name"])
                    check_type(argname="argument datastore_status", value=datastore_status, expected_type=type_hints["datastore_status"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if datastore_name is not None:
                    self._values["datastore_name"] = datastore_name
                if datastore_status is not None:
                    self._values["datastore_status"] = datastore_status
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def datastore_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreName property.

                Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("datastore_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def datastore_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreStatus property.

                Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("datastore_status")
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
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DataStoreCreatedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class DataStoreCreating(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.DataStoreCreating",
    ):
        '''(experimental) aws.healthimaging@DataStoreCreating event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            data_store_creating = healthimaging_events.DatastoreEvents.DataStoreCreating()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.DataStoreCreating.DataStoreCreatingProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "datastore_name": "datastoreName",
                "datastore_status": "datastoreStatus",
                "event_metadata": "eventMetadata",
                "imaging_version": "imagingVersion",
            },
        )
        class DataStoreCreatingProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@DataStoreCreating event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param datastore_name: (experimental) datastoreName property. Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param datastore_status: (experimental) datastoreStatus property. Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    data_store_creating_props = healthimaging_events.DatastoreEvents.DataStoreCreating.DataStoreCreatingProps(
                        datastore_id=["datastoreId"],
                        datastore_name=["datastoreName"],
                        datastore_status=["datastoreStatus"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ed55e5fff196758596b97ae599bf3c40992a720da649d35f1965cd9500d2ee81)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument datastore_name", value=datastore_name, expected_type=type_hints["datastore_name"])
                    check_type(argname="argument datastore_status", value=datastore_status, expected_type=type_hints["datastore_status"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if datastore_name is not None:
                    self._values["datastore_name"] = datastore_name
                if datastore_status is not None:
                    self._values["datastore_status"] = datastore_status
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def datastore_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreName property.

                Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("datastore_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def datastore_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreStatus property.

                Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("datastore_status")
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
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DataStoreCreatingProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class DataStoreCreationFailed(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.DataStoreCreationFailed",
    ):
        '''(experimental) aws.healthimaging@DataStoreCreationFailed event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            data_store_creation_failed = healthimaging_events.DatastoreEvents.DataStoreCreationFailed()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.DataStoreCreationFailed.DataStoreCreationFailedProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "datastore_name": "datastoreName",
                "datastore_status": "datastoreStatus",
                "event_metadata": "eventMetadata",
                "imaging_version": "imagingVersion",
            },
        )
        class DataStoreCreationFailedProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@DataStoreCreationFailed event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param datastore_name: (experimental) datastoreName property. Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param datastore_status: (experimental) datastoreStatus property. Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    data_store_creation_failed_props = healthimaging_events.DatastoreEvents.DataStoreCreationFailed.DataStoreCreationFailedProps(
                        datastore_id=["datastoreId"],
                        datastore_name=["datastoreName"],
                        datastore_status=["datastoreStatus"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__e0425c77a76ca4705210826e43d8c73bf4a8c56941ac5190da634ef30438644d)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument datastore_name", value=datastore_name, expected_type=type_hints["datastore_name"])
                    check_type(argname="argument datastore_status", value=datastore_status, expected_type=type_hints["datastore_status"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if datastore_name is not None:
                    self._values["datastore_name"] = datastore_name
                if datastore_status is not None:
                    self._values["datastore_status"] = datastore_status
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def datastore_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreName property.

                Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("datastore_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def datastore_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreStatus property.

                Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("datastore_status")
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
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DataStoreCreationFailedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class DataStoreDeleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.DataStoreDeleted",
    ):
        '''(experimental) aws.healthimaging@DataStoreDeleted event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            data_store_deleted = healthimaging_events.DatastoreEvents.DataStoreDeleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.DataStoreDeleted.DataStoreDeletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "datastore_name": "datastoreName",
                "datastore_status": "datastoreStatus",
                "event_metadata": "eventMetadata",
                "imaging_version": "imagingVersion",
            },
        )
        class DataStoreDeletedProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@DataStoreDeleted event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param datastore_name: (experimental) datastoreName property. Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param datastore_status: (experimental) datastoreStatus property. Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    data_store_deleted_props = healthimaging_events.DatastoreEvents.DataStoreDeleted.DataStoreDeletedProps(
                        datastore_id=["datastoreId"],
                        datastore_name=["datastoreName"],
                        datastore_status=["datastoreStatus"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__0a07e2d107b7ea80e08901660b2a16cb0f719421399285186468b9a7c5ed9598)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument datastore_name", value=datastore_name, expected_type=type_hints["datastore_name"])
                    check_type(argname="argument datastore_status", value=datastore_status, expected_type=type_hints["datastore_status"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if datastore_name is not None:
                    self._values["datastore_name"] = datastore_name
                if datastore_status is not None:
                    self._values["datastore_status"] = datastore_status
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def datastore_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreName property.

                Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("datastore_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def datastore_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreStatus property.

                Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("datastore_status")
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
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DataStoreDeletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class DataStoreDeleting(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.DataStoreDeleting",
    ):
        '''(experimental) aws.healthimaging@DataStoreDeleting event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            data_store_deleting = healthimaging_events.DatastoreEvents.DataStoreDeleting()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.DataStoreDeleting.DataStoreDeletingProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "datastore_name": "datastoreName",
                "datastore_status": "datastoreStatus",
                "event_metadata": "eventMetadata",
                "imaging_version": "imagingVersion",
            },
        )
        class DataStoreDeletingProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@DataStoreDeleting event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param datastore_name: (experimental) datastoreName property. Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param datastore_status: (experimental) datastoreStatus property. Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    data_store_deleting_props = healthimaging_events.DatastoreEvents.DataStoreDeleting.DataStoreDeletingProps(
                        datastore_id=["datastoreId"],
                        datastore_name=["datastoreName"],
                        datastore_status=["datastoreStatus"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a1799c1fd6a086755e0eba2d0f79f634b336b3e6a19da7faa557bcbed6620706)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument datastore_name", value=datastore_name, expected_type=type_hints["datastore_name"])
                    check_type(argname="argument datastore_status", value=datastore_status, expected_type=type_hints["datastore_status"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if datastore_name is not None:
                    self._values["datastore_name"] = datastore_name
                if datastore_status is not None:
                    self._values["datastore_status"] = datastore_status
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def datastore_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreName property.

                Specify an array of string values to match this event if the actual value of datastoreName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("datastore_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def datastore_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreStatus property.

                Specify an array of string values to match this event if the actual value of datastoreStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("datastore_status")
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
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DataStoreDeletingProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ImageSetCopied(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetCopied",
    ):
        '''(experimental) aws.healthimaging@ImageSetCopied event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            image_set_copied = healthimaging_events.DatastoreEvents.ImageSetCopied()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetCopied.ImageSetCopiedProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "event_metadata": "eventMetadata",
                "image_set_id": "imageSetId",
                "image_set_state": "imageSetState",
                "image_set_workflow_status": "imageSetWorkflowStatus",
                "imaging_version": "imagingVersion",
            },
        )
        class ImageSetCopiedProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@ImageSetCopied event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    image_set_copied_props = healthimaging_events.DatastoreEvents.ImageSetCopied.ImageSetCopiedProps(
                        datastore_id=["datastoreId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        image_set_id=["imageSetId"],
                        image_set_state=["imageSetState"],
                        image_set_workflow_status=["imageSetWorkflowStatus"],
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__fe4fc278513849c1d9b45855cae8f41258bd15fd5446bf5953e082e68e104091)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument image_set_id", value=image_set_id, expected_type=type_hints["image_set_id"])
                    check_type(argname="argument image_set_state", value=image_set_state, expected_type=type_hints["image_set_state"])
                    check_type(argname="argument image_set_workflow_status", value=image_set_workflow_status, expected_type=type_hints["image_set_workflow_status"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if image_set_id is not None:
                    self._values["image_set_id"] = image_set_id
                if image_set_state is not None:
                    self._values["image_set_state"] = image_set_state
                if image_set_workflow_status is not None:
                    self._values["image_set_workflow_status"] = image_set_workflow_status
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
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
            def image_set_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetId property.

                Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetState property.

                Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_workflow_status(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetWorkflowStatus property.

                Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_workflow_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ImageSetCopiedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ImageSetCopyFailed(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetCopyFailed",
    ):
        '''(experimental) aws.healthimaging@ImageSetCopyFailed event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            image_set_copy_failed = healthimaging_events.DatastoreEvents.ImageSetCopyFailed()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetCopyFailed.ImageSetCopyFailedProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "event_metadata": "eventMetadata",
                "image_set_id": "imageSetId",
                "image_set_state": "imageSetState",
                "image_set_workflow_status": "imageSetWorkflowStatus",
                "imaging_version": "imagingVersion",
            },
        )
        class ImageSetCopyFailedProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@ImageSetCopyFailed event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    image_set_copy_failed_props = healthimaging_events.DatastoreEvents.ImageSetCopyFailed.ImageSetCopyFailedProps(
                        datastore_id=["datastoreId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        image_set_id=["imageSetId"],
                        image_set_state=["imageSetState"],
                        image_set_workflow_status=["imageSetWorkflowStatus"],
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__2178d745fa07792399da17d1b6dca27831eeaab192b6c96f95e492bafc9d2851)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument image_set_id", value=image_set_id, expected_type=type_hints["image_set_id"])
                    check_type(argname="argument image_set_state", value=image_set_state, expected_type=type_hints["image_set_state"])
                    check_type(argname="argument image_set_workflow_status", value=image_set_workflow_status, expected_type=type_hints["image_set_workflow_status"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if image_set_id is not None:
                    self._values["image_set_id"] = image_set_id
                if image_set_state is not None:
                    self._values["image_set_state"] = image_set_state
                if image_set_workflow_status is not None:
                    self._values["image_set_workflow_status"] = image_set_workflow_status
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
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
            def image_set_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetId property.

                Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetState property.

                Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_workflow_status(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetWorkflowStatus property.

                Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_workflow_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ImageSetCopyFailedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ImageSetCopying(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetCopying",
    ):
        '''(experimental) aws.healthimaging@ImageSetCopying event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            image_set_copying = healthimaging_events.DatastoreEvents.ImageSetCopying()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetCopying.ImageSetCopyingProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "event_metadata": "eventMetadata",
                "image_set_id": "imageSetId",
                "image_set_state": "imageSetState",
                "image_set_workflow_status": "imageSetWorkflowStatus",
                "imaging_version": "imagingVersion",
            },
        )
        class ImageSetCopyingProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@ImageSetCopying event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    image_set_copying_props = healthimaging_events.DatastoreEvents.ImageSetCopying.ImageSetCopyingProps(
                        datastore_id=["datastoreId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        image_set_id=["imageSetId"],
                        image_set_state=["imageSetState"],
                        image_set_workflow_status=["imageSetWorkflowStatus"],
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a7cf994140cabb653cc480a3ea98e2eff82f99ba43403fb2f88bc3fd8fb2812a)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument image_set_id", value=image_set_id, expected_type=type_hints["image_set_id"])
                    check_type(argname="argument image_set_state", value=image_set_state, expected_type=type_hints["image_set_state"])
                    check_type(argname="argument image_set_workflow_status", value=image_set_workflow_status, expected_type=type_hints["image_set_workflow_status"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if image_set_id is not None:
                    self._values["image_set_id"] = image_set_id
                if image_set_state is not None:
                    self._values["image_set_state"] = image_set_state
                if image_set_workflow_status is not None:
                    self._values["image_set_workflow_status"] = image_set_workflow_status
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
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
            def image_set_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetId property.

                Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetState property.

                Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_workflow_status(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetWorkflowStatus property.

                Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_workflow_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ImageSetCopyingProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ImageSetCopyingWithReadOnlyAccess(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetCopyingWithReadOnlyAccess",
    ):
        '''(experimental) aws.healthimaging@ImageSetCopyingWithReadOnlyAccess event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            image_set_copying_with_read_only_access = healthimaging_events.DatastoreEvents.ImageSetCopyingWithReadOnlyAccess()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetCopyingWithReadOnlyAccess.ImageSetCopyingWithReadOnlyAccessProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "event_metadata": "eventMetadata",
                "image_set_id": "imageSetId",
                "image_set_state": "imageSetState",
                "image_set_workflow_status": "imageSetWorkflowStatus",
                "imaging_version": "imagingVersion",
            },
        )
        class ImageSetCopyingWithReadOnlyAccessProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@ImageSetCopyingWithReadOnlyAccess event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    image_set_copying_with_read_only_access_props = healthimaging_events.DatastoreEvents.ImageSetCopyingWithReadOnlyAccess.ImageSetCopyingWithReadOnlyAccessProps(
                        datastore_id=["datastoreId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        image_set_id=["imageSetId"],
                        image_set_state=["imageSetState"],
                        image_set_workflow_status=["imageSetWorkflowStatus"],
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__08b118236682f832af9978754461f32fb470d4726c57bace61ec8feb3178ef20)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument image_set_id", value=image_set_id, expected_type=type_hints["image_set_id"])
                    check_type(argname="argument image_set_state", value=image_set_state, expected_type=type_hints["image_set_state"])
                    check_type(argname="argument image_set_workflow_status", value=image_set_workflow_status, expected_type=type_hints["image_set_workflow_status"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if image_set_id is not None:
                    self._values["image_set_id"] = image_set_id
                if image_set_state is not None:
                    self._values["image_set_state"] = image_set_state
                if image_set_workflow_status is not None:
                    self._values["image_set_workflow_status"] = image_set_workflow_status
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
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
            def image_set_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetId property.

                Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetState property.

                Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_workflow_status(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetWorkflowStatus property.

                Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_workflow_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ImageSetCopyingWithReadOnlyAccessProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ImageSetCreated(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetCreated",
    ):
        '''(experimental) aws.healthimaging@ImageSetCreated event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            image_set_created = healthimaging_events.DatastoreEvents.ImageSetCreated()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetCreated.ImageSetCreatedProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "event_metadata": "eventMetadata",
                "image_set_id": "imageSetId",
                "image_set_state": "imageSetState",
                "image_set_workflow_status": "imageSetWorkflowStatus",
                "imaging_version": "imagingVersion",
            },
        )
        class ImageSetCreatedProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@ImageSetCreated event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    image_set_created_props = healthimaging_events.DatastoreEvents.ImageSetCreated.ImageSetCreatedProps(
                        datastore_id=["datastoreId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        image_set_id=["imageSetId"],
                        image_set_state=["imageSetState"],
                        image_set_workflow_status=["imageSetWorkflowStatus"],
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__78a1f218b54a7eb345df4b9d4c38ab7b6800f535c2b7432c844e255b10eeb06a)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument image_set_id", value=image_set_id, expected_type=type_hints["image_set_id"])
                    check_type(argname="argument image_set_state", value=image_set_state, expected_type=type_hints["image_set_state"])
                    check_type(argname="argument image_set_workflow_status", value=image_set_workflow_status, expected_type=type_hints["image_set_workflow_status"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if image_set_id is not None:
                    self._values["image_set_id"] = image_set_id
                if image_set_state is not None:
                    self._values["image_set_state"] = image_set_state
                if image_set_workflow_status is not None:
                    self._values["image_set_workflow_status"] = image_set_workflow_status
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
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
            def image_set_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetId property.

                Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetState property.

                Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_workflow_status(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetWorkflowStatus property.

                Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_workflow_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ImageSetCreatedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ImageSetDeleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetDeleted",
    ):
        '''(experimental) aws.healthimaging@ImageSetDeleted event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            image_set_deleted = healthimaging_events.DatastoreEvents.ImageSetDeleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetDeleted.ImageSetDeletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "event_metadata": "eventMetadata",
                "image_set_id": "imageSetId",
                "image_set_state": "imageSetState",
                "image_set_workflow_status": "imageSetWorkflowStatus",
                "imaging_version": "imagingVersion",
            },
        )
        class ImageSetDeletedProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@ImageSetDeleted event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    image_set_deleted_props = healthimaging_events.DatastoreEvents.ImageSetDeleted.ImageSetDeletedProps(
                        datastore_id=["datastoreId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        image_set_id=["imageSetId"],
                        image_set_state=["imageSetState"],
                        image_set_workflow_status=["imageSetWorkflowStatus"],
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4c79377a0d548b2a24f4deaf7514daab148e6afa66bafee0ca739fd488ef338e)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument image_set_id", value=image_set_id, expected_type=type_hints["image_set_id"])
                    check_type(argname="argument image_set_state", value=image_set_state, expected_type=type_hints["image_set_state"])
                    check_type(argname="argument image_set_workflow_status", value=image_set_workflow_status, expected_type=type_hints["image_set_workflow_status"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if image_set_id is not None:
                    self._values["image_set_id"] = image_set_id
                if image_set_state is not None:
                    self._values["image_set_state"] = image_set_state
                if image_set_workflow_status is not None:
                    self._values["image_set_workflow_status"] = image_set_workflow_status
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
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
            def image_set_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetId property.

                Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetState property.

                Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_workflow_status(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetWorkflowStatus property.

                Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_workflow_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ImageSetDeletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ImageSetDeleting(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetDeleting",
    ):
        '''(experimental) aws.healthimaging@ImageSetDeleting event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            image_set_deleting = healthimaging_events.DatastoreEvents.ImageSetDeleting()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetDeleting.ImageSetDeletingProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "event_metadata": "eventMetadata",
                "image_set_id": "imageSetId",
                "image_set_state": "imageSetState",
                "image_set_workflow_status": "imageSetWorkflowStatus",
                "imaging_version": "imagingVersion",
            },
        )
        class ImageSetDeletingProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@ImageSetDeleting event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    image_set_deleting_props = healthimaging_events.DatastoreEvents.ImageSetDeleting.ImageSetDeletingProps(
                        datastore_id=["datastoreId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        image_set_id=["imageSetId"],
                        image_set_state=["imageSetState"],
                        image_set_workflow_status=["imageSetWorkflowStatus"],
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__9a775ee84c99194b844db92146754219ccb876813fb717b4a25e62a45a6d349e)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument image_set_id", value=image_set_id, expected_type=type_hints["image_set_id"])
                    check_type(argname="argument image_set_state", value=image_set_state, expected_type=type_hints["image_set_state"])
                    check_type(argname="argument image_set_workflow_status", value=image_set_workflow_status, expected_type=type_hints["image_set_workflow_status"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if image_set_id is not None:
                    self._values["image_set_id"] = image_set_id
                if image_set_state is not None:
                    self._values["image_set_state"] = image_set_state
                if image_set_workflow_status is not None:
                    self._values["image_set_workflow_status"] = image_set_workflow_status
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
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
            def image_set_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetId property.

                Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetState property.

                Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_workflow_status(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetWorkflowStatus property.

                Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_workflow_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ImageSetDeletingProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ImageSetUpdateFailed(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetUpdateFailed",
    ):
        '''(experimental) aws.healthimaging@ImageSetUpdateFailed event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            image_set_update_failed = healthimaging_events.DatastoreEvents.ImageSetUpdateFailed()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetUpdateFailed.ImageSetUpdateFailedProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "event_metadata": "eventMetadata",
                "image_set_id": "imageSetId",
                "image_set_state": "imageSetState",
                "image_set_workflow_status": "imageSetWorkflowStatus",
                "imaging_version": "imagingVersion",
            },
        )
        class ImageSetUpdateFailedProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@ImageSetUpdateFailed event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    image_set_update_failed_props = healthimaging_events.DatastoreEvents.ImageSetUpdateFailed.ImageSetUpdateFailedProps(
                        datastore_id=["datastoreId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        image_set_id=["imageSetId"],
                        image_set_state=["imageSetState"],
                        image_set_workflow_status=["imageSetWorkflowStatus"],
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1ceff61b967826ead8f17340df2eb27464019594c7ae0cf3e72f50379b3f5073)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument image_set_id", value=image_set_id, expected_type=type_hints["image_set_id"])
                    check_type(argname="argument image_set_state", value=image_set_state, expected_type=type_hints["image_set_state"])
                    check_type(argname="argument image_set_workflow_status", value=image_set_workflow_status, expected_type=type_hints["image_set_workflow_status"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if image_set_id is not None:
                    self._values["image_set_id"] = image_set_id
                if image_set_state is not None:
                    self._values["image_set_state"] = image_set_state
                if image_set_workflow_status is not None:
                    self._values["image_set_workflow_status"] = image_set_workflow_status
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
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
            def image_set_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetId property.

                Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetState property.

                Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_workflow_status(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetWorkflowStatus property.

                Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_workflow_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ImageSetUpdateFailedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ImageSetUpdated(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetUpdated",
    ):
        '''(experimental) aws.healthimaging@ImageSetUpdated event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            image_set_updated = healthimaging_events.DatastoreEvents.ImageSetUpdated()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetUpdated.ImageSetUpdatedProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "event_metadata": "eventMetadata",
                "image_set_id": "imageSetId",
                "image_set_state": "imageSetState",
                "image_set_workflow_status": "imageSetWorkflowStatus",
                "imaging_version": "imagingVersion",
            },
        )
        class ImageSetUpdatedProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@ImageSetUpdated event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    image_set_updated_props = healthimaging_events.DatastoreEvents.ImageSetUpdated.ImageSetUpdatedProps(
                        datastore_id=["datastoreId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        image_set_id=["imageSetId"],
                        image_set_state=["imageSetState"],
                        image_set_workflow_status=["imageSetWorkflowStatus"],
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8ed667caa3fc6db6e321626edab24fd6d9acab874d4f1b8068121df353b12440)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument image_set_id", value=image_set_id, expected_type=type_hints["image_set_id"])
                    check_type(argname="argument image_set_state", value=image_set_state, expected_type=type_hints["image_set_state"])
                    check_type(argname="argument image_set_workflow_status", value=image_set_workflow_status, expected_type=type_hints["image_set_workflow_status"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if image_set_id is not None:
                    self._values["image_set_id"] = image_set_id
                if image_set_state is not None:
                    self._values["image_set_state"] = image_set_state
                if image_set_workflow_status is not None:
                    self._values["image_set_workflow_status"] = image_set_workflow_status
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
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
            def image_set_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetId property.

                Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetState property.

                Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_workflow_status(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetWorkflowStatus property.

                Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_workflow_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ImageSetUpdatedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ImageSetUpdating(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetUpdating",
    ):
        '''(experimental) aws.healthimaging@ImageSetUpdating event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            image_set_updating = healthimaging_events.DatastoreEvents.ImageSetUpdating()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImageSetUpdating.ImageSetUpdatingProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "event_metadata": "eventMetadata",
                "image_set_id": "imageSetId",
                "image_set_state": "imageSetState",
                "image_set_workflow_status": "imageSetWorkflowStatus",
                "imaging_version": "imagingVersion",
            },
        )
        class ImageSetUpdatingProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@ImageSetUpdating event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param image_set_id: (experimental) imageSetId property. Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_state: (experimental) imageSetState property. Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_set_workflow_status: (experimental) imageSetWorkflowStatus property. Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    image_set_updating_props = healthimaging_events.DatastoreEvents.ImageSetUpdating.ImageSetUpdatingProps(
                        datastore_id=["datastoreId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        image_set_id=["imageSetId"],
                        image_set_state=["imageSetState"],
                        image_set_workflow_status=["imageSetWorkflowStatus"],
                        imaging_version=["imagingVersion"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__62d4638ff305a474edb82ec727318d96645f7079455b0c12d9de0f2f69459aaf)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument image_set_id", value=image_set_id, expected_type=type_hints["image_set_id"])
                    check_type(argname="argument image_set_state", value=image_set_state, expected_type=type_hints["image_set_state"])
                    check_type(argname="argument image_set_workflow_status", value=image_set_workflow_status, expected_type=type_hints["image_set_workflow_status"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if image_set_id is not None:
                    self._values["image_set_id"] = image_set_id
                if image_set_state is not None:
                    self._values["image_set_state"] = image_set_state
                if image_set_workflow_status is not None:
                    self._values["image_set_workflow_status"] = image_set_workflow_status
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
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
            def image_set_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetId property.

                Specify an array of string values to match this event if the actual value of imageSetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetState property.

                Specify an array of string values to match this event if the actual value of imageSetState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_set_workflow_status(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageSetWorkflowStatus property.

                Specify an array of string values to match this event if the actual value of imageSetWorkflowStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_set_workflow_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ImageSetUpdatingProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ImportJobCompleted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImportJobCompleted",
    ):
        '''(experimental) aws.healthimaging@ImportJobCompleted event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            import_job_completed = healthimaging_events.DatastoreEvents.ImportJobCompleted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImportJobCompleted.ImportJobCompletedProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "event_metadata": "eventMetadata",
                "imaging_version": "imagingVersion",
                "input_s3_uri": "inputS3Uri",
                "job_id": "jobId",
                "job_name": "jobName",
                "job_status": "jobStatus",
                "output_s3_uri": "outputS3Uri",
            },
        )
        class ImportJobCompletedProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                input_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                output_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@ImportJobCompleted event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param input_s3_uri: (experimental) inputS3Uri property. Specify an array of string values to match this event if the actual value of inputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param job_id: (experimental) jobId property. Specify an array of string values to match this event if the actual value of jobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param job_name: (experimental) jobName property. Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param job_status: (experimental) jobStatus property. Specify an array of string values to match this event if the actual value of jobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param output_s3_uri: (experimental) outputS3Uri property. Specify an array of string values to match this event if the actual value of outputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    import_job_completed_props = healthimaging_events.DatastoreEvents.ImportJobCompleted.ImportJobCompletedProps(
                        datastore_id=["datastoreId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        imaging_version=["imagingVersion"],
                        input_s3_uri=["inputS3Uri"],
                        job_id=["jobId"],
                        job_name=["jobName"],
                        job_status=["jobStatus"],
                        output_s3_uri=["outputS3Uri"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__6f58e81d704ff877088dc336e96601f77c257c2a68f33cbc7d630d8bff1557a1)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                    check_type(argname="argument input_s3_uri", value=input_s3_uri, expected_type=type_hints["input_s3_uri"])
                    check_type(argname="argument job_id", value=job_id, expected_type=type_hints["job_id"])
                    check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
                    check_type(argname="argument job_status", value=job_status, expected_type=type_hints["job_status"])
                    check_type(argname="argument output_s3_uri", value=output_s3_uri, expected_type=type_hints["output_s3_uri"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version
                if input_s3_uri is not None:
                    self._values["input_s3_uri"] = input_s3_uri
                if job_id is not None:
                    self._values["job_id"] = job_id
                if job_name is not None:
                    self._values["job_name"] = job_name
                if job_status is not None:
                    self._values["job_status"] = job_status
                if output_s3_uri is not None:
                    self._values["output_s3_uri"] = output_s3_uri

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
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
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def input_s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) inputS3Uri property.

                Specify an array of string values to match this event if the actual value of inputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("input_s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobId property.

                Specify an array of string values to match this event if the actual value of jobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobName property.

                Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobStatus property.

                Specify an array of string values to match this event if the actual value of jobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def output_s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) outputS3Uri property.

                Specify an array of string values to match this event if the actual value of outputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("output_s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ImportJobCompletedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ImportJobFailed(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImportJobFailed",
    ):
        '''(experimental) aws.healthimaging@ImportJobFailed event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            import_job_failed = healthimaging_events.DatastoreEvents.ImportJobFailed()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImportJobFailed.ImportJobFailedProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "event_metadata": "eventMetadata",
                "imaging_version": "imagingVersion",
                "input_s3_uri": "inputS3Uri",
                "job_id": "jobId",
                "job_name": "jobName",
                "job_status": "jobStatus",
                "output_s3_uri": "outputS3Uri",
            },
        )
        class ImportJobFailedProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                input_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                output_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@ImportJobFailed event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param input_s3_uri: (experimental) inputS3Uri property. Specify an array of string values to match this event if the actual value of inputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param job_id: (experimental) jobId property. Specify an array of string values to match this event if the actual value of jobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param job_name: (experimental) jobName property. Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param job_status: (experimental) jobStatus property. Specify an array of string values to match this event if the actual value of jobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param output_s3_uri: (experimental) outputS3Uri property. Specify an array of string values to match this event if the actual value of outputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    import_job_failed_props = healthimaging_events.DatastoreEvents.ImportJobFailed.ImportJobFailedProps(
                        datastore_id=["datastoreId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        imaging_version=["imagingVersion"],
                        input_s3_uri=["inputS3Uri"],
                        job_id=["jobId"],
                        job_name=["jobName"],
                        job_status=["jobStatus"],
                        output_s3_uri=["outputS3Uri"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__6432e7870b009ac16b7084c3a3f72974a57411ce34dd275d8533402fcc320795)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                    check_type(argname="argument input_s3_uri", value=input_s3_uri, expected_type=type_hints["input_s3_uri"])
                    check_type(argname="argument job_id", value=job_id, expected_type=type_hints["job_id"])
                    check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
                    check_type(argname="argument job_status", value=job_status, expected_type=type_hints["job_status"])
                    check_type(argname="argument output_s3_uri", value=output_s3_uri, expected_type=type_hints["output_s3_uri"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version
                if input_s3_uri is not None:
                    self._values["input_s3_uri"] = input_s3_uri
                if job_id is not None:
                    self._values["job_id"] = job_id
                if job_name is not None:
                    self._values["job_name"] = job_name
                if job_status is not None:
                    self._values["job_status"] = job_status
                if output_s3_uri is not None:
                    self._values["output_s3_uri"] = output_s3_uri

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
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
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def input_s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) inputS3Uri property.

                Specify an array of string values to match this event if the actual value of inputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("input_s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobId property.

                Specify an array of string values to match this event if the actual value of jobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobName property.

                Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobStatus property.

                Specify an array of string values to match this event if the actual value of jobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def output_s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) outputS3Uri property.

                Specify an array of string values to match this event if the actual value of outputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("output_s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ImportJobFailedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ImportJobInProgress(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImportJobInProgress",
    ):
        '''(experimental) aws.healthimaging@ImportJobInProgress event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            import_job_in_progress = healthimaging_events.DatastoreEvents.ImportJobInProgress()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImportJobInProgress.ImportJobInProgressProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "event_metadata": "eventMetadata",
                "imaging_version": "imagingVersion",
                "input_s3_uri": "inputS3Uri",
                "job_id": "jobId",
                "job_name": "jobName",
                "job_status": "jobStatus",
                "output_s3_uri": "outputS3Uri",
            },
        )
        class ImportJobInProgressProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                input_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                output_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@ImportJobInProgress event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param input_s3_uri: (experimental) inputS3Uri property. Specify an array of string values to match this event if the actual value of inputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param job_id: (experimental) jobId property. Specify an array of string values to match this event if the actual value of jobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param job_name: (experimental) jobName property. Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param job_status: (experimental) jobStatus property. Specify an array of string values to match this event if the actual value of jobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param output_s3_uri: (experimental) outputS3Uri property. Specify an array of string values to match this event if the actual value of outputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    import_job_in_progress_props = healthimaging_events.DatastoreEvents.ImportJobInProgress.ImportJobInProgressProps(
                        datastore_id=["datastoreId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        imaging_version=["imagingVersion"],
                        input_s3_uri=["inputS3Uri"],
                        job_id=["jobId"],
                        job_name=["jobName"],
                        job_status=["jobStatus"],
                        output_s3_uri=["outputS3Uri"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__367138ab4facecbc1f9b6bf4e67e1867de104a1cde9a6ca2a901d26039e493c1)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                    check_type(argname="argument input_s3_uri", value=input_s3_uri, expected_type=type_hints["input_s3_uri"])
                    check_type(argname="argument job_id", value=job_id, expected_type=type_hints["job_id"])
                    check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
                    check_type(argname="argument job_status", value=job_status, expected_type=type_hints["job_status"])
                    check_type(argname="argument output_s3_uri", value=output_s3_uri, expected_type=type_hints["output_s3_uri"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version
                if input_s3_uri is not None:
                    self._values["input_s3_uri"] = input_s3_uri
                if job_id is not None:
                    self._values["job_id"] = job_id
                if job_name is not None:
                    self._values["job_name"] = job_name
                if job_status is not None:
                    self._values["job_status"] = job_status
                if output_s3_uri is not None:
                    self._values["output_s3_uri"] = output_s3_uri

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
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
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def input_s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) inputS3Uri property.

                Specify an array of string values to match this event if the actual value of inputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("input_s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobId property.

                Specify an array of string values to match this event if the actual value of jobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobName property.

                Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobStatus property.

                Specify an array of string values to match this event if the actual value of jobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def output_s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) outputS3Uri property.

                Specify an array of string values to match this event if the actual value of outputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("output_s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ImportJobInProgressProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ImportJobSubmitted(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImportJobSubmitted",
    ):
        '''(experimental) aws.healthimaging@ImportJobSubmitted event types for Datastore.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
            
            import_job_submitted = healthimaging_events.DatastoreEvents.ImportJobSubmitted()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_healthimaging.events.DatastoreEvents.ImportJobSubmitted.ImportJobSubmittedProps",
            jsii_struct_bases=[],
            name_mapping={
                "datastore_id": "datastoreId",
                "event_metadata": "eventMetadata",
                "imaging_version": "imagingVersion",
                "input_s3_uri": "inputS3Uri",
                "job_id": "jobId",
                "job_name": "jobName",
                "job_status": "jobStatus",
                "output_s3_uri": "outputS3Uri",
            },
        )
        class ImportJobSubmittedProps:
            def __init__(
                self,
                *,
                datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                input_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
                output_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Datastore aws.healthimaging@ImportJobSubmitted event.

                :param datastore_id: (experimental) datastoreId property. Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Datastore reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param imaging_version: (experimental) imagingVersion property. Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param input_s3_uri: (experimental) inputS3Uri property. Specify an array of string values to match this event if the actual value of inputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param job_id: (experimental) jobId property. Specify an array of string values to match this event if the actual value of jobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param job_name: (experimental) jobName property. Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param job_status: (experimental) jobStatus property. Specify an array of string values to match this event if the actual value of jobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param output_s3_uri: (experimental) outputS3Uri property. Specify an array of string values to match this event if the actual value of outputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_healthimaging import events as healthimaging_events
                    
                    import_job_submitted_props = healthimaging_events.DatastoreEvents.ImportJobSubmitted.ImportJobSubmittedProps(
                        datastore_id=["datastoreId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        imaging_version=["imagingVersion"],
                        input_s3_uri=["inputS3Uri"],
                        job_id=["jobId"],
                        job_name=["jobName"],
                        job_status=["jobStatus"],
                        output_s3_uri=["outputS3Uri"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__b272d71f7f6a11bdc36ef34be98aac267c9c6ed967be9c257b28bdec7239bdd2)
                    check_type(argname="argument datastore_id", value=datastore_id, expected_type=type_hints["datastore_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument imaging_version", value=imaging_version, expected_type=type_hints["imaging_version"])
                    check_type(argname="argument input_s3_uri", value=input_s3_uri, expected_type=type_hints["input_s3_uri"])
                    check_type(argname="argument job_id", value=job_id, expected_type=type_hints["job_id"])
                    check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
                    check_type(argname="argument job_status", value=job_status, expected_type=type_hints["job_status"])
                    check_type(argname="argument output_s3_uri", value=output_s3_uri, expected_type=type_hints["output_s3_uri"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if datastore_id is not None:
                    self._values["datastore_id"] = datastore_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if imaging_version is not None:
                    self._values["imaging_version"] = imaging_version
                if input_s3_uri is not None:
                    self._values["input_s3_uri"] = input_s3_uri
                if job_id is not None:
                    self._values["job_id"] = job_id
                if job_name is not None:
                    self._values["job_name"] = job_name
                if job_status is not None:
                    self._values["job_status"] = job_status
                if output_s3_uri is not None:
                    self._values["output_s3_uri"] = output_s3_uri

            @builtins.property
            def datastore_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) datastoreId property.

                Specify an array of string values to match this event if the actual value of datastoreId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Datastore reference

                :stability: experimental
                '''
                result = self._values.get("datastore_id")
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
            def imaging_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagingVersion property.

                Specify an array of string values to match this event if the actual value of imagingVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("imaging_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def input_s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) inputS3Uri property.

                Specify an array of string values to match this event if the actual value of inputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("input_s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobId property.

                Specify an array of string values to match this event if the actual value of jobId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobName property.

                Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobStatus property.

                Specify an array of string values to match this event if the actual value of jobStatus is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def output_s3_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) outputS3Uri property.

                Specify an array of string values to match this event if the actual value of outputS3Uri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("output_s3_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ImportJobSubmittedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "DatastoreEvents",
]

publication.publish()

def _typecheckingstub__3ca879ca9e80089c19b1c74410be72304e565fe5c3eb228c8d71887426e98d3d(
    datastore_ref: _aws_cdk_interfaces_aws_healthimaging_ceddda9d.IDatastoreRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab19a59976c7256f7d655e05796472951d856031fd8249b48b921a52f67eaebd(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed55e5fff196758596b97ae599bf3c40992a720da649d35f1965cd9500d2ee81(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0425c77a76ca4705210826e43d8c73bf4a8c56941ac5190da634ef30438644d(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a07e2d107b7ea80e08901660b2a16cb0f719421399285186468b9a7c5ed9598(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1799c1fd6a086755e0eba2d0f79f634b336b3e6a19da7faa557bcbed6620706(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    datastore_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    datastore_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4fc278513849c1d9b45855cae8f41258bd15fd5446bf5953e082e68e104091(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2178d745fa07792399da17d1b6dca27831eeaab192b6c96f95e492bafc9d2851(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7cf994140cabb653cc480a3ea98e2eff82f99ba43403fb2f88bc3fd8fb2812a(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b118236682f832af9978754461f32fb470d4726c57bace61ec8feb3178ef20(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a1f218b54a7eb345df4b9d4c38ab7b6800f535c2b7432c844e255b10eeb06a(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c79377a0d548b2a24f4deaf7514daab148e6afa66bafee0ca739fd488ef338e(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a775ee84c99194b844db92146754219ccb876813fb717b4a25e62a45a6d349e(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ceff61b967826ead8f17340df2eb27464019594c7ae0cf3e72f50379b3f5073(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed667caa3fc6db6e321626edab24fd6d9acab874d4f1b8068121df353b12440(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d4638ff305a474edb82ec727318d96645f7079455b0c12d9de0f2f69459aaf(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    image_set_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_set_workflow_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f58e81d704ff877088dc336e96601f77c257c2a68f33cbc7d630d8bff1557a1(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    input_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    output_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6432e7870b009ac16b7084c3a3f72974a57411ce34dd275d8533402fcc320795(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    input_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    output_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367138ab4facecbc1f9b6bf4e67e1867de104a1cde9a6ca2a901d26039e493c1(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    input_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    output_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b272d71f7f6a11bdc36ef34be98aac267c9c6ed967be9c257b28bdec7239bdd2(
    *,
    datastore_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    imaging_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    input_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_status: typing.Optional[typing.Sequence[builtins.str]] = None,
    output_s3_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
