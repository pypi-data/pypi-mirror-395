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
import aws_cdk.interfaces.aws_iotanalytics as _aws_cdk_interfaces_aws_iotanalytics_ceddda9d


class DatasetEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.events.DatasetEvents",
):
    '''(experimental) EventBridge event patterns for Dataset.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_iotanalytics import events as iotanalytics_events
        from aws_cdk.interfaces import aws_iotanalytics as interfaces_iotanalytics
        
        # dataset_ref: interfaces_iotanalytics.IDatasetRef
        
        dataset_events = iotanalytics_events.DatasetEvents.from_dataset(dataset_ref)
    '''

    @jsii.member(jsii_name="fromDataset")
    @builtins.classmethod
    def from_dataset(
        cls,
        dataset_ref: _aws_cdk_interfaces_aws_iotanalytics_ceddda9d.IDatasetRef,
    ) -> "DatasetEvents":
        '''(experimental) Create DatasetEvents from a Dataset reference.

        :param dataset_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0888a757557b64940c14f06424ba81603a9a1b6e2c2701ce4d4636ce0eeffee)
            check_type(argname="argument dataset_ref", value=dataset_ref, expected_type=type_hints["dataset_ref"])
        return typing.cast("DatasetEvents", jsii.sinvoke(cls, "fromDataset", [dataset_ref]))

    @jsii.member(jsii_name="ioTAnalyticsDataSetLifeCycleNotificationPattern")
    def io_t_analytics_data_set_life_cycle_notification_pattern(
        self,
        *,
        content_delivery_rule_index: typing.Optional[typing.Sequence[builtins.str]] = None,
        dataset_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_detail_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        message: typing.Optional[typing.Sequence[builtins.str]] = None,
        state: typing.Optional[typing.Sequence[builtins.str]] = None,
        version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Dataset IoT Analytics DataSet Lifecycle Notification.

        :param content_delivery_rule_index: (experimental) content-delivery-rule-index property. Specify an array of string values to match this event if the actual value of content-delivery-rule-index is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param dataset_name: (experimental) dataset-name property. Specify an array of string values to match this event if the actual value of dataset-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Dataset reference
        :param event_detail_version: (experimental) event-detail-version property. Specify an array of string values to match this event if the actual value of event-detail-version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param message: (experimental) message property. Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param state: (experimental) state property. Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version_id: (experimental) version-id property. Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatasetEvents.IoTAnalyticsDataSetLifeCycleNotification.IoTAnalyticsDataSetLifeCycleNotificationProps(
            content_delivery_rule_index=content_delivery_rule_index,
            dataset_name=dataset_name,
            event_detail_version=event_detail_version,
            event_metadata=event_metadata,
            message=message,
            state=state,
            version_id=version_id,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "ioTAnalyticsDataSetLifeCycleNotificationPattern", [options]))

    class IoTAnalyticsDataSetLifeCycleNotification(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.events.DatasetEvents.IoTAnalyticsDataSetLifeCycleNotification",
    ):
        '''(experimental) aws.iotanalytics@IoTAnalyticsDataSetLifeCycleNotification event types for Dataset.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotanalytics import events as iotanalytics_events
            
            io_tAnalytics_data_set_life_cycle_notification = iotanalytics_events.DatasetEvents.IoTAnalyticsDataSetLifeCycleNotification()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_iotanalytics.events.DatasetEvents.IoTAnalyticsDataSetLifeCycleNotification.IoTAnalyticsDataSetLifeCycleNotificationProps",
            jsii_struct_bases=[],
            name_mapping={
                "content_delivery_rule_index": "contentDeliveryRuleIndex",
                "dataset_name": "datasetName",
                "event_detail_version": "eventDetailVersion",
                "event_metadata": "eventMetadata",
                "message": "message",
                "state": "state",
                "version_id": "versionId",
            },
        )
        class IoTAnalyticsDataSetLifeCycleNotificationProps:
            def __init__(
                self,
                *,
                content_delivery_rule_index: typing.Optional[typing.Sequence[builtins.str]] = None,
                dataset_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_detail_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                message: typing.Optional[typing.Sequence[builtins.str]] = None,
                state: typing.Optional[typing.Sequence[builtins.str]] = None,
                version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Dataset aws.iotanalytics@IoTAnalyticsDataSetLifeCycleNotification event.

                :param content_delivery_rule_index: (experimental) content-delivery-rule-index property. Specify an array of string values to match this event if the actual value of content-delivery-rule-index is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param dataset_name: (experimental) dataset-name property. Specify an array of string values to match this event if the actual value of dataset-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Dataset reference
                :param event_detail_version: (experimental) event-detail-version property. Specify an array of string values to match this event if the actual value of event-detail-version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param message: (experimental) message property. Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param state: (experimental) state property. Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version_id: (experimental) version-id property. Specify an array of string values to match this event if the actual value of version-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_iotanalytics import events as iotanalytics_events
                    
                    io_tAnalytics_data_set_life_cycle_notification_props = iotanalytics_events.DatasetEvents.IoTAnalyticsDataSetLifeCycleNotification.IoTAnalyticsDataSetLifeCycleNotificationProps(
                        content_delivery_rule_index=["contentDeliveryRuleIndex"],
                        dataset_name=["datasetName"],
                        event_detail_version=["eventDetailVersion"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        message=["message"],
                        state=["state"],
                        version_id=["versionId"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__83f10d07de7f3969495991b322af9e5d0c264bd2c5dce8d6a7688bd5537207e8)
                    check_type(argname="argument content_delivery_rule_index", value=content_delivery_rule_index, expected_type=type_hints["content_delivery_rule_index"])
                    check_type(argname="argument dataset_name", value=dataset_name, expected_type=type_hints["dataset_name"])
                    check_type(argname="argument event_detail_version", value=event_detail_version, expected_type=type_hints["event_detail_version"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument message", value=message, expected_type=type_hints["message"])
                    check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                    check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if content_delivery_rule_index is not None:
                    self._values["content_delivery_rule_index"] = content_delivery_rule_index
                if dataset_name is not None:
                    self._values["dataset_name"] = dataset_name
                if event_detail_version is not None:
                    self._values["event_detail_version"] = event_detail_version
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if message is not None:
                    self._values["message"] = message
                if state is not None:
                    self._values["state"] = state
                if version_id is not None:
                    self._values["version_id"] = version_id

            @builtins.property
            def content_delivery_rule_index(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) content-delivery-rule-index property.

                Specify an array of string values to match this event if the actual value of content-delivery-rule-index is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("content_delivery_rule_index")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def dataset_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) dataset-name property.

                Specify an array of string values to match this event if the actual value of dataset-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Dataset reference

                :stability: experimental
                '''
                result = self._values.get("dataset_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_detail_version(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) event-detail-version property.

                Specify an array of string values to match this event if the actual value of event-detail-version is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_detail_version")
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
            def message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) message property.

                Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("message")
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
                return "IoTAnalyticsDataSetLifeCycleNotificationProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "DatasetEvents",
]

publication.publish()

def _typecheckingstub__d0888a757557b64940c14f06424ba81603a9a1b6e2c2701ce4d4636ce0eeffee(
    dataset_ref: _aws_cdk_interfaces_aws_iotanalytics_ceddda9d.IDatasetRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f10d07de7f3969495991b322af9e5d0c264bd2c5dce8d6a7688bd5537207e8(
    *,
    content_delivery_rule_index: typing.Optional[typing.Sequence[builtins.str]] = None,
    dataset_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_detail_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    message: typing.Optional[typing.Sequence[builtins.str]] = None,
    state: typing.Optional[typing.Sequence[builtins.str]] = None,
    version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
