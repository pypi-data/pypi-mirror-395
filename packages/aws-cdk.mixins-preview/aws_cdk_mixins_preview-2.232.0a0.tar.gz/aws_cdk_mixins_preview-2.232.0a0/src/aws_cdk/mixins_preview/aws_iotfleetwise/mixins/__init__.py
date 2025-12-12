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
import aws_cdk.interfaces.aws_kinesisfirehose as _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d
import aws_cdk.interfaces.aws_logs as _aws_cdk_interfaces_aws_logs_ceddda9d
import aws_cdk.interfaces.aws_s3 as _aws_cdk_interfaces_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8
from ...aws_logs import ILogsDelivery as _ILogsDelivery_0d3c9e29
from ...core import IMixin as _IMixin_11e4b965, Mixin as _Mixin_a69446c0
from ...mixins import (
    CfnPropertyMixinOptions as _CfnPropertyMixinOptions_9cbff649,
    PropertyMergeStrategy as _PropertyMergeStrategy_49c157e8,
)


class CfnCampaignIotFleetwiseLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignIotFleetwiseLogs",
):
    '''Builder for CfnCampaignLogsMixin to generate IOT_FLEETWISE_LOGS for CfnCampaign.

    :cloudformationResource: AWS::IoTFleetWise::Campaign
    :logType: IOT_FLEETWISE_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
        
        cfn_campaign_iot_fleetwise_logs = iotfleetwise_mixins.CfnCampaignIotFleetwiseLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> "CfnCampaignLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630fec47114c66fbf5f43dad52048cc8e1c197ba952ba7ba924711ffe0b460b3)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnCampaignLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnCampaignLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__512c3d621d8d9c3890261d0dad562241b190570d99d13ad5c1c2465a53a1df98)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnCampaignLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnCampaignLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd57edef5bc4d1901ec9a5d34ea72bccfdd5d806203dc67418816dff487e7868)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnCampaignLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnCampaignLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignLogsMixin",
):
    '''Creates an orchestration of data collection rules.

    The AWS IoT FleetWise Edge Agent software running in vehicles uses campaigns to decide how to collect and transfer data to the cloud. You create campaigns in the cloud. After you or your team approve campaigns, AWS IoT FleetWise automatically deploys them to vehicles.

    For more information, see `Campaigns <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/campaigns.html>`_ in the *AWS IoT FleetWise Developer Guide* .
    .. epigraph::

       Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html
    :cloudformationResource: AWS::IoTFleetWise::Campaign
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_campaign_logs_mixin = iotfleetwise_mixins.CfnCampaignLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::IoTFleetWise::Campaign``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c4d9cffac2f9300d18014c39cef28b00cf3d8ae1c0b3644be9e56476020297)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
        jsii.create(self.__class__, self, [log_type, log_delivery])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        resource: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply vended logs configuration to the construct.

        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd58e2e3d7d32f233fed65ac0184e9ee913c86758e2a2b249d9b768546047140)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9986aed3b65eb283281ac9ce9f9c853f8ed770db37b151fa2454a8416cbd6825)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="IOT_FLEETWISE_LOGS")
    def IOT_FLEETWISE_LOGS(cls) -> CfnCampaignIotFleetwiseLogs:
        return typing.cast(CfnCampaignIotFleetwiseLogs, jsii.sget(cls, "IOT_FLEETWISE_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "collection_scheme": "collectionScheme",
        "compression": "compression",
        "data_destination_configs": "dataDestinationConfigs",
        "data_extra_dimensions": "dataExtraDimensions",
        "data_partitions": "dataPartitions",
        "description": "description",
        "diagnostics_mode": "diagnosticsMode",
        "expiry_time": "expiryTime",
        "name": "name",
        "post_trigger_collection_duration": "postTriggerCollectionDuration",
        "priority": "priority",
        "signal_catalog_arn": "signalCatalogArn",
        "signals_to_collect": "signalsToCollect",
        "signals_to_fetch": "signalsToFetch",
        "spooling_mode": "spoolingMode",
        "start_time": "startTime",
        "tags": "tags",
        "target_arn": "targetArn",
    },
)
class CfnCampaignMixinProps:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        collection_scheme: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.CollectionSchemeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        compression: typing.Optional[builtins.str] = None,
        data_destination_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.DataDestinationConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        data_extra_dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        data_partitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.DataPartitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        diagnostics_mode: typing.Optional[builtins.str] = None,
        expiry_time: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        post_trigger_collection_duration: typing.Optional[jsii.Number] = None,
        priority: typing.Optional[jsii.Number] = None,
        signal_catalog_arn: typing.Optional[builtins.str] = None,
        signals_to_collect: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.SignalInformationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        signals_to_fetch: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.SignalFetchInformationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        spooling_mode: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCampaignPropsMixin.

        :param action: Specifies how to update a campaign. The action can be one of the following:. - ``APPROVE`` - To approve delivering a data collection scheme to vehicles. - ``SUSPEND`` - To suspend collecting signal data. The campaign is deleted from vehicles and all vehicles in the suspended campaign will stop sending data. - ``RESUME`` - To reactivate the ``SUSPEND`` campaign. The campaign is redeployed to all vehicles and the vehicles will resume sending data. - ``UPDATE`` - To update a campaign.
        :param collection_scheme: The data collection scheme associated with the campaign. You can specify a scheme that collects data based on time or an event.
        :param compression: Whether to compress signals before transmitting data to AWS IoT FleetWise . If you don't want to compress the signals, use ``OFF`` . If it's not specified, ``SNAPPY`` is used. Default: ``SNAPPY`` Default: - "OFF"
        :param data_destination_configs: The destination where the campaign sends data. You can choose to send data to be stored in Amazon S3 or Amazon Timestream . Amazon S3 optimizes the cost of data storage and provides additional mechanisms to use vehicle data, such as data lakes, centralized data storage, data processing pipelines, and analytics. AWS IoT FleetWise supports at-least-once file delivery to S3. Your vehicle data is stored on multiple AWS IoT FleetWise servers for redundancy and high availability. You can use Amazon Timestream to access and analyze time series data, and Timestream to query vehicle data so that you can identify trends and patterns.
        :param data_extra_dimensions: A list of vehicle attributes to associate with a campaign. Enrich the data with specified vehicle attributes. For example, add ``make`` and ``model`` to the campaign, and AWS IoT FleetWise will associate the data with those attributes as dimensions in Amazon Timestream . You can then query the data against ``make`` and ``model`` . Default: An empty array
        :param data_partitions: The data partitions associated with the signals collected from the vehicle.
        :param description: The description of the campaign.
        :param diagnostics_mode: Option for a vehicle to send diagnostic trouble codes to AWS IoT FleetWise . If you want to send diagnostic trouble codes, use ``SEND_ACTIVE_DTCS`` . If it's not specified, ``OFF`` is used. Default: ``OFF`` Default: - "OFF"
        :param expiry_time: The time the campaign expires, in seconds since epoch (January 1, 1970 at midnight UTC time). Vehicle data isn't collected after the campaign expires. Default: 253402214400 (December 31, 9999, 00:00:00 UTC) Default: - "253402214400"
        :param name: The name of a campaign.
        :param post_trigger_collection_duration: How long (in milliseconds) to collect raw data after a triggering event initiates the collection. If it's not specified, ``0`` is used. Default: ``0`` Default: - 0
        :param priority: A number indicating the priority of one campaign over another campaign for a certain vehicle or fleet. A campaign with the lowest value is deployed to vehicles before any other campaigns. If it's not specified, ``0`` is used. Default: ``0`` Default: - 0
        :param signal_catalog_arn: The Amazon Resource Name (ARN) of the signal catalog associated with the campaign.
        :param signals_to_collect: A list of information about signals to collect.
        :param signals_to_fetch: A list of information about signals to fetch.
        :param spooling_mode: Whether to store collected data after a vehicle lost a connection with the cloud. After a connection is re-established, the data is automatically forwarded to AWS IoT FleetWise . If you want to store collected data when a vehicle loses connection with the cloud, use ``TO_DISK`` . If it's not specified, ``OFF`` is used. Default: ``OFF`` Default: - "OFF"
        :param start_time: The time, in milliseconds, to deliver a campaign after it was approved. If it's not specified, ``0`` is used. Default: ``0`` Default: - "0"
        :param tags: Metadata that can be used to manage the campaign.
        :param target_arn: The Amazon Resource Name (ARN) of a vehicle or fleet to which the campaign is deployed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
            
            cfn_campaign_mixin_props = iotfleetwise_mixins.CfnCampaignMixinProps(
                action="action",
                collection_scheme=iotfleetwise_mixins.CfnCampaignPropsMixin.CollectionSchemeProperty(
                    condition_based_collection_scheme=iotfleetwise_mixins.CfnCampaignPropsMixin.ConditionBasedCollectionSchemeProperty(
                        condition_language_version=123,
                        expression="expression",
                        minimum_trigger_interval_ms=123,
                        trigger_mode="triggerMode"
                    ),
                    time_based_collection_scheme=iotfleetwise_mixins.CfnCampaignPropsMixin.TimeBasedCollectionSchemeProperty(
                        period_ms=123
                    )
                ),
                compression="compression",
                data_destination_configs=[iotfleetwise_mixins.CfnCampaignPropsMixin.DataDestinationConfigProperty(
                    mqtt_topic_config=iotfleetwise_mixins.CfnCampaignPropsMixin.MqttTopicConfigProperty(
                        execution_role_arn="executionRoleArn",
                        mqtt_topic_arn="mqttTopicArn"
                    ),
                    s3_config=iotfleetwise_mixins.CfnCampaignPropsMixin.S3ConfigProperty(
                        bucket_arn="bucketArn",
                        data_format="dataFormat",
                        prefix="prefix",
                        storage_compression_format="storageCompressionFormat"
                    ),
                    timestream_config=iotfleetwise_mixins.CfnCampaignPropsMixin.TimestreamConfigProperty(
                        execution_role_arn="executionRoleArn",
                        timestream_table_arn="timestreamTableArn"
                    )
                )],
                data_extra_dimensions=["dataExtraDimensions"],
                data_partitions=[iotfleetwise_mixins.CfnCampaignPropsMixin.DataPartitionProperty(
                    id="id",
                    storage_options=iotfleetwise_mixins.CfnCampaignPropsMixin.DataPartitionStorageOptionsProperty(
                        maximum_size=iotfleetwise_mixins.CfnCampaignPropsMixin.StorageMaximumSizeProperty(
                            unit="unit",
                            value=123
                        ),
                        minimum_time_to_live=iotfleetwise_mixins.CfnCampaignPropsMixin.StorageMinimumTimeToLiveProperty(
                            unit="unit",
                            value=123
                        ),
                        storage_location="storageLocation"
                    ),
                    upload_options=iotfleetwise_mixins.CfnCampaignPropsMixin.DataPartitionUploadOptionsProperty(
                        condition_language_version=123,
                        expression="expression"
                    )
                )],
                description="description",
                diagnostics_mode="diagnosticsMode",
                expiry_time="expiryTime",
                name="name",
                post_trigger_collection_duration=123,
                priority=123,
                signal_catalog_arn="signalCatalogArn",
                signals_to_collect=[iotfleetwise_mixins.CfnCampaignPropsMixin.SignalInformationProperty(
                    data_partition_id="dataPartitionId",
                    max_sample_count=123,
                    minimum_sampling_interval_ms=123,
                    name="name"
                )],
                signals_to_fetch=[iotfleetwise_mixins.CfnCampaignPropsMixin.SignalFetchInformationProperty(
                    actions=["actions"],
                    condition_language_version=123,
                    fully_qualified_name="fullyQualifiedName",
                    signal_fetch_config=iotfleetwise_mixins.CfnCampaignPropsMixin.SignalFetchConfigProperty(
                        condition_based=iotfleetwise_mixins.CfnCampaignPropsMixin.ConditionBasedSignalFetchConfigProperty(
                            condition_expression="conditionExpression",
                            trigger_mode="triggerMode"
                        ),
                        time_based=iotfleetwise_mixins.CfnCampaignPropsMixin.TimeBasedSignalFetchConfigProperty(
                            execution_frequency_ms=123
                        )
                    )
                )],
                spooling_mode="spoolingMode",
                start_time="startTime",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_arn="targetArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef469060f2a29d712b4d16a2f4a2dcf59a2a4de41d076e9cc4a7c13ac48f8b29)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument collection_scheme", value=collection_scheme, expected_type=type_hints["collection_scheme"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument data_destination_configs", value=data_destination_configs, expected_type=type_hints["data_destination_configs"])
            check_type(argname="argument data_extra_dimensions", value=data_extra_dimensions, expected_type=type_hints["data_extra_dimensions"])
            check_type(argname="argument data_partitions", value=data_partitions, expected_type=type_hints["data_partitions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument diagnostics_mode", value=diagnostics_mode, expected_type=type_hints["diagnostics_mode"])
            check_type(argname="argument expiry_time", value=expiry_time, expected_type=type_hints["expiry_time"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument post_trigger_collection_duration", value=post_trigger_collection_duration, expected_type=type_hints["post_trigger_collection_duration"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument signal_catalog_arn", value=signal_catalog_arn, expected_type=type_hints["signal_catalog_arn"])
            check_type(argname="argument signals_to_collect", value=signals_to_collect, expected_type=type_hints["signals_to_collect"])
            check_type(argname="argument signals_to_fetch", value=signals_to_fetch, expected_type=type_hints["signals_to_fetch"])
            check_type(argname="argument spooling_mode", value=spooling_mode, expected_type=type_hints["spooling_mode"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if collection_scheme is not None:
            self._values["collection_scheme"] = collection_scheme
        if compression is not None:
            self._values["compression"] = compression
        if data_destination_configs is not None:
            self._values["data_destination_configs"] = data_destination_configs
        if data_extra_dimensions is not None:
            self._values["data_extra_dimensions"] = data_extra_dimensions
        if data_partitions is not None:
            self._values["data_partitions"] = data_partitions
        if description is not None:
            self._values["description"] = description
        if diagnostics_mode is not None:
            self._values["diagnostics_mode"] = diagnostics_mode
        if expiry_time is not None:
            self._values["expiry_time"] = expiry_time
        if name is not None:
            self._values["name"] = name
        if post_trigger_collection_duration is not None:
            self._values["post_trigger_collection_duration"] = post_trigger_collection_duration
        if priority is not None:
            self._values["priority"] = priority
        if signal_catalog_arn is not None:
            self._values["signal_catalog_arn"] = signal_catalog_arn
        if signals_to_collect is not None:
            self._values["signals_to_collect"] = signals_to_collect
        if signals_to_fetch is not None:
            self._values["signals_to_fetch"] = signals_to_fetch
        if spooling_mode is not None:
            self._values["spooling_mode"] = spooling_mode
        if start_time is not None:
            self._values["start_time"] = start_time
        if tags is not None:
            self._values["tags"] = tags
        if target_arn is not None:
            self._values["target_arn"] = target_arn

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Specifies how to update a campaign. The action can be one of the following:.

        - ``APPROVE`` - To approve delivering a data collection scheme to vehicles.
        - ``SUSPEND`` - To suspend collecting signal data. The campaign is deleted from vehicles and all vehicles in the suspended campaign will stop sending data.
        - ``RESUME`` - To reactivate the ``SUSPEND`` campaign. The campaign is redeployed to all vehicles and the vehicles will resume sending data.
        - ``UPDATE`` - To update a campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def collection_scheme(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CollectionSchemeProperty"]]:
        '''The data collection scheme associated with the campaign.

        You can specify a scheme that collects data based on time or an event.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-collectionscheme
        '''
        result = self._values.get("collection_scheme")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CollectionSchemeProperty"]], result)

    @builtins.property
    def compression(self) -> typing.Optional[builtins.str]:
        '''Whether to compress signals before transmitting data to AWS IoT FleetWise .

        If you don't want to compress the signals, use ``OFF`` . If it's not specified, ``SNAPPY`` is used.

        Default: ``SNAPPY``

        :default: - "OFF"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-compression
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_destination_configs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.DataDestinationConfigProperty"]]]]:
        '''The destination where the campaign sends data.

        You can choose to send data to be stored in Amazon S3 or Amazon Timestream .

        Amazon S3 optimizes the cost of data storage and provides additional mechanisms to use vehicle data, such as data lakes, centralized data storage, data processing pipelines, and analytics. AWS IoT FleetWise supports at-least-once file delivery to S3. Your vehicle data is stored on multiple AWS IoT FleetWise servers for redundancy and high availability.

        You can use Amazon Timestream to access and analyze time series data, and Timestream to query vehicle data so that you can identify trends and patterns.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-datadestinationconfigs
        '''
        result = self._values.get("data_destination_configs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.DataDestinationConfigProperty"]]]], result)

    @builtins.property
    def data_extra_dimensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of vehicle attributes to associate with a campaign.

        Enrich the data with specified vehicle attributes. For example, add ``make`` and ``model`` to the campaign, and AWS IoT FleetWise will associate the data with those attributes as dimensions in Amazon Timestream . You can then query the data against ``make`` and ``model`` .

        Default: An empty array

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-dataextradimensions
        '''
        result = self._values.get("data_extra_dimensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def data_partitions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.DataPartitionProperty"]]]]:
        '''The data partitions associated with the signals collected from the vehicle.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-datapartitions
        '''
        result = self._values.get("data_partitions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.DataPartitionProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def diagnostics_mode(self) -> typing.Optional[builtins.str]:
        '''Option for a vehicle to send diagnostic trouble codes to AWS IoT FleetWise .

        If you want to send diagnostic trouble codes, use ``SEND_ACTIVE_DTCS`` . If it's not specified, ``OFF`` is used.

        Default: ``OFF``

        :default: - "OFF"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-diagnosticsmode
        '''
        result = self._values.get("diagnostics_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiry_time(self) -> typing.Optional[builtins.str]:
        '''The time the campaign expires, in seconds since epoch (January 1, 1970 at midnight UTC time).

        Vehicle data isn't collected after the campaign expires.

        Default: 253402214400 (December 31, 9999, 00:00:00 UTC)

        :default: - "253402214400"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-expirytime
        '''
        result = self._values.get("expiry_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of a campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_trigger_collection_duration(self) -> typing.Optional[jsii.Number]:
        '''How long (in milliseconds) to collect raw data after a triggering event initiates the collection.

        If it's not specified, ``0`` is used.

        Default: ``0``

        :default: - 0

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-posttriggercollectionduration
        '''
        result = self._values.get("post_trigger_collection_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''A number indicating the priority of one campaign over another campaign for a certain vehicle or fleet.

        A campaign with the lowest value is deployed to vehicles before any other campaigns. If it's not specified, ``0`` is used.

        Default: ``0``

        :default: - 0

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-priority
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def signal_catalog_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the signal catalog associated with the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-signalcatalogarn
        '''
        result = self._values.get("signal_catalog_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signals_to_collect(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SignalInformationProperty"]]]]:
        '''A list of information about signals to collect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-signalstocollect
        '''
        result = self._values.get("signals_to_collect")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SignalInformationProperty"]]]], result)

    @builtins.property
    def signals_to_fetch(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SignalFetchInformationProperty"]]]]:
        '''A list of information about signals to fetch.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-signalstofetch
        '''
        result = self._values.get("signals_to_fetch")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SignalFetchInformationProperty"]]]], result)

    @builtins.property
    def spooling_mode(self) -> typing.Optional[builtins.str]:
        '''Whether to store collected data after a vehicle lost a connection with the cloud.

        After a connection is re-established, the data is automatically forwarded to AWS IoT FleetWise . If you want to store collected data when a vehicle loses connection with the cloud, use ``TO_DISK`` . If it's not specified, ``OFF`` is used.

        Default: ``OFF``

        :default: - "OFF"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-spoolingmode
        '''
        result = self._values.get("spooling_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The time, in milliseconds, to deliver a campaign after it was approved. If it's not specified, ``0`` is used.

        Default: ``0``

        :default: - "0"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-starttime
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata that can be used to manage the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of a vehicle or fleet to which the campaign is deployed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html#cfn-iotfleetwise-campaign-targetarn
        '''
        result = self._values.get("target_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCampaignMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCampaignPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin",
):
    '''Creates an orchestration of data collection rules.

    The AWS IoT FleetWise Edge Agent software running in vehicles uses campaigns to decide how to collect and transfer data to the cloud. You create campaigns in the cloud. After you or your team approve campaigns, AWS IoT FleetWise automatically deploys them to vehicles.

    For more information, see `Campaigns <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/campaigns.html>`_ in the *AWS IoT FleetWise Developer Guide* .
    .. epigraph::

       Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-campaign.html
    :cloudformationResource: AWS::IoTFleetWise::Campaign
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
        
        cfn_campaign_props_mixin = iotfleetwise_mixins.CfnCampaignPropsMixin(iotfleetwise_mixins.CfnCampaignMixinProps(
            action="action",
            collection_scheme=iotfleetwise_mixins.CfnCampaignPropsMixin.CollectionSchemeProperty(
                condition_based_collection_scheme=iotfleetwise_mixins.CfnCampaignPropsMixin.ConditionBasedCollectionSchemeProperty(
                    condition_language_version=123,
                    expression="expression",
                    minimum_trigger_interval_ms=123,
                    trigger_mode="triggerMode"
                ),
                time_based_collection_scheme=iotfleetwise_mixins.CfnCampaignPropsMixin.TimeBasedCollectionSchemeProperty(
                    period_ms=123
                )
            ),
            compression="compression",
            data_destination_configs=[iotfleetwise_mixins.CfnCampaignPropsMixin.DataDestinationConfigProperty(
                mqtt_topic_config=iotfleetwise_mixins.CfnCampaignPropsMixin.MqttTopicConfigProperty(
                    execution_role_arn="executionRoleArn",
                    mqtt_topic_arn="mqttTopicArn"
                ),
                s3_config=iotfleetwise_mixins.CfnCampaignPropsMixin.S3ConfigProperty(
                    bucket_arn="bucketArn",
                    data_format="dataFormat",
                    prefix="prefix",
                    storage_compression_format="storageCompressionFormat"
                ),
                timestream_config=iotfleetwise_mixins.CfnCampaignPropsMixin.TimestreamConfigProperty(
                    execution_role_arn="executionRoleArn",
                    timestream_table_arn="timestreamTableArn"
                )
            )],
            data_extra_dimensions=["dataExtraDimensions"],
            data_partitions=[iotfleetwise_mixins.CfnCampaignPropsMixin.DataPartitionProperty(
                id="id",
                storage_options=iotfleetwise_mixins.CfnCampaignPropsMixin.DataPartitionStorageOptionsProperty(
                    maximum_size=iotfleetwise_mixins.CfnCampaignPropsMixin.StorageMaximumSizeProperty(
                        unit="unit",
                        value=123
                    ),
                    minimum_time_to_live=iotfleetwise_mixins.CfnCampaignPropsMixin.StorageMinimumTimeToLiveProperty(
                        unit="unit",
                        value=123
                    ),
                    storage_location="storageLocation"
                ),
                upload_options=iotfleetwise_mixins.CfnCampaignPropsMixin.DataPartitionUploadOptionsProperty(
                    condition_language_version=123,
                    expression="expression"
                )
            )],
            description="description",
            diagnostics_mode="diagnosticsMode",
            expiry_time="expiryTime",
            name="name",
            post_trigger_collection_duration=123,
            priority=123,
            signal_catalog_arn="signalCatalogArn",
            signals_to_collect=[iotfleetwise_mixins.CfnCampaignPropsMixin.SignalInformationProperty(
                data_partition_id="dataPartitionId",
                max_sample_count=123,
                minimum_sampling_interval_ms=123,
                name="name"
            )],
            signals_to_fetch=[iotfleetwise_mixins.CfnCampaignPropsMixin.SignalFetchInformationProperty(
                actions=["actions"],
                condition_language_version=123,
                fully_qualified_name="fullyQualifiedName",
                signal_fetch_config=iotfleetwise_mixins.CfnCampaignPropsMixin.SignalFetchConfigProperty(
                    condition_based=iotfleetwise_mixins.CfnCampaignPropsMixin.ConditionBasedSignalFetchConfigProperty(
                        condition_expression="conditionExpression",
                        trigger_mode="triggerMode"
                    ),
                    time_based=iotfleetwise_mixins.CfnCampaignPropsMixin.TimeBasedSignalFetchConfigProperty(
                        execution_frequency_ms=123
                    )
                )
            )],
            spooling_mode="spoolingMode",
            start_time="startTime",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_arn="targetArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCampaignMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTFleetWise::Campaign``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29efdcd8395af7f9b54278e8edb3b73730306c5057af1e093e8436fb6a028899)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        options = _CfnPropertyMixinOptions_9cbff649(strategy=strategy)

        jsii.create(self.__class__, self, [props, options])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply the mixin properties to the construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e23a8d5ac0623715aaf47d042ece0a0e9205eb2bb26f91e338738d6566cb445)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf10d24ef247d923dd5c3606b12b7bc85dfaf02f37f872aa5832755d15ef344e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCampaignMixinProps:
        return typing.cast(CfnCampaignMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.CollectionSchemeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition_based_collection_scheme": "conditionBasedCollectionScheme",
            "time_based_collection_scheme": "timeBasedCollectionScheme",
        },
    )
    class CollectionSchemeProperty:
        def __init__(
            self,
            *,
            condition_based_collection_scheme: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.ConditionBasedCollectionSchemeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            time_based_collection_scheme: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TimeBasedCollectionSchemeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies what data to collect and how often or when to collect it.

            :param condition_based_collection_scheme: Information about a collection scheme that uses a simple logical expression to recognize what data to collect.
            :param time_based_collection_scheme: Information about a collection scheme that uses a time period to decide how often to collect data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-collectionscheme.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                collection_scheme_property = iotfleetwise_mixins.CfnCampaignPropsMixin.CollectionSchemeProperty(
                    condition_based_collection_scheme=iotfleetwise_mixins.CfnCampaignPropsMixin.ConditionBasedCollectionSchemeProperty(
                        condition_language_version=123,
                        expression="expression",
                        minimum_trigger_interval_ms=123,
                        trigger_mode="triggerMode"
                    ),
                    time_based_collection_scheme=iotfleetwise_mixins.CfnCampaignPropsMixin.TimeBasedCollectionSchemeProperty(
                        period_ms=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__29b660eb8c2290b786c9bb8b2b6509b0fa76546e3d34dd04153af10d8af5cd8e)
                check_type(argname="argument condition_based_collection_scheme", value=condition_based_collection_scheme, expected_type=type_hints["condition_based_collection_scheme"])
                check_type(argname="argument time_based_collection_scheme", value=time_based_collection_scheme, expected_type=type_hints["time_based_collection_scheme"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition_based_collection_scheme is not None:
                self._values["condition_based_collection_scheme"] = condition_based_collection_scheme
            if time_based_collection_scheme is not None:
                self._values["time_based_collection_scheme"] = time_based_collection_scheme

        @builtins.property
        def condition_based_collection_scheme(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ConditionBasedCollectionSchemeProperty"]]:
            '''Information about a collection scheme that uses a simple logical expression to recognize what data to collect.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-collectionscheme.html#cfn-iotfleetwise-campaign-collectionscheme-conditionbasedcollectionscheme
            '''
            result = self._values.get("condition_based_collection_scheme")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ConditionBasedCollectionSchemeProperty"]], result)

        @builtins.property
        def time_based_collection_scheme(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimeBasedCollectionSchemeProperty"]]:
            '''Information about a collection scheme that uses a time period to decide how often to collect data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-collectionscheme.html#cfn-iotfleetwise-campaign-collectionscheme-timebasedcollectionscheme
            '''
            result = self._values.get("time_based_collection_scheme")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimeBasedCollectionSchemeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CollectionSchemeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.ConditionBasedCollectionSchemeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition_language_version": "conditionLanguageVersion",
            "expression": "expression",
            "minimum_trigger_interval_ms": "minimumTriggerIntervalMs",
            "trigger_mode": "triggerMode",
        },
    )
    class ConditionBasedCollectionSchemeProperty:
        def __init__(
            self,
            *,
            condition_language_version: typing.Optional[jsii.Number] = None,
            expression: typing.Optional[builtins.str] = None,
            minimum_trigger_interval_ms: typing.Optional[jsii.Number] = None,
            trigger_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a collection scheme that uses a simple logical expression to recognize what data to collect.

            :param condition_language_version: Specifies the version of the conditional expression language.
            :param expression: The logical expression used to recognize what data to collect. For example, ``$variable.Vehicle.OutsideAirTemperature >= 105.0`` .
            :param minimum_trigger_interval_ms: The minimum duration of time between two triggering events to collect data, in milliseconds. .. epigraph:: If a signal changes often, you might want to collect data at a slower rate.
            :param trigger_mode: Whether to collect data for all triggering events ( ``ALWAYS`` ). Specify ( ``RISING_EDGE`` ), or specify only when the condition first evaluates to false. For example, triggering on "AirbagDeployed"; Users aren't interested on triggering when the airbag is already exploded; they only care about the change from not deployed => deployed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-conditionbasedcollectionscheme.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                condition_based_collection_scheme_property = iotfleetwise_mixins.CfnCampaignPropsMixin.ConditionBasedCollectionSchemeProperty(
                    condition_language_version=123,
                    expression="expression",
                    minimum_trigger_interval_ms=123,
                    trigger_mode="triggerMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ad8e7775f292e4ce1f0fe49769a4ae42901e727983a5dc2a7ec6e470bc4bf28)
                check_type(argname="argument condition_language_version", value=condition_language_version, expected_type=type_hints["condition_language_version"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument minimum_trigger_interval_ms", value=minimum_trigger_interval_ms, expected_type=type_hints["minimum_trigger_interval_ms"])
                check_type(argname="argument trigger_mode", value=trigger_mode, expected_type=type_hints["trigger_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition_language_version is not None:
                self._values["condition_language_version"] = condition_language_version
            if expression is not None:
                self._values["expression"] = expression
            if minimum_trigger_interval_ms is not None:
                self._values["minimum_trigger_interval_ms"] = minimum_trigger_interval_ms
            if trigger_mode is not None:
                self._values["trigger_mode"] = trigger_mode

        @builtins.property
        def condition_language_version(self) -> typing.Optional[jsii.Number]:
            '''Specifies the version of the conditional expression language.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-conditionbasedcollectionscheme.html#cfn-iotfleetwise-campaign-conditionbasedcollectionscheme-conditionlanguageversion
            '''
            result = self._values.get("condition_language_version")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The logical expression used to recognize what data to collect.

            For example, ``$variable.Vehicle.OutsideAirTemperature >= 105.0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-conditionbasedcollectionscheme.html#cfn-iotfleetwise-campaign-conditionbasedcollectionscheme-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def minimum_trigger_interval_ms(self) -> typing.Optional[jsii.Number]:
            '''The minimum duration of time between two triggering events to collect data, in milliseconds.

            .. epigraph::

               If a signal changes often, you might want to collect data at a slower rate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-conditionbasedcollectionscheme.html#cfn-iotfleetwise-campaign-conditionbasedcollectionscheme-minimumtriggerintervalms
            '''
            result = self._values.get("minimum_trigger_interval_ms")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def trigger_mode(self) -> typing.Optional[builtins.str]:
            '''Whether to collect data for all triggering events ( ``ALWAYS`` ).

            Specify ( ``RISING_EDGE`` ), or specify only when the condition first evaluates to false. For example, triggering on "AirbagDeployed"; Users aren't interested on triggering when the airbag is already exploded; they only care about the change from not deployed => deployed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-conditionbasedcollectionscheme.html#cfn-iotfleetwise-campaign-conditionbasedcollectionscheme-triggermode
            '''
            result = self._values.get("trigger_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionBasedCollectionSchemeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.ConditionBasedSignalFetchConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition_expression": "conditionExpression",
            "trigger_mode": "triggerMode",
        },
    )
    class ConditionBasedSignalFetchConfigProperty:
        def __init__(
            self,
            *,
            condition_expression: typing.Optional[builtins.str] = None,
            trigger_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the condition under which a signal fetch occurs.

            :param condition_expression: The condition that must be satisfied to trigger a signal fetch.
            :param trigger_mode: Indicates the mode in which the signal fetch is triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-conditionbasedsignalfetchconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                condition_based_signal_fetch_config_property = iotfleetwise_mixins.CfnCampaignPropsMixin.ConditionBasedSignalFetchConfigProperty(
                    condition_expression="conditionExpression",
                    trigger_mode="triggerMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02d899366ccf1ea4679bc1c55781b9ac6761cb2005c8d9ee66244b4c27978a73)
                check_type(argname="argument condition_expression", value=condition_expression, expected_type=type_hints["condition_expression"])
                check_type(argname="argument trigger_mode", value=trigger_mode, expected_type=type_hints["trigger_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition_expression is not None:
                self._values["condition_expression"] = condition_expression
            if trigger_mode is not None:
                self._values["trigger_mode"] = trigger_mode

        @builtins.property
        def condition_expression(self) -> typing.Optional[builtins.str]:
            '''The condition that must be satisfied to trigger a signal fetch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-conditionbasedsignalfetchconfig.html#cfn-iotfleetwise-campaign-conditionbasedsignalfetchconfig-conditionexpression
            '''
            result = self._values.get("condition_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def trigger_mode(self) -> typing.Optional[builtins.str]:
            '''Indicates the mode in which the signal fetch is triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-conditionbasedsignalfetchconfig.html#cfn-iotfleetwise-campaign-conditionbasedsignalfetchconfig-triggermode
            '''
            result = self._values.get("trigger_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionBasedSignalFetchConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.DataDestinationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "mqtt_topic_config": "mqttTopicConfig",
            "s3_config": "s3Config",
            "timestream_config": "timestreamConfig",
        },
    )
    class DataDestinationConfigProperty:
        def __init__(
            self,
            *,
            mqtt_topic_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.MqttTopicConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.S3ConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timestream_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TimestreamConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The destination where the AWS IoT FleetWise campaign sends data.

            You can send data to be stored in Amazon S3 or Amazon Timestream .

            :param mqtt_topic_config: The MQTT topic to which the AWS IoT FleetWise campaign routes data. .. epigraph:: Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .
            :param s3_config: The Amazon S3 bucket where the AWS IoT FleetWise campaign sends data.
            :param timestream_config: The Amazon Timestream table where the campaign sends data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datadestinationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                data_destination_config_property = iotfleetwise_mixins.CfnCampaignPropsMixin.DataDestinationConfigProperty(
                    mqtt_topic_config=iotfleetwise_mixins.CfnCampaignPropsMixin.MqttTopicConfigProperty(
                        execution_role_arn="executionRoleArn",
                        mqtt_topic_arn="mqttTopicArn"
                    ),
                    s3_config=iotfleetwise_mixins.CfnCampaignPropsMixin.S3ConfigProperty(
                        bucket_arn="bucketArn",
                        data_format="dataFormat",
                        prefix="prefix",
                        storage_compression_format="storageCompressionFormat"
                    ),
                    timestream_config=iotfleetwise_mixins.CfnCampaignPropsMixin.TimestreamConfigProperty(
                        execution_role_arn="executionRoleArn",
                        timestream_table_arn="timestreamTableArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1e97707447746c3cd40d98aef1cd412bc0775d74db4d40cd46ac2785a92cdbc8)
                check_type(argname="argument mqtt_topic_config", value=mqtt_topic_config, expected_type=type_hints["mqtt_topic_config"])
                check_type(argname="argument s3_config", value=s3_config, expected_type=type_hints["s3_config"])
                check_type(argname="argument timestream_config", value=timestream_config, expected_type=type_hints["timestream_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mqtt_topic_config is not None:
                self._values["mqtt_topic_config"] = mqtt_topic_config
            if s3_config is not None:
                self._values["s3_config"] = s3_config
            if timestream_config is not None:
                self._values["timestream_config"] = timestream_config

        @builtins.property
        def mqtt_topic_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MqttTopicConfigProperty"]]:
            '''The MQTT topic to which the AWS IoT FleetWise campaign routes data.

            .. epigraph::

               Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datadestinationconfig.html#cfn-iotfleetwise-campaign-datadestinationconfig-mqtttopicconfig
            '''
            result = self._values.get("mqtt_topic_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.MqttTopicConfigProperty"]], result)

        @builtins.property
        def s3_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.S3ConfigProperty"]]:
            '''The Amazon S3 bucket where the AWS IoT FleetWise campaign sends data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datadestinationconfig.html#cfn-iotfleetwise-campaign-datadestinationconfig-s3config
            '''
            result = self._values.get("s3_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.S3ConfigProperty"]], result)

        @builtins.property
        def timestream_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimestreamConfigProperty"]]:
            '''The Amazon Timestream table where the campaign sends data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datadestinationconfig.html#cfn-iotfleetwise-campaign-datadestinationconfig-timestreamconfig
            '''
            result = self._values.get("timestream_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimestreamConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataDestinationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.DataPartitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "storage_options": "storageOptions",
            "upload_options": "uploadOptions",
        },
    )
    class DataPartitionProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            storage_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.DataPartitionStorageOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            upload_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.DataPartitionUploadOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for signal data storage and upload options.

            You can only specify these options when the campaign's spooling mode is ``TO_DISK`` .
            .. epigraph::

               Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

            :param id: The ID of the data partition. The data partition ID must be unique within a campaign. You can establish a data partition as the default partition for a campaign by using ``default`` as the ID.
            :param storage_options: The storage options for a data partition.
            :param upload_options: The upload options for the data partition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datapartition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                data_partition_property = iotfleetwise_mixins.CfnCampaignPropsMixin.DataPartitionProperty(
                    id="id",
                    storage_options=iotfleetwise_mixins.CfnCampaignPropsMixin.DataPartitionStorageOptionsProperty(
                        maximum_size=iotfleetwise_mixins.CfnCampaignPropsMixin.StorageMaximumSizeProperty(
                            unit="unit",
                            value=123
                        ),
                        minimum_time_to_live=iotfleetwise_mixins.CfnCampaignPropsMixin.StorageMinimumTimeToLiveProperty(
                            unit="unit",
                            value=123
                        ),
                        storage_location="storageLocation"
                    ),
                    upload_options=iotfleetwise_mixins.CfnCampaignPropsMixin.DataPartitionUploadOptionsProperty(
                        condition_language_version=123,
                        expression="expression"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__564c891e9b1c0bef0fc7fe315cabd79dcede4a9fbe1dbf46c82c44674ad127e3)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument storage_options", value=storage_options, expected_type=type_hints["storage_options"])
                check_type(argname="argument upload_options", value=upload_options, expected_type=type_hints["upload_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if storage_options is not None:
                self._values["storage_options"] = storage_options
            if upload_options is not None:
                self._values["upload_options"] = upload_options

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the data partition.

            The data partition ID must be unique within a campaign. You can establish a data partition as the default partition for a campaign by using ``default`` as the ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datapartition.html#cfn-iotfleetwise-campaign-datapartition-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def storage_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.DataPartitionStorageOptionsProperty"]]:
            '''The storage options for a data partition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datapartition.html#cfn-iotfleetwise-campaign-datapartition-storageoptions
            '''
            result = self._values.get("storage_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.DataPartitionStorageOptionsProperty"]], result)

        @builtins.property
        def upload_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.DataPartitionUploadOptionsProperty"]]:
            '''The upload options for the data partition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datapartition.html#cfn-iotfleetwise-campaign-datapartition-uploadoptions
            '''
            result = self._values.get("upload_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.DataPartitionUploadOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataPartitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.DataPartitionStorageOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maximum_size": "maximumSize",
            "minimum_time_to_live": "minimumTimeToLive",
            "storage_location": "storageLocation",
        },
    )
    class DataPartitionStorageOptionsProperty:
        def __init__(
            self,
            *,
            maximum_size: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.StorageMaximumSizeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            minimum_time_to_live: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.StorageMinimumTimeToLiveProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            storage_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Size, time, and location options for the data partition.

            :param maximum_size: The maximum storage size of the data stored in the data partition. .. epigraph:: Newer data overwrites older data when the partition reaches the maximum size.
            :param minimum_time_to_live: The amount of time that data in this partition will be kept on disk. - After the designated amount of time passes, the data can be removed, but it's not guaranteed to be removed. - Before the time expires, data in this partition can still be deleted if the partition reaches its configured maximum size. - Newer data will overwrite older data when the partition reaches the maximum size.
            :param storage_location: The folder name for the data partition under the campaign storage folder.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datapartitionstorageoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                data_partition_storage_options_property = iotfleetwise_mixins.CfnCampaignPropsMixin.DataPartitionStorageOptionsProperty(
                    maximum_size=iotfleetwise_mixins.CfnCampaignPropsMixin.StorageMaximumSizeProperty(
                        unit="unit",
                        value=123
                    ),
                    minimum_time_to_live=iotfleetwise_mixins.CfnCampaignPropsMixin.StorageMinimumTimeToLiveProperty(
                        unit="unit",
                        value=123
                    ),
                    storage_location="storageLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1be44bc980597a32848ecf63d22cbe4aee7e143ed3426333ac0d6e0bc11d797f)
                check_type(argname="argument maximum_size", value=maximum_size, expected_type=type_hints["maximum_size"])
                check_type(argname="argument minimum_time_to_live", value=minimum_time_to_live, expected_type=type_hints["minimum_time_to_live"])
                check_type(argname="argument storage_location", value=storage_location, expected_type=type_hints["storage_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maximum_size is not None:
                self._values["maximum_size"] = maximum_size
            if minimum_time_to_live is not None:
                self._values["minimum_time_to_live"] = minimum_time_to_live
            if storage_location is not None:
                self._values["storage_location"] = storage_location

        @builtins.property
        def maximum_size(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.StorageMaximumSizeProperty"]]:
            '''The maximum storage size of the data stored in the data partition.

            .. epigraph::

               Newer data overwrites older data when the partition reaches the maximum size.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datapartitionstorageoptions.html#cfn-iotfleetwise-campaign-datapartitionstorageoptions-maximumsize
            '''
            result = self._values.get("maximum_size")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.StorageMaximumSizeProperty"]], result)

        @builtins.property
        def minimum_time_to_live(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.StorageMinimumTimeToLiveProperty"]]:
            '''The amount of time that data in this partition will be kept on disk.

            - After the designated amount of time passes, the data can be removed, but it's not guaranteed to be removed.
            - Before the time expires, data in this partition can still be deleted if the partition reaches its configured maximum size.
            - Newer data will overwrite older data when the partition reaches the maximum size.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datapartitionstorageoptions.html#cfn-iotfleetwise-campaign-datapartitionstorageoptions-minimumtimetolive
            '''
            result = self._values.get("minimum_time_to_live")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.StorageMinimumTimeToLiveProperty"]], result)

        @builtins.property
        def storage_location(self) -> typing.Optional[builtins.str]:
            '''The folder name for the data partition under the campaign storage folder.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datapartitionstorageoptions.html#cfn-iotfleetwise-campaign-datapartitionstorageoptions-storagelocation
            '''
            result = self._values.get("storage_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataPartitionStorageOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.DataPartitionUploadOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition_language_version": "conditionLanguageVersion",
            "expression": "expression",
        },
    )
    class DataPartitionUploadOptionsProperty:
        def __init__(
            self,
            *,
            condition_language_version: typing.Optional[jsii.Number] = None,
            expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The upload options for the data partition.

            If upload options are specified, you must also specify storage options. See `DataPartitionStorageOptions <https://docs.aws.amazon.com/iot-fleetwise/latest/APIReference/API_DataPartitionStorageOptions.html>`_ .
            .. epigraph::

               Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

            :param condition_language_version: The version of the condition language. Defaults to the most recent condition language version.
            :param expression: The logical expression used to recognize what data to collect. For example, ``$variable.``Vehicle.OutsideAirTemperature`` >= 105.0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datapartitionuploadoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                data_partition_upload_options_property = iotfleetwise_mixins.CfnCampaignPropsMixin.DataPartitionUploadOptionsProperty(
                    condition_language_version=123,
                    expression="expression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f7142fda7b830738813a9f50893c67e500ad35281dcdb4bc55fe8f4e6ae771c5)
                check_type(argname="argument condition_language_version", value=condition_language_version, expected_type=type_hints["condition_language_version"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition_language_version is not None:
                self._values["condition_language_version"] = condition_language_version
            if expression is not None:
                self._values["expression"] = expression

        @builtins.property
        def condition_language_version(self) -> typing.Optional[jsii.Number]:
            '''The version of the condition language.

            Defaults to the most recent condition language version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datapartitionuploadoptions.html#cfn-iotfleetwise-campaign-datapartitionuploadoptions-conditionlanguageversion
            '''
            result = self._values.get("condition_language_version")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The logical expression used to recognize what data to collect.

            For example, ``$variable.``Vehicle.OutsideAirTemperature`` >= 105.0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-datapartitionuploadoptions.html#cfn-iotfleetwise-campaign-datapartitionuploadoptions-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataPartitionUploadOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.MqttTopicConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "execution_role_arn": "executionRoleArn",
            "mqtt_topic_arn": "mqttTopicArn",
        },
    )
    class MqttTopicConfigProperty:
        def __init__(
            self,
            *,
            execution_role_arn: typing.Optional[builtins.str] = None,
            mqtt_topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The MQTT topic to which the AWS IoT FleetWise campaign routes data.

            For more information, see `Device communication protocols <https://docs.aws.amazon.com/iot/latest/developerguide/protocols.html>`_ in the *AWS IoT Core Developer Guide* .
            .. epigraph::

               Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

            :param execution_role_arn: The ARN of the role that grants AWS IoT FleetWise permission to access and act on messages sent to the MQTT topic.
            :param mqtt_topic_arn: The ARN of the MQTT topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-mqtttopicconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                mqtt_topic_config_property = iotfleetwise_mixins.CfnCampaignPropsMixin.MqttTopicConfigProperty(
                    execution_role_arn="executionRoleArn",
                    mqtt_topic_arn="mqttTopicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f5d04c8e775759659605ff3c19c9fd657f3428d5fa8e09c4570ac2faef8686b1)
                check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
                check_type(argname="argument mqtt_topic_arn", value=mqtt_topic_arn, expected_type=type_hints["mqtt_topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if execution_role_arn is not None:
                self._values["execution_role_arn"] = execution_role_arn
            if mqtt_topic_arn is not None:
                self._values["mqtt_topic_arn"] = mqtt_topic_arn

        @builtins.property
        def execution_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role that grants AWS IoT FleetWise permission to access and act on messages sent to the MQTT topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-mqtttopicconfig.html#cfn-iotfleetwise-campaign-mqtttopicconfig-executionrolearn
            '''
            result = self._values.get("execution_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mqtt_topic_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the MQTT topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-mqtttopicconfig.html#cfn-iotfleetwise-campaign-mqtttopicconfig-mqtttopicarn
            '''
            result = self._values.get("mqtt_topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MqttTopicConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.S3ConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_arn": "bucketArn",
            "data_format": "dataFormat",
            "prefix": "prefix",
            "storage_compression_format": "storageCompressionFormat",
        },
    )
    class S3ConfigProperty:
        def __init__(
            self,
            *,
            bucket_arn: typing.Optional[builtins.str] = None,
            data_format: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            storage_compression_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon S3 bucket where the AWS IoT FleetWise campaign sends data.

            Amazon S3 is an object storage service that stores data as objects within buckets. For more information, see `Creating, configuring, and working with Amazon S3 buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html>`_ in the *Amazon Simple Storage Service User Guide* .

            :param bucket_arn: The Amazon Resource Name (ARN) of the Amazon S3 bucket.
            :param data_format: Specify the format that files are saved in the Amazon S3 bucket. You can save files in an Apache Parquet or JSON format. - Parquet - Store data in a columnar storage file format. Parquet is optimal for fast data retrieval and can reduce costs. This option is selected by default. - JSON - Store data in a standard text-based JSON file format.
            :param prefix: Enter an S3 bucket prefix. The prefix is the string of characters after the bucket name and before the object name. You can use the prefix to organize data stored in Amazon S3 buckets. For more information, see `Organizing objects using prefixes <https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html>`_ in the *Amazon Simple Storage Service User Guide* . By default, AWS IoT FleetWise sets the prefix ``processed-data/year=YY/month=MM/date=DD/hour=HH/`` (in UTC) to data it delivers to Amazon S3 . You can enter a prefix to append it to this default prefix. For example, if you enter the prefix ``vehicles`` , the prefix will be ``vehicles/processed-data/year=YY/month=MM/date=DD/hour=HH/`` .
            :param storage_compression_format: By default, stored data is compressed as a .gzip file. Compressed files have a reduced file size, which can optimize the cost of data storage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-s3config.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                s3_config_property = iotfleetwise_mixins.CfnCampaignPropsMixin.S3ConfigProperty(
                    bucket_arn="bucketArn",
                    data_format="dataFormat",
                    prefix="prefix",
                    storage_compression_format="storageCompressionFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__28a9be0620d83d7baedc1e41f05639d0ae280ed4f1fdce57a004a2f7f377f402)
                check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
                check_type(argname="argument data_format", value=data_format, expected_type=type_hints["data_format"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument storage_compression_format", value=storage_compression_format, expected_type=type_hints["storage_compression_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_arn is not None:
                self._values["bucket_arn"] = bucket_arn
            if data_format is not None:
                self._values["data_format"] = data_format
            if prefix is not None:
                self._values["prefix"] = prefix
            if storage_compression_format is not None:
                self._values["storage_compression_format"] = storage_compression_format

        @builtins.property
        def bucket_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-s3config.html#cfn-iotfleetwise-campaign-s3config-bucketarn
            '''
            result = self._values.get("bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_format(self) -> typing.Optional[builtins.str]:
            '''Specify the format that files are saved in the Amazon S3 bucket.

            You can save files in an Apache Parquet or JSON format.

            - Parquet - Store data in a columnar storage file format. Parquet is optimal for fast data retrieval and can reduce costs. This option is selected by default.
            - JSON - Store data in a standard text-based JSON file format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-s3config.html#cfn-iotfleetwise-campaign-s3config-dataformat
            '''
            result = self._values.get("data_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''Enter an S3 bucket prefix.

            The prefix is the string of characters after the bucket name and before the object name. You can use the prefix to organize data stored in Amazon S3 buckets. For more information, see `Organizing objects using prefixes <https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html>`_ in the *Amazon Simple Storage Service User Guide* .

            By default, AWS IoT FleetWise sets the prefix ``processed-data/year=YY/month=MM/date=DD/hour=HH/`` (in UTC) to data it delivers to Amazon S3 . You can enter a prefix to append it to this default prefix. For example, if you enter the prefix ``vehicles`` , the prefix will be ``vehicles/processed-data/year=YY/month=MM/date=DD/hour=HH/`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-s3config.html#cfn-iotfleetwise-campaign-s3config-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def storage_compression_format(self) -> typing.Optional[builtins.str]:
            '''By default, stored data is compressed as a .gzip file. Compressed files have a reduced file size, which can optimize the cost of data storage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-s3config.html#cfn-iotfleetwise-campaign-s3config-storagecompressionformat
            '''
            result = self._values.get("storage_compression_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.SignalFetchConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"condition_based": "conditionBased", "time_based": "timeBased"},
    )
    class SignalFetchConfigProperty:
        def __init__(
            self,
            *,
            condition_based: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.ConditionBasedSignalFetchConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            time_based: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TimeBasedSignalFetchConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration of the signal fetch operation.

            .. epigraph::

               Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

            :param condition_based: The configuration of a condition-based signal fetch operation.
            :param time_based: The configuration of a time-based signal fetch operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalfetchconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                signal_fetch_config_property = iotfleetwise_mixins.CfnCampaignPropsMixin.SignalFetchConfigProperty(
                    condition_based=iotfleetwise_mixins.CfnCampaignPropsMixin.ConditionBasedSignalFetchConfigProperty(
                        condition_expression="conditionExpression",
                        trigger_mode="triggerMode"
                    ),
                    time_based=iotfleetwise_mixins.CfnCampaignPropsMixin.TimeBasedSignalFetchConfigProperty(
                        execution_frequency_ms=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a7114651e76d4a14d71ec9b95f7db89a2bb4829c3f71218f6fd5960ac8ca1d0d)
                check_type(argname="argument condition_based", value=condition_based, expected_type=type_hints["condition_based"])
                check_type(argname="argument time_based", value=time_based, expected_type=type_hints["time_based"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition_based is not None:
                self._values["condition_based"] = condition_based
            if time_based is not None:
                self._values["time_based"] = time_based

        @builtins.property
        def condition_based(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ConditionBasedSignalFetchConfigProperty"]]:
            '''The configuration of a condition-based signal fetch operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalfetchconfig.html#cfn-iotfleetwise-campaign-signalfetchconfig-conditionbased
            '''
            result = self._values.get("condition_based")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ConditionBasedSignalFetchConfigProperty"]], result)

        @builtins.property
        def time_based(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimeBasedSignalFetchConfigProperty"]]:
            '''The configuration of a time-based signal fetch operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalfetchconfig.html#cfn-iotfleetwise-campaign-signalfetchconfig-timebased
            '''
            result = self._values.get("time_based")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimeBasedSignalFetchConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SignalFetchConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.SignalFetchInformationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "condition_language_version": "conditionLanguageVersion",
            "fully_qualified_name": "fullyQualifiedName",
            "signal_fetch_config": "signalFetchConfig",
        },
    )
    class SignalFetchInformationProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Sequence[builtins.str]] = None,
            condition_language_version: typing.Optional[jsii.Number] = None,
            fully_qualified_name: typing.Optional[builtins.str] = None,
            signal_fetch_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.SignalFetchConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about the signal to be fetched.

            .. epigraph::

               Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

            :param actions: The actions to be performed by the signal fetch.
            :param condition_language_version: The version of the condition language used.
            :param fully_qualified_name: The fully qualified name of the signal to be fetched.
            :param signal_fetch_config: The configuration of the signal fetch operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalfetchinformation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                signal_fetch_information_property = iotfleetwise_mixins.CfnCampaignPropsMixin.SignalFetchInformationProperty(
                    actions=["actions"],
                    condition_language_version=123,
                    fully_qualified_name="fullyQualifiedName",
                    signal_fetch_config=iotfleetwise_mixins.CfnCampaignPropsMixin.SignalFetchConfigProperty(
                        condition_based=iotfleetwise_mixins.CfnCampaignPropsMixin.ConditionBasedSignalFetchConfigProperty(
                            condition_expression="conditionExpression",
                            trigger_mode="triggerMode"
                        ),
                        time_based=iotfleetwise_mixins.CfnCampaignPropsMixin.TimeBasedSignalFetchConfigProperty(
                            execution_frequency_ms=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6a7d2eef2c678729d44751c71b1fa1a9a0fc6c3e3c418ad43a016c9b6116691)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument condition_language_version", value=condition_language_version, expected_type=type_hints["condition_language_version"])
                check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
                check_type(argname="argument signal_fetch_config", value=signal_fetch_config, expected_type=type_hints["signal_fetch_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if condition_language_version is not None:
                self._values["condition_language_version"] = condition_language_version
            if fully_qualified_name is not None:
                self._values["fully_qualified_name"] = fully_qualified_name
            if signal_fetch_config is not None:
                self._values["signal_fetch_config"] = signal_fetch_config

        @builtins.property
        def actions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The actions to be performed by the signal fetch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalfetchinformation.html#cfn-iotfleetwise-campaign-signalfetchinformation-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def condition_language_version(self) -> typing.Optional[jsii.Number]:
            '''The version of the condition language used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalfetchinformation.html#cfn-iotfleetwise-campaign-signalfetchinformation-conditionlanguageversion
            '''
            result = self._values.get("condition_language_version")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def fully_qualified_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified name of the signal to be fetched.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalfetchinformation.html#cfn-iotfleetwise-campaign-signalfetchinformation-fullyqualifiedname
            '''
            result = self._values.get("fully_qualified_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def signal_fetch_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SignalFetchConfigProperty"]]:
            '''The configuration of the signal fetch operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalfetchinformation.html#cfn-iotfleetwise-campaign-signalfetchinformation-signalfetchconfig
            '''
            result = self._values.get("signal_fetch_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SignalFetchConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SignalFetchInformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.SignalInformationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_partition_id": "dataPartitionId",
            "max_sample_count": "maxSampleCount",
            "minimum_sampling_interval_ms": "minimumSamplingIntervalMs",
            "name": "name",
        },
    )
    class SignalInformationProperty:
        def __init__(
            self,
            *,
            data_partition_id: typing.Optional[builtins.str] = None,
            max_sample_count: typing.Optional[jsii.Number] = None,
            minimum_sampling_interval_ms: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a signal.

            :param data_partition_id: The ID of the data partition this signal is associated with. The ID must match one of the IDs provided in ``dataPartitions`` . This is accomplished either by specifying a particular data partition ID or by using ``default`` for an established default partition. You can establish a default partition in the ``DataPartition`` data type. .. epigraph:: If you upload a signal as a condition for a campaign's data partition, the same signal must be included in ``signalsToCollect`` . > Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .
            :param max_sample_count: The maximum number of samples to collect.
            :param minimum_sampling_interval_ms: The minimum duration of time (in milliseconds) between two triggering events to collect data. .. epigraph:: If a signal changes often, you might want to collect data at a slower rate.
            :param name: The name of the signal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalinformation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                signal_information_property = iotfleetwise_mixins.CfnCampaignPropsMixin.SignalInformationProperty(
                    data_partition_id="dataPartitionId",
                    max_sample_count=123,
                    minimum_sampling_interval_ms=123,
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cee1e91d30cb5be643418d21c2022f87159fe57ff4f64c27c9d4e31b087e0205)
                check_type(argname="argument data_partition_id", value=data_partition_id, expected_type=type_hints["data_partition_id"])
                check_type(argname="argument max_sample_count", value=max_sample_count, expected_type=type_hints["max_sample_count"])
                check_type(argname="argument minimum_sampling_interval_ms", value=minimum_sampling_interval_ms, expected_type=type_hints["minimum_sampling_interval_ms"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_partition_id is not None:
                self._values["data_partition_id"] = data_partition_id
            if max_sample_count is not None:
                self._values["max_sample_count"] = max_sample_count
            if minimum_sampling_interval_ms is not None:
                self._values["minimum_sampling_interval_ms"] = minimum_sampling_interval_ms
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def data_partition_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the data partition this signal is associated with.

            The ID must match one of the IDs provided in ``dataPartitions`` . This is accomplished either by specifying a particular data partition ID or by using ``default`` for an established default partition. You can establish a default partition in the ``DataPartition`` data type.
            .. epigraph::

               If you upload a signal as a condition for a campaign's data partition, the same signal must be included in ``signalsToCollect`` . > Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalinformation.html#cfn-iotfleetwise-campaign-signalinformation-datapartitionid
            '''
            result = self._values.get("data_partition_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_sample_count(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of samples to collect.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalinformation.html#cfn-iotfleetwise-campaign-signalinformation-maxsamplecount
            '''
            result = self._values.get("max_sample_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minimum_sampling_interval_ms(self) -> typing.Optional[jsii.Number]:
            '''The minimum duration of time (in milliseconds) between two triggering events to collect data.

            .. epigraph::

               If a signal changes often, you might want to collect data at a slower rate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalinformation.html#cfn-iotfleetwise-campaign-signalinformation-minimumsamplingintervalms
            '''
            result = self._values.get("minimum_sampling_interval_ms")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the signal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-signalinformation.html#cfn-iotfleetwise-campaign-signalinformation-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SignalInformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.StorageMaximumSizeProperty",
        jsii_struct_bases=[],
        name_mapping={"unit": "unit", "value": "value"},
    )
    class StorageMaximumSizeProperty:
        def __init__(
            self,
            *,
            unit: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The maximum storage size for the data partition.

            .. epigraph::

               Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

            :param unit: The data type of the data to store.
            :param value: The maximum amount of time to store data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-storagemaximumsize.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                storage_maximum_size_property = iotfleetwise_mixins.CfnCampaignPropsMixin.StorageMaximumSizeProperty(
                    unit="unit",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c79e2fa3d530de8780a20dce6c314533e78c694bc690f52718ebed80c0f3c669)
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unit is not None:
                self._values["unit"] = unit
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The data type of the data to store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-storagemaximumsize.html#cfn-iotfleetwise-campaign-storagemaximumsize-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time to store data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-storagemaximumsize.html#cfn-iotfleetwise-campaign-storagemaximumsize-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageMaximumSizeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.StorageMinimumTimeToLiveProperty",
        jsii_struct_bases=[],
        name_mapping={"unit": "unit", "value": "value"},
    )
    class StorageMinimumTimeToLiveProperty:
        def __init__(
            self,
            *,
            unit: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about the minimum amount of time that data will be kept.

            .. epigraph::

               Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

            :param unit: The time increment type.
            :param value: The minimum amount of time to store the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-storageminimumtimetolive.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                storage_minimum_time_to_live_property = iotfleetwise_mixins.CfnCampaignPropsMixin.StorageMinimumTimeToLiveProperty(
                    unit="unit",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1145dde21b1ec271c3636fa1da82a3bb0ace0797f08b7fec83735a72807dfac9)
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unit is not None:
                self._values["unit"] = unit
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The time increment type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-storageminimumtimetolive.html#cfn-iotfleetwise-campaign-storageminimumtimetolive-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The minimum amount of time to store the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-storageminimumtimetolive.html#cfn-iotfleetwise-campaign-storageminimumtimetolive-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageMinimumTimeToLiveProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.TimeBasedCollectionSchemeProperty",
        jsii_struct_bases=[],
        name_mapping={"period_ms": "periodMs"},
    )
    class TimeBasedCollectionSchemeProperty:
        def __init__(self, *, period_ms: typing.Optional[jsii.Number] = None) -> None:
            '''Information about a collection scheme that uses a time period to decide how often to collect data.

            :param period_ms: The time period (in milliseconds) to decide how often to collect data. For example, if the time period is ``60000`` , the Edge Agent software collects data once every minute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-timebasedcollectionscheme.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                time_based_collection_scheme_property = iotfleetwise_mixins.CfnCampaignPropsMixin.TimeBasedCollectionSchemeProperty(
                    period_ms=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b1114a59d094dcf524034b3499ac4696d76dc0eed60fcb62561d9621704906d)
                check_type(argname="argument period_ms", value=period_ms, expected_type=type_hints["period_ms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if period_ms is not None:
                self._values["period_ms"] = period_ms

        @builtins.property
        def period_ms(self) -> typing.Optional[jsii.Number]:
            '''The time period (in milliseconds) to decide how often to collect data.

            For example, if the time period is ``60000`` , the Edge Agent software collects data once every minute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-timebasedcollectionscheme.html#cfn-iotfleetwise-campaign-timebasedcollectionscheme-periodms
            '''
            result = self._values.get("period_ms")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeBasedCollectionSchemeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.TimeBasedSignalFetchConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"execution_frequency_ms": "executionFrequencyMs"},
    )
    class TimeBasedSignalFetchConfigProperty:
        def __init__(
            self,
            *,
            execution_frequency_ms: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Used to configure a frequency-based vehicle signal fetch.

            :param execution_frequency_ms: The frequency with which the signal fetch will be executed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-timebasedsignalfetchconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                time_based_signal_fetch_config_property = iotfleetwise_mixins.CfnCampaignPropsMixin.TimeBasedSignalFetchConfigProperty(
                    execution_frequency_ms=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__293f10767265ecdf5a9adc081b31e6a97f708b509a8225ba6f2153ef5b6db5b3)
                check_type(argname="argument execution_frequency_ms", value=execution_frequency_ms, expected_type=type_hints["execution_frequency_ms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if execution_frequency_ms is not None:
                self._values["execution_frequency_ms"] = execution_frequency_ms

        @builtins.property
        def execution_frequency_ms(self) -> typing.Optional[jsii.Number]:
            '''The frequency with which the signal fetch will be executed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-timebasedsignalfetchconfig.html#cfn-iotfleetwise-campaign-timebasedsignalfetchconfig-executionfrequencyms
            '''
            result = self._values.get("execution_frequency_ms")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeBasedSignalFetchConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnCampaignPropsMixin.TimestreamConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "execution_role_arn": "executionRoleArn",
            "timestream_table_arn": "timestreamTableArn",
        },
    )
    class TimestreamConfigProperty:
        def __init__(
            self,
            *,
            execution_role_arn: typing.Optional[builtins.str] = None,
            timestream_table_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon Timestream table where the AWS IoT FleetWise campaign sends data.

            Timestream stores and organizes data to optimize query processing time and to reduce storage costs. For more information, see `Data modeling <https://docs.aws.amazon.com/timestream/latest/developerguide/data-modeling.html>`_ in the *Amazon Timestream Developer Guide* .

            :param execution_role_arn: The Amazon Resource Name (ARN) of the task execution role that grants AWS IoT FleetWise permission to deliver data to the Amazon Timestream table.
            :param timestream_table_arn: The Amazon Resource Name (ARN) of the Amazon Timestream table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-timestreamconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                timestream_config_property = iotfleetwise_mixins.CfnCampaignPropsMixin.TimestreamConfigProperty(
                    execution_role_arn="executionRoleArn",
                    timestream_table_arn="timestreamTableArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0ff1003f2881835162963e1e870e8ef2dad7594bbd02e895954ea7ad766ab2f8)
                check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
                check_type(argname="argument timestream_table_arn", value=timestream_table_arn, expected_type=type_hints["timestream_table_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if execution_role_arn is not None:
                self._values["execution_role_arn"] = execution_role_arn
            if timestream_table_arn is not None:
                self._values["timestream_table_arn"] = timestream_table_arn

        @builtins.property
        def execution_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the task execution role that grants AWS IoT FleetWise permission to deliver data to the Amazon Timestream table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-timestreamconfig.html#cfn-iotfleetwise-campaign-timestreamconfig-executionrolearn
            '''
            result = self._values.get("execution_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timestream_table_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon Timestream table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-campaign-timestreamconfig.html#cfn-iotfleetwise-campaign-timestreamconfig-timestreamtablearn
            '''
            result = self._values.get("timestream_table_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimestreamConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnDecoderManifestMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_for_unmapped_signals": "defaultForUnmappedSignals",
        "description": "description",
        "model_manifest_arn": "modelManifestArn",
        "name": "name",
        "network_interfaces": "networkInterfaces",
        "signal_decoders": "signalDecoders",
        "status": "status",
        "tags": "tags",
    },
)
class CfnDecoderManifestMixinProps:
    def __init__(
        self,
        *,
        default_for_unmapped_signals: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        model_manifest_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_interfaces: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDecoderManifestPropsMixin.NetworkInterfacesItemsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        signal_decoders: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDecoderManifestPropsMixin.SignalDecodersItemsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDecoderManifestPropsMixin.

        :param default_for_unmapped_signals: Use default decoders for all unmapped signals in the model. You don't need to provide any detailed decoding information.
        :param description: A brief description of the decoder manifest.
        :param model_manifest_arn: The Amazon Resource Name (ARN) of a vehicle model (model manifest) associated with the decoder manifest.
        :param name: The name of the decoder manifest.
        :param network_interfaces: A list of information about available network interfaces.
        :param signal_decoders: A list of information about signal decoders.
        :param status: The state of the decoder manifest. If the status is ``ACTIVE`` , the decoder manifest can't be edited. If the status is marked ``DRAFT`` , you can edit the decoder manifest. Default: - "DRAFT"
        :param tags: Metadata that can be used to manage the decoder manifest.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
            
            cfn_decoder_manifest_mixin_props = iotfleetwise_mixins.CfnDecoderManifestMixinProps(
                default_for_unmapped_signals="defaultForUnmappedSignals",
                description="description",
                model_manifest_arn="modelManifestArn",
                name="name",
                network_interfaces=[iotfleetwise_mixins.CfnDecoderManifestPropsMixin.NetworkInterfacesItemsProperty(
                    can_interface=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.CanInterfaceProperty(
                        name="name",
                        protocol_name="protocolName",
                        protocol_version="protocolVersion"
                    ),
                    interface_id="interfaceId",
                    obd_interface=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.ObdInterfaceProperty(
                        dtc_request_interval_seconds="dtcRequestIntervalSeconds",
                        has_transmission_ecu="hasTransmissionEcu",
                        name="name",
                        obd_standard="obdStandard",
                        pid_request_interval_seconds="pidRequestIntervalSeconds",
                        request_message_id="requestMessageId",
                        use_extended_ids="useExtendedIds"
                    ),
                    type="type"
                )],
                signal_decoders=[iotfleetwise_mixins.CfnDecoderManifestPropsMixin.SignalDecodersItemsProperty(
                    can_signal=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.CanSignalProperty(
                        factor="factor",
                        is_big_endian="isBigEndian",
                        is_signed="isSigned",
                        length="length",
                        message_id="messageId",
                        name="name",
                        offset="offset",
                        signal_value_type="signalValueType",
                        start_bit="startBit"
                    ),
                    fully_qualified_name="fullyQualifiedName",
                    interface_id="interfaceId",
                    obd_signal=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.ObdSignalProperty(
                        bit_mask_length="bitMaskLength",
                        bit_right_shift="bitRightShift",
                        byte_length="byteLength",
                        is_signed="isSigned",
                        offset="offset",
                        pid="pid",
                        pid_response_length="pidResponseLength",
                        scaling="scaling",
                        service_mode="serviceMode",
                        signal_value_type="signalValueType",
                        start_byte="startByte"
                    ),
                    type="type"
                )],
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce34c01882b69d4b1a1163eba55583bd2a0ebb209e3678aab4394c032d67b4e)
            check_type(argname="argument default_for_unmapped_signals", value=default_for_unmapped_signals, expected_type=type_hints["default_for_unmapped_signals"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument model_manifest_arn", value=model_manifest_arn, expected_type=type_hints["model_manifest_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
            check_type(argname="argument signal_decoders", value=signal_decoders, expected_type=type_hints["signal_decoders"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_for_unmapped_signals is not None:
            self._values["default_for_unmapped_signals"] = default_for_unmapped_signals
        if description is not None:
            self._values["description"] = description
        if model_manifest_arn is not None:
            self._values["model_manifest_arn"] = model_manifest_arn
        if name is not None:
            self._values["name"] = name
        if network_interfaces is not None:
            self._values["network_interfaces"] = network_interfaces
        if signal_decoders is not None:
            self._values["signal_decoders"] = signal_decoders
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def default_for_unmapped_signals(self) -> typing.Optional[builtins.str]:
        '''Use default decoders for all unmapped signals in the model.

        You don't need to provide any detailed decoding information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-defaultforunmappedsignals
        '''
        result = self._values.get("default_for_unmapped_signals")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the decoder manifest.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_manifest_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of a vehicle model (model manifest) associated with the decoder manifest.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-modelmanifestarn
        '''
        result = self._values.get("model_manifest_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the decoder manifest.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interfaces(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.NetworkInterfacesItemsProperty"]]]]:
        '''A list of information about available network interfaces.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-networkinterfaces
        '''
        result = self._values.get("network_interfaces")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.NetworkInterfacesItemsProperty"]]]], result)

    @builtins.property
    def signal_decoders(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.SignalDecodersItemsProperty"]]]]:
        '''A list of information about signal decoders.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-signaldecoders
        '''
        result = self._values.get("signal_decoders")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.SignalDecodersItemsProperty"]]]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The state of the decoder manifest.

        If the status is ``ACTIVE`` , the decoder manifest can't be edited. If the status is marked ``DRAFT`` , you can edit the decoder manifest.

        :default: - "DRAFT"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata that can be used to manage the decoder manifest.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html#cfn-iotfleetwise-decodermanifest-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDecoderManifestMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDecoderManifestPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnDecoderManifestPropsMixin",
):
    '''Creates the decoder manifest associated with a model manifest. To create a decoder manifest, the following must be true:.

    - Every signal decoder has a unique name.
    - Each signal decoder is associated with a network interface.
    - Each network interface has a unique ID.
    - The signal decoders are specified in the model manifest.

    For more information, see `Decoder manifests <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/decoder-manifests.html>`_ in the *AWS IoT FleetWise Developer Guide* .
    .. epigraph::

       Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-decodermanifest.html
    :cloudformationResource: AWS::IoTFleetWise::DecoderManifest
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
        
        cfn_decoder_manifest_props_mixin = iotfleetwise_mixins.CfnDecoderManifestPropsMixin(iotfleetwise_mixins.CfnDecoderManifestMixinProps(
            default_for_unmapped_signals="defaultForUnmappedSignals",
            description="description",
            model_manifest_arn="modelManifestArn",
            name="name",
            network_interfaces=[iotfleetwise_mixins.CfnDecoderManifestPropsMixin.NetworkInterfacesItemsProperty(
                can_interface=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.CanInterfaceProperty(
                    name="name",
                    protocol_name="protocolName",
                    protocol_version="protocolVersion"
                ),
                interface_id="interfaceId",
                obd_interface=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.ObdInterfaceProperty(
                    dtc_request_interval_seconds="dtcRequestIntervalSeconds",
                    has_transmission_ecu="hasTransmissionEcu",
                    name="name",
                    obd_standard="obdStandard",
                    pid_request_interval_seconds="pidRequestIntervalSeconds",
                    request_message_id="requestMessageId",
                    use_extended_ids="useExtendedIds"
                ),
                type="type"
            )],
            signal_decoders=[iotfleetwise_mixins.CfnDecoderManifestPropsMixin.SignalDecodersItemsProperty(
                can_signal=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.CanSignalProperty(
                    factor="factor",
                    is_big_endian="isBigEndian",
                    is_signed="isSigned",
                    length="length",
                    message_id="messageId",
                    name="name",
                    offset="offset",
                    signal_value_type="signalValueType",
                    start_bit="startBit"
                ),
                fully_qualified_name="fullyQualifiedName",
                interface_id="interfaceId",
                obd_signal=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.ObdSignalProperty(
                    bit_mask_length="bitMaskLength",
                    bit_right_shift="bitRightShift",
                    byte_length="byteLength",
                    is_signed="isSigned",
                    offset="offset",
                    pid="pid",
                    pid_response_length="pidResponseLength",
                    scaling="scaling",
                    service_mode="serviceMode",
                    signal_value_type="signalValueType",
                    start_byte="startByte"
                ),
                type="type"
            )],
            status="status",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDecoderManifestMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTFleetWise::DecoderManifest``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8978afa7100af71765088f653764144ddf042def34db82bdd9a6df497dcd3e7)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        options = _CfnPropertyMixinOptions_9cbff649(strategy=strategy)

        jsii.create(self.__class__, self, [props, options])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply the mixin properties to the construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e57f1564150fbc6704d35040b8e3b52a65e4a24cd49b0fe3bafedbbc53b103)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f32852211e693f7a7285e604323fdcc4906fbffb29cf2751a2a3e51ee94d675)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDecoderManifestMixinProps:
        return typing.cast(CfnDecoderManifestMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnDecoderManifestPropsMixin.CanInterfaceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "protocol_name": "protocolName",
            "protocol_version": "protocolVersion",
        },
    )
    class CanInterfaceProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            protocol_name: typing.Optional[builtins.str] = None,
            protocol_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A single controller area network (CAN) device interface.

            :param name: The unique name of the interface.
            :param protocol_name: The name of the communication protocol for the interface.
            :param protocol_version: The version of the communication protocol for the interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-caninterface.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                can_interface_property = iotfleetwise_mixins.CfnDecoderManifestPropsMixin.CanInterfaceProperty(
                    name="name",
                    protocol_name="protocolName",
                    protocol_version="protocolVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__75c657b9093371550a24cdb14c4f440b71af3b4fae173ff93a9fa199e2485b37)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument protocol_name", value=protocol_name, expected_type=type_hints["protocol_name"])
                check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if protocol_name is not None:
                self._values["protocol_name"] = protocol_name
            if protocol_version is not None:
                self._values["protocol_version"] = protocol_version

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The unique name of the interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-caninterface.html#cfn-iotfleetwise-decodermanifest-caninterface-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol_name(self) -> typing.Optional[builtins.str]:
            '''The name of the communication protocol for the interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-caninterface.html#cfn-iotfleetwise-decodermanifest-caninterface-protocolname
            '''
            result = self._values.get("protocol_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol_version(self) -> typing.Optional[builtins.str]:
            '''The version of the communication protocol for the interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-caninterface.html#cfn-iotfleetwise-decodermanifest-caninterface-protocolversion
            '''
            result = self._values.get("protocol_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CanInterfaceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnDecoderManifestPropsMixin.CanNetworkInterfaceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "can_interface": "canInterface",
            "interface_id": "interfaceId",
            "type": "type",
        },
    )
    class CanNetworkInterfaceProperty:
        def __init__(
            self,
            *,
            can_interface: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDecoderManifestPropsMixin.CanInterfaceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            interface_id: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a node and its specifications in an in-vehicle communication network.

            All signal decoders must be associated with a network node.

            To return this information about all the network interfaces specified in a decoder manifest, use the `ListDecoderManifestNetworkInterfaces <https://docs.aws.amazon.com/iot-fleetwise/latest/APIReference/API_ListDecoderManifestNetworkInterfaces.html>`_ in the *AWS IoT FleetWise API Reference* .

            :param can_interface: Information about a network interface specified by the Controller Area Network (CAN) protocol.
            :param interface_id: The ID of the network interface.
            :param type: The network protocol for the vehicle. For example, ``CAN_SIGNAL`` specifies a protocol that defines how data is communicated between electronic control units (ECUs). ``OBD_SIGNAL`` specifies a protocol that defines how self-diagnostic data is communicated between ECUs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cannetworkinterface.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                can_network_interface_property = iotfleetwise_mixins.CfnDecoderManifestPropsMixin.CanNetworkInterfaceProperty(
                    can_interface=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.CanInterfaceProperty(
                        name="name",
                        protocol_name="protocolName",
                        protocol_version="protocolVersion"
                    ),
                    interface_id="interfaceId",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4559b5e688b36adebe33bc2af42b896252b7f0d8f92a21e53dd6a5e167f5ba41)
                check_type(argname="argument can_interface", value=can_interface, expected_type=type_hints["can_interface"])
                check_type(argname="argument interface_id", value=interface_id, expected_type=type_hints["interface_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if can_interface is not None:
                self._values["can_interface"] = can_interface
            if interface_id is not None:
                self._values["interface_id"] = interface_id
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def can_interface(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.CanInterfaceProperty"]]:
            '''Information about a network interface specified by the Controller Area Network (CAN) protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cannetworkinterface.html#cfn-iotfleetwise-decodermanifest-cannetworkinterface-caninterface
            '''
            result = self._values.get("can_interface")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.CanInterfaceProperty"]], result)

        @builtins.property
        def interface_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the network interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cannetworkinterface.html#cfn-iotfleetwise-decodermanifest-cannetworkinterface-interfaceid
            '''
            result = self._values.get("interface_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The network protocol for the vehicle.

            For example, ``CAN_SIGNAL`` specifies a protocol that defines how data is communicated between electronic control units (ECUs). ``OBD_SIGNAL`` specifies a protocol that defines how self-diagnostic data is communicated between ECUs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cannetworkinterface.html#cfn-iotfleetwise-decodermanifest-cannetworkinterface-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CanNetworkInterfaceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnDecoderManifestPropsMixin.CanSignalDecoderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "can_signal": "canSignal",
            "fully_qualified_name": "fullyQualifiedName",
            "interface_id": "interfaceId",
            "type": "type",
        },
    )
    class CanSignalDecoderProperty:
        def __init__(
            self,
            *,
            can_signal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDecoderManifestPropsMixin.CanSignalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            fully_qualified_name: typing.Optional[builtins.str] = None,
            interface_id: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about signal decoder using the Controller Area Network (CAN) protocol.

            :param can_signal: Information about a single controller area network (CAN) signal and the messages it receives and transmits.
            :param fully_qualified_name: The fully qualified name of a signal decoder as defined in a vehicle model.
            :param interface_id: The ID of a network interface that specifies what network protocol a vehicle follows.
            :param type: The network protocol for the vehicle. For example, ``CAN_SIGNAL`` specifies a protocol that defines how data is communicated between electronic control units (ECUs). ``OBD_SIGNAL`` specifies a protocol that defines how self-diagnostic data is communicated between ECUs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignaldecoder.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                can_signal_decoder_property = iotfleetwise_mixins.CfnDecoderManifestPropsMixin.CanSignalDecoderProperty(
                    can_signal=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.CanSignalProperty(
                        factor="factor",
                        is_big_endian="isBigEndian",
                        is_signed="isSigned",
                        length="length",
                        message_id="messageId",
                        name="name",
                        offset="offset",
                        signal_value_type="signalValueType",
                        start_bit="startBit"
                    ),
                    fully_qualified_name="fullyQualifiedName",
                    interface_id="interfaceId",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__75a7033b3e7ceb75648bb4c58383b0c6ea8f30eebff16a0b809f87293d216959)
                check_type(argname="argument can_signal", value=can_signal, expected_type=type_hints["can_signal"])
                check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
                check_type(argname="argument interface_id", value=interface_id, expected_type=type_hints["interface_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if can_signal is not None:
                self._values["can_signal"] = can_signal
            if fully_qualified_name is not None:
                self._values["fully_qualified_name"] = fully_qualified_name
            if interface_id is not None:
                self._values["interface_id"] = interface_id
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def can_signal(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.CanSignalProperty"]]:
            '''Information about a single controller area network (CAN) signal and the messages it receives and transmits.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignaldecoder.html#cfn-iotfleetwise-decodermanifest-cansignaldecoder-cansignal
            '''
            result = self._values.get("can_signal")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.CanSignalProperty"]], result)

        @builtins.property
        def fully_qualified_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified name of a signal decoder as defined in a vehicle model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignaldecoder.html#cfn-iotfleetwise-decodermanifest-cansignaldecoder-fullyqualifiedname
            '''
            result = self._values.get("fully_qualified_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def interface_id(self) -> typing.Optional[builtins.str]:
            '''The ID of a network interface that specifies what network protocol a vehicle follows.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignaldecoder.html#cfn-iotfleetwise-decodermanifest-cansignaldecoder-interfaceid
            '''
            result = self._values.get("interface_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The network protocol for the vehicle.

            For example, ``CAN_SIGNAL`` specifies a protocol that defines how data is communicated between electronic control units (ECUs). ``OBD_SIGNAL`` specifies a protocol that defines how self-diagnostic data is communicated between ECUs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignaldecoder.html#cfn-iotfleetwise-decodermanifest-cansignaldecoder-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CanSignalDecoderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnDecoderManifestPropsMixin.CanSignalProperty",
        jsii_struct_bases=[],
        name_mapping={
            "factor": "factor",
            "is_big_endian": "isBigEndian",
            "is_signed": "isSigned",
            "length": "length",
            "message_id": "messageId",
            "name": "name",
            "offset": "offset",
            "signal_value_type": "signalValueType",
            "start_bit": "startBit",
        },
    )
    class CanSignalProperty:
        def __init__(
            self,
            *,
            factor: typing.Optional[builtins.str] = None,
            is_big_endian: typing.Optional[builtins.str] = None,
            is_signed: typing.Optional[builtins.str] = None,
            length: typing.Optional[builtins.str] = None,
            message_id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            offset: typing.Optional[builtins.str] = None,
            signal_value_type: typing.Optional[builtins.str] = None,
            start_bit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a single controller area network (CAN) signal and the messages it receives and transmits.

            :param factor: A multiplier used to decode the CAN message.
            :param is_big_endian: Whether the byte ordering of a CAN message is big-endian.
            :param is_signed: Whether the message data is specified as a signed value.
            :param length: How many bytes of data are in the message.
            :param message_id: The ID of the message.
            :param name: The name of the signal.
            :param offset: The offset used to calculate the signal value. Combined with factor, the calculation is ``value = raw_value * factor + offset`` .
            :param signal_value_type: The value type of the signal. The default value is ``INTEGER`` .
            :param start_bit: Indicates the beginning of the CAN message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                can_signal_property = iotfleetwise_mixins.CfnDecoderManifestPropsMixin.CanSignalProperty(
                    factor="factor",
                    is_big_endian="isBigEndian",
                    is_signed="isSigned",
                    length="length",
                    message_id="messageId",
                    name="name",
                    offset="offset",
                    signal_value_type="signalValueType",
                    start_bit="startBit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__abdfb351664115cc83110de47fe13f6f4a39ca8afd9cd962bd04b4c6cf53208f)
                check_type(argname="argument factor", value=factor, expected_type=type_hints["factor"])
                check_type(argname="argument is_big_endian", value=is_big_endian, expected_type=type_hints["is_big_endian"])
                check_type(argname="argument is_signed", value=is_signed, expected_type=type_hints["is_signed"])
                check_type(argname="argument length", value=length, expected_type=type_hints["length"])
                check_type(argname="argument message_id", value=message_id, expected_type=type_hints["message_id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
                check_type(argname="argument signal_value_type", value=signal_value_type, expected_type=type_hints["signal_value_type"])
                check_type(argname="argument start_bit", value=start_bit, expected_type=type_hints["start_bit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if factor is not None:
                self._values["factor"] = factor
            if is_big_endian is not None:
                self._values["is_big_endian"] = is_big_endian
            if is_signed is not None:
                self._values["is_signed"] = is_signed
            if length is not None:
                self._values["length"] = length
            if message_id is not None:
                self._values["message_id"] = message_id
            if name is not None:
                self._values["name"] = name
            if offset is not None:
                self._values["offset"] = offset
            if signal_value_type is not None:
                self._values["signal_value_type"] = signal_value_type
            if start_bit is not None:
                self._values["start_bit"] = start_bit

        @builtins.property
        def factor(self) -> typing.Optional[builtins.str]:
            '''A multiplier used to decode the CAN message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-factor
            '''
            result = self._values.get("factor")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_big_endian(self) -> typing.Optional[builtins.str]:
            '''Whether the byte ordering of a CAN message is big-endian.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-isbigendian
            '''
            result = self._values.get("is_big_endian")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_signed(self) -> typing.Optional[builtins.str]:
            '''Whether the message data is specified as a signed value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-issigned
            '''
            result = self._values.get("is_signed")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def length(self) -> typing.Optional[builtins.str]:
            '''How many bytes of data are in the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-length
            '''
            result = self._values.get("length")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-messageid
            '''
            result = self._values.get("message_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the signal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def offset(self) -> typing.Optional[builtins.str]:
            '''The offset used to calculate the signal value.

            Combined with factor, the calculation is ``value = raw_value * factor + offset`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-offset
            '''
            result = self._values.get("offset")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def signal_value_type(self) -> typing.Optional[builtins.str]:
            '''The value type of the signal.

            The default value is ``INTEGER`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-signalvaluetype
            '''
            result = self._values.get("signal_value_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_bit(self) -> typing.Optional[builtins.str]:
            '''Indicates the beginning of the CAN message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-cansignal.html#cfn-iotfleetwise-decodermanifest-cansignal-startbit
            '''
            result = self._values.get("start_bit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CanSignalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnDecoderManifestPropsMixin.NetworkInterfacesItemsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "can_interface": "canInterface",
            "interface_id": "interfaceId",
            "obd_interface": "obdInterface",
            "type": "type",
        },
    )
    class NetworkInterfacesItemsProperty:
        def __init__(
            self,
            *,
            can_interface: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDecoderManifestPropsMixin.CanInterfaceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            interface_id: typing.Optional[builtins.str] = None,
            obd_interface: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDecoderManifestPropsMixin.ObdInterfaceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of information about available network interfaces.

            :param can_interface: 
            :param interface_id: 
            :param obd_interface: 
            :param type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-networkinterfacesitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                network_interfaces_items_property = iotfleetwise_mixins.CfnDecoderManifestPropsMixin.NetworkInterfacesItemsProperty(
                    can_interface=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.CanInterfaceProperty(
                        name="name",
                        protocol_name="protocolName",
                        protocol_version="protocolVersion"
                    ),
                    interface_id="interfaceId",
                    obd_interface=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.ObdInterfaceProperty(
                        dtc_request_interval_seconds="dtcRequestIntervalSeconds",
                        has_transmission_ecu="hasTransmissionEcu",
                        name="name",
                        obd_standard="obdStandard",
                        pid_request_interval_seconds="pidRequestIntervalSeconds",
                        request_message_id="requestMessageId",
                        use_extended_ids="useExtendedIds"
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cacc524fd8219ca210fdd0c7bb66bf371d867b6f4705fa2ddd710b7d167292dd)
                check_type(argname="argument can_interface", value=can_interface, expected_type=type_hints["can_interface"])
                check_type(argname="argument interface_id", value=interface_id, expected_type=type_hints["interface_id"])
                check_type(argname="argument obd_interface", value=obd_interface, expected_type=type_hints["obd_interface"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if can_interface is not None:
                self._values["can_interface"] = can_interface
            if interface_id is not None:
                self._values["interface_id"] = interface_id
            if obd_interface is not None:
                self._values["obd_interface"] = obd_interface
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def can_interface(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.CanInterfaceProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-networkinterfacesitems.html#cfn-iotfleetwise-decodermanifest-networkinterfacesitems-caninterface
            '''
            result = self._values.get("can_interface")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.CanInterfaceProperty"]], result)

        @builtins.property
        def interface_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-networkinterfacesitems.html#cfn-iotfleetwise-decodermanifest-networkinterfacesitems-interfaceid
            '''
            result = self._values.get("interface_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def obd_interface(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.ObdInterfaceProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-networkinterfacesitems.html#cfn-iotfleetwise-decodermanifest-networkinterfacesitems-obdinterface
            '''
            result = self._values.get("obd_interface")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.ObdInterfaceProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-networkinterfacesitems.html#cfn-iotfleetwise-decodermanifest-networkinterfacesitems-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkInterfacesItemsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnDecoderManifestPropsMixin.ObdInterfaceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dtc_request_interval_seconds": "dtcRequestIntervalSeconds",
            "has_transmission_ecu": "hasTransmissionEcu",
            "name": "name",
            "obd_standard": "obdStandard",
            "pid_request_interval_seconds": "pidRequestIntervalSeconds",
            "request_message_id": "requestMessageId",
            "use_extended_ids": "useExtendedIds",
        },
    )
    class ObdInterfaceProperty:
        def __init__(
            self,
            *,
            dtc_request_interval_seconds: typing.Optional[builtins.str] = None,
            has_transmission_ecu: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            obd_standard: typing.Optional[builtins.str] = None,
            pid_request_interval_seconds: typing.Optional[builtins.str] = None,
            request_message_id: typing.Optional[builtins.str] = None,
            use_extended_ids: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A network interface that specifies the On-board diagnostic (OBD) II network protocol.

            :param dtc_request_interval_seconds: The maximum number message requests per diagnostic trouble code per second.
            :param has_transmission_ecu: Whether the vehicle has a transmission control module (TCM).
            :param name: The name of the interface.
            :param obd_standard: The standard OBD II PID.
            :param pid_request_interval_seconds: The maximum number message requests per second.
            :param request_message_id: The ID of the message requesting vehicle data.
            :param use_extended_ids: Whether to use extended IDs in the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                obd_interface_property = iotfleetwise_mixins.CfnDecoderManifestPropsMixin.ObdInterfaceProperty(
                    dtc_request_interval_seconds="dtcRequestIntervalSeconds",
                    has_transmission_ecu="hasTransmissionEcu",
                    name="name",
                    obd_standard="obdStandard",
                    pid_request_interval_seconds="pidRequestIntervalSeconds",
                    request_message_id="requestMessageId",
                    use_extended_ids="useExtendedIds"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__871053b314f74d7eb35d96a21d2344647fc16bcfebae44e0086e4b851d8e00e9)
                check_type(argname="argument dtc_request_interval_seconds", value=dtc_request_interval_seconds, expected_type=type_hints["dtc_request_interval_seconds"])
                check_type(argname="argument has_transmission_ecu", value=has_transmission_ecu, expected_type=type_hints["has_transmission_ecu"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument obd_standard", value=obd_standard, expected_type=type_hints["obd_standard"])
                check_type(argname="argument pid_request_interval_seconds", value=pid_request_interval_seconds, expected_type=type_hints["pid_request_interval_seconds"])
                check_type(argname="argument request_message_id", value=request_message_id, expected_type=type_hints["request_message_id"])
                check_type(argname="argument use_extended_ids", value=use_extended_ids, expected_type=type_hints["use_extended_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dtc_request_interval_seconds is not None:
                self._values["dtc_request_interval_seconds"] = dtc_request_interval_seconds
            if has_transmission_ecu is not None:
                self._values["has_transmission_ecu"] = has_transmission_ecu
            if name is not None:
                self._values["name"] = name
            if obd_standard is not None:
                self._values["obd_standard"] = obd_standard
            if pid_request_interval_seconds is not None:
                self._values["pid_request_interval_seconds"] = pid_request_interval_seconds
            if request_message_id is not None:
                self._values["request_message_id"] = request_message_id
            if use_extended_ids is not None:
                self._values["use_extended_ids"] = use_extended_ids

        @builtins.property
        def dtc_request_interval_seconds(self) -> typing.Optional[builtins.str]:
            '''The maximum number message requests per diagnostic trouble code per second.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html#cfn-iotfleetwise-decodermanifest-obdinterface-dtcrequestintervalseconds
            '''
            result = self._values.get("dtc_request_interval_seconds")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def has_transmission_ecu(self) -> typing.Optional[builtins.str]:
            '''Whether the vehicle has a transmission control module (TCM).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html#cfn-iotfleetwise-decodermanifest-obdinterface-hastransmissionecu
            '''
            result = self._values.get("has_transmission_ecu")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html#cfn-iotfleetwise-decodermanifest-obdinterface-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def obd_standard(self) -> typing.Optional[builtins.str]:
            '''The standard OBD II PID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html#cfn-iotfleetwise-decodermanifest-obdinterface-obdstandard
            '''
            result = self._values.get("obd_standard")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pid_request_interval_seconds(self) -> typing.Optional[builtins.str]:
            '''The maximum number message requests per second.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html#cfn-iotfleetwise-decodermanifest-obdinterface-pidrequestintervalseconds
            '''
            result = self._values.get("pid_request_interval_seconds")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def request_message_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the message requesting vehicle data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html#cfn-iotfleetwise-decodermanifest-obdinterface-requestmessageid
            '''
            result = self._values.get("request_message_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def use_extended_ids(self) -> typing.Optional[builtins.str]:
            '''Whether to use extended IDs in the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdinterface.html#cfn-iotfleetwise-decodermanifest-obdinterface-useextendedids
            '''
            result = self._values.get("use_extended_ids")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObdInterfaceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnDecoderManifestPropsMixin.ObdNetworkInterfaceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "interface_id": "interfaceId",
            "obd_interface": "obdInterface",
            "type": "type",
        },
    )
    class ObdNetworkInterfaceProperty:
        def __init__(
            self,
            *,
            interface_id: typing.Optional[builtins.str] = None,
            obd_interface: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDecoderManifestPropsMixin.ObdInterfaceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a network interface specified by the On-board diagnostic (OBD) II protocol.

            :param interface_id: The ID of the network interface.
            :param obd_interface: Information about a network interface specified by the On-board diagnostic (OBD) II protocol.
            :param type: The network protocol for the vehicle. For example, ``CAN_SIGNAL`` specifies a protocol that defines how data is communicated between electronic control units (ECUs). ``OBD_SIGNAL`` specifies a protocol that defines how self-diagnostic data is communicated between ECUs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdnetworkinterface.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                obd_network_interface_property = iotfleetwise_mixins.CfnDecoderManifestPropsMixin.ObdNetworkInterfaceProperty(
                    interface_id="interfaceId",
                    obd_interface=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.ObdInterfaceProperty(
                        dtc_request_interval_seconds="dtcRequestIntervalSeconds",
                        has_transmission_ecu="hasTransmissionEcu",
                        name="name",
                        obd_standard="obdStandard",
                        pid_request_interval_seconds="pidRequestIntervalSeconds",
                        request_message_id="requestMessageId",
                        use_extended_ids="useExtendedIds"
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da6a269fe3cdffdccfb5ffb6758dc07e54dbed6743a1ebbcf6bf29f0004884aa)
                check_type(argname="argument interface_id", value=interface_id, expected_type=type_hints["interface_id"])
                check_type(argname="argument obd_interface", value=obd_interface, expected_type=type_hints["obd_interface"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if interface_id is not None:
                self._values["interface_id"] = interface_id
            if obd_interface is not None:
                self._values["obd_interface"] = obd_interface
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def interface_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the network interface.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdnetworkinterface.html#cfn-iotfleetwise-decodermanifest-obdnetworkinterface-interfaceid
            '''
            result = self._values.get("interface_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def obd_interface(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.ObdInterfaceProperty"]]:
            '''Information about a network interface specified by the On-board diagnostic (OBD) II protocol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdnetworkinterface.html#cfn-iotfleetwise-decodermanifest-obdnetworkinterface-obdinterface
            '''
            result = self._values.get("obd_interface")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.ObdInterfaceProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The network protocol for the vehicle.

            For example, ``CAN_SIGNAL`` specifies a protocol that defines how data is communicated between electronic control units (ECUs). ``OBD_SIGNAL`` specifies a protocol that defines how self-diagnostic data is communicated between ECUs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdnetworkinterface.html#cfn-iotfleetwise-decodermanifest-obdnetworkinterface-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObdNetworkInterfaceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnDecoderManifestPropsMixin.ObdSignalDecoderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "fully_qualified_name": "fullyQualifiedName",
            "interface_id": "interfaceId",
            "obd_signal": "obdSignal",
            "type": "type",
        },
    )
    class ObdSignalDecoderProperty:
        def __init__(
            self,
            *,
            fully_qualified_name: typing.Optional[builtins.str] = None,
            interface_id: typing.Optional[builtins.str] = None,
            obd_signal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDecoderManifestPropsMixin.ObdSignalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of information about signal decoders.

            :param fully_qualified_name: The fully qualified name of a signal decoder as defined in a vehicle model.
            :param interface_id: The ID of a network interface that specifies what network protocol a vehicle follows.
            :param obd_signal: Information about signal messages using the on-board diagnostics (OBD) II protocol in a vehicle.
            :param type: The network protocol for the vehicle. For example, ``CAN_SIGNAL`` specifies a protocol that defines how data is communicated between electronic control units (ECUs). ``OBD_SIGNAL`` specifies a protocol that defines how self-diagnostic data is communicated between ECUs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignaldecoder.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                obd_signal_decoder_property = iotfleetwise_mixins.CfnDecoderManifestPropsMixin.ObdSignalDecoderProperty(
                    fully_qualified_name="fullyQualifiedName",
                    interface_id="interfaceId",
                    obd_signal=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.ObdSignalProperty(
                        bit_mask_length="bitMaskLength",
                        bit_right_shift="bitRightShift",
                        byte_length="byteLength",
                        is_signed="isSigned",
                        offset="offset",
                        pid="pid",
                        pid_response_length="pidResponseLength",
                        scaling="scaling",
                        service_mode="serviceMode",
                        signal_value_type="signalValueType",
                        start_byte="startByte"
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2997b0a79061399d5b1a4f68ad18ad6e6a2fc1fb25150ae698b10e930f99c856)
                check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
                check_type(argname="argument interface_id", value=interface_id, expected_type=type_hints["interface_id"])
                check_type(argname="argument obd_signal", value=obd_signal, expected_type=type_hints["obd_signal"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fully_qualified_name is not None:
                self._values["fully_qualified_name"] = fully_qualified_name
            if interface_id is not None:
                self._values["interface_id"] = interface_id
            if obd_signal is not None:
                self._values["obd_signal"] = obd_signal
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def fully_qualified_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified name of a signal decoder as defined in a vehicle model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignaldecoder.html#cfn-iotfleetwise-decodermanifest-obdsignaldecoder-fullyqualifiedname
            '''
            result = self._values.get("fully_qualified_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def interface_id(self) -> typing.Optional[builtins.str]:
            '''The ID of a network interface that specifies what network protocol a vehicle follows.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignaldecoder.html#cfn-iotfleetwise-decodermanifest-obdsignaldecoder-interfaceid
            '''
            result = self._values.get("interface_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def obd_signal(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.ObdSignalProperty"]]:
            '''Information about signal messages using the on-board diagnostics (OBD) II protocol in a vehicle.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignaldecoder.html#cfn-iotfleetwise-decodermanifest-obdsignaldecoder-obdsignal
            '''
            result = self._values.get("obd_signal")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.ObdSignalProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The network protocol for the vehicle.

            For example, ``CAN_SIGNAL`` specifies a protocol that defines how data is communicated between electronic control units (ECUs). ``OBD_SIGNAL`` specifies a protocol that defines how self-diagnostic data is communicated between ECUs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignaldecoder.html#cfn-iotfleetwise-decodermanifest-obdsignaldecoder-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObdSignalDecoderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnDecoderManifestPropsMixin.ObdSignalProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bit_mask_length": "bitMaskLength",
            "bit_right_shift": "bitRightShift",
            "byte_length": "byteLength",
            "is_signed": "isSigned",
            "offset": "offset",
            "pid": "pid",
            "pid_response_length": "pidResponseLength",
            "scaling": "scaling",
            "service_mode": "serviceMode",
            "signal_value_type": "signalValueType",
            "start_byte": "startByte",
        },
    )
    class ObdSignalProperty:
        def __init__(
            self,
            *,
            bit_mask_length: typing.Optional[builtins.str] = None,
            bit_right_shift: typing.Optional[builtins.str] = None,
            byte_length: typing.Optional[builtins.str] = None,
            is_signed: typing.Optional[typing.Union[builtins.str, builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            offset: typing.Optional[builtins.str] = None,
            pid: typing.Optional[builtins.str] = None,
            pid_response_length: typing.Optional[builtins.str] = None,
            scaling: typing.Optional[builtins.str] = None,
            service_mode: typing.Optional[builtins.str] = None,
            signal_value_type: typing.Optional[builtins.str] = None,
            start_byte: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about signal messages using the on-board diagnostics (OBD) II protocol in a vehicle.

            :param bit_mask_length: The number of bits to mask in a message.
            :param bit_right_shift: The number of positions to shift bits in the message.
            :param byte_length: The length of a message.
            :param is_signed: Determines whether the message is signed ( ``true`` ) or not ( ``false`` ). If it's signed, the message can represent both positive and negative numbers. The ``isSigned`` parameter only applies to the ``INTEGER`` raw signal type, and it doesn't affect the ``FLOATING_POINT`` raw signal type. The default value is ``false`` .
            :param offset: The offset used to calculate the signal value. Combined with scaling, the calculation is ``value = raw_value * scaling + offset`` .
            :param pid: The diagnostic code used to request data from a vehicle for this signal.
            :param pid_response_length: The length of the requested data.
            :param scaling: A multiplier used to decode the message.
            :param service_mode: The mode of operation (diagnostic service) in a message.
            :param signal_value_type: The value type of the signal. The default value is ``INTEGER`` .
            :param start_byte: Indicates the beginning of the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                obd_signal_property = iotfleetwise_mixins.CfnDecoderManifestPropsMixin.ObdSignalProperty(
                    bit_mask_length="bitMaskLength",
                    bit_right_shift="bitRightShift",
                    byte_length="byteLength",
                    is_signed="isSigned",
                    offset="offset",
                    pid="pid",
                    pid_response_length="pidResponseLength",
                    scaling="scaling",
                    service_mode="serviceMode",
                    signal_value_type="signalValueType",
                    start_byte="startByte"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__58ce2b874d934827107656ca59c7d9c5fdf461be5712ea3342af31b6b477ffd8)
                check_type(argname="argument bit_mask_length", value=bit_mask_length, expected_type=type_hints["bit_mask_length"])
                check_type(argname="argument bit_right_shift", value=bit_right_shift, expected_type=type_hints["bit_right_shift"])
                check_type(argname="argument byte_length", value=byte_length, expected_type=type_hints["byte_length"])
                check_type(argname="argument is_signed", value=is_signed, expected_type=type_hints["is_signed"])
                check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
                check_type(argname="argument pid", value=pid, expected_type=type_hints["pid"])
                check_type(argname="argument pid_response_length", value=pid_response_length, expected_type=type_hints["pid_response_length"])
                check_type(argname="argument scaling", value=scaling, expected_type=type_hints["scaling"])
                check_type(argname="argument service_mode", value=service_mode, expected_type=type_hints["service_mode"])
                check_type(argname="argument signal_value_type", value=signal_value_type, expected_type=type_hints["signal_value_type"])
                check_type(argname="argument start_byte", value=start_byte, expected_type=type_hints["start_byte"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bit_mask_length is not None:
                self._values["bit_mask_length"] = bit_mask_length
            if bit_right_shift is not None:
                self._values["bit_right_shift"] = bit_right_shift
            if byte_length is not None:
                self._values["byte_length"] = byte_length
            if is_signed is not None:
                self._values["is_signed"] = is_signed
            if offset is not None:
                self._values["offset"] = offset
            if pid is not None:
                self._values["pid"] = pid
            if pid_response_length is not None:
                self._values["pid_response_length"] = pid_response_length
            if scaling is not None:
                self._values["scaling"] = scaling
            if service_mode is not None:
                self._values["service_mode"] = service_mode
            if signal_value_type is not None:
                self._values["signal_value_type"] = signal_value_type
            if start_byte is not None:
                self._values["start_byte"] = start_byte

        @builtins.property
        def bit_mask_length(self) -> typing.Optional[builtins.str]:
            '''The number of bits to mask in a message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-bitmasklength
            '''
            result = self._values.get("bit_mask_length")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bit_right_shift(self) -> typing.Optional[builtins.str]:
            '''The number of positions to shift bits in the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-bitrightshift
            '''
            result = self._values.get("bit_right_shift")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def byte_length(self) -> typing.Optional[builtins.str]:
            '''The length of a message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-bytelength
            '''
            result = self._values.get("byte_length")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_signed(
            self,
        ) -> typing.Optional[typing.Union[builtins.str, builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether the message is signed ( ``true`` ) or not ( ``false`` ).

            If it's signed, the message can represent both positive and negative numbers. The ``isSigned`` parameter only applies to the ``INTEGER`` raw signal type, and it doesn't affect the ``FLOATING_POINT`` raw signal type. The default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-issigned
            '''
            result = self._values.get("is_signed")
            return typing.cast(typing.Optional[typing.Union[builtins.str, builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def offset(self) -> typing.Optional[builtins.str]:
            '''The offset used to calculate the signal value.

            Combined with scaling, the calculation is ``value = raw_value * scaling + offset`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-offset
            '''
            result = self._values.get("offset")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pid(self) -> typing.Optional[builtins.str]:
            '''The diagnostic code used to request data from a vehicle for this signal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-pid
            '''
            result = self._values.get("pid")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pid_response_length(self) -> typing.Optional[builtins.str]:
            '''The length of the requested data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-pidresponselength
            '''
            result = self._values.get("pid_response_length")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scaling(self) -> typing.Optional[builtins.str]:
            '''A multiplier used to decode the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-scaling
            '''
            result = self._values.get("scaling")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_mode(self) -> typing.Optional[builtins.str]:
            '''The mode of operation (diagnostic service) in a message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-servicemode
            '''
            result = self._values.get("service_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def signal_value_type(self) -> typing.Optional[builtins.str]:
            '''The value type of the signal.

            The default value is ``INTEGER`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-signalvaluetype
            '''
            result = self._values.get("signal_value_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_byte(self) -> typing.Optional[builtins.str]:
            '''Indicates the beginning of the message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-obdsignal.html#cfn-iotfleetwise-decodermanifest-obdsignal-startbyte
            '''
            result = self._values.get("start_byte")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObdSignalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnDecoderManifestPropsMixin.SignalDecodersItemsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "can_signal": "canSignal",
            "fully_qualified_name": "fullyQualifiedName",
            "interface_id": "interfaceId",
            "obd_signal": "obdSignal",
            "type": "type",
        },
    )
    class SignalDecodersItemsProperty:
        def __init__(
            self,
            *,
            can_signal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDecoderManifestPropsMixin.CanSignalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            fully_qualified_name: typing.Optional[builtins.str] = None,
            interface_id: typing.Optional[builtins.str] = None,
            obd_signal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDecoderManifestPropsMixin.ObdSignalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a signal decoder.

            :param can_signal: 
            :param fully_qualified_name: 
            :param interface_id: 
            :param obd_signal: 
            :param type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-signaldecodersitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                signal_decoders_items_property = iotfleetwise_mixins.CfnDecoderManifestPropsMixin.SignalDecodersItemsProperty(
                    can_signal=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.CanSignalProperty(
                        factor="factor",
                        is_big_endian="isBigEndian",
                        is_signed="isSigned",
                        length="length",
                        message_id="messageId",
                        name="name",
                        offset="offset",
                        signal_value_type="signalValueType",
                        start_bit="startBit"
                    ),
                    fully_qualified_name="fullyQualifiedName",
                    interface_id="interfaceId",
                    obd_signal=iotfleetwise_mixins.CfnDecoderManifestPropsMixin.ObdSignalProperty(
                        bit_mask_length="bitMaskLength",
                        bit_right_shift="bitRightShift",
                        byte_length="byteLength",
                        is_signed="isSigned",
                        offset="offset",
                        pid="pid",
                        pid_response_length="pidResponseLength",
                        scaling="scaling",
                        service_mode="serviceMode",
                        signal_value_type="signalValueType",
                        start_byte="startByte"
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c0fd2753092e780334321e82d1933ab3831e1f8ec374bc110b7a8b37ac72855)
                check_type(argname="argument can_signal", value=can_signal, expected_type=type_hints["can_signal"])
                check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
                check_type(argname="argument interface_id", value=interface_id, expected_type=type_hints["interface_id"])
                check_type(argname="argument obd_signal", value=obd_signal, expected_type=type_hints["obd_signal"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if can_signal is not None:
                self._values["can_signal"] = can_signal
            if fully_qualified_name is not None:
                self._values["fully_qualified_name"] = fully_qualified_name
            if interface_id is not None:
                self._values["interface_id"] = interface_id
            if obd_signal is not None:
                self._values["obd_signal"] = obd_signal
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def can_signal(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.CanSignalProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-signaldecodersitems.html#cfn-iotfleetwise-decodermanifest-signaldecodersitems-cansignal
            '''
            result = self._values.get("can_signal")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.CanSignalProperty"]], result)

        @builtins.property
        def fully_qualified_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-signaldecodersitems.html#cfn-iotfleetwise-decodermanifest-signaldecodersitems-fullyqualifiedname
            '''
            result = self._values.get("fully_qualified_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def interface_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-signaldecodersitems.html#cfn-iotfleetwise-decodermanifest-signaldecodersitems-interfaceid
            '''
            result = self._values.get("interface_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def obd_signal(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.ObdSignalProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-signaldecodersitems.html#cfn-iotfleetwise-decodermanifest-signaldecodersitems-obdsignal
            '''
            result = self._values.get("obd_signal")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDecoderManifestPropsMixin.ObdSignalProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-decodermanifest-signaldecodersitems.html#cfn-iotfleetwise-decodermanifest-signaldecodersitems-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SignalDecodersItemsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnFleetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "id": "id",
        "signal_catalog_arn": "signalCatalogArn",
        "tags": "tags",
    },
)
class CfnFleetMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        signal_catalog_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFleetPropsMixin.

        :param description: A brief description of the fleet.
        :param id: The unique ID of the fleet.
        :param signal_catalog_arn: The ARN of the signal catalog associated with the fleet.
        :param tags: Metadata that can be used to manage the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
            
            cfn_fleet_mixin_props = iotfleetwise_mixins.CfnFleetMixinProps(
                description="description",
                id="id",
                signal_catalog_arn="signalCatalogArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd6140175f0378cdc58e38d32a8cddd7c33edaaf3d58a19a079f1b67d68350da)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument signal_catalog_arn", value=signal_catalog_arn, expected_type=type_hints["signal_catalog_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if signal_catalog_arn is not None:
            self._values["signal_catalog_arn"] = signal_catalog_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html#cfn-iotfleetwise-fleet-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''The unique ID of the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html#cfn-iotfleetwise-fleet-id
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signal_catalog_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the signal catalog associated with the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html#cfn-iotfleetwise-fleet-signalcatalogarn
        '''
        result = self._values.get("signal_catalog_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata that can be used to manage the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html#cfn-iotfleetwise-fleet-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFleetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFleetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnFleetPropsMixin",
):
    '''Creates a fleet that represents a group of vehicles.

    .. epigraph::

       You must create both a signal catalog and vehicles before you can create a fleet.

    For more information, see `Fleets <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleets.html>`_ in the *AWS IoT FleetWise Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-fleet.html
    :cloudformationResource: AWS::IoTFleetWise::Fleet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
        
        cfn_fleet_props_mixin = iotfleetwise_mixins.CfnFleetPropsMixin(iotfleetwise_mixins.CfnFleetMixinProps(
            description="description",
            id="id",
            signal_catalog_arn="signalCatalogArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFleetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTFleetWise::Fleet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adbd7909610650249a1f4c9459faf6ed4ff8d376507f7b30dc04ef7b9381ba1b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        options = _CfnPropertyMixinOptions_9cbff649(strategy=strategy)

        jsii.create(self.__class__, self, [props, options])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply the mixin properties to the construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3f71a4b144c85c468e8743b4824a6d1e48df1899590b351b5daeb27d4f4852)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a55395afa1fda3665709ee59e4f317871bae808c796a33113e0e4a95df44442)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFleetMixinProps:
        return typing.cast(CfnFleetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnModelManifestMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "nodes": "nodes",
        "signal_catalog_arn": "signalCatalogArn",
        "status": "status",
        "tags": "tags",
    },
)
class CfnModelManifestMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
        signal_catalog_arn: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnModelManifestPropsMixin.

        :param description: A brief description of the vehicle model.
        :param name: The name of the vehicle model.
        :param nodes: A list of nodes, which are a general abstraction of signals.
        :param signal_catalog_arn: The Amazon Resource Name (ARN) of the signal catalog associated with the vehicle model.
        :param status: The state of the vehicle model. If the status is ``ACTIVE`` , the vehicle model can't be edited. If the status is ``DRAFT`` , you can edit the vehicle model. Default: - "DRAFT"
        :param tags: Metadata that can be used to manage the vehicle model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
            
            cfn_model_manifest_mixin_props = iotfleetwise_mixins.CfnModelManifestMixinProps(
                description="description",
                name="name",
                nodes=["nodes"],
                signal_catalog_arn="signalCatalogArn",
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b96e37a1aa4b5adadd82e431bd60c8b29259f7d5b84b0e4896300c780f825d6)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument nodes", value=nodes, expected_type=type_hints["nodes"])
            check_type(argname="argument signal_catalog_arn", value=signal_catalog_arn, expected_type=type_hints["signal_catalog_arn"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if nodes is not None:
            self._values["nodes"] = nodes
        if signal_catalog_arn is not None:
            self._values["signal_catalog_arn"] = signal_catalog_arn
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the vehicle model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the vehicle model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nodes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of nodes, which are a general abstraction of signals.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-nodes
        '''
        result = self._values.get("nodes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def signal_catalog_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the signal catalog associated with the vehicle model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-signalcatalogarn
        '''
        result = self._values.get("signal_catalog_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The state of the vehicle model.

        If the status is ``ACTIVE`` , the vehicle model can't be edited. If the status is ``DRAFT`` , you can edit the vehicle model.

        :default: - "DRAFT"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata that can be used to manage the vehicle model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html#cfn-iotfleetwise-modelmanifest-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnModelManifestMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnModelManifestPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnModelManifestPropsMixin",
):
    '''Creates a vehicle model (model manifest) that specifies signals (attributes, branches, sensors, and actuators).

    For more information, see `Vehicle models <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/vehicle-models.html>`_ in the *AWS IoT FleetWise Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-modelmanifest.html
    :cloudformationResource: AWS::IoTFleetWise::ModelManifest
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
        
        cfn_model_manifest_props_mixin = iotfleetwise_mixins.CfnModelManifestPropsMixin(iotfleetwise_mixins.CfnModelManifestMixinProps(
            description="description",
            name="name",
            nodes=["nodes"],
            signal_catalog_arn="signalCatalogArn",
            status="status",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnModelManifestMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTFleetWise::ModelManifest``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd8d8e2a85706b3a1bdaad68cb632c216fcd8ecda145baad4ea95ffad46643e8)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        options = _CfnPropertyMixinOptions_9cbff649(strategy=strategy)

        jsii.create(self.__class__, self, [props, options])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply the mixin properties to the construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43ac4b988214ada91f89066dc6da284a4dcadb220dd614d7fa709b3c77cf61f7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7b830df0b4877c43f6a0fcdc0d528cfd77bdaa3a4ee60e26e3b2163bb48fbc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnModelManifestMixinProps:
        return typing.cast(CfnModelManifestMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnSignalCatalogMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "node_counts": "nodeCounts",
        "nodes": "nodes",
        "tags": "tags",
    },
)
class CfnSignalCatalogMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        node_counts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSignalCatalogPropsMixin.NodeCountsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        nodes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSignalCatalogPropsMixin.NodeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSignalCatalogPropsMixin.

        :param description: A brief description of the signal catalog.
        :param name: The name of the signal catalog.
        :param node_counts: Information about the number of nodes and node types in a vehicle network.
        :param nodes: A list of information about nodes, which are a general abstraction of signals.
        :param tags: Metadata that can be used to manage the signal catalog.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
            
            cfn_signal_catalog_mixin_props = iotfleetwise_mixins.CfnSignalCatalogMixinProps(
                description="description",
                name="name",
                node_counts=iotfleetwise_mixins.CfnSignalCatalogPropsMixin.NodeCountsProperty(
                    total_actuators=123,
                    total_attributes=123,
                    total_branches=123,
                    total_nodes=123,
                    total_sensors=123
                ),
                nodes=[iotfleetwise_mixins.CfnSignalCatalogPropsMixin.NodeProperty(
                    actuator=iotfleetwise_mixins.CfnSignalCatalogPropsMixin.ActuatorProperty(
                        allowed_values=["allowedValues"],
                        assigned_value="assignedValue",
                        data_type="dataType",
                        description="description",
                        fully_qualified_name="fullyQualifiedName",
                        max=123,
                        min=123,
                        unit="unit"
                    ),
                    attribute=iotfleetwise_mixins.CfnSignalCatalogPropsMixin.AttributeProperty(
                        allowed_values=["allowedValues"],
                        assigned_value="assignedValue",
                        data_type="dataType",
                        default_value="defaultValue",
                        description="description",
                        fully_qualified_name="fullyQualifiedName",
                        max=123,
                        min=123,
                        unit="unit"
                    ),
                    branch=iotfleetwise_mixins.CfnSignalCatalogPropsMixin.BranchProperty(
                        description="description",
                        fully_qualified_name="fullyQualifiedName"
                    ),
                    sensor=iotfleetwise_mixins.CfnSignalCatalogPropsMixin.SensorProperty(
                        allowed_values=["allowedValues"],
                        data_type="dataType",
                        description="description",
                        fully_qualified_name="fullyQualifiedName",
                        max=123,
                        min=123,
                        unit="unit"
                    )
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c1d3177697effcaa5ca0f2b365c920b0e77bdd774b5f3304fb26ed6ee99a325)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_counts", value=node_counts, expected_type=type_hints["node_counts"])
            check_type(argname="argument nodes", value=nodes, expected_type=type_hints["nodes"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if node_counts is not None:
            self._values["node_counts"] = node_counts
        if nodes is not None:
            self._values["nodes"] = nodes
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the signal catalog.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the signal catalog.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_counts(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSignalCatalogPropsMixin.NodeCountsProperty"]]:
        '''Information about the number of nodes and node types in a vehicle network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-nodecounts
        '''
        result = self._values.get("node_counts")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSignalCatalogPropsMixin.NodeCountsProperty"]], result)

    @builtins.property
    def nodes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSignalCatalogPropsMixin.NodeProperty"]]]]:
        '''A list of information about nodes, which are a general abstraction of signals.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-nodes
        '''
        result = self._values.get("nodes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSignalCatalogPropsMixin.NodeProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata that can be used to manage the signal catalog.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html#cfn-iotfleetwise-signalcatalog-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSignalCatalogMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSignalCatalogPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnSignalCatalogPropsMixin",
):
    '''Creates a collection of standardized signals that can be reused to create vehicle models.

    For more information, see `Signal catalogs <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/signal-catalogs.html>`_ in the *AWS IoT FleetWise Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-signalcatalog.html
    :cloudformationResource: AWS::IoTFleetWise::SignalCatalog
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
        
        cfn_signal_catalog_props_mixin = iotfleetwise_mixins.CfnSignalCatalogPropsMixin(iotfleetwise_mixins.CfnSignalCatalogMixinProps(
            description="description",
            name="name",
            node_counts=iotfleetwise_mixins.CfnSignalCatalogPropsMixin.NodeCountsProperty(
                total_actuators=123,
                total_attributes=123,
                total_branches=123,
                total_nodes=123,
                total_sensors=123
            ),
            nodes=[iotfleetwise_mixins.CfnSignalCatalogPropsMixin.NodeProperty(
                actuator=iotfleetwise_mixins.CfnSignalCatalogPropsMixin.ActuatorProperty(
                    allowed_values=["allowedValues"],
                    assigned_value="assignedValue",
                    data_type="dataType",
                    description="description",
                    fully_qualified_name="fullyQualifiedName",
                    max=123,
                    min=123,
                    unit="unit"
                ),
                attribute=iotfleetwise_mixins.CfnSignalCatalogPropsMixin.AttributeProperty(
                    allowed_values=["allowedValues"],
                    assigned_value="assignedValue",
                    data_type="dataType",
                    default_value="defaultValue",
                    description="description",
                    fully_qualified_name="fullyQualifiedName",
                    max=123,
                    min=123,
                    unit="unit"
                ),
                branch=iotfleetwise_mixins.CfnSignalCatalogPropsMixin.BranchProperty(
                    description="description",
                    fully_qualified_name="fullyQualifiedName"
                ),
                sensor=iotfleetwise_mixins.CfnSignalCatalogPropsMixin.SensorProperty(
                    allowed_values=["allowedValues"],
                    data_type="dataType",
                    description="description",
                    fully_qualified_name="fullyQualifiedName",
                    max=123,
                    min=123,
                    unit="unit"
                )
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSignalCatalogMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTFleetWise::SignalCatalog``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a9d38fff8cb50ff987cd6b20fa98d077e9da851d86c09d48ac3cc95c3d0138)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        options = _CfnPropertyMixinOptions_9cbff649(strategy=strategy)

        jsii.create(self.__class__, self, [props, options])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply the mixin properties to the construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf30f6bde7fecfd42d506876157ecc5446a8c2ce352087620130de4c2e62ec7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8396febc416257057eca60de05c4e8ae59a05f10dae3e21fc3f15fa4cdab780e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSignalCatalogMixinProps:
        return typing.cast(CfnSignalCatalogMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnSignalCatalogPropsMixin.ActuatorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_values": "allowedValues",
            "assigned_value": "assignedValue",
            "data_type": "dataType",
            "description": "description",
            "fully_qualified_name": "fullyQualifiedName",
            "max": "max",
            "min": "min",
            "unit": "unit",
        },
    )
    class ActuatorProperty:
        def __init__(
            self,
            *,
            allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            assigned_value: typing.Optional[builtins.str] = None,
            data_type: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            fully_qualified_name: typing.Optional[builtins.str] = None,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A signal that represents a vehicle device such as the engine, heater, and door locks.

            Data from an actuator reports the state of a certain vehicle device.
            .. epigraph::

               Updating actuator data can change the state of a device. For example, you can turn on or off the heater by updating its actuator data.

            :param allowed_values: A list of possible values an actuator can take.
            :param assigned_value: A specified value for the actuator.
            :param data_type: The specified data type of the actuator.
            :param description: A brief description of the actuator.
            :param fully_qualified_name: The fully qualified name of the actuator. For example, the fully qualified name of an actuator might be ``Vehicle.Front.Left.Door.Lock`` .
            :param max: The specified possible maximum value of an actuator.
            :param min: The specified possible minimum value of an actuator.
            :param unit: The scientific unit for the actuator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                actuator_property = iotfleetwise_mixins.CfnSignalCatalogPropsMixin.ActuatorProperty(
                    allowed_values=["allowedValues"],
                    assigned_value="assignedValue",
                    data_type="dataType",
                    description="description",
                    fully_qualified_name="fullyQualifiedName",
                    max=123,
                    min=123,
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__47ac5f67864be9e0ec3352628b124e3e1236b0cd5f619163cac0f70358cc4105)
                check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
                check_type(argname="argument assigned_value", value=assigned_value, expected_type=type_hints["assigned_value"])
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_values is not None:
                self._values["allowed_values"] = allowed_values
            if assigned_value is not None:
                self._values["assigned_value"] = assigned_value
            if data_type is not None:
                self._values["data_type"] = data_type
            if description is not None:
                self._values["description"] = description
            if fully_qualified_name is not None:
                self._values["fully_qualified_name"] = fully_qualified_name
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of possible values an actuator can take.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def assigned_value(self) -> typing.Optional[builtins.str]:
            '''A specified value for the actuator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-assignedvalue
            '''
            result = self._values.get("assigned_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_type(self) -> typing.Optional[builtins.str]:
            '''The specified data type of the actuator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A brief description of the actuator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fully_qualified_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified name of the actuator.

            For example, the fully qualified name of an actuator might be ``Vehicle.Front.Left.Door.Lock`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-fullyqualifiedname
            '''
            result = self._values.get("fully_qualified_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The specified possible maximum value of an actuator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The specified possible minimum value of an actuator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The scientific unit for the actuator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-actuator.html#cfn-iotfleetwise-signalcatalog-actuator-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActuatorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnSignalCatalogPropsMixin.AttributeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_values": "allowedValues",
            "assigned_value": "assignedValue",
            "data_type": "dataType",
            "default_value": "defaultValue",
            "description": "description",
            "fully_qualified_name": "fullyQualifiedName",
            "max": "max",
            "min": "min",
            "unit": "unit",
        },
    )
    class AttributeProperty:
        def __init__(
            self,
            *,
            allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            assigned_value: typing.Optional[builtins.str] = None,
            data_type: typing.Optional[builtins.str] = None,
            default_value: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            fully_qualified_name: typing.Optional[builtins.str] = None,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A signal that represents static information about the vehicle, such as engine type or manufacturing date.

            :param allowed_values: A list of possible values an attribute can be assigned.
            :param assigned_value: A specified value for the attribute.
            :param data_type: The specified data type of the attribute.
            :param default_value: The default value of the attribute.
            :param description: A brief description of the attribute.
            :param fully_qualified_name: The fully qualified name of the attribute. For example, the fully qualified name of an attribute might be ``Vehicle.Body.Engine.Type`` .
            :param max: The specified possible maximum value of the attribute.
            :param min: The specified possible minimum value of the attribute.
            :param unit: The scientific unit for the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                attribute_property = iotfleetwise_mixins.CfnSignalCatalogPropsMixin.AttributeProperty(
                    allowed_values=["allowedValues"],
                    assigned_value="assignedValue",
                    data_type="dataType",
                    default_value="defaultValue",
                    description="description",
                    fully_qualified_name="fullyQualifiedName",
                    max=123,
                    min=123,
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__71a3a879fd7620450b99101d9bcd99402191aaa77e5c086a0f8884af6cc13faf)
                check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
                check_type(argname="argument assigned_value", value=assigned_value, expected_type=type_hints["assigned_value"])
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_values is not None:
                self._values["allowed_values"] = allowed_values
            if assigned_value is not None:
                self._values["assigned_value"] = assigned_value
            if data_type is not None:
                self._values["data_type"] = data_type
            if default_value is not None:
                self._values["default_value"] = default_value
            if description is not None:
                self._values["description"] = description
            if fully_qualified_name is not None:
                self._values["fully_qualified_name"] = fully_qualified_name
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of possible values an attribute can be assigned.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def assigned_value(self) -> typing.Optional[builtins.str]:
            '''A specified value for the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-assignedvalue
            '''
            result = self._values.get("assigned_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_type(self) -> typing.Optional[builtins.str]:
            '''The specified data type of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A brief description of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fully_qualified_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified name of the attribute.

            For example, the fully qualified name of an attribute might be ``Vehicle.Body.Engine.Type`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-fullyqualifiedname
            '''
            result = self._values.get("fully_qualified_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The specified possible maximum value of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The specified possible minimum value of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The scientific unit for the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-attribute.html#cfn-iotfleetwise-signalcatalog-attribute-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnSignalCatalogPropsMixin.BranchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "fully_qualified_name": "fullyQualifiedName",
        },
    )
    class BranchProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            fully_qualified_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A group of signals that are defined in a hierarchical structure.

            :param description: A brief description of the branch.
            :param fully_qualified_name: The fully qualified name of the branch. For example, the fully qualified name of a branch might be ``Vehicle.Body.Engine`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-branch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                branch_property = iotfleetwise_mixins.CfnSignalCatalogPropsMixin.BranchProperty(
                    description="description",
                    fully_qualified_name="fullyQualifiedName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae21e9c3913406e8c61fc73dd688d8499a153d9d6a310245be02dba671df93e4)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if fully_qualified_name is not None:
                self._values["fully_qualified_name"] = fully_qualified_name

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A brief description of the branch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-branch.html#cfn-iotfleetwise-signalcatalog-branch-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fully_qualified_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified name of the branch.

            For example, the fully qualified name of a branch might be ``Vehicle.Body.Engine`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-branch.html#cfn-iotfleetwise-signalcatalog-branch-fullyqualifiedname
            '''
            result = self._values.get("fully_qualified_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BranchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnSignalCatalogPropsMixin.NodeCountsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "total_actuators": "totalActuators",
            "total_attributes": "totalAttributes",
            "total_branches": "totalBranches",
            "total_nodes": "totalNodes",
            "total_sensors": "totalSensors",
        },
    )
    class NodeCountsProperty:
        def __init__(
            self,
            *,
            total_actuators: typing.Optional[jsii.Number] = None,
            total_attributes: typing.Optional[jsii.Number] = None,
            total_branches: typing.Optional[jsii.Number] = None,
            total_nodes: typing.Optional[jsii.Number] = None,
            total_sensors: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about the number of nodes and node types in a vehicle network.

            :param total_actuators: The total number of nodes in a vehicle network that represent actuators.
            :param total_attributes: The total number of nodes in a vehicle network that represent attributes.
            :param total_branches: The total number of nodes in a vehicle network that represent branches.
            :param total_nodes: The total number of nodes in a vehicle network.
            :param total_sensors: The total number of nodes in a vehicle network that represent sensors.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-nodecounts.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                node_counts_property = iotfleetwise_mixins.CfnSignalCatalogPropsMixin.NodeCountsProperty(
                    total_actuators=123,
                    total_attributes=123,
                    total_branches=123,
                    total_nodes=123,
                    total_sensors=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e6dca2442bca2e00afcf0a469ee44a48165f295e1e2c092afb7e2db62068e28)
                check_type(argname="argument total_actuators", value=total_actuators, expected_type=type_hints["total_actuators"])
                check_type(argname="argument total_attributes", value=total_attributes, expected_type=type_hints["total_attributes"])
                check_type(argname="argument total_branches", value=total_branches, expected_type=type_hints["total_branches"])
                check_type(argname="argument total_nodes", value=total_nodes, expected_type=type_hints["total_nodes"])
                check_type(argname="argument total_sensors", value=total_sensors, expected_type=type_hints["total_sensors"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if total_actuators is not None:
                self._values["total_actuators"] = total_actuators
            if total_attributes is not None:
                self._values["total_attributes"] = total_attributes
            if total_branches is not None:
                self._values["total_branches"] = total_branches
            if total_nodes is not None:
                self._values["total_nodes"] = total_nodes
            if total_sensors is not None:
                self._values["total_sensors"] = total_sensors

        @builtins.property
        def total_actuators(self) -> typing.Optional[jsii.Number]:
            '''The total number of nodes in a vehicle network that represent actuators.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-nodecounts.html#cfn-iotfleetwise-signalcatalog-nodecounts-totalactuators
            '''
            result = self._values.get("total_actuators")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total_attributes(self) -> typing.Optional[jsii.Number]:
            '''The total number of nodes in a vehicle network that represent attributes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-nodecounts.html#cfn-iotfleetwise-signalcatalog-nodecounts-totalattributes
            '''
            result = self._values.get("total_attributes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total_branches(self) -> typing.Optional[jsii.Number]:
            '''The total number of nodes in a vehicle network that represent branches.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-nodecounts.html#cfn-iotfleetwise-signalcatalog-nodecounts-totalbranches
            '''
            result = self._values.get("total_branches")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total_nodes(self) -> typing.Optional[jsii.Number]:
            '''The total number of nodes in a vehicle network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-nodecounts.html#cfn-iotfleetwise-signalcatalog-nodecounts-totalnodes
            '''
            result = self._values.get("total_nodes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total_sensors(self) -> typing.Optional[jsii.Number]:
            '''The total number of nodes in a vehicle network that represent sensors.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-nodecounts.html#cfn-iotfleetwise-signalcatalog-nodecounts-totalsensors
            '''
            result = self._values.get("total_sensors")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeCountsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnSignalCatalogPropsMixin.NodeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actuator": "actuator",
            "attribute": "attribute",
            "branch": "branch",
            "sensor": "sensor",
        },
    )
    class NodeProperty:
        def __init__(
            self,
            *,
            actuator: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSignalCatalogPropsMixin.ActuatorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            attribute: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSignalCatalogPropsMixin.AttributeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            branch: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSignalCatalogPropsMixin.BranchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sensor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSignalCatalogPropsMixin.SensorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A general abstraction of a signal.

            A node can be specified as an actuator, attribute, branch, or sensor.

            :param actuator: Information about a node specified as an actuator. .. epigraph:: An actuator is a digital representation of a vehicle device.
            :param attribute: Information about a node specified as an attribute. .. epigraph:: An attribute represents static information about a vehicle.
            :param branch: Information about a node specified as a branch. .. epigraph:: A group of signals that are defined in a hierarchical structure.
            :param sensor: An input component that reports the environmental condition of a vehicle. .. epigraph:: You can collect data about fluid levels, temperatures, vibrations, or battery voltage from sensors.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-node.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                node_property = iotfleetwise_mixins.CfnSignalCatalogPropsMixin.NodeProperty(
                    actuator=iotfleetwise_mixins.CfnSignalCatalogPropsMixin.ActuatorProperty(
                        allowed_values=["allowedValues"],
                        assigned_value="assignedValue",
                        data_type="dataType",
                        description="description",
                        fully_qualified_name="fullyQualifiedName",
                        max=123,
                        min=123,
                        unit="unit"
                    ),
                    attribute=iotfleetwise_mixins.CfnSignalCatalogPropsMixin.AttributeProperty(
                        allowed_values=["allowedValues"],
                        assigned_value="assignedValue",
                        data_type="dataType",
                        default_value="defaultValue",
                        description="description",
                        fully_qualified_name="fullyQualifiedName",
                        max=123,
                        min=123,
                        unit="unit"
                    ),
                    branch=iotfleetwise_mixins.CfnSignalCatalogPropsMixin.BranchProperty(
                        description="description",
                        fully_qualified_name="fullyQualifiedName"
                    ),
                    sensor=iotfleetwise_mixins.CfnSignalCatalogPropsMixin.SensorProperty(
                        allowed_values=["allowedValues"],
                        data_type="dataType",
                        description="description",
                        fully_qualified_name="fullyQualifiedName",
                        max=123,
                        min=123,
                        unit="unit"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92eb72e3c1a7ffe8a3cbfe3a057b02562b0b523a557b14c6af20dd9145024c32)
                check_type(argname="argument actuator", value=actuator, expected_type=type_hints["actuator"])
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
                check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
                check_type(argname="argument sensor", value=sensor, expected_type=type_hints["sensor"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actuator is not None:
                self._values["actuator"] = actuator
            if attribute is not None:
                self._values["attribute"] = attribute
            if branch is not None:
                self._values["branch"] = branch
            if sensor is not None:
                self._values["sensor"] = sensor

        @builtins.property
        def actuator(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSignalCatalogPropsMixin.ActuatorProperty"]]:
            '''Information about a node specified as an actuator.

            .. epigraph::

               An actuator is a digital representation of a vehicle device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-node.html#cfn-iotfleetwise-signalcatalog-node-actuator
            '''
            result = self._values.get("actuator")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSignalCatalogPropsMixin.ActuatorProperty"]], result)

        @builtins.property
        def attribute(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSignalCatalogPropsMixin.AttributeProperty"]]:
            '''Information about a node specified as an attribute.

            .. epigraph::

               An attribute represents static information about a vehicle.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-node.html#cfn-iotfleetwise-signalcatalog-node-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSignalCatalogPropsMixin.AttributeProperty"]], result)

        @builtins.property
        def branch(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSignalCatalogPropsMixin.BranchProperty"]]:
            '''Information about a node specified as a branch.

            .. epigraph::

               A group of signals that are defined in a hierarchical structure.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-node.html#cfn-iotfleetwise-signalcatalog-node-branch
            '''
            result = self._values.get("branch")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSignalCatalogPropsMixin.BranchProperty"]], result)

        @builtins.property
        def sensor(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSignalCatalogPropsMixin.SensorProperty"]]:
            '''An input component that reports the environmental condition of a vehicle.

            .. epigraph::

               You can collect data about fluid levels, temperatures, vibrations, or battery voltage from sensors.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-node.html#cfn-iotfleetwise-signalcatalog-node-sensor
            '''
            result = self._values.get("sensor")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSignalCatalogPropsMixin.SensorProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnSignalCatalogPropsMixin.SensorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_values": "allowedValues",
            "data_type": "dataType",
            "description": "description",
            "fully_qualified_name": "fullyQualifiedName",
            "max": "max",
            "min": "min",
            "unit": "unit",
        },
    )
    class SensorProperty:
        def __init__(
            self,
            *,
            allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            data_type: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            fully_qualified_name: typing.Optional[builtins.str] = None,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An input component that reports the environmental condition of a vehicle.

            .. epigraph::

               You can collect data about fluid levels, temperatures, vibrations, or battery voltage from sensors.

            :param allowed_values: A list of possible values a sensor can take.
            :param data_type: The specified data type of the sensor.
            :param description: A brief description of a sensor.
            :param fully_qualified_name: The fully qualified name of the sensor. For example, the fully qualified name of a sensor might be ``Vehicle.Body.Engine.Battery`` .
            :param max: The specified possible maximum value of the sensor.
            :param min: The specified possible minimum value of the sensor.
            :param unit: The scientific unit of measurement for data collected by the sensor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                sensor_property = iotfleetwise_mixins.CfnSignalCatalogPropsMixin.SensorProperty(
                    allowed_values=["allowedValues"],
                    data_type="dataType",
                    description="description",
                    fully_qualified_name="fullyQualifiedName",
                    max=123,
                    min=123,
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e69e34f0675f3f89a1a5bf4dd973ea8e00e1f86e37c955222df92c6de7e01d5a)
                check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_values is not None:
                self._values["allowed_values"] = allowed_values
            if data_type is not None:
                self._values["data_type"] = data_type
            if description is not None:
                self._values["description"] = description
            if fully_qualified_name is not None:
                self._values["fully_qualified_name"] = fully_qualified_name
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of possible values a sensor can take.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html#cfn-iotfleetwise-signalcatalog-sensor-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def data_type(self) -> typing.Optional[builtins.str]:
            '''The specified data type of the sensor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html#cfn-iotfleetwise-signalcatalog-sensor-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A brief description of a sensor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html#cfn-iotfleetwise-signalcatalog-sensor-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fully_qualified_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified name of the sensor.

            For example, the fully qualified name of a sensor might be ``Vehicle.Body.Engine.Battery`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html#cfn-iotfleetwise-signalcatalog-sensor-fullyqualifiedname
            '''
            result = self._values.get("fully_qualified_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The specified possible maximum value of the sensor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html#cfn-iotfleetwise-signalcatalog-sensor-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The specified possible minimum value of the sensor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html#cfn-iotfleetwise-signalcatalog-sensor-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The scientific unit of measurement for data collected by the sensor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-signalcatalog-sensor.html#cfn-iotfleetwise-signalcatalog-sensor-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SensorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnStateTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_extra_dimensions": "dataExtraDimensions",
        "description": "description",
        "metadata_extra_dimensions": "metadataExtraDimensions",
        "name": "name",
        "signal_catalog_arn": "signalCatalogArn",
        "state_template_properties": "stateTemplateProperties",
        "tags": "tags",
    },
)
class CfnStateTemplateMixinProps:
    def __init__(
        self,
        *,
        data_extra_dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        metadata_extra_dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        signal_catalog_arn: typing.Optional[builtins.str] = None,
        state_template_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnStateTemplatePropsMixin.

        :param data_extra_dimensions: A list of vehicle attributes associated with the payload published on the state template's MQTT topic.
        :param description: A brief description of the state template.
        :param metadata_extra_dimensions: A list of vehicle attributes to associate with the user properties of the messages published on the state template's MQTT topic. For example, if you add ``Vehicle.Attributes.Make`` and ``Vehicle.Attributes.Model`` attributes, these attributes are included as user properties with the MQTT message.
        :param name: The unique alias of the state template.
        :param signal_catalog_arn: The Amazon Resource Name (ARN) of the signal catalog associated with the state template.
        :param state_template_properties: A list of signals from which data is collected. The state template properties contain the fully qualified names of the signals.
        :param tags: Metadata that can be used to manage the state template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-statetemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
            
            cfn_state_template_mixin_props = iotfleetwise_mixins.CfnStateTemplateMixinProps(
                data_extra_dimensions=["dataExtraDimensions"],
                description="description",
                metadata_extra_dimensions=["metadataExtraDimensions"],
                name="name",
                signal_catalog_arn="signalCatalogArn",
                state_template_properties=["stateTemplateProperties"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edbe3aa4a32b325e293b09d271eb27024f5e1960caad4f11de599885ebfce3d4)
            check_type(argname="argument data_extra_dimensions", value=data_extra_dimensions, expected_type=type_hints["data_extra_dimensions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument metadata_extra_dimensions", value=metadata_extra_dimensions, expected_type=type_hints["metadata_extra_dimensions"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument signal_catalog_arn", value=signal_catalog_arn, expected_type=type_hints["signal_catalog_arn"])
            check_type(argname="argument state_template_properties", value=state_template_properties, expected_type=type_hints["state_template_properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_extra_dimensions is not None:
            self._values["data_extra_dimensions"] = data_extra_dimensions
        if description is not None:
            self._values["description"] = description
        if metadata_extra_dimensions is not None:
            self._values["metadata_extra_dimensions"] = metadata_extra_dimensions
        if name is not None:
            self._values["name"] = name
        if signal_catalog_arn is not None:
            self._values["signal_catalog_arn"] = signal_catalog_arn
        if state_template_properties is not None:
            self._values["state_template_properties"] = state_template_properties
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_extra_dimensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of vehicle attributes associated with the payload published on the state template's MQTT topic.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-statetemplate.html#cfn-iotfleetwise-statetemplate-dataextradimensions
        '''
        result = self._values.get("data_extra_dimensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the state template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-statetemplate.html#cfn-iotfleetwise-statetemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_extra_dimensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of vehicle attributes to associate with the user properties of the messages published on the state template's MQTT topic.

        For example, if you add ``Vehicle.Attributes.Make`` and ``Vehicle.Attributes.Model`` attributes, these attributes are included as user properties with the MQTT message.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-statetemplate.html#cfn-iotfleetwise-statetemplate-metadataextradimensions
        '''
        result = self._values.get("metadata_extra_dimensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique alias of the state template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-statetemplate.html#cfn-iotfleetwise-statetemplate-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signal_catalog_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the signal catalog associated with the state template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-statetemplate.html#cfn-iotfleetwise-statetemplate-signalcatalogarn
        '''
        result = self._values.get("signal_catalog_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state_template_properties(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of signals from which data is collected.

        The state template properties contain the fully qualified names of the signals.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-statetemplate.html#cfn-iotfleetwise-statetemplate-statetemplateproperties
        '''
        result = self._values.get("state_template_properties")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata that can be used to manage the state template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-statetemplate.html#cfn-iotfleetwise-statetemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStateTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStateTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnStateTemplatePropsMixin",
):
    '''Creates a mechanism for vehicle owners to track the state of their vehicles.

    State templates determine which signal updates the vehicle sends to the cloud.

    For more information, see `State templates <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/state-templates.html>`_ in the *AWS IoT FleetWise Developer Guide* .
    .. epigraph::

       Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-statetemplate.html
    :cloudformationResource: AWS::IoTFleetWise::StateTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
        
        cfn_state_template_props_mixin = iotfleetwise_mixins.CfnStateTemplatePropsMixin(iotfleetwise_mixins.CfnStateTemplateMixinProps(
            data_extra_dimensions=["dataExtraDimensions"],
            description="description",
            metadata_extra_dimensions=["metadataExtraDimensions"],
            name="name",
            signal_catalog_arn="signalCatalogArn",
            state_template_properties=["stateTemplateProperties"],
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStateTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTFleetWise::StateTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0400670c45304580f501248de8ee73b014823b4cfe4f8e5b36e723176d3e40c9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        options = _CfnPropertyMixinOptions_9cbff649(strategy=strategy)

        jsii.create(self.__class__, self, [props, options])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply the mixin properties to the construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f56f4aa21cd642ecd0052d734a6477182b5b026dd7dedc486f63c089af9cdd7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83809e8cd0ada0c003761ab808b900dae8a94546634d6fe22e610403e02a93fd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStateTemplateMixinProps:
        return typing.cast(CfnStateTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


class CfnVehicleIotFleetwiseLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnVehicleIotFleetwiseLogs",
):
    '''Builder for CfnVehicleLogsMixin to generate IOT_FLEETWISE_LOGS for CfnVehicle.

    :cloudformationResource: AWS::IoTFleetWise::Vehicle
    :logType: IOT_FLEETWISE_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
        
        cfn_vehicle_iot_fleetwise_logs = iotfleetwise_mixins.CfnVehicleIotFleetwiseLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> "CfnVehicleLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415eb6423b97a78ad45a0c91f6b4238eae064aa3b9f95589e4df27579a7665aa)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnVehicleLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnVehicleLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__886578f717376bbc9957d64d49206ff1ae88f7842c0223bba0a9d44976576aef)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnVehicleLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnVehicleLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643fcff8ccf9bba92e15cc0ec69726367e955537fb7636c4605c1481a3893516)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnVehicleLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnVehicleLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnVehicleLogsMixin",
):
    '''Creates a vehicle, which is an instance of a vehicle model (model manifest).

    Vehicles created from the same vehicle model consist of the same signals inherited from the vehicle model.
    .. epigraph::

       If you have an existing AWS IoT thing, you can use AWS IoT FleetWise to create a vehicle and collect data from your thing.

    For more information, see `Vehicles <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/vehicles.html>`_ in the *AWS IoT FleetWise Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html
    :cloudformationResource: AWS::IoTFleetWise::Vehicle
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_vehicle_logs_mixin = iotfleetwise_mixins.CfnVehicleLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::IoTFleetWise::Vehicle``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c7d2d659078d6d2082daf528cb24cea57c05cc04178356157d251e4d069a81d)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
        jsii.create(self.__class__, self, [log_type, log_delivery])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        resource: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply vended logs configuration to the construct.

        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5cae60ee244e0f88ad43344015b8edaae877e40b8ec2796ea582a2200e6484)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f3d4b2e6684a66ad66d74c9e086a3d530e41217891fde6d421b615f04824b2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="IOT_FLEETWISE_LOGS")
    def IOT_FLEETWISE_LOGS(cls) -> CfnVehicleIotFleetwiseLogs:
        return typing.cast(CfnVehicleIotFleetwiseLogs, jsii.sget(cls, "IOT_FLEETWISE_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnVehicleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "association_behavior": "associationBehavior",
        "attributes": "attributes",
        "decoder_manifest_arn": "decoderManifestArn",
        "model_manifest_arn": "modelManifestArn",
        "name": "name",
        "state_templates": "stateTemplates",
        "tags": "tags",
    },
)
class CfnVehicleMixinProps:
    def __init__(
        self,
        *,
        association_behavior: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        decoder_manifest_arn: typing.Optional[builtins.str] = None,
        model_manifest_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        state_templates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVehiclePropsMixin.StateTemplateAssociationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnVehiclePropsMixin.

        :param association_behavior: An option to create a new AWS IoT thing when creating a vehicle, or to validate an existing thing as a vehicle.
        :param attributes: Static information about a vehicle in a key-value pair. For example: ``"engine Type"`` : ``"v6"``
        :param decoder_manifest_arn: The Amazon Resource Name (ARN) of a decoder manifest associated with the vehicle to create.
        :param model_manifest_arn: The Amazon Resource Name (ARN) of the vehicle model (model manifest) to create the vehicle from.
        :param name: The unique ID of the vehicle.
        :param state_templates: Associate state templates to track the state of the vehicle. State templates determine which signal updates the vehicle sends to the cloud.
        :param tags: Metadata which can be used to manage the vehicle.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
            
            # on_change: Any
            
            cfn_vehicle_mixin_props = iotfleetwise_mixins.CfnVehicleMixinProps(
                association_behavior="associationBehavior",
                attributes={
                    "attributes_key": "attributes"
                },
                decoder_manifest_arn="decoderManifestArn",
                model_manifest_arn="modelManifestArn",
                name="name",
                state_templates=[iotfleetwise_mixins.CfnVehiclePropsMixin.StateTemplateAssociationProperty(
                    identifier="identifier",
                    state_template_update_strategy=iotfleetwise_mixins.CfnVehiclePropsMixin.StateTemplateUpdateStrategyProperty(
                        on_change=on_change,
                        periodic=iotfleetwise_mixins.CfnVehiclePropsMixin.PeriodicStateTemplateUpdateStrategyProperty(
                            state_template_update_rate=iotfleetwise_mixins.CfnVehiclePropsMixin.TimePeriodProperty(
                                unit="unit",
                                value=123
                            )
                        )
                    )
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9a992cadc365853b127609fa123d7427ac5ab074a5d1655c0e11cb6adc2c34)
            check_type(argname="argument association_behavior", value=association_behavior, expected_type=type_hints["association_behavior"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument decoder_manifest_arn", value=decoder_manifest_arn, expected_type=type_hints["decoder_manifest_arn"])
            check_type(argname="argument model_manifest_arn", value=model_manifest_arn, expected_type=type_hints["model_manifest_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument state_templates", value=state_templates, expected_type=type_hints["state_templates"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if association_behavior is not None:
            self._values["association_behavior"] = association_behavior
        if attributes is not None:
            self._values["attributes"] = attributes
        if decoder_manifest_arn is not None:
            self._values["decoder_manifest_arn"] = decoder_manifest_arn
        if model_manifest_arn is not None:
            self._values["model_manifest_arn"] = model_manifest_arn
        if name is not None:
            self._values["name"] = name
        if state_templates is not None:
            self._values["state_templates"] = state_templates
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def association_behavior(self) -> typing.Optional[builtins.str]:
        '''An option to create a new AWS IoT thing when creating a vehicle, or to validate an existing thing as a vehicle.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-associationbehavior
        '''
        result = self._values.get("association_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''Static information about a vehicle in a key-value pair.

        For example: ``"engine Type"`` : ``"v6"``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-attributes
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def decoder_manifest_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of a decoder manifest associated with the vehicle to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-decodermanifestarn
        '''
        result = self._values.get("decoder_manifest_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_manifest_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the vehicle model (model manifest) to create the vehicle from.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-modelmanifestarn
        '''
        result = self._values.get("model_manifest_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique ID of the vehicle.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state_templates(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVehiclePropsMixin.StateTemplateAssociationProperty"]]]]:
        '''Associate state templates to track the state of the vehicle.

        State templates determine which signal updates the vehicle sends to the cloud.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-statetemplates
        '''
        result = self._values.get("state_templates")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVehiclePropsMixin.StateTemplateAssociationProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata which can be used to manage the vehicle.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html#cfn-iotfleetwise-vehicle-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVehicleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVehiclePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnVehiclePropsMixin",
):
    '''Creates a vehicle, which is an instance of a vehicle model (model manifest).

    Vehicles created from the same vehicle model consist of the same signals inherited from the vehicle model.
    .. epigraph::

       If you have an existing AWS IoT thing, you can use AWS IoT FleetWise to create a vehicle and collect data from your thing.

    For more information, see `Vehicles <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/vehicles.html>`_ in the *AWS IoT FleetWise Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotfleetwise-vehicle.html
    :cloudformationResource: AWS::IoTFleetWise::Vehicle
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
        
        # on_change: Any
        
        cfn_vehicle_props_mixin = iotfleetwise_mixins.CfnVehiclePropsMixin(iotfleetwise_mixins.CfnVehicleMixinProps(
            association_behavior="associationBehavior",
            attributes={
                "attributes_key": "attributes"
            },
            decoder_manifest_arn="decoderManifestArn",
            model_manifest_arn="modelManifestArn",
            name="name",
            state_templates=[iotfleetwise_mixins.CfnVehiclePropsMixin.StateTemplateAssociationProperty(
                identifier="identifier",
                state_template_update_strategy=iotfleetwise_mixins.CfnVehiclePropsMixin.StateTemplateUpdateStrategyProperty(
                    on_change=on_change,
                    periodic=iotfleetwise_mixins.CfnVehiclePropsMixin.PeriodicStateTemplateUpdateStrategyProperty(
                        state_template_update_rate=iotfleetwise_mixins.CfnVehiclePropsMixin.TimePeriodProperty(
                            unit="unit",
                            value=123
                        )
                    )
                )
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVehicleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTFleetWise::Vehicle``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9657c802c2b2ba3ee5c5457dc446a73bf08e8d888d526dd400d0895d1c436b83)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        options = _CfnPropertyMixinOptions_9cbff649(strategy=strategy)

        jsii.create(self.__class__, self, [props, options])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply the mixin properties to the construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b83edf2305d7fe3964a1a521bb1b7b98671d1fbae0bb2cfe6aba412aa8676409)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be3889a4d844b9b6da32d644c66b536930767edb6fa42632666eb5850bc4be5c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVehicleMixinProps:
        return typing.cast(CfnVehicleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnVehiclePropsMixin.PeriodicStateTemplateUpdateStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"state_template_update_rate": "stateTemplateUpdateRate"},
    )
    class PeriodicStateTemplateUpdateStrategyProperty:
        def __init__(
            self,
            *,
            state_template_update_rate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVehiclePropsMixin.TimePeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Vehicles associated with the state template will stream telemetry data during a specified time period.

            :param state_template_update_rate: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-vehicle-periodicstatetemplateupdatestrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                periodic_state_template_update_strategy_property = iotfleetwise_mixins.CfnVehiclePropsMixin.PeriodicStateTemplateUpdateStrategyProperty(
                    state_template_update_rate=iotfleetwise_mixins.CfnVehiclePropsMixin.TimePeriodProperty(
                        unit="unit",
                        value=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__755c4ced2edad2d131ded445aa2fdaea25e89692afa6d04ef9362eb307582f41)
                check_type(argname="argument state_template_update_rate", value=state_template_update_rate, expected_type=type_hints["state_template_update_rate"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if state_template_update_rate is not None:
                self._values["state_template_update_rate"] = state_template_update_rate

        @builtins.property
        def state_template_update_rate(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVehiclePropsMixin.TimePeriodProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-vehicle-periodicstatetemplateupdatestrategy.html#cfn-iotfleetwise-vehicle-periodicstatetemplateupdatestrategy-statetemplateupdaterate
            '''
            result = self._values.get("state_template_update_rate")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVehiclePropsMixin.TimePeriodProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PeriodicStateTemplateUpdateStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnVehiclePropsMixin.StateTemplateAssociationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "identifier": "identifier",
            "state_template_update_strategy": "stateTemplateUpdateStrategy",
        },
    )
    class StateTemplateAssociationProperty:
        def __init__(
            self,
            *,
            identifier: typing.Optional[builtins.str] = None,
            state_template_update_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVehiclePropsMixin.StateTemplateUpdateStrategyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The state template associated with a vehicle.

            State templates contain state properties, which are signals that belong to a signal catalog that is synchronized between the AWS IoT FleetWise Edge and the AWS Cloud .
            .. epigraph::

               Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

            :param identifier: The unique ID of the state template.
            :param state_template_update_strategy: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-vehicle-statetemplateassociation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                # on_change: Any
                
                state_template_association_property = iotfleetwise_mixins.CfnVehiclePropsMixin.StateTemplateAssociationProperty(
                    identifier="identifier",
                    state_template_update_strategy=iotfleetwise_mixins.CfnVehiclePropsMixin.StateTemplateUpdateStrategyProperty(
                        on_change=on_change,
                        periodic=iotfleetwise_mixins.CfnVehiclePropsMixin.PeriodicStateTemplateUpdateStrategyProperty(
                            state_template_update_rate=iotfleetwise_mixins.CfnVehiclePropsMixin.TimePeriodProperty(
                                unit="unit",
                                value=123
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2fe7196718f6a44605f1d6d0f4ee78ba90301f7c86f7125a15ec0ce225d542f3)
                check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
                check_type(argname="argument state_template_update_strategy", value=state_template_update_strategy, expected_type=type_hints["state_template_update_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if identifier is not None:
                self._values["identifier"] = identifier
            if state_template_update_strategy is not None:
                self._values["state_template_update_strategy"] = state_template_update_strategy

        @builtins.property
        def identifier(self) -> typing.Optional[builtins.str]:
            '''The unique ID of the state template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-vehicle-statetemplateassociation.html#cfn-iotfleetwise-vehicle-statetemplateassociation-identifier
            '''
            result = self._values.get("identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def state_template_update_strategy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVehiclePropsMixin.StateTemplateUpdateStrategyProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-vehicle-statetemplateassociation.html#cfn-iotfleetwise-vehicle-statetemplateassociation-statetemplateupdatestrategy
            '''
            result = self._values.get("state_template_update_strategy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVehiclePropsMixin.StateTemplateUpdateStrategyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StateTemplateAssociationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnVehiclePropsMixin.StateTemplateUpdateStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"on_change": "onChange", "periodic": "periodic"},
    )
    class StateTemplateUpdateStrategyProperty:
        def __init__(
            self,
            *,
            on_change: typing.Any = None,
            periodic: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVehiclePropsMixin.PeriodicStateTemplateUpdateStrategyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The update strategy for the state template.

            Vehicles associated with the state template can stream telemetry data with either an ``onChange`` or ``periodic`` update strategy.
            .. epigraph::

               Access to certain AWS IoT FleetWise features is currently gated. For more information, see `AWS Region and feature availability <https://docs.aws.amazon.com/iot-fleetwise/latest/developerguide/fleetwise-regions.html>`_ in the *AWS IoT FleetWise Developer Guide* .

            :param on_change: 
            :param periodic: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-vehicle-statetemplateupdatestrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                # on_change: Any
                
                state_template_update_strategy_property = iotfleetwise_mixins.CfnVehiclePropsMixin.StateTemplateUpdateStrategyProperty(
                    on_change=on_change,
                    periodic=iotfleetwise_mixins.CfnVehiclePropsMixin.PeriodicStateTemplateUpdateStrategyProperty(
                        state_template_update_rate=iotfleetwise_mixins.CfnVehiclePropsMixin.TimePeriodProperty(
                            unit="unit",
                            value=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__146d47ff19124d07f3d8fdc3ceaac44e99266f73b60f10945cd7d828a353e198)
                check_type(argname="argument on_change", value=on_change, expected_type=type_hints["on_change"])
                check_type(argname="argument periodic", value=periodic, expected_type=type_hints["periodic"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_change is not None:
                self._values["on_change"] = on_change
            if periodic is not None:
                self._values["periodic"] = periodic

        @builtins.property
        def on_change(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-vehicle-statetemplateupdatestrategy.html#cfn-iotfleetwise-vehicle-statetemplateupdatestrategy-onchange
            '''
            result = self._values.get("on_change")
            return typing.cast(typing.Any, result)

        @builtins.property
        def periodic(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVehiclePropsMixin.PeriodicStateTemplateUpdateStrategyProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-vehicle-statetemplateupdatestrategy.html#cfn-iotfleetwise-vehicle-statetemplateupdatestrategy-periodic
            '''
            result = self._values.get("periodic")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVehiclePropsMixin.PeriodicStateTemplateUpdateStrategyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StateTemplateUpdateStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotfleetwise.mixins.CfnVehiclePropsMixin.TimePeriodProperty",
        jsii_struct_bases=[],
        name_mapping={"unit": "unit", "value": "value"},
    )
    class TimePeriodProperty:
        def __init__(
            self,
            *,
            unit: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The length of time between state template updates.

            :param unit: A unit of time.
            :param value: A number of time units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-vehicle-timeperiod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotfleetwise import mixins as iotfleetwise_mixins
                
                time_period_property = iotfleetwise_mixins.CfnVehiclePropsMixin.TimePeriodProperty(
                    unit="unit",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8bffff72c6f5284212390f83bfee8eef806de3c34e309575d5348318493b1115)
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unit is not None:
                self._values["unit"] = unit
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''A unit of time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-vehicle-timeperiod.html#cfn-iotfleetwise-vehicle-timeperiod-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''A number of time units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotfleetwise-vehicle-timeperiod.html#cfn-iotfleetwise-vehicle-timeperiod-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimePeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnCampaignIotFleetwiseLogs",
    "CfnCampaignLogsMixin",
    "CfnCampaignMixinProps",
    "CfnCampaignPropsMixin",
    "CfnDecoderManifestMixinProps",
    "CfnDecoderManifestPropsMixin",
    "CfnFleetMixinProps",
    "CfnFleetPropsMixin",
    "CfnModelManifestMixinProps",
    "CfnModelManifestPropsMixin",
    "CfnSignalCatalogMixinProps",
    "CfnSignalCatalogPropsMixin",
    "CfnStateTemplateMixinProps",
    "CfnStateTemplatePropsMixin",
    "CfnVehicleIotFleetwiseLogs",
    "CfnVehicleLogsMixin",
    "CfnVehicleMixinProps",
    "CfnVehiclePropsMixin",
]

publication.publish()

def _typecheckingstub__630fec47114c66fbf5f43dad52048cc8e1c197ba952ba7ba924711ffe0b460b3(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512c3d621d8d9c3890261d0dad562241b190570d99d13ad5c1c2465a53a1df98(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd57edef5bc4d1901ec9a5d34ea72bccfdd5d806203dc67418816dff487e7868(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c4d9cffac2f9300d18014c39cef28b00cf3d8ae1c0b3644be9e56476020297(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd58e2e3d7d32f233fed65ac0184e9ee913c86758e2a2b249d9b768546047140(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9986aed3b65eb283281ac9ce9f9c853f8ed770db37b151fa2454a8416cbd6825(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef469060f2a29d712b4d16a2f4a2dcf59a2a4de41d076e9cc4a7c13ac48f8b29(
    *,
    action: typing.Optional[builtins.str] = None,
    collection_scheme: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.CollectionSchemeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    compression: typing.Optional[builtins.str] = None,
    data_destination_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.DataDestinationConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    data_extra_dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_partitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.DataPartitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    diagnostics_mode: typing.Optional[builtins.str] = None,
    expiry_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    post_trigger_collection_duration: typing.Optional[jsii.Number] = None,
    priority: typing.Optional[jsii.Number] = None,
    signal_catalog_arn: typing.Optional[builtins.str] = None,
    signals_to_collect: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.SignalInformationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    signals_to_fetch: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.SignalFetchInformationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    spooling_mode: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29efdcd8395af7f9b54278e8edb3b73730306c5057af1e093e8436fb6a028899(
    props: typing.Union[CfnCampaignMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e23a8d5ac0623715aaf47d042ece0a0e9205eb2bb26f91e338738d6566cb445(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf10d24ef247d923dd5c3606b12b7bc85dfaf02f37f872aa5832755d15ef344e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b660eb8c2290b786c9bb8b2b6509b0fa76546e3d34dd04153af10d8af5cd8e(
    *,
    condition_based_collection_scheme: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.ConditionBasedCollectionSchemeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_based_collection_scheme: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TimeBasedCollectionSchemeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad8e7775f292e4ce1f0fe49769a4ae42901e727983a5dc2a7ec6e470bc4bf28(
    *,
    condition_language_version: typing.Optional[jsii.Number] = None,
    expression: typing.Optional[builtins.str] = None,
    minimum_trigger_interval_ms: typing.Optional[jsii.Number] = None,
    trigger_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d899366ccf1ea4679bc1c55781b9ac6761cb2005c8d9ee66244b4c27978a73(
    *,
    condition_expression: typing.Optional[builtins.str] = None,
    trigger_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e97707447746c3cd40d98aef1cd412bc0775d74db4d40cd46ac2785a92cdbc8(
    *,
    mqtt_topic_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.MqttTopicConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timestream_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TimestreamConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564c891e9b1c0bef0fc7fe315cabd79dcede4a9fbe1dbf46c82c44674ad127e3(
    *,
    id: typing.Optional[builtins.str] = None,
    storage_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.DataPartitionStorageOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    upload_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.DataPartitionUploadOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be44bc980597a32848ecf63d22cbe4aee7e143ed3426333ac0d6e0bc11d797f(
    *,
    maximum_size: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.StorageMaximumSizeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    minimum_time_to_live: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.StorageMinimumTimeToLiveProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7142fda7b830738813a9f50893c67e500ad35281dcdb4bc55fe8f4e6ae771c5(
    *,
    condition_language_version: typing.Optional[jsii.Number] = None,
    expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d04c8e775759659605ff3c19c9fd657f3428d5fa8e09c4570ac2faef8686b1(
    *,
    execution_role_arn: typing.Optional[builtins.str] = None,
    mqtt_topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a9be0620d83d7baedc1e41f05639d0ae280ed4f1fdce57a004a2f7f377f402(
    *,
    bucket_arn: typing.Optional[builtins.str] = None,
    data_format: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    storage_compression_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7114651e76d4a14d71ec9b95f7db89a2bb4829c3f71218f6fd5960ac8ca1d0d(
    *,
    condition_based: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.ConditionBasedSignalFetchConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_based: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TimeBasedSignalFetchConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a7d2eef2c678729d44751c71b1fa1a9a0fc6c3e3c418ad43a016c9b6116691(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition_language_version: typing.Optional[jsii.Number] = None,
    fully_qualified_name: typing.Optional[builtins.str] = None,
    signal_fetch_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.SignalFetchConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee1e91d30cb5be643418d21c2022f87159fe57ff4f64c27c9d4e31b087e0205(
    *,
    data_partition_id: typing.Optional[builtins.str] = None,
    max_sample_count: typing.Optional[jsii.Number] = None,
    minimum_sampling_interval_ms: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79e2fa3d530de8780a20dce6c314533e78c694bc690f52718ebed80c0f3c669(
    *,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1145dde21b1ec271c3636fa1da82a3bb0ace0797f08b7fec83735a72807dfac9(
    *,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1114a59d094dcf524034b3499ac4696d76dc0eed60fcb62561d9621704906d(
    *,
    period_ms: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293f10767265ecdf5a9adc081b31e6a97f708b509a8225ba6f2153ef5b6db5b3(
    *,
    execution_frequency_ms: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff1003f2881835162963e1e870e8ef2dad7594bbd02e895954ea7ad766ab2f8(
    *,
    execution_role_arn: typing.Optional[builtins.str] = None,
    timestream_table_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce34c01882b69d4b1a1163eba55583bd2a0ebb209e3678aab4394c032d67b4e(
    *,
    default_for_unmapped_signals: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    model_manifest_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_interfaces: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDecoderManifestPropsMixin.NetworkInterfacesItemsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    signal_decoders: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDecoderManifestPropsMixin.SignalDecodersItemsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8978afa7100af71765088f653764144ddf042def34db82bdd9a6df497dcd3e7(
    props: typing.Union[CfnDecoderManifestMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e57f1564150fbc6704d35040b8e3b52a65e4a24cd49b0fe3bafedbbc53b103(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f32852211e693f7a7285e604323fdcc4906fbffb29cf2751a2a3e51ee94d675(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c657b9093371550a24cdb14c4f440b71af3b4fae173ff93a9fa199e2485b37(
    *,
    name: typing.Optional[builtins.str] = None,
    protocol_name: typing.Optional[builtins.str] = None,
    protocol_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4559b5e688b36adebe33bc2af42b896252b7f0d8f92a21e53dd6a5e167f5ba41(
    *,
    can_interface: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDecoderManifestPropsMixin.CanInterfaceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    interface_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a7033b3e7ceb75648bb4c58383b0c6ea8f30eebff16a0b809f87293d216959(
    *,
    can_signal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDecoderManifestPropsMixin.CanSignalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fully_qualified_name: typing.Optional[builtins.str] = None,
    interface_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abdfb351664115cc83110de47fe13f6f4a39ca8afd9cd962bd04b4c6cf53208f(
    *,
    factor: typing.Optional[builtins.str] = None,
    is_big_endian: typing.Optional[builtins.str] = None,
    is_signed: typing.Optional[builtins.str] = None,
    length: typing.Optional[builtins.str] = None,
    message_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    offset: typing.Optional[builtins.str] = None,
    signal_value_type: typing.Optional[builtins.str] = None,
    start_bit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cacc524fd8219ca210fdd0c7bb66bf371d867b6f4705fa2ddd710b7d167292dd(
    *,
    can_interface: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDecoderManifestPropsMixin.CanInterfaceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    interface_id: typing.Optional[builtins.str] = None,
    obd_interface: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDecoderManifestPropsMixin.ObdInterfaceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871053b314f74d7eb35d96a21d2344647fc16bcfebae44e0086e4b851d8e00e9(
    *,
    dtc_request_interval_seconds: typing.Optional[builtins.str] = None,
    has_transmission_ecu: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    obd_standard: typing.Optional[builtins.str] = None,
    pid_request_interval_seconds: typing.Optional[builtins.str] = None,
    request_message_id: typing.Optional[builtins.str] = None,
    use_extended_ids: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6a269fe3cdffdccfb5ffb6758dc07e54dbed6743a1ebbcf6bf29f0004884aa(
    *,
    interface_id: typing.Optional[builtins.str] = None,
    obd_interface: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDecoderManifestPropsMixin.ObdInterfaceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2997b0a79061399d5b1a4f68ad18ad6e6a2fc1fb25150ae698b10e930f99c856(
    *,
    fully_qualified_name: typing.Optional[builtins.str] = None,
    interface_id: typing.Optional[builtins.str] = None,
    obd_signal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDecoderManifestPropsMixin.ObdSignalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ce2b874d934827107656ca59c7d9c5fdf461be5712ea3342af31b6b477ffd8(
    *,
    bit_mask_length: typing.Optional[builtins.str] = None,
    bit_right_shift: typing.Optional[builtins.str] = None,
    byte_length: typing.Optional[builtins.str] = None,
    is_signed: typing.Optional[typing.Union[builtins.str, builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    offset: typing.Optional[builtins.str] = None,
    pid: typing.Optional[builtins.str] = None,
    pid_response_length: typing.Optional[builtins.str] = None,
    scaling: typing.Optional[builtins.str] = None,
    service_mode: typing.Optional[builtins.str] = None,
    signal_value_type: typing.Optional[builtins.str] = None,
    start_byte: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0fd2753092e780334321e82d1933ab3831e1f8ec374bc110b7a8b37ac72855(
    *,
    can_signal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDecoderManifestPropsMixin.CanSignalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fully_qualified_name: typing.Optional[builtins.str] = None,
    interface_id: typing.Optional[builtins.str] = None,
    obd_signal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDecoderManifestPropsMixin.ObdSignalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd6140175f0378cdc58e38d32a8cddd7c33edaaf3d58a19a079f1b67d68350da(
    *,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    signal_catalog_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adbd7909610650249a1f4c9459faf6ed4ff8d376507f7b30dc04ef7b9381ba1b(
    props: typing.Union[CfnFleetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3f71a4b144c85c468e8743b4824a6d1e48df1899590b351b5daeb27d4f4852(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a55395afa1fda3665709ee59e4f317871bae808c796a33113e0e4a95df44442(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b96e37a1aa4b5adadd82e431bd60c8b29259f7d5b84b0e4896300c780f825d6(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
    signal_catalog_arn: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8d8e2a85706b3a1bdaad68cb632c216fcd8ecda145baad4ea95ffad46643e8(
    props: typing.Union[CfnModelManifestMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ac4b988214ada91f89066dc6da284a4dcadb220dd614d7fa709b3c77cf61f7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7b830df0b4877c43f6a0fcdc0d528cfd77bdaa3a4ee60e26e3b2163bb48fbc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1d3177697effcaa5ca0f2b365c920b0e77bdd774b5f3304fb26ed6ee99a325(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    node_counts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSignalCatalogPropsMixin.NodeCountsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    nodes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSignalCatalogPropsMixin.NodeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a9d38fff8cb50ff987cd6b20fa98d077e9da851d86c09d48ac3cc95c3d0138(
    props: typing.Union[CfnSignalCatalogMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf30f6bde7fecfd42d506876157ecc5446a8c2ce352087620130de4c2e62ec7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8396febc416257057eca60de05c4e8ae59a05f10dae3e21fc3f15fa4cdab780e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ac5f67864be9e0ec3352628b124e3e1236b0cd5f619163cac0f70358cc4105(
    *,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    assigned_value: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    fully_qualified_name: typing.Optional[builtins.str] = None,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a3a879fd7620450b99101d9bcd99402191aaa77e5c086a0f8884af6cc13faf(
    *,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    assigned_value: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    default_value: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    fully_qualified_name: typing.Optional[builtins.str] = None,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae21e9c3913406e8c61fc73dd688d8499a153d9d6a310245be02dba671df93e4(
    *,
    description: typing.Optional[builtins.str] = None,
    fully_qualified_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6dca2442bca2e00afcf0a469ee44a48165f295e1e2c092afb7e2db62068e28(
    *,
    total_actuators: typing.Optional[jsii.Number] = None,
    total_attributes: typing.Optional[jsii.Number] = None,
    total_branches: typing.Optional[jsii.Number] = None,
    total_nodes: typing.Optional[jsii.Number] = None,
    total_sensors: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92eb72e3c1a7ffe8a3cbfe3a057b02562b0b523a557b14c6af20dd9145024c32(
    *,
    actuator: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSignalCatalogPropsMixin.ActuatorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    attribute: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSignalCatalogPropsMixin.AttributeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    branch: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSignalCatalogPropsMixin.BranchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sensor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSignalCatalogPropsMixin.SensorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69e34f0675f3f89a1a5bf4dd973ea8e00e1f86e37c955222df92c6de7e01d5a(
    *,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    fully_qualified_name: typing.Optional[builtins.str] = None,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edbe3aa4a32b325e293b09d271eb27024f5e1960caad4f11de599885ebfce3d4(
    *,
    data_extra_dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    metadata_extra_dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    signal_catalog_arn: typing.Optional[builtins.str] = None,
    state_template_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0400670c45304580f501248de8ee73b014823b4cfe4f8e5b36e723176d3e40c9(
    props: typing.Union[CfnStateTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f56f4aa21cd642ecd0052d734a6477182b5b026dd7dedc486f63c089af9cdd7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83809e8cd0ada0c003761ab808b900dae8a94546634d6fe22e610403e02a93fd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415eb6423b97a78ad45a0c91f6b4238eae064aa3b9f95589e4df27579a7665aa(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886578f717376bbc9957d64d49206ff1ae88f7842c0223bba0a9d44976576aef(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643fcff8ccf9bba92e15cc0ec69726367e955537fb7636c4605c1481a3893516(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c7d2d659078d6d2082daf528cb24cea57c05cc04178356157d251e4d069a81d(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5cae60ee244e0f88ad43344015b8edaae877e40b8ec2796ea582a2200e6484(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f3d4b2e6684a66ad66d74c9e086a3d530e41217891fde6d421b615f04824b2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9a992cadc365853b127609fa123d7427ac5ab074a5d1655c0e11cb6adc2c34(
    *,
    association_behavior: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    decoder_manifest_arn: typing.Optional[builtins.str] = None,
    model_manifest_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    state_templates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVehiclePropsMixin.StateTemplateAssociationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9657c802c2b2ba3ee5c5457dc446a73bf08e8d888d526dd400d0895d1c436b83(
    props: typing.Union[CfnVehicleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83edf2305d7fe3964a1a521bb1b7b98671d1fbae0bb2cfe6aba412aa8676409(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3889a4d844b9b6da32d644c66b536930767edb6fa42632666eb5850bc4be5c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755c4ced2edad2d131ded445aa2fdaea25e89692afa6d04ef9362eb307582f41(
    *,
    state_template_update_rate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVehiclePropsMixin.TimePeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe7196718f6a44605f1d6d0f4ee78ba90301f7c86f7125a15ec0ce225d542f3(
    *,
    identifier: typing.Optional[builtins.str] = None,
    state_template_update_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVehiclePropsMixin.StateTemplateUpdateStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146d47ff19124d07f3d8fdc3ceaac44e99266f73b60f10945cd7d828a353e198(
    *,
    on_change: typing.Any = None,
    periodic: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVehiclePropsMixin.PeriodicStateTemplateUpdateStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bffff72c6f5284212390f83bfee8eef806de3c34e309575d5348318493b1115(
    *,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
