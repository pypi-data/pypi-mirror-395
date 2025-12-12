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
import constructs as _constructs_77d1e7e8
from ...core import IMixin as _IMixin_11e4b965, Mixin as _Mixin_a69446c0
from ...mixins import (
    CfnPropertyMixinOptions as _CfnPropertyMixinOptions_9cbff649,
    PropertyMergeStrategy as _PropertyMergeStrategy_49c157e8,
)


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "amazon_open_search_serverless_destination_configuration": "amazonOpenSearchServerlessDestinationConfiguration",
        "amazonopensearchservice_destination_configuration": "amazonopensearchserviceDestinationConfiguration",
        "database_source_configuration": "databaseSourceConfiguration",
        "delivery_stream_encryption_configuration_input": "deliveryStreamEncryptionConfigurationInput",
        "delivery_stream_name": "deliveryStreamName",
        "delivery_stream_type": "deliveryStreamType",
        "direct_put_source_configuration": "directPutSourceConfiguration",
        "elasticsearch_destination_configuration": "elasticsearchDestinationConfiguration",
        "extended_s3_destination_configuration": "extendedS3DestinationConfiguration",
        "http_endpoint_destination_configuration": "httpEndpointDestinationConfiguration",
        "iceberg_destination_configuration": "icebergDestinationConfiguration",
        "kinesis_stream_source_configuration": "kinesisStreamSourceConfiguration",
        "msk_source_configuration": "mskSourceConfiguration",
        "redshift_destination_configuration": "redshiftDestinationConfiguration",
        "s3_destination_configuration": "s3DestinationConfiguration",
        "snowflake_destination_configuration": "snowflakeDestinationConfiguration",
        "splunk_destination_configuration": "splunkDestinationConfiguration",
        "tags": "tags",
    },
)
class CfnDeliveryStreamMixinProps:
    def __init__(
        self,
        *,
        amazon_open_search_serverless_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        amazonopensearchservice_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.AmazonopensearchserviceDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        database_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.DatabaseSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        delivery_stream_encryption_configuration_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.DeliveryStreamEncryptionConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        delivery_stream_name: typing.Optional[builtins.str] = None,
        delivery_stream_type: typing.Optional[builtins.str] = None,
        direct_put_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.DirectPutSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        elasticsearch_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ElasticsearchDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        extended_s3_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ExtendedS3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        http_endpoint_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.HttpEndpointDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        iceberg_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.IcebergDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kinesis_stream_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.KinesisStreamSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        msk_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.MSKSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        redshift_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.RedshiftDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        s3_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        snowflake_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SnowflakeDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        splunk_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SplunkDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDeliveryStreamPropsMixin.

        :param amazon_open_search_serverless_destination_configuration: Describes the configuration of a destination in the Serverless offering for Amazon OpenSearch Service.
        :param amazonopensearchservice_destination_configuration: The destination in Amazon OpenSearch Service. You can specify only one destination.
        :param database_source_configuration: The top level object for configuring streams with database as a source. Amazon Data Firehose is in preview release and is subject to change.
        :param delivery_stream_encryption_configuration_input: Specifies the type and Amazon Resource Name (ARN) of the CMK to use for Server-Side Encryption (SSE).
        :param delivery_stream_name: The name of the Firehose stream.
        :param delivery_stream_type: The Firehose stream type. This can be one of the following values:. - ``DirectPut`` : Provider applications access the Firehose stream directly. - ``KinesisStreamAsSource`` : The Firehose stream uses a Kinesis data stream as a source.
        :param direct_put_source_configuration: The structure that configures parameters such as ``ThroughputHintInMBs`` for a stream configured with Direct PUT as a source.
        :param elasticsearch_destination_configuration: An Amazon ES destination for the delivery stream. Conditional. You must specify only one destination configuration. If you change the delivery stream destination from an Amazon ES destination to an Amazon S3 or Amazon Redshift destination, update requires `some interruptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt>`_ .
        :param extended_s3_destination_configuration: An Amazon S3 destination for the delivery stream. Conditional. You must specify only one destination configuration. If you change the delivery stream destination from an Amazon Extended S3 destination to an Amazon ES destination, update requires `some interruptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt>`_ .
        :param http_endpoint_destination_configuration: Enables configuring Kinesis Firehose to deliver data to any HTTP endpoint destination. You can specify only one destination.
        :param iceberg_destination_configuration: Specifies the destination configure settings for Apache Iceberg Table.
        :param kinesis_stream_source_configuration: When a Kinesis stream is used as the source for the delivery stream, a `KinesisStreamSourceConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration.html>`_ containing the Kinesis stream ARN and the role ARN for the source stream.
        :param msk_source_configuration: The configuration for the Amazon MSK cluster to be used as the source for a delivery stream.
        :param redshift_destination_configuration: An Amazon Redshift destination for the delivery stream. Conditional. You must specify only one destination configuration. If you change the delivery stream destination from an Amazon Redshift destination to an Amazon ES destination, update requires `some interruptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt>`_ .
        :param s3_destination_configuration: The ``S3DestinationConfiguration`` property type specifies an Amazon Simple Storage Service (Amazon S3) destination to which Amazon Kinesis Data Firehose (Kinesis Data Firehose) delivers data. Conditional. You must specify only one destination configuration. If you change the delivery stream destination from an Amazon S3 destination to an Amazon ES destination, update requires `some interruptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt>`_ .
        :param snowflake_destination_configuration: Configure Snowflake destination.
        :param splunk_destination_configuration: The configuration of a destination in Splunk for the delivery stream.
        :param tags: A set of tags to assign to the Firehose stream. A tag is a key-value pair that you can define and assign to AWS resources. Tags are metadata. For example, you can add friendly names and descriptions or other types of information that can help you distinguish the Firehose stream. For more information about tags, see `Using Cost Allocation Tags <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>`_ in the AWS Billing and Cost Management User Guide. You can specify up to 50 tags when creating a Firehose stream. If you specify tags in the ``CreateDeliveryStream`` action, Amazon Data Firehose performs an additional authorization on the ``firehose:TagDeliveryStream`` action to verify if users have permissions to create tags. If you do not provide this permission, requests to create new Firehose streams with IAM resource tags will fail with an ``AccessDeniedException`` such as following. *AccessDeniedException* User: arn:aws:sts::x:assumed-role/x/x is not authorized to perform: firehose:TagDeliveryStream on resource: arn:aws:firehose:us-east-1:x:deliverystream/x with an explicit deny in an identity-based policy. For an example IAM policy, see `Tag example. <https://docs.aws.amazon.com/firehose/latest/APIReference/API_CreateDeliveryStream.html#API_CreateDeliveryStream_Examples>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html
        :exampleMetadata: fixture=_generated

        Example::

            
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c0d24ea05685a9b99a2ef6fc106d75e6d53124454b910e42658f04d8979294)
            check_type(argname="argument amazon_open_search_serverless_destination_configuration", value=amazon_open_search_serverless_destination_configuration, expected_type=type_hints["amazon_open_search_serverless_destination_configuration"])
            check_type(argname="argument amazonopensearchservice_destination_configuration", value=amazonopensearchservice_destination_configuration, expected_type=type_hints["amazonopensearchservice_destination_configuration"])
            check_type(argname="argument database_source_configuration", value=database_source_configuration, expected_type=type_hints["database_source_configuration"])
            check_type(argname="argument delivery_stream_encryption_configuration_input", value=delivery_stream_encryption_configuration_input, expected_type=type_hints["delivery_stream_encryption_configuration_input"])
            check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
            check_type(argname="argument delivery_stream_type", value=delivery_stream_type, expected_type=type_hints["delivery_stream_type"])
            check_type(argname="argument direct_put_source_configuration", value=direct_put_source_configuration, expected_type=type_hints["direct_put_source_configuration"])
            check_type(argname="argument elasticsearch_destination_configuration", value=elasticsearch_destination_configuration, expected_type=type_hints["elasticsearch_destination_configuration"])
            check_type(argname="argument extended_s3_destination_configuration", value=extended_s3_destination_configuration, expected_type=type_hints["extended_s3_destination_configuration"])
            check_type(argname="argument http_endpoint_destination_configuration", value=http_endpoint_destination_configuration, expected_type=type_hints["http_endpoint_destination_configuration"])
            check_type(argname="argument iceberg_destination_configuration", value=iceberg_destination_configuration, expected_type=type_hints["iceberg_destination_configuration"])
            check_type(argname="argument kinesis_stream_source_configuration", value=kinesis_stream_source_configuration, expected_type=type_hints["kinesis_stream_source_configuration"])
            check_type(argname="argument msk_source_configuration", value=msk_source_configuration, expected_type=type_hints["msk_source_configuration"])
            check_type(argname="argument redshift_destination_configuration", value=redshift_destination_configuration, expected_type=type_hints["redshift_destination_configuration"])
            check_type(argname="argument s3_destination_configuration", value=s3_destination_configuration, expected_type=type_hints["s3_destination_configuration"])
            check_type(argname="argument snowflake_destination_configuration", value=snowflake_destination_configuration, expected_type=type_hints["snowflake_destination_configuration"])
            check_type(argname="argument splunk_destination_configuration", value=splunk_destination_configuration, expected_type=type_hints["splunk_destination_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amazon_open_search_serverless_destination_configuration is not None:
            self._values["amazon_open_search_serverless_destination_configuration"] = amazon_open_search_serverless_destination_configuration
        if amazonopensearchservice_destination_configuration is not None:
            self._values["amazonopensearchservice_destination_configuration"] = amazonopensearchservice_destination_configuration
        if database_source_configuration is not None:
            self._values["database_source_configuration"] = database_source_configuration
        if delivery_stream_encryption_configuration_input is not None:
            self._values["delivery_stream_encryption_configuration_input"] = delivery_stream_encryption_configuration_input
        if delivery_stream_name is not None:
            self._values["delivery_stream_name"] = delivery_stream_name
        if delivery_stream_type is not None:
            self._values["delivery_stream_type"] = delivery_stream_type
        if direct_put_source_configuration is not None:
            self._values["direct_put_source_configuration"] = direct_put_source_configuration
        if elasticsearch_destination_configuration is not None:
            self._values["elasticsearch_destination_configuration"] = elasticsearch_destination_configuration
        if extended_s3_destination_configuration is not None:
            self._values["extended_s3_destination_configuration"] = extended_s3_destination_configuration
        if http_endpoint_destination_configuration is not None:
            self._values["http_endpoint_destination_configuration"] = http_endpoint_destination_configuration
        if iceberg_destination_configuration is not None:
            self._values["iceberg_destination_configuration"] = iceberg_destination_configuration
        if kinesis_stream_source_configuration is not None:
            self._values["kinesis_stream_source_configuration"] = kinesis_stream_source_configuration
        if msk_source_configuration is not None:
            self._values["msk_source_configuration"] = msk_source_configuration
        if redshift_destination_configuration is not None:
            self._values["redshift_destination_configuration"] = redshift_destination_configuration
        if s3_destination_configuration is not None:
            self._values["s3_destination_configuration"] = s3_destination_configuration
        if snowflake_destination_configuration is not None:
            self._values["snowflake_destination_configuration"] = snowflake_destination_configuration
        if splunk_destination_configuration is not None:
            self._values["splunk_destination_configuration"] = splunk_destination_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def amazon_open_search_serverless_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessDestinationConfigurationProperty"]]:
        '''Describes the configuration of a destination in the Serverless offering for Amazon OpenSearch Service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration
        '''
        result = self._values.get("amazon_open_search_serverless_destination_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessDestinationConfigurationProperty"]], result)

    @builtins.property
    def amazonopensearchservice_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.AmazonopensearchserviceDestinationConfigurationProperty"]]:
        '''The destination in Amazon OpenSearch Service.

        You can specify only one destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration
        '''
        result = self._values.get("amazonopensearchservice_destination_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.AmazonopensearchserviceDestinationConfigurationProperty"]], result)

    @builtins.property
    def database_source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DatabaseSourceConfigurationProperty"]]:
        '''The top level object for configuring streams with database as a source.

        Amazon Data Firehose is in preview release and is subject to change.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-databasesourceconfiguration
        '''
        result = self._values.get("database_source_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DatabaseSourceConfigurationProperty"]], result)

    @builtins.property
    def delivery_stream_encryption_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DeliveryStreamEncryptionConfigurationInputProperty"]]:
        '''Specifies the type and Amazon Resource Name (ARN) of the CMK to use for Server-Side Encryption (SSE).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-deliverystreamencryptionconfigurationinput
        '''
        result = self._values.get("delivery_stream_encryption_configuration_input")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DeliveryStreamEncryptionConfigurationInputProperty"]], result)

    @builtins.property
    def delivery_stream_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Firehose stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-deliverystreamname
        '''
        result = self._values.get("delivery_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delivery_stream_type(self) -> typing.Optional[builtins.str]:
        '''The Firehose stream type. This can be one of the following values:.

        - ``DirectPut`` : Provider applications access the Firehose stream directly.
        - ``KinesisStreamAsSource`` : The Firehose stream uses a Kinesis data stream as a source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-deliverystreamtype
        '''
        result = self._values.get("delivery_stream_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def direct_put_source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DirectPutSourceConfigurationProperty"]]:
        '''The structure that configures parameters such as ``ThroughputHintInMBs`` for a stream configured with Direct PUT as a source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-directputsourceconfiguration
        '''
        result = self._values.get("direct_put_source_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DirectPutSourceConfigurationProperty"]], result)

    @builtins.property
    def elasticsearch_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ElasticsearchDestinationConfigurationProperty"]]:
        '''An Amazon ES destination for the delivery stream.

        Conditional. You must specify only one destination configuration.

        If you change the delivery stream destination from an Amazon ES destination to an Amazon S3 or Amazon Redshift destination, update requires `some interruptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration
        '''
        result = self._values.get("elasticsearch_destination_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ElasticsearchDestinationConfigurationProperty"]], result)

    @builtins.property
    def extended_s3_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ExtendedS3DestinationConfigurationProperty"]]:
        '''An Amazon S3 destination for the delivery stream.

        Conditional. You must specify only one destination configuration.

        If you change the delivery stream destination from an Amazon Extended S3 destination to an Amazon ES destination, update requires `some interruptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration
        '''
        result = self._values.get("extended_s3_destination_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ExtendedS3DestinationConfigurationProperty"]], result)

    @builtins.property
    def http_endpoint_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.HttpEndpointDestinationConfigurationProperty"]]:
        '''Enables configuring Kinesis Firehose to deliver data to any HTTP endpoint destination.

        You can specify only one destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration
        '''
        result = self._values.get("http_endpoint_destination_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.HttpEndpointDestinationConfigurationProperty"]], result)

    @builtins.property
    def iceberg_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.IcebergDestinationConfigurationProperty"]]:
        '''Specifies the destination configure settings for Apache Iceberg Table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-icebergdestinationconfiguration
        '''
        result = self._values.get("iceberg_destination_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.IcebergDestinationConfigurationProperty"]], result)

    @builtins.property
    def kinesis_stream_source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.KinesisStreamSourceConfigurationProperty"]]:
        '''When a Kinesis stream is used as the source for the delivery stream, a `KinesisStreamSourceConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration.html>`_ containing the Kinesis stream ARN and the role ARN for the source stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration
        '''
        result = self._values.get("kinesis_stream_source_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.KinesisStreamSourceConfigurationProperty"]], result)

    @builtins.property
    def msk_source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.MSKSourceConfigurationProperty"]]:
        '''The configuration for the Amazon MSK cluster to be used as the source for a delivery stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-msksourceconfiguration
        '''
        result = self._values.get("msk_source_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.MSKSourceConfigurationProperty"]], result)

    @builtins.property
    def redshift_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.RedshiftDestinationConfigurationProperty"]]:
        '''An Amazon Redshift destination for the delivery stream.

        Conditional. You must specify only one destination configuration.

        If you change the delivery stream destination from an Amazon Redshift destination to an Amazon ES destination, update requires `some interruptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration
        '''
        result = self._values.get("redshift_destination_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.RedshiftDestinationConfigurationProperty"]], result)

    @builtins.property
    def s3_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]]:
        '''The ``S3DestinationConfiguration`` property type specifies an Amazon Simple Storage Service (Amazon S3) destination to which Amazon Kinesis Data Firehose (Kinesis Data Firehose) delivers data.

        Conditional. You must specify only one destination configuration.

        If you change the delivery stream destination from an Amazon S3 destination to an Amazon ES destination, update requires `some interruptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration
        '''
        result = self._values.get("s3_destination_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]], result)

    @builtins.property
    def snowflake_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SnowflakeDestinationConfigurationProperty"]]:
        '''Configure Snowflake destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration
        '''
        result = self._values.get("snowflake_destination_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SnowflakeDestinationConfigurationProperty"]], result)

    @builtins.property
    def splunk_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SplunkDestinationConfigurationProperty"]]:
        '''The configuration of a destination in Splunk for the delivery stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration
        '''
        result = self._values.get("splunk_destination_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SplunkDestinationConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A set of tags to assign to the Firehose stream.

        A tag is a key-value pair that you can define and assign to AWS resources. Tags are metadata. For example, you can add friendly names and descriptions or other types of information that can help you distinguish the Firehose stream. For more information about tags, see `Using Cost Allocation Tags <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>`_ in the AWS Billing and Cost Management User Guide.

        You can specify up to 50 tags when creating a Firehose stream.

        If you specify tags in the ``CreateDeliveryStream`` action, Amazon Data Firehose performs an additional authorization on the ``firehose:TagDeliveryStream`` action to verify if users have permissions to create tags. If you do not provide this permission, requests to create new Firehose streams with IAM resource tags will fail with an ``AccessDeniedException`` such as following.

        *AccessDeniedException*

        User: arn:aws:sts::x:assumed-role/x/x is not authorized to perform: firehose:TagDeliveryStream on resource: arn:aws:firehose:us-east-1:x:deliverystream/x with an explicit deny in an identity-based policy.

        For an example IAM policy, see `Tag example. <https://docs.aws.amazon.com/firehose/latest/APIReference/API_CreateDeliveryStream.html#API_CreateDeliveryStream_Examples>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeliveryStreamMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDeliveryStreamPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin",
):
    '''The ``AWS::KinesisFirehose::DeliveryStream`` resource specifies an Amazon Kinesis Data Firehose (Kinesis Data Firehose) delivery stream that delivers real-time streaming data to an Amazon Simple Storage Service (Amazon S3), Amazon Redshift, or Amazon Elasticsearch Service (Amazon ES) destination.

    For more information, see `Creating an Amazon Kinesis Data Firehose Delivery Stream <https://docs.aws.amazon.com/firehose/latest/dev/basic-create.html>`_ in the *Amazon Kinesis Data Firehose Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html
    :cloudformationResource: AWS::KinesisFirehose::DeliveryStream
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        
    '''

    def __init__(
        self,
        props: typing.Union[CfnDeliveryStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::KinesisFirehose::DeliveryStream``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__072742e9c2f67afb5cd43f5cc52a2a4dd22f37af49634ebc1b8ed5a6e520830e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9b9f940583cf5aac1ecd5a66026c8c04bcff9587ba5ccd52b780e5b673ab6c3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c92079f2c941668202bdcb18075579c349b3d6d82b26e21a4f22aef1d7f89203)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDeliveryStreamMixinProps:
        return typing.cast(CfnDeliveryStreamMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessBufferingHintsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "interval_in_seconds": "intervalInSeconds",
            "size_in_m_bs": "sizeInMBs",
        },
    )
    class AmazonOpenSearchServerlessBufferingHintsProperty:
        def __init__(
            self,
            *,
            interval_in_seconds: typing.Optional[jsii.Number] = None,
            size_in_m_bs: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the buffering to perform before delivering data to the Serverless offering for Amazon OpenSearch Service destination.

            :param interval_in_seconds: Buffer incoming data for the specified period of time, in seconds, before delivering it to the destination. The default value is 300 (5 minutes).
            :param size_in_m_bs: Buffer incoming data to the specified size, in MBs, before delivering it to the destination. The default value is 5. We recommend setting this parameter to a value greater than the amount of data you typically ingest into the Firehose stream in 10 seconds. For example, if you typically ingest data at 1 MB/sec, the value should be 10 MB or higher.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessbufferinghints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                amazon_open_search_serverless_buffering_hints_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessBufferingHintsProperty(
                    interval_in_seconds=123,
                    size_in_mBs=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__558756424ad3de0a7d8dc47092a36c08349a04f2f4ba97d2b7be735faaa4ae51)
                check_type(argname="argument interval_in_seconds", value=interval_in_seconds, expected_type=type_hints["interval_in_seconds"])
                check_type(argname="argument size_in_m_bs", value=size_in_m_bs, expected_type=type_hints["size_in_m_bs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if interval_in_seconds is not None:
                self._values["interval_in_seconds"] = interval_in_seconds
            if size_in_m_bs is not None:
                self._values["size_in_m_bs"] = size_in_m_bs

        @builtins.property
        def interval_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''Buffer incoming data for the specified period of time, in seconds, before delivering it to the destination.

            The default value is 300 (5 minutes).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessbufferinghints.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserverlessbufferinghints-intervalinseconds
            '''
            result = self._values.get("interval_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def size_in_m_bs(self) -> typing.Optional[jsii.Number]:
            '''Buffer incoming data to the specified size, in MBs, before delivering it to the destination.

            The default value is 5.

            We recommend setting this parameter to a value greater than the amount of data you typically ingest into the Firehose stream in 10 seconds. For example, if you typically ingest data at 1 MB/sec, the value should be 10 MB or higher.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessbufferinghints.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserverlessbufferinghints-sizeinmbs
            '''
            result = self._values.get("size_in_m_bs")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmazonOpenSearchServerlessBufferingHintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "buffering_hints": "bufferingHints",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "collection_endpoint": "collectionEndpoint",
            "index_name": "indexName",
            "processing_configuration": "processingConfiguration",
            "retry_options": "retryOptions",
            "role_arn": "roleArn",
            "s3_backup_mode": "s3BackupMode",
            "s3_configuration": "s3Configuration",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class AmazonOpenSearchServerlessDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessBufferingHintsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            collection_endpoint: typing.Optional[builtins.str] = None,
            index_name: typing.Optional[builtins.str] = None,
            processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessRetryOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            s3_backup_mode: typing.Optional[builtins.str] = None,
            s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the configuration of a destination in the Serverless offering for Amazon OpenSearch Service.

            :param buffering_hints: The buffering options. If no value is specified, the default values for AmazonopensearchserviceBufferingHints are used.
            :param cloud_watch_logging_options: 
            :param collection_endpoint: The endpoint to use when communicating with the collection in the Serverless offering for Amazon OpenSearch Service.
            :param index_name: The Serverless offering for Amazon OpenSearch Service index name.
            :param processing_configuration: 
            :param retry_options: The retry behavior in case Firehose is unable to deliver documents to the Serverless offering for Amazon OpenSearch Service. The default value is 300 (5 minutes).
            :param role_arn: The Amazon Resource Name (ARN) of the IAM role to be assumed by Firehose for calling the Serverless offering for Amazon OpenSearch Service Configuration API and for indexing documents.
            :param s3_backup_mode: Defines how documents should be delivered to Amazon S3. When it is set to FailedDocumentsOnly, Firehose writes any documents that could not be indexed to the configured Amazon S3 destination, with AmazonOpenSearchService-failed/ appended to the key prefix. When set to AllDocuments, Firehose delivers all incoming records to Amazon S3, and also writes failed documents with AmazonOpenSearchService-failed/ appended to the prefix.
            :param s3_configuration: 
            :param vpc_configuration: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                amazon_open_search_serverless_destination_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessDestinationConfigurationProperty(
                    buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessBufferingHintsProperty(
                        interval_in_seconds=123,
                        size_in_mBs=123
                    ),
                    cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                        enabled=False,
                        log_group_name="logGroupName",
                        log_stream_name="logStreamName"
                    ),
                    collection_endpoint="collectionEndpoint",
                    index_name="indexName",
                    processing_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty(
                        enabled=False,
                        processors=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorProperty(
                            parameters=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorParameterProperty(
                                parameter_name="parameterName",
                                parameter_value="parameterValue"
                            )],
                            type="type"
                        )]
                    ),
                    retry_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessRetryOptionsProperty(
                        duration_in_seconds=123
                    ),
                    role_arn="roleArn",
                    s3_backup_mode="s3BackupMode",
                    s3_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty(
                        bucket_arn="bucketArn",
                        buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                            interval_in_seconds=123,
                            size_in_mBs=123
                        ),
                        cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                            enabled=False,
                            log_group_name="logGroupName",
                            log_stream_name="logStreamName"
                        ),
                        compression_format="compressionFormat",
                        encryption_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty(
                            kms_encryption_config=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty(
                                awskms_key_arn="awskmsKeyArn"
                            ),
                            no_encryption_config="noEncryptionConfig"
                        ),
                        error_output_prefix="errorOutputPrefix",
                        prefix="prefix",
                        role_arn="roleArn"
                    ),
                    vpc_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.VpcConfigurationProperty(
                        role_arn="roleArn",
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__386908b8d9789dbdfb1c2e7ec419619a60b896ed27520f6082030f29101c88bb)
                check_type(argname="argument buffering_hints", value=buffering_hints, expected_type=type_hints["buffering_hints"])
                check_type(argname="argument cloud_watch_logging_options", value=cloud_watch_logging_options, expected_type=type_hints["cloud_watch_logging_options"])
                check_type(argname="argument collection_endpoint", value=collection_endpoint, expected_type=type_hints["collection_endpoint"])
                check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
                check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
                check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if buffering_hints is not None:
                self._values["buffering_hints"] = buffering_hints
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if collection_endpoint is not None:
                self._values["collection_endpoint"] = collection_endpoint
            if index_name is not None:
                self._values["index_name"] = index_name
            if processing_configuration is not None:
                self._values["processing_configuration"] = processing_configuration
            if retry_options is not None:
                self._values["retry_options"] = retry_options
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if s3_backup_mode is not None:
                self._values["s3_backup_mode"] = s3_backup_mode
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def buffering_hints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessBufferingHintsProperty"]]:
            '''The buffering options.

            If no value is specified, the default values for AmazonopensearchserviceBufferingHints are used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration-bufferinghints
            '''
            result = self._values.get("buffering_hints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessBufferingHintsProperty"]], result)

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration-cloudwatchloggingoptions
            '''
            result = self._values.get("cloud_watch_logging_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]], result)

        @builtins.property
        def collection_endpoint(self) -> typing.Optional[builtins.str]:
            '''The endpoint to use when communicating with the collection in the Serverless offering for Amazon OpenSearch Service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration-collectionendpoint
            '''
            result = self._values.get("collection_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def index_name(self) -> typing.Optional[builtins.str]:
            '''The Serverless offering for Amazon OpenSearch Service index name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration-indexname
            '''
            result = self._values.get("index_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration-processingconfiguration
            '''
            result = self._values.get("processing_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]], result)

        @builtins.property
        def retry_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessRetryOptionsProperty"]]:
            '''The retry behavior in case Firehose is unable to deliver documents to the Serverless offering for Amazon OpenSearch Service.

            The default value is 300 (5 minutes).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration-retryoptions
            '''
            result = self._values.get("retry_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessRetryOptionsProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role to be assumed by Firehose for calling the Serverless offering for Amazon OpenSearch Service Configuration API and for indexing documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_backup_mode(self) -> typing.Optional[builtins.str]:
            '''Defines how documents should be delivered to Amazon S3.

            When it is set to FailedDocumentsOnly, Firehose writes any documents that could not be indexed to the configured Amazon S3 destination, with AmazonOpenSearchService-failed/ appended to the key prefix. When set to AllDocuments, Firehose delivers all incoming records to Amazon S3, and also writes failed documents with AmazonOpenSearchService-failed/ appended to the prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration-s3backupmode
            '''
            result = self._values.get("s3_backup_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.VpcConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserverlessdestinationconfiguration-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.VpcConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmazonOpenSearchServerlessDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessRetryOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_in_seconds": "durationInSeconds"},
    )
    class AmazonOpenSearchServerlessRetryOptionsProperty:
        def __init__(
            self,
            *,
            duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configures retry behavior in case Firehose is unable to deliver documents to the Serverless offering for Amazon OpenSearch Service.

            :param duration_in_seconds: After an initial failure to deliver to the Serverless offering for Amazon OpenSearch Service, the total amount of time during which Firehose retries delivery (including the first attempt). After this time has elapsed, the failed documents are written to Amazon S3. Default value is 300 seconds (5 minutes). A value of 0 (zero) results in no retries.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessretryoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                amazon_open_search_serverless_retry_options_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessRetryOptionsProperty(
                    duration_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d06d6416eb798b2d42ad0753a77feac835ec40948bad96d1579c78690039ebb7)
                check_type(argname="argument duration_in_seconds", value=duration_in_seconds, expected_type=type_hints["duration_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''After an initial failure to deliver to the Serverless offering for Amazon OpenSearch Service, the total amount of time during which Firehose retries delivery (including the first attempt).

            After this time has elapsed, the failed documents are written to Amazon S3. Default value is 300 seconds (5 minutes). A value of 0 (zero) results in no retries.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserverlessretryoptions.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserverlessretryoptions-durationinseconds
            '''
            result = self._values.get("duration_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmazonOpenSearchServerlessRetryOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.AmazonopensearchserviceBufferingHintsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "interval_in_seconds": "intervalInSeconds",
            "size_in_m_bs": "sizeInMBs",
        },
    )
    class AmazonopensearchserviceBufferingHintsProperty:
        def __init__(
            self,
            *,
            interval_in_seconds: typing.Optional[jsii.Number] = None,
            size_in_m_bs: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the buffering to perform before delivering data to the Amazon OpenSearch Service destination.

            :param interval_in_seconds: Buffer incoming data for the specified period of time, in seconds, before delivering it to the destination. The default value is 300 (5 minutes).
            :param size_in_m_bs: Buffer incoming data to the specified size, in MBs, before delivering it to the destination. The default value is 5. We recommend setting this parameter to a value greater than the amount of data you typically ingest into the delivery stream in 10 seconds. For example, if you typically ingest data at 1 MB/sec, the value should be 10 MB or higher.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicebufferinghints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                amazonopensearchservice_buffering_hints_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.AmazonopensearchserviceBufferingHintsProperty(
                    interval_in_seconds=123,
                    size_in_mBs=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d9d475873392836595dd9e85cce970f1ca92bc822958718beaccb4968e7dc1d)
                check_type(argname="argument interval_in_seconds", value=interval_in_seconds, expected_type=type_hints["interval_in_seconds"])
                check_type(argname="argument size_in_m_bs", value=size_in_m_bs, expected_type=type_hints["size_in_m_bs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if interval_in_seconds is not None:
                self._values["interval_in_seconds"] = interval_in_seconds
            if size_in_m_bs is not None:
                self._values["size_in_m_bs"] = size_in_m_bs

        @builtins.property
        def interval_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''Buffer incoming data for the specified period of time, in seconds, before delivering it to the destination.

            The default value is 300 (5 minutes).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicebufferinghints.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicebufferinghints-intervalinseconds
            '''
            result = self._values.get("interval_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def size_in_m_bs(self) -> typing.Optional[jsii.Number]:
            '''Buffer incoming data to the specified size, in MBs, before delivering it to the destination.

            The default value is 5. We recommend setting this parameter to a value greater than the amount of data you typically ingest into the delivery stream in 10 seconds. For example, if you typically ingest data at 1 MB/sec, the value should be 10 MB or higher.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicebufferinghints.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicebufferinghints-sizeinmbs
            '''
            result = self._values.get("size_in_m_bs")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmazonopensearchserviceBufferingHintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.AmazonopensearchserviceDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "buffering_hints": "bufferingHints",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "cluster_endpoint": "clusterEndpoint",
            "document_id_options": "documentIdOptions",
            "domain_arn": "domainArn",
            "index_name": "indexName",
            "index_rotation_period": "indexRotationPeriod",
            "processing_configuration": "processingConfiguration",
            "retry_options": "retryOptions",
            "role_arn": "roleArn",
            "s3_backup_mode": "s3BackupMode",
            "s3_configuration": "s3Configuration",
            "type_name": "typeName",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class AmazonopensearchserviceDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.AmazonopensearchserviceBufferingHintsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cluster_endpoint: typing.Optional[builtins.str] = None,
            document_id_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.DocumentIdOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            domain_arn: typing.Optional[builtins.str] = None,
            index_name: typing.Optional[builtins.str] = None,
            index_rotation_period: typing.Optional[builtins.str] = None,
            processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.AmazonopensearchserviceRetryOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            s3_backup_mode: typing.Optional[builtins.str] = None,
            s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type_name: typing.Optional[builtins.str] = None,
            vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the configuration of a destination in Amazon OpenSearch Service.

            :param buffering_hints: The buffering options. If no value is specified, the default values for AmazonopensearchserviceBufferingHints are used.
            :param cloud_watch_logging_options: Describes the Amazon CloudWatch logging options for your delivery stream.
            :param cluster_endpoint: The endpoint to use when communicating with the cluster. Specify either this ClusterEndpoint or the DomainARN field.
            :param document_id_options: Indicates the method for setting up document ID. The supported methods are Firehose generated document ID and OpenSearch Service generated document ID.
            :param domain_arn: The ARN of the Amazon OpenSearch Service domain.
            :param index_name: The Amazon OpenSearch Service index name.
            :param index_rotation_period: The Amazon OpenSearch Service index rotation period. Index rotation appends a timestamp to the IndexName to facilitate the expiration of old data.
            :param processing_configuration: Describes a data processing configuration.
            :param retry_options: The retry behavior in case Kinesis Data Firehose is unable to deliver documents to Amazon OpenSearch Service. The default value is 300 (5 minutes).
            :param role_arn: The Amazon Resource Name (ARN) of the IAM role to be assumed by Kinesis Data Firehose for calling the Amazon OpenSearch Service Configuration API and for indexing documents.
            :param s3_backup_mode: Defines how documents should be delivered to Amazon S3.
            :param s3_configuration: Describes the configuration of a destination in Amazon S3.
            :param type_name: The Amazon OpenSearch Service type name.
            :param vpc_configuration: The details of the VPC of the Amazon OpenSearch Service destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                amazonopensearchservice_destination_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.AmazonopensearchserviceDestinationConfigurationProperty(
                    buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.AmazonopensearchserviceBufferingHintsProperty(
                        interval_in_seconds=123,
                        size_in_mBs=123
                    ),
                    cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                        enabled=False,
                        log_group_name="logGroupName",
                        log_stream_name="logStreamName"
                    ),
                    cluster_endpoint="clusterEndpoint",
                    document_id_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DocumentIdOptionsProperty(
                        default_document_id_format="defaultDocumentIdFormat"
                    ),
                    domain_arn="domainArn",
                    index_name="indexName",
                    index_rotation_period="indexRotationPeriod",
                    processing_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty(
                        enabled=False,
                        processors=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorProperty(
                            parameters=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorParameterProperty(
                                parameter_name="parameterName",
                                parameter_value="parameterValue"
                            )],
                            type="type"
                        )]
                    ),
                    retry_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.AmazonopensearchserviceRetryOptionsProperty(
                        duration_in_seconds=123
                    ),
                    role_arn="roleArn",
                    s3_backup_mode="s3BackupMode",
                    s3_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty(
                        bucket_arn="bucketArn",
                        buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                            interval_in_seconds=123,
                            size_in_mBs=123
                        ),
                        cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                            enabled=False,
                            log_group_name="logGroupName",
                            log_stream_name="logStreamName"
                        ),
                        compression_format="compressionFormat",
                        encryption_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty(
                            kms_encryption_config=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty(
                                awskms_key_arn="awskmsKeyArn"
                            ),
                            no_encryption_config="noEncryptionConfig"
                        ),
                        error_output_prefix="errorOutputPrefix",
                        prefix="prefix",
                        role_arn="roleArn"
                    ),
                    type_name="typeName",
                    vpc_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.VpcConfigurationProperty(
                        role_arn="roleArn",
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bb7ba29e1bed5a99a7bea24258262e71d8b12c176ca6a269175c595d00649ac3)
                check_type(argname="argument buffering_hints", value=buffering_hints, expected_type=type_hints["buffering_hints"])
                check_type(argname="argument cloud_watch_logging_options", value=cloud_watch_logging_options, expected_type=type_hints["cloud_watch_logging_options"])
                check_type(argname="argument cluster_endpoint", value=cluster_endpoint, expected_type=type_hints["cluster_endpoint"])
                check_type(argname="argument document_id_options", value=document_id_options, expected_type=type_hints["document_id_options"])
                check_type(argname="argument domain_arn", value=domain_arn, expected_type=type_hints["domain_arn"])
                check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
                check_type(argname="argument index_rotation_period", value=index_rotation_period, expected_type=type_hints["index_rotation_period"])
                check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
                check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
                check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if buffering_hints is not None:
                self._values["buffering_hints"] = buffering_hints
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if cluster_endpoint is not None:
                self._values["cluster_endpoint"] = cluster_endpoint
            if document_id_options is not None:
                self._values["document_id_options"] = document_id_options
            if domain_arn is not None:
                self._values["domain_arn"] = domain_arn
            if index_name is not None:
                self._values["index_name"] = index_name
            if index_rotation_period is not None:
                self._values["index_rotation_period"] = index_rotation_period
            if processing_configuration is not None:
                self._values["processing_configuration"] = processing_configuration
            if retry_options is not None:
                self._values["retry_options"] = retry_options
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if s3_backup_mode is not None:
                self._values["s3_backup_mode"] = s3_backup_mode
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration
            if type_name is not None:
                self._values["type_name"] = type_name
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def buffering_hints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.AmazonopensearchserviceBufferingHintsProperty"]]:
            '''The buffering options.

            If no value is specified, the default values for AmazonopensearchserviceBufferingHints are used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration-bufferinghints
            '''
            result = self._values.get("buffering_hints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.AmazonopensearchserviceBufferingHintsProperty"]], result)

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]]:
            '''Describes the Amazon CloudWatch logging options for your delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration-cloudwatchloggingoptions
            '''
            result = self._values.get("cloud_watch_logging_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]], result)

        @builtins.property
        def cluster_endpoint(self) -> typing.Optional[builtins.str]:
            '''The endpoint to use when communicating with the cluster.

            Specify either this ClusterEndpoint or the DomainARN field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration-clusterendpoint
            '''
            result = self._values.get("cluster_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_id_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DocumentIdOptionsProperty"]]:
            '''Indicates the method for setting up document ID.

            The supported methods are Firehose generated document ID and OpenSearch Service generated document ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration-documentidoptions
            '''
            result = self._values.get("document_id_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DocumentIdOptionsProperty"]], result)

        @builtins.property
        def domain_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Amazon OpenSearch Service domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration-domainarn
            '''
            result = self._values.get("domain_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def index_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon OpenSearch Service index name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration-indexname
            '''
            result = self._values.get("index_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def index_rotation_period(self) -> typing.Optional[builtins.str]:
            '''The Amazon OpenSearch Service index rotation period.

            Index rotation appends a timestamp to the IndexName to facilitate the expiration of old data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration-indexrotationperiod
            '''
            result = self._values.get("index_rotation_period")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]]:
            '''Describes a data processing configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration-processingconfiguration
            '''
            result = self._values.get("processing_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]], result)

        @builtins.property
        def retry_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.AmazonopensearchserviceRetryOptionsProperty"]]:
            '''The retry behavior in case Kinesis Data Firehose is unable to deliver documents to Amazon OpenSearch Service.

            The default value is 300 (5 minutes).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration-retryoptions
            '''
            result = self._values.get("retry_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.AmazonopensearchserviceRetryOptionsProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role to be assumed by Kinesis Data Firehose for calling the Amazon OpenSearch Service Configuration API and for indexing documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_backup_mode(self) -> typing.Optional[builtins.str]:
            '''Defines how documents should be delivered to Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration-s3backupmode
            '''
            result = self._values.get("s3_backup_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]]:
            '''Describes the configuration of a destination in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]], result)

        @builtins.property
        def type_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon OpenSearch Service type name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration-typename
            '''
            result = self._values.get("type_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.VpcConfigurationProperty"]]:
            '''The details of the VPC of the Amazon OpenSearch Service destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-amazonopensearchservicedestinationconfiguration-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.VpcConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmazonopensearchserviceDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.AmazonopensearchserviceRetryOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_in_seconds": "durationInSeconds"},
    )
    class AmazonopensearchserviceRetryOptionsProperty:
        def __init__(
            self,
            *,
            duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configures retry behavior in case Kinesis Data Firehose is unable to deliver documents to Amazon OpenSearch Service.

            :param duration_in_seconds: After an initial failure to deliver to Amazon OpenSearch Service, the total amount of time during which Kinesis Data Firehose retries delivery (including the first attempt). After this time has elapsed, the failed documents are written to Amazon S3. Default value is 300 seconds (5 minutes). A value of 0 (zero) results in no retries.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserviceretryoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                amazonopensearchservice_retry_options_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.AmazonopensearchserviceRetryOptionsProperty(
                    duration_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8c82e62670e75160b68ab7cbfeec549797c4285d1c2b3e6168e471e9ecf6aa55)
                check_type(argname="argument duration_in_seconds", value=duration_in_seconds, expected_type=type_hints["duration_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''After an initial failure to deliver to Amazon OpenSearch Service, the total amount of time during which Kinesis Data Firehose retries delivery (including the first attempt).

            After this time has elapsed, the failed documents are written to Amazon S3. Default value is 300 seconds (5 minutes). A value of 0 (zero) results in no retries.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-amazonopensearchserviceretryoptions.html#cfn-kinesisfirehose-deliverystream-amazonopensearchserviceretryoptions-durationinseconds
            '''
            result = self._values.get("duration_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmazonopensearchserviceRetryOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.AuthenticationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"connectivity": "connectivity", "role_arn": "roleArn"},
    )
    class AuthenticationConfigurationProperty:
        def __init__(
            self,
            *,
            connectivity: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The authentication configuration of the Amazon MSK cluster.

            :param connectivity: The type of connectivity used to access the Amazon MSK cluster.
            :param role_arn: The ARN of the role used to access the Amazon MSK cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-authenticationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                authentication_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.AuthenticationConfigurationProperty(
                    connectivity="connectivity",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b40b33da2bf525e4e5893f6c761af0b5afff44296dc380fecb52b85e953f5d5e)
                check_type(argname="argument connectivity", value=connectivity, expected_type=type_hints["connectivity"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connectivity is not None:
                self._values["connectivity"] = connectivity
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def connectivity(self) -> typing.Optional[builtins.str]:
            '''The type of connectivity used to access the Amazon MSK cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-authenticationconfiguration.html#cfn-kinesisfirehose-deliverystream-authenticationconfiguration-connectivity
            '''
            result = self._values.get("connectivity")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role used to access the Amazon MSK cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-authenticationconfiguration.html#cfn-kinesisfirehose-deliverystream-authenticationconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "interval_in_seconds": "intervalInSeconds",
            "size_in_m_bs": "sizeInMBs",
        },
    )
    class BufferingHintsProperty:
        def __init__(
            self,
            *,
            interval_in_seconds: typing.Optional[jsii.Number] = None,
            size_in_m_bs: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ``BufferingHints`` property type specifies how Amazon Kinesis Data Firehose (Kinesis Data Firehose) buffers incoming data before delivering it to the destination.

            The first buffer condition that is satisfied triggers Kinesis Data Firehose to deliver the data.

            :param interval_in_seconds: The length of time, in seconds, that Kinesis Data Firehose buffers incoming data before delivering it to the destination. For valid values, see the ``IntervalInSeconds`` content for the `BufferingHints <https://docs.aws.amazon.com/firehose/latest/APIReference/API_BufferingHints.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .
            :param size_in_m_bs: The size of the buffer, in MBs, that Kinesis Data Firehose uses for incoming data before delivering it to the destination. For valid values, see the ``SizeInMBs`` content for the `BufferingHints <https://docs.aws.amazon.com/firehose/latest/APIReference/API_BufferingHints.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-bufferinghints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                buffering_hints_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                    interval_in_seconds=123,
                    size_in_mBs=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f663354b24573aee29f12af489e12e95cd1d98e976e4aaa1514904b4e35021dc)
                check_type(argname="argument interval_in_seconds", value=interval_in_seconds, expected_type=type_hints["interval_in_seconds"])
                check_type(argname="argument size_in_m_bs", value=size_in_m_bs, expected_type=type_hints["size_in_m_bs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if interval_in_seconds is not None:
                self._values["interval_in_seconds"] = interval_in_seconds
            if size_in_m_bs is not None:
                self._values["size_in_m_bs"] = size_in_m_bs

        @builtins.property
        def interval_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The length of time, in seconds, that Kinesis Data Firehose buffers incoming data before delivering it to the destination.

            For valid values, see the ``IntervalInSeconds`` content for the `BufferingHints <https://docs.aws.amazon.com/firehose/latest/APIReference/API_BufferingHints.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-bufferinghints.html#cfn-kinesisfirehose-deliverystream-bufferinghints-intervalinseconds
            '''
            result = self._values.get("interval_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def size_in_m_bs(self) -> typing.Optional[jsii.Number]:
            '''The size of the buffer, in MBs, that Kinesis Data Firehose uses for incoming data before delivering it to the destination.

            For valid values, see the ``SizeInMBs`` content for the `BufferingHints <https://docs.aws.amazon.com/firehose/latest/APIReference/API_BufferingHints.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-bufferinghints.html#cfn-kinesisfirehose-deliverystream-bufferinghints-sizeinmbs
            '''
            result = self._values.get("size_in_m_bs")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BufferingHintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.CatalogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_arn": "catalogArn",
            "warehouse_location": "warehouseLocation",
        },
    )
    class CatalogConfigurationProperty:
        def __init__(
            self,
            *,
            catalog_arn: typing.Optional[builtins.str] = None,
            warehouse_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the containers where the destination Apache Iceberg Tables are persisted.

            :param catalog_arn: Specifies the Glue catalog ARN identifier of the destination Apache Iceberg Tables. You must specify the ARN in the format ``arn:aws:glue:region:account-id:catalog`` .
            :param warehouse_location: The warehouse location for Apache Iceberg tables. You must configure this when schema evolution and table creation is enabled. Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-catalogconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                catalog_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CatalogConfigurationProperty(
                    catalog_arn="catalogArn",
                    warehouse_location="warehouseLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a9f7cf40c12ecbff12591f0a1a4f894e641a1712591c0c1f1f56fde8e927f30)
                check_type(argname="argument catalog_arn", value=catalog_arn, expected_type=type_hints["catalog_arn"])
                check_type(argname="argument warehouse_location", value=warehouse_location, expected_type=type_hints["warehouse_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_arn is not None:
                self._values["catalog_arn"] = catalog_arn
            if warehouse_location is not None:
                self._values["warehouse_location"] = warehouse_location

        @builtins.property
        def catalog_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the Glue catalog ARN identifier of the destination Apache Iceberg Tables.

            You must specify the ARN in the format ``arn:aws:glue:region:account-id:catalog`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-catalogconfiguration.html#cfn-kinesisfirehose-deliverystream-catalogconfiguration-catalogarn
            '''
            result = self._values.get("catalog_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def warehouse_location(self) -> typing.Optional[builtins.str]:
            '''The warehouse location for Apache Iceberg tables. You must configure this when schema evolution and table creation is enabled.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-catalogconfiguration.html#cfn-kinesisfirehose-deliverystream-catalogconfiguration-warehouselocation
            '''
            result = self._values.get("warehouse_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CatalogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "log_group_name": "logGroupName",
            "log_stream_name": "logStreamName",
        },
    )
    class CloudWatchLoggingOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            log_group_name: typing.Optional[builtins.str] = None,
            log_stream_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``CloudWatchLoggingOptions`` property type specifies Amazon CloudWatch Logs (CloudWatch Logs) logging options that Amazon Kinesis Data Firehose (Kinesis Data Firehose) uses for the delivery stream.

            :param enabled: Indicates whether CloudWatch Logs logging is enabled.
            :param log_group_name: The name of the CloudWatch Logs log group that contains the log stream that Kinesis Data Firehose will use. Conditional. If you enable logging, you must specify this property.
            :param log_stream_name: The name of the CloudWatch Logs log stream that Kinesis Data Firehose uses to send logs about data delivery. Conditional. If you enable logging, you must specify this property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-cloudwatchloggingoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                cloud_watch_logging_options_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                    enabled=False,
                    log_group_name="logGroupName",
                    log_stream_name="logStreamName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0bc6dec41148b6f531f60b4316f60bb8a252973a724e78e2c6fbad50986e97a5)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
                check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name
            if log_stream_name is not None:
                self._values["log_stream_name"] = log_stream_name

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether CloudWatch Logs logging is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-cloudwatchloggingoptions.html#cfn-kinesisfirehose-deliverystream-cloudwatchloggingoptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch Logs log group that contains the log stream that Kinesis Data Firehose will use.

            Conditional. If you enable logging, you must specify this property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-cloudwatchloggingoptions.html#cfn-kinesisfirehose-deliverystream-cloudwatchloggingoptions-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_stream_name(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch Logs log stream that Kinesis Data Firehose uses to send logs about data delivery.

            Conditional. If you enable logging, you must specify this property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-cloudwatchloggingoptions.html#cfn-kinesisfirehose-deliverystream-cloudwatchloggingoptions-logstreamname
            '''
            result = self._values.get("log_stream_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLoggingOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.CopyCommandProperty",
        jsii_struct_bases=[],
        name_mapping={
            "copy_options": "copyOptions",
            "data_table_columns": "dataTableColumns",
            "data_table_name": "dataTableName",
        },
    )
    class CopyCommandProperty:
        def __init__(
            self,
            *,
            copy_options: typing.Optional[builtins.str] = None,
            data_table_columns: typing.Optional[builtins.str] = None,
            data_table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``CopyCommand`` property type configures the Amazon Redshift ``COPY`` command that Amazon Kinesis Data Firehose (Kinesis Data Firehose) uses to load data into an Amazon Redshift cluster from an Amazon S3 bucket.

            :param copy_options: Parameters to use with the Amazon Redshift ``COPY`` command. For examples, see the ``CopyOptions`` content for the `CopyCommand <https://docs.aws.amazon.com/firehose/latest/APIReference/API_CopyCommand.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .
            :param data_table_columns: A comma-separated list of column names.
            :param data_table_name: The name of the target table. The table must already exist in the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-copycommand.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                copy_command_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CopyCommandProperty(
                    copy_options="copyOptions",
                    data_table_columns="dataTableColumns",
                    data_table_name="dataTableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d34aa859756ee18037f6d46647870395666701787ba01cbcab05f3774115a2f8)
                check_type(argname="argument copy_options", value=copy_options, expected_type=type_hints["copy_options"])
                check_type(argname="argument data_table_columns", value=data_table_columns, expected_type=type_hints["data_table_columns"])
                check_type(argname="argument data_table_name", value=data_table_name, expected_type=type_hints["data_table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if copy_options is not None:
                self._values["copy_options"] = copy_options
            if data_table_columns is not None:
                self._values["data_table_columns"] = data_table_columns
            if data_table_name is not None:
                self._values["data_table_name"] = data_table_name

        @builtins.property
        def copy_options(self) -> typing.Optional[builtins.str]:
            '''Parameters to use with the Amazon Redshift ``COPY`` command.

            For examples, see the ``CopyOptions`` content for the `CopyCommand <https://docs.aws.amazon.com/firehose/latest/APIReference/API_CopyCommand.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-copycommand.html#cfn-kinesisfirehose-deliverystream-copycommand-copyoptions
            '''
            result = self._values.get("copy_options")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_table_columns(self) -> typing.Optional[builtins.str]:
            '''A comma-separated list of column names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-copycommand.html#cfn-kinesisfirehose-deliverystream-copycommand-datatablecolumns
            '''
            result = self._values.get("data_table_columns")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the target table.

            The table must already exist in the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-copycommand.html#cfn-kinesisfirehose-deliverystream-copycommand-datatablename
            '''
            result = self._values.get("data_table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CopyCommandProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.DataFormatConversionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "input_format_configuration": "inputFormatConfiguration",
            "output_format_configuration": "outputFormatConfiguration",
            "schema_configuration": "schemaConfiguration",
        },
    )
    class DataFormatConversionConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            input_format_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.InputFormatConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            output_format_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.OutputFormatConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            schema_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SchemaConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies that you want Kinesis Data Firehose to convert data from the JSON format to the Parquet or ORC format before writing it to Amazon S3.

            Kinesis Data Firehose uses the serializer and deserializer that you specify, in addition to the column information from the AWS Glue table, to deserialize your input data from JSON and then serialize it to the Parquet or ORC format. For more information, see `Kinesis Data Firehose Record Format Conversion <https://docs.aws.amazon.com/firehose/latest/dev/record-format-conversion.html>`_ .

            :param enabled: Defaults to ``true`` . Set it to ``false`` if you want to disable format conversion while preserving the configuration details.
            :param input_format_configuration: Specifies the deserializer that you want Firehose to use to convert the format of your data from JSON. This parameter is required if ``Enabled`` is set to true.
            :param output_format_configuration: Specifies the serializer that you want Firehose to use to convert the format of your data to the Parquet or ORC format. This parameter is required if ``Enabled`` is set to true.
            :param schema_configuration: Specifies the AWS Glue Data Catalog table that contains the column information. This parameter is required if ``Enabled`` is set to true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-dataformatconversionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                data_format_conversion_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DataFormatConversionConfigurationProperty(
                    enabled=False,
                    input_format_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.InputFormatConfigurationProperty(
                        deserializer=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DeserializerProperty(
                            hive_json_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.HiveJsonSerDeProperty(
                                timestamp_formats=["timestampFormats"]
                            ),
                            open_xJson_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.OpenXJsonSerDeProperty(
                                case_insensitive=False,
                                column_to_json_key_mappings={
                                    "column_to_json_key_mappings_key": "columnToJsonKeyMappings"
                                },
                                convert_dots_in_json_keys_to_underscores=False
                            )
                        )
                    ),
                    output_format_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.OutputFormatConfigurationProperty(
                        serializer=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SerializerProperty(
                            orc_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.OrcSerDeProperty(
                                block_size_bytes=123,
                                bloom_filter_columns=["bloomFilterColumns"],
                                bloom_filter_false_positive_probability=123,
                                compression="compression",
                                dictionary_key_threshold=123,
                                enable_padding=False,
                                format_version="formatVersion",
                                padding_tolerance=123,
                                row_index_stride=123,
                                stripe_size_bytes=123
                            ),
                            parquet_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ParquetSerDeProperty(
                                block_size_bytes=123,
                                compression="compression",
                                enable_dictionary_compression=False,
                                max_padding_bytes=123,
                                page_size_bytes=123,
                                writer_version="writerVersion"
                            )
                        )
                    ),
                    schema_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SchemaConfigurationProperty(
                        catalog_id="catalogId",
                        database_name="databaseName",
                        region="region",
                        role_arn="roleArn",
                        table_name="tableName",
                        version_id="versionId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__290dff42a7e66004a43d6d32c49e894292f7f8b13e5fbbfe899a32fa57468b83)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument input_format_configuration", value=input_format_configuration, expected_type=type_hints["input_format_configuration"])
                check_type(argname="argument output_format_configuration", value=output_format_configuration, expected_type=type_hints["output_format_configuration"])
                check_type(argname="argument schema_configuration", value=schema_configuration, expected_type=type_hints["schema_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if input_format_configuration is not None:
                self._values["input_format_configuration"] = input_format_configuration
            if output_format_configuration is not None:
                self._values["output_format_configuration"] = output_format_configuration
            if schema_configuration is not None:
                self._values["schema_configuration"] = schema_configuration

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Defaults to ``true`` .

            Set it to ``false`` if you want to disable format conversion while preserving the configuration details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-dataformatconversionconfiguration.html#cfn-kinesisfirehose-deliverystream-dataformatconversionconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def input_format_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.InputFormatConfigurationProperty"]]:
            '''Specifies the deserializer that you want Firehose to use to convert the format of your data from JSON.

            This parameter is required if ``Enabled`` is set to true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-dataformatconversionconfiguration.html#cfn-kinesisfirehose-deliverystream-dataformatconversionconfiguration-inputformatconfiguration
            '''
            result = self._values.get("input_format_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.InputFormatConfigurationProperty"]], result)

        @builtins.property
        def output_format_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.OutputFormatConfigurationProperty"]]:
            '''Specifies the serializer that you want Firehose to use to convert the format of your data to the Parquet or ORC format.

            This parameter is required if ``Enabled`` is set to true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-dataformatconversionconfiguration.html#cfn-kinesisfirehose-deliverystream-dataformatconversionconfiguration-outputformatconfiguration
            '''
            result = self._values.get("output_format_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.OutputFormatConfigurationProperty"]], result)

        @builtins.property
        def schema_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SchemaConfigurationProperty"]]:
            '''Specifies the AWS Glue Data Catalog table that contains the column information.

            This parameter is required if ``Enabled`` is set to true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-dataformatconversionconfiguration.html#cfn-kinesisfirehose-deliverystream-dataformatconversionconfiguration-schemaconfiguration
            '''
            result = self._values.get("schema_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SchemaConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataFormatConversionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.DatabaseColumnsProperty",
        jsii_struct_bases=[],
        name_mapping={"exclude": "exclude", "include": "include"},
    )
    class DatabaseColumnsProperty:
        def __init__(
            self,
            *,
            exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
            include: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param exclude: 
            :param include: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasecolumns.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                database_columns_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DatabaseColumnsProperty(
                    exclude=["exclude"],
                    include=["include"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c1f82f7b00716b63fcd9bfa364c01a840d424b0ea36511064ef8af4e0f315b8)
                check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
                check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude is not None:
                self._values["exclude"] = exclude
            if include is not None:
                self._values["include"] = include

        @builtins.property
        def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasecolumns.html#cfn-kinesisfirehose-deliverystream-databasecolumns-exclude
            '''
            result = self._values.get("exclude")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasecolumns.html#cfn-kinesisfirehose-deliverystream-databasecolumns-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseColumnsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.DatabaseSourceAuthenticationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"secrets_manager_configuration": "secretsManagerConfiguration"},
    )
    class DatabaseSourceAuthenticationConfigurationProperty:
        def __init__(
            self,
            *,
            secrets_manager_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The structure to configure the authentication methods for Firehose to connect to source database endpoint.

            Amazon Data Firehose is in preview release and is subject to change.

            :param secrets_manager_configuration: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceauthenticationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                database_source_authentication_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DatabaseSourceAuthenticationConfigurationProperty(
                    secrets_manager_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty(
                        enabled=False,
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ec93158e976b5f4ce0d343666f294325c3e2caf58954b8923b5114a7bc51fbd)
                check_type(argname="argument secrets_manager_configuration", value=secrets_manager_configuration, expected_type=type_hints["secrets_manager_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secrets_manager_configuration is not None:
                self._values["secrets_manager_configuration"] = secrets_manager_configuration

        @builtins.property
        def secrets_manager_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceauthenticationconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourceauthenticationconfiguration-secretsmanagerconfiguration
            '''
            result = self._values.get("secrets_manager_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseSourceAuthenticationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.DatabaseSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "columns": "columns",
            "databases": "databases",
            "database_source_authentication_configuration": "databaseSourceAuthenticationConfiguration",
            "database_source_vpc_configuration": "databaseSourceVpcConfiguration",
            "digest": "digest",
            "endpoint": "endpoint",
            "port": "port",
            "public_certificate": "publicCertificate",
            "snapshot_watermark_table": "snapshotWatermarkTable",
            "ssl_mode": "sslMode",
            "surrogate_keys": "surrogateKeys",
            "tables": "tables",
            "type": "type",
        },
    )
    class DatabaseSourceConfigurationProperty:
        def __init__(
            self,
            *,
            columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.DatabaseColumnsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            databases: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.DatabasesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            database_source_authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.DatabaseSourceAuthenticationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            database_source_vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.DatabaseSourceVPCConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            digest: typing.Optional[builtins.str] = None,
            endpoint: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            public_certificate: typing.Optional[builtins.str] = None,
            snapshot_watermark_table: typing.Optional[builtins.str] = None,
            ssl_mode: typing.Optional[builtins.str] = None,
            surrogate_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
            tables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.DatabaseTablesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The top level object for configuring streams with database as a source.

            Amazon Data Firehose is in preview release and is subject to change.

            :param columns: The list of column patterns in source database endpoint for Firehose to read from. Amazon Data Firehose is in preview release and is subject to change.
            :param databases: The list of database patterns in source database endpoint for Firehose to read from. Amazon Data Firehose is in preview release and is subject to change.
            :param database_source_authentication_configuration: The structure to configure the authentication methods for Firehose to connect to source database endpoint. Amazon Data Firehose is in preview release and is subject to change.
            :param database_source_vpc_configuration: The details of the VPC Endpoint Service which Firehose uses to create a PrivateLink to the database. Amazon Data Firehose is in preview release and is subject to change.
            :param digest: 
            :param endpoint: The endpoint of the database server. Amazon Data Firehose is in preview release and is subject to change.
            :param port: The port of the database. This can be one of the following values. - 3306 for MySQL database type - 5432 for PostgreSQL database type Amazon Data Firehose is in preview release and is subject to change.
            :param public_certificate: 
            :param snapshot_watermark_table: The fully qualified name of the table in source database endpoint that Firehose uses to track snapshot progress. Amazon Data Firehose is in preview release and is subject to change.
            :param ssl_mode: The mode to enable or disable SSL when Firehose connects to the database endpoint. Amazon Data Firehose is in preview release and is subject to change.
            :param surrogate_keys: The optional list of table and column names used as unique key columns when taking snapshot if the tables don’t have primary keys configured. Amazon Data Firehose is in preview release and is subject to change.
            :param tables: The list of table patterns in source database endpoint for Firehose to read from. Amazon Data Firehose is in preview release and is subject to change.
            :param type: The type of database engine. This can be one of the following values. - MySQL - PostgreSQL Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                database_source_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DatabaseSourceConfigurationProperty(
                    columns=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DatabaseColumnsProperty(
                        exclude=["exclude"],
                        include=["include"]
                    ),
                    databases=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DatabasesProperty(
                        exclude=["exclude"],
                        include=["include"]
                    ),
                    database_source_authentication_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DatabaseSourceAuthenticationConfigurationProperty(
                        secrets_manager_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty(
                            enabled=False,
                            role_arn="roleArn",
                            secret_arn="secretArn"
                        )
                    ),
                    database_source_vpc_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DatabaseSourceVPCConfigurationProperty(
                        vpc_endpoint_service_name="vpcEndpointServiceName"
                    ),
                    digest="digest",
                    endpoint="endpoint",
                    port=123,
                    public_certificate="publicCertificate",
                    snapshot_watermark_table="snapshotWatermarkTable",
                    ssl_mode="sslMode",
                    surrogate_keys=["surrogateKeys"],
                    tables=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DatabaseTablesProperty(
                        exclude=["exclude"],
                        include=["include"]
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__afcad6b2c3e4247aa2069f48fbaf06fec0167181216b3bc1dfabe15f168b978d)
                check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
                check_type(argname="argument databases", value=databases, expected_type=type_hints["databases"])
                check_type(argname="argument database_source_authentication_configuration", value=database_source_authentication_configuration, expected_type=type_hints["database_source_authentication_configuration"])
                check_type(argname="argument database_source_vpc_configuration", value=database_source_vpc_configuration, expected_type=type_hints["database_source_vpc_configuration"])
                check_type(argname="argument digest", value=digest, expected_type=type_hints["digest"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument public_certificate", value=public_certificate, expected_type=type_hints["public_certificate"])
                check_type(argname="argument snapshot_watermark_table", value=snapshot_watermark_table, expected_type=type_hints["snapshot_watermark_table"])
                check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
                check_type(argname="argument surrogate_keys", value=surrogate_keys, expected_type=type_hints["surrogate_keys"])
                check_type(argname="argument tables", value=tables, expected_type=type_hints["tables"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if columns is not None:
                self._values["columns"] = columns
            if databases is not None:
                self._values["databases"] = databases
            if database_source_authentication_configuration is not None:
                self._values["database_source_authentication_configuration"] = database_source_authentication_configuration
            if database_source_vpc_configuration is not None:
                self._values["database_source_vpc_configuration"] = database_source_vpc_configuration
            if digest is not None:
                self._values["digest"] = digest
            if endpoint is not None:
                self._values["endpoint"] = endpoint
            if port is not None:
                self._values["port"] = port
            if public_certificate is not None:
                self._values["public_certificate"] = public_certificate
            if snapshot_watermark_table is not None:
                self._values["snapshot_watermark_table"] = snapshot_watermark_table
            if ssl_mode is not None:
                self._values["ssl_mode"] = ssl_mode
            if surrogate_keys is not None:
                self._values["surrogate_keys"] = surrogate_keys
            if tables is not None:
                self._values["tables"] = tables
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def columns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DatabaseColumnsProperty"]]:
            '''The list of column patterns in source database endpoint for Firehose to read from.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourceconfiguration-columns
            '''
            result = self._values.get("columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DatabaseColumnsProperty"]], result)

        @builtins.property
        def databases(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DatabasesProperty"]]:
            '''The list of database patterns in source database endpoint for Firehose to read from.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourceconfiguration-databases
            '''
            result = self._values.get("databases")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DatabasesProperty"]], result)

        @builtins.property
        def database_source_authentication_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DatabaseSourceAuthenticationConfigurationProperty"]]:
            '''The structure to configure the authentication methods for Firehose to connect to source database endpoint.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourceconfiguration-databasesourceauthenticationconfiguration
            '''
            result = self._values.get("database_source_authentication_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DatabaseSourceAuthenticationConfigurationProperty"]], result)

        @builtins.property
        def database_source_vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DatabaseSourceVPCConfigurationProperty"]]:
            '''The details of the VPC Endpoint Service which Firehose uses to create a PrivateLink to the database.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourceconfiguration-databasesourcevpcconfiguration
            '''
            result = self._values.get("database_source_vpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DatabaseSourceVPCConfigurationProperty"]], result)

        @builtins.property
        def digest(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourceconfiguration-digest
            '''
            result = self._values.get("digest")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''The endpoint of the database server.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourceconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port of the database. This can be one of the following values.

            - 3306 for MySQL database type
            - 5432 for PostgreSQL database type

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourceconfiguration-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def public_certificate(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourceconfiguration-publiccertificate
            '''
            result = self._values.get("public_certificate")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def snapshot_watermark_table(self) -> typing.Optional[builtins.str]:
            '''The fully qualified name of the table in source database endpoint that Firehose uses to track snapshot progress.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourceconfiguration-snapshotwatermarktable
            '''
            result = self._values.get("snapshot_watermark_table")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_mode(self) -> typing.Optional[builtins.str]:
            '''The mode to enable or disable SSL when Firehose connects to the database endpoint.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourceconfiguration-sslmode
            '''
            result = self._values.get("ssl_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def surrogate_keys(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The optional list of table and column names used as unique key columns when taking snapshot if the tables don’t have primary keys configured.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourceconfiguration-surrogatekeys
            '''
            result = self._values.get("surrogate_keys")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def tables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DatabaseTablesProperty"]]:
            '''The list of table patterns in source database endpoint for Firehose to read from.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourceconfiguration-tables
            '''
            result = self._values.get("tables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DatabaseTablesProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of database engine. This can be one of the following values.

            - MySQL
            - PostgreSQL

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourceconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourceconfiguration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.DatabaseSourceVPCConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_endpoint_service_name": "vpcEndpointServiceName"},
    )
    class DatabaseSourceVPCConfigurationProperty:
        def __init__(
            self,
            *,
            vpc_endpoint_service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The structure for details of the VPC Endpoint Service which Firehose uses to create a PrivateLink to the database.

            Amazon Data Firehose is in preview release and is subject to change.

            :param vpc_endpoint_service_name: The VPC endpoint service name which Firehose uses to create a PrivateLink to the database. The endpoint service must have the Firehose service principle ``firehose.amazonaws.com`` as an allowed principal on the VPC endpoint service. The VPC endpoint service name is a string that looks like ``com.amazonaws.vpce.<region>.<vpc-endpoint-service-id>`` . Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourcevpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                database_source_vPCConfiguration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DatabaseSourceVPCConfigurationProperty(
                    vpc_endpoint_service_name="vpcEndpointServiceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8906a2d07384fa31f04a3fff73f920e4e2c557107d2c5ea9616bb9ca5e397958)
                check_type(argname="argument vpc_endpoint_service_name", value=vpc_endpoint_service_name, expected_type=type_hints["vpc_endpoint_service_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_endpoint_service_name is not None:
                self._values["vpc_endpoint_service_name"] = vpc_endpoint_service_name

        @builtins.property
        def vpc_endpoint_service_name(self) -> typing.Optional[builtins.str]:
            '''The VPC endpoint service name which Firehose uses to create a PrivateLink to the database.

            The endpoint service must have the Firehose service principle ``firehose.amazonaws.com`` as an allowed principal on the VPC endpoint service. The VPC endpoint service name is a string that looks like ``com.amazonaws.vpce.<region>.<vpc-endpoint-service-id>`` .

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasesourcevpcconfiguration.html#cfn-kinesisfirehose-deliverystream-databasesourcevpcconfiguration-vpcendpointservicename
            '''
            result = self._values.get("vpc_endpoint_service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseSourceVPCConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.DatabaseTablesProperty",
        jsii_struct_bases=[],
        name_mapping={"exclude": "exclude", "include": "include"},
    )
    class DatabaseTablesProperty:
        def __init__(
            self,
            *,
            exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
            include: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param exclude: 
            :param include: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasetables.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                database_tables_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DatabaseTablesProperty(
                    exclude=["exclude"],
                    include=["include"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__76984fad2f6460a0e5d29bb52d5cab787135dc6d015eb9d9e544601f95543574)
                check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
                check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude is not None:
                self._values["exclude"] = exclude
            if include is not None:
                self._values["include"] = include

        @builtins.property
        def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasetables.html#cfn-kinesisfirehose-deliverystream-databasetables-exclude
            '''
            result = self._values.get("exclude")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databasetables.html#cfn-kinesisfirehose-deliverystream-databasetables-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseTablesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.DatabasesProperty",
        jsii_struct_bases=[],
        name_mapping={"exclude": "exclude", "include": "include"},
    )
    class DatabasesProperty:
        def __init__(
            self,
            *,
            exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
            include: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param exclude: 
            :param include: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databases.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                databases_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DatabasesProperty(
                    exclude=["exclude"],
                    include=["include"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b72b01d120be0197745a951a4bc951e324044f229c292520c6a21b26495eee2c)
                check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
                check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude is not None:
                self._values["exclude"] = exclude
            if include is not None:
                self._values["include"] = include

        @builtins.property
        def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databases.html#cfn-kinesisfirehose-deliverystream-databases-exclude
            '''
            result = self._values.get("exclude")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-databases.html#cfn-kinesisfirehose-deliverystream-databases-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabasesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.DeliveryStreamEncryptionConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={"key_arn": "keyArn", "key_type": "keyType"},
    )
    class DeliveryStreamEncryptionConfigurationInputProperty:
        def __init__(
            self,
            *,
            key_arn: typing.Optional[builtins.str] = None,
            key_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the type and Amazon Resource Name (ARN) of the CMK to use for Server-Side Encryption (SSE).

            :param key_arn: If you set ``KeyType`` to ``CUSTOMER_MANAGED_CMK`` , you must specify the Amazon Resource Name (ARN) of the CMK. If you set ``KeyType`` to ``AWS _OWNED_CMK`` , Firehose uses a service-account CMK.
            :param key_type: Indicates the type of customer master key (CMK) to use for encryption. The default setting is ``AWS_OWNED_CMK`` . For more information about CMKs, see `Customer Master Keys (CMKs) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#master_keys>`_ . You can use a CMK of type CUSTOMER_MANAGED_CMK to encrypt up to 500 delivery streams. .. epigraph:: To encrypt your delivery stream, use symmetric CMKs. Kinesis Data Firehose doesn't support asymmetric CMKs. For information about symmetric and asymmetric CMKs, see `About Symmetric and Asymmetric CMKs <https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-concepts.html>`_ in the AWS Key Management Service developer guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-deliverystreamencryptionconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                delivery_stream_encryption_configuration_input_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DeliveryStreamEncryptionConfigurationInputProperty(
                    key_arn="keyArn",
                    key_type="keyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__efaeb1b8ee044e076d2a5b7b0736db82180b3bac71a8aaa9e98dd834ebce700d)
                check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_arn is not None:
                self._values["key_arn"] = key_arn
            if key_type is not None:
                self._values["key_type"] = key_type

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            '''If you set ``KeyType`` to ``CUSTOMER_MANAGED_CMK`` , you must specify the Amazon Resource Name (ARN) of the CMK.

            If you set ``KeyType`` to ``AWS _OWNED_CMK`` , Firehose uses a service-account CMK.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-deliverystreamencryptionconfigurationinput.html#cfn-kinesisfirehose-deliverystream-deliverystreamencryptionconfigurationinput-keyarn
            '''
            result = self._values.get("key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_type(self) -> typing.Optional[builtins.str]:
            '''Indicates the type of customer master key (CMK) to use for encryption.

            The default setting is ``AWS_OWNED_CMK`` . For more information about CMKs, see `Customer Master Keys (CMKs) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#master_keys>`_ .

            You can use a CMK of type CUSTOMER_MANAGED_CMK to encrypt up to 500 delivery streams.
            .. epigraph::

               To encrypt your delivery stream, use symmetric CMKs. Kinesis Data Firehose doesn't support asymmetric CMKs. For information about symmetric and asymmetric CMKs, see `About Symmetric and Asymmetric CMKs <https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-concepts.html>`_ in the AWS Key Management Service developer guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-deliverystreamencryptionconfigurationinput.html#cfn-kinesisfirehose-deliverystream-deliverystreamencryptionconfigurationinput-keytype
            '''
            result = self._values.get("key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeliveryStreamEncryptionConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.DeserializerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hive_json_ser_de": "hiveJsonSerDe",
            "open_x_json_ser_de": "openXJsonSerDe",
        },
    )
    class DeserializerProperty:
        def __init__(
            self,
            *,
            hive_json_ser_de: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.HiveJsonSerDeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            open_x_json_ser_de: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.OpenXJsonSerDeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The deserializer you want Kinesis Data Firehose to use for converting the input data from JSON.

            Kinesis Data Firehose then serializes the data to its final format using the ``Serializer`` . Kinesis Data Firehose supports two types of deserializers: the `Apache Hive JSON SerDe <https://docs.aws.amazon.com/https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-JSON>`_ and the `OpenX JSON SerDe <https://docs.aws.amazon.com/https://github.com/rcongiu/Hive-JSON-Serde>`_ .

            :param hive_json_ser_de: The native Hive / HCatalog JsonSerDe. Used by Firehose for deserializing data, which means converting it from the JSON format in preparation for serializing it to the Parquet or ORC format. This is one of two deserializers you can choose, depending on which one offers the functionality you need. The other option is the OpenX SerDe.
            :param open_x_json_ser_de: The OpenX SerDe. Used by Firehose for deserializing data, which means converting it from the JSON format in preparation for serializing it to the Parquet or ORC format. This is one of two deserializers you can choose, depending on which one offers the functionality you need. The other option is the native Hive / HCatalog JsonSerDe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-deserializer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                deserializer_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DeserializerProperty(
                    hive_json_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.HiveJsonSerDeProperty(
                        timestamp_formats=["timestampFormats"]
                    ),
                    open_xJson_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.OpenXJsonSerDeProperty(
                        case_insensitive=False,
                        column_to_json_key_mappings={
                            "column_to_json_key_mappings_key": "columnToJsonKeyMappings"
                        },
                        convert_dots_in_json_keys_to_underscores=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__604fb0ece70a83cbe743cb1074f2e1dbfe2e43be5a3f3bab98be63ff99fb35c7)
                check_type(argname="argument hive_json_ser_de", value=hive_json_ser_de, expected_type=type_hints["hive_json_ser_de"])
                check_type(argname="argument open_x_json_ser_de", value=open_x_json_ser_de, expected_type=type_hints["open_x_json_ser_de"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hive_json_ser_de is not None:
                self._values["hive_json_ser_de"] = hive_json_ser_de
            if open_x_json_ser_de is not None:
                self._values["open_x_json_ser_de"] = open_x_json_ser_de

        @builtins.property
        def hive_json_ser_de(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.HiveJsonSerDeProperty"]]:
            '''The native Hive / HCatalog JsonSerDe.

            Used by Firehose for deserializing data, which means converting it from the JSON format in preparation for serializing it to the Parquet or ORC format. This is one of two deserializers you can choose, depending on which one offers the functionality you need. The other option is the OpenX SerDe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-deserializer.html#cfn-kinesisfirehose-deliverystream-deserializer-hivejsonserde
            '''
            result = self._values.get("hive_json_ser_de")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.HiveJsonSerDeProperty"]], result)

        @builtins.property
        def open_x_json_ser_de(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.OpenXJsonSerDeProperty"]]:
            '''The OpenX SerDe.

            Used by Firehose for deserializing data, which means converting it from the JSON format in preparation for serializing it to the Parquet or ORC format. This is one of two deserializers you can choose, depending on which one offers the functionality you need. The other option is the native Hive / HCatalog JsonSerDe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-deserializer.html#cfn-kinesisfirehose-deliverystream-deserializer-openxjsonserde
            '''
            result = self._values.get("open_x_json_ser_de")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.OpenXJsonSerDeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeserializerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.DestinationTableConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_database_name": "destinationDatabaseName",
            "destination_table_name": "destinationTableName",
            "partition_spec": "partitionSpec",
            "s3_error_output_prefix": "s3ErrorOutputPrefix",
            "unique_keys": "uniqueKeys",
        },
    )
    class DestinationTableConfigurationProperty:
        def __init__(
            self,
            *,
            destination_database_name: typing.Optional[builtins.str] = None,
            destination_table_name: typing.Optional[builtins.str] = None,
            partition_spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.PartitionSpecProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_error_output_prefix: typing.Optional[builtins.str] = None,
            unique_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Describes the configuration of a destination in Apache Iceberg Tables.

            This section is only needed for tables where you want to update or delete data.

            :param destination_database_name: The name of the Apache Iceberg database.
            :param destination_table_name: Specifies the name of the Apache Iceberg Table.
            :param partition_spec: The partition spec configuration for a table that is used by automatic table creation. Amazon Data Firehose is in preview release and is subject to change.
            :param s3_error_output_prefix: The table specific S3 error output prefix. All the errors that occurred while delivering to this table will be prefixed with this value in S3 destination.
            :param unique_keys: A list of unique keys for a given Apache Iceberg table. Firehose will use these for running Create, Update, or Delete operations on the given Iceberg table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-destinationtableconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                destination_table_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DestinationTableConfigurationProperty(
                    destination_database_name="destinationDatabaseName",
                    destination_table_name="destinationTableName",
                    partition_spec=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.PartitionSpecProperty(
                        identity=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.PartitionFieldProperty(
                            source_name="sourceName"
                        )]
                    ),
                    s3_error_output_prefix="s3ErrorOutputPrefix",
                    unique_keys=["uniqueKeys"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e14427d07417bca7c3409605d1d312907aa3d97f9dd6921658bbc2fa9943bb9f)
                check_type(argname="argument destination_database_name", value=destination_database_name, expected_type=type_hints["destination_database_name"])
                check_type(argname="argument destination_table_name", value=destination_table_name, expected_type=type_hints["destination_table_name"])
                check_type(argname="argument partition_spec", value=partition_spec, expected_type=type_hints["partition_spec"])
                check_type(argname="argument s3_error_output_prefix", value=s3_error_output_prefix, expected_type=type_hints["s3_error_output_prefix"])
                check_type(argname="argument unique_keys", value=unique_keys, expected_type=type_hints["unique_keys"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_database_name is not None:
                self._values["destination_database_name"] = destination_database_name
            if destination_table_name is not None:
                self._values["destination_table_name"] = destination_table_name
            if partition_spec is not None:
                self._values["partition_spec"] = partition_spec
            if s3_error_output_prefix is not None:
                self._values["s3_error_output_prefix"] = s3_error_output_prefix
            if unique_keys is not None:
                self._values["unique_keys"] = unique_keys

        @builtins.property
        def destination_database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Apache Iceberg database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-destinationtableconfiguration.html#cfn-kinesisfirehose-deliverystream-destinationtableconfiguration-destinationdatabasename
            '''
            result = self._values.get("destination_database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_table_name(self) -> typing.Optional[builtins.str]:
            '''Specifies the name of the Apache Iceberg Table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-destinationtableconfiguration.html#cfn-kinesisfirehose-deliverystream-destinationtableconfiguration-destinationtablename
            '''
            result = self._values.get("destination_table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def partition_spec(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.PartitionSpecProperty"]]:
            '''The partition spec configuration for a table that is used by automatic table creation.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-destinationtableconfiguration.html#cfn-kinesisfirehose-deliverystream-destinationtableconfiguration-partitionspec
            '''
            result = self._values.get("partition_spec")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.PartitionSpecProperty"]], result)

        @builtins.property
        def s3_error_output_prefix(self) -> typing.Optional[builtins.str]:
            '''The table specific S3 error output prefix.

            All the errors that occurred while delivering to this table will be prefixed with this value in S3 destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-destinationtableconfiguration.html#cfn-kinesisfirehose-deliverystream-destinationtableconfiguration-s3erroroutputprefix
            '''
            result = self._values.get("s3_error_output_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unique_keys(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of unique keys for a given Apache Iceberg table.

            Firehose will use these for running Create, Update, or Delete operations on the given Iceberg table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-destinationtableconfiguration.html#cfn-kinesisfirehose-deliverystream-destinationtableconfiguration-uniquekeys
            '''
            result = self._values.get("unique_keys")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationTableConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.DirectPutSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"throughput_hint_in_m_bs": "throughputHintInMBs"},
    )
    class DirectPutSourceConfigurationProperty:
        def __init__(
            self,
            *,
            throughput_hint_in_m_bs: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The structure that configures parameters such as ``ThroughputHintInMBs`` for a stream configured with Direct PUT as a source.

            :param throughput_hint_in_m_bs: The value that you configure for this parameter is for information purpose only and does not affect Firehose delivery throughput limit. You can use the `Firehose Limits form <https://docs.aws.amazon.com/https://support.console.aws.amazon.com/support/home#/case/create%3FissueType=service-limit-increase%26limitType=kinesis-firehose-limits>`_ to request a throughput limit increase.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-directputsourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                direct_put_source_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DirectPutSourceConfigurationProperty(
                    throughput_hint_in_mBs=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e8359d3837050f0bfbac79499997adbd44e39b7302474919b1b41d654b09d651)
                check_type(argname="argument throughput_hint_in_m_bs", value=throughput_hint_in_m_bs, expected_type=type_hints["throughput_hint_in_m_bs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if throughput_hint_in_m_bs is not None:
                self._values["throughput_hint_in_m_bs"] = throughput_hint_in_m_bs

        @builtins.property
        def throughput_hint_in_m_bs(self) -> typing.Optional[jsii.Number]:
            '''The value that you configure for this parameter is for information purpose only and does not affect Firehose delivery throughput limit.

            You can use the `Firehose Limits form <https://docs.aws.amazon.com/https://support.console.aws.amazon.com/support/home#/case/create%3FissueType=service-limit-increase%26limitType=kinesis-firehose-limits>`_ to request a throughput limit increase.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-directputsourceconfiguration.html#cfn-kinesisfirehose-deliverystream-directputsourceconfiguration-throughputhintinmbs
            '''
            result = self._values.get("throughput_hint_in_m_bs")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DirectPutSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.DocumentIdOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"default_document_id_format": "defaultDocumentIdFormat"},
    )
    class DocumentIdOptionsProperty:
        def __init__(
            self,
            *,
            default_document_id_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Indicates the method for setting up document ID.

            The supported methods are Firehose generated document ID and OpenSearch Service generated document ID.

            :param default_document_id_format: When the ``FIREHOSE_DEFAULT`` option is chosen, Firehose generates a unique document ID for each record based on a unique internal identifier. The generated document ID is stable across multiple delivery attempts, which helps prevent the same record from being indexed multiple times with different document IDs. When the ``NO_DOCUMENT_ID`` option is chosen, Firehose does not include any document IDs in the requests it sends to the Amazon OpenSearch Service. This causes the Amazon OpenSearch Service domain to generate document IDs. In case of multiple delivery attempts, this may cause the same record to be indexed more than once with different document IDs. This option enables write-heavy operations, such as the ingestion of logs and observability data, to consume less resources in the Amazon OpenSearch Service domain, resulting in improved performance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-documentidoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                document_id_options_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DocumentIdOptionsProperty(
                    default_document_id_format="defaultDocumentIdFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b26a659e91deb4e511aaa9d98e27f7c04af731bbd5b6b2cefcc19e79737b4b2c)
                check_type(argname="argument default_document_id_format", value=default_document_id_format, expected_type=type_hints["default_document_id_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_document_id_format is not None:
                self._values["default_document_id_format"] = default_document_id_format

        @builtins.property
        def default_document_id_format(self) -> typing.Optional[builtins.str]:
            '''When the ``FIREHOSE_DEFAULT`` option is chosen, Firehose generates a unique document ID for each record based on a unique internal identifier.

            The generated document ID is stable across multiple delivery attempts, which helps prevent the same record from being indexed multiple times with different document IDs.

            When the ``NO_DOCUMENT_ID`` option is chosen, Firehose does not include any document IDs in the requests it sends to the Amazon OpenSearch Service. This causes the Amazon OpenSearch Service domain to generate document IDs. In case of multiple delivery attempts, this may cause the same record to be indexed more than once with different document IDs. This option enables write-heavy operations, such as the ingestion of logs and observability data, to consume less resources in the Amazon OpenSearch Service domain, resulting in improved performance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-documentidoptions.html#cfn-kinesisfirehose-deliverystream-documentidoptions-defaultdocumentidformat
            '''
            result = self._values.get("default_document_id_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentIdOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.DynamicPartitioningConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "retry_options": "retryOptions"},
    )
    class DynamicPartitioningConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.RetryOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``DynamicPartitioningConfiguration`` property type specifies the configuration of the dynamic partitioning mechanism that creates targeted data sets from the streaming data by partitioning it based on partition keys.

            :param enabled: Specifies whether dynamic partitioning is enabled for this Kinesis Data Firehose delivery stream.
            :param retry_options: Specifies the retry behavior in case Kinesis Data Firehose is unable to deliver data to an Amazon S3 prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-dynamicpartitioningconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                dynamic_partitioning_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DynamicPartitioningConfigurationProperty(
                    enabled=False,
                    retry_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.RetryOptionsProperty(
                        duration_in_seconds=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da020658709eee245354e7f069f003de29499203033f78755b5a8b912733f2f9)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if retry_options is not None:
                self._values["retry_options"] = retry_options

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether dynamic partitioning is enabled for this Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-dynamicpartitioningconfiguration.html#cfn-kinesisfirehose-deliverystream-dynamicpartitioningconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def retry_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.RetryOptionsProperty"]]:
            '''Specifies the retry behavior in case Kinesis Data Firehose is unable to deliver data to an Amazon S3 prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-dynamicpartitioningconfiguration.html#cfn-kinesisfirehose-deliverystream-dynamicpartitioningconfiguration-retryoptions
            '''
            result = self._values.get("retry_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.RetryOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamicPartitioningConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.ElasticsearchBufferingHintsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "interval_in_seconds": "intervalInSeconds",
            "size_in_m_bs": "sizeInMBs",
        },
    )
    class ElasticsearchBufferingHintsProperty:
        def __init__(
            self,
            *,
            interval_in_seconds: typing.Optional[jsii.Number] = None,
            size_in_m_bs: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ``ElasticsearchBufferingHints`` property type specifies how Amazon Kinesis Data Firehose (Kinesis Data Firehose) buffers incoming data while delivering it to the destination.

            The first buffer condition that is satisfied triggers Kinesis Data Firehose to deliver the data.

            ElasticsearchBufferingHints is the property type for the ``BufferingHints`` property of the `Amazon Kinesis Data Firehose DeliveryStream ElasticsearchDestinationConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html>`_ property type.

            :param interval_in_seconds: The length of time, in seconds, that Kinesis Data Firehose buffers incoming data before delivering it to the destination. For valid values, see the ``IntervalInSeconds`` content for the `BufferingHints <https://docs.aws.amazon.com/firehose/latest/APIReference/API_BufferingHints.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .
            :param size_in_m_bs: The size of the buffer, in MBs, that Kinesis Data Firehose uses for incoming data before delivering it to the destination. For valid values, see the ``SizeInMBs`` content for the `BufferingHints <https://docs.aws.amazon.com/firehose/latest/APIReference/API_BufferingHints.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchbufferinghints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                elasticsearch_buffering_hints_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ElasticsearchBufferingHintsProperty(
                    interval_in_seconds=123,
                    size_in_mBs=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1dd326602ce0a3bfa4a28c4673a090a746382a31023093312c23256f32aea3a9)
                check_type(argname="argument interval_in_seconds", value=interval_in_seconds, expected_type=type_hints["interval_in_seconds"])
                check_type(argname="argument size_in_m_bs", value=size_in_m_bs, expected_type=type_hints["size_in_m_bs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if interval_in_seconds is not None:
                self._values["interval_in_seconds"] = interval_in_seconds
            if size_in_m_bs is not None:
                self._values["size_in_m_bs"] = size_in_m_bs

        @builtins.property
        def interval_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The length of time, in seconds, that Kinesis Data Firehose buffers incoming data before delivering it to the destination.

            For valid values, see the ``IntervalInSeconds`` content for the `BufferingHints <https://docs.aws.amazon.com/firehose/latest/APIReference/API_BufferingHints.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchbufferinghints.html#cfn-kinesisfirehose-deliverystream-elasticsearchbufferinghints-intervalinseconds
            '''
            result = self._values.get("interval_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def size_in_m_bs(self) -> typing.Optional[jsii.Number]:
            '''The size of the buffer, in MBs, that Kinesis Data Firehose uses for incoming data before delivering it to the destination.

            For valid values, see the ``SizeInMBs`` content for the `BufferingHints <https://docs.aws.amazon.com/firehose/latest/APIReference/API_BufferingHints.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchbufferinghints.html#cfn-kinesisfirehose-deliverystream-elasticsearchbufferinghints-sizeinmbs
            '''
            result = self._values.get("size_in_m_bs")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticsearchBufferingHintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.ElasticsearchDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "buffering_hints": "bufferingHints",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "cluster_endpoint": "clusterEndpoint",
            "document_id_options": "documentIdOptions",
            "domain_arn": "domainArn",
            "index_name": "indexName",
            "index_rotation_period": "indexRotationPeriod",
            "processing_configuration": "processingConfiguration",
            "retry_options": "retryOptions",
            "role_arn": "roleArn",
            "s3_backup_mode": "s3BackupMode",
            "s3_configuration": "s3Configuration",
            "type_name": "typeName",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class ElasticsearchDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ElasticsearchBufferingHintsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cluster_endpoint: typing.Optional[builtins.str] = None,
            document_id_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.DocumentIdOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            domain_arn: typing.Optional[builtins.str] = None,
            index_name: typing.Optional[builtins.str] = None,
            index_rotation_period: typing.Optional[builtins.str] = None,
            processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ElasticsearchRetryOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            s3_backup_mode: typing.Optional[builtins.str] = None,
            s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type_name: typing.Optional[builtins.str] = None,
            vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``ElasticsearchDestinationConfiguration`` property type specifies an Amazon Elasticsearch Service (Amazon ES) domain that Amazon Kinesis Data Firehose (Kinesis Data Firehose) delivers data to.

            :param buffering_hints: Configures how Kinesis Data Firehose buffers incoming data while delivering it to the Amazon ES domain.
            :param cloud_watch_logging_options: The Amazon CloudWatch Logs logging options for the delivery stream.
            :param cluster_endpoint: The endpoint to use when communicating with the cluster. Specify either this ``ClusterEndpoint`` or the ``DomainARN`` field.
            :param document_id_options: Indicates the method for setting up document ID. The supported methods are Firehose generated document ID and OpenSearch Service generated document ID.
            :param domain_arn: The ARN of the Amazon ES domain. The IAM role must have permissions for ``DescribeElasticsearchDomain`` , ``DescribeElasticsearchDomains`` , and ``DescribeElasticsearchDomainConfig`` after assuming the role specified in *RoleARN* . Specify either ``ClusterEndpoint`` or ``DomainARN`` .
            :param index_name: The name of the Elasticsearch index to which Kinesis Data Firehose adds data for indexing.
            :param index_rotation_period: The frequency of Elasticsearch index rotation. If you enable index rotation, Kinesis Data Firehose appends a portion of the UTC arrival timestamp to the specified index name, and rotates the appended timestamp accordingly. For more information, see `Index Rotation for the Amazon ES Destination <https://docs.aws.amazon.com/firehose/latest/dev/basic-deliver.html#es-index-rotation>`_ in the *Amazon Kinesis Data Firehose Developer Guide* .
            :param processing_configuration: The data processing configuration for the Kinesis Data Firehose delivery stream.
            :param retry_options: The retry behavior when Kinesis Data Firehose is unable to deliver data to Amazon ES.
            :param role_arn: The Amazon Resource Name (ARN) of the IAM role to be assumed by Kinesis Data Firehose for calling the Amazon ES Configuration API and for indexing documents. For more information, see `Controlling Access with Amazon Kinesis Data Firehose <https://docs.aws.amazon.com/firehose/latest/dev/controlling-access.html>`_ .
            :param s3_backup_mode: The condition under which Kinesis Data Firehose delivers data to Amazon Simple Storage Service (Amazon S3). You can send Amazon S3 all documents (all data) or only the documents that Kinesis Data Firehose could not deliver to the Amazon ES destination. For more information and valid values, see the ``S3BackupMode`` content for the `ElasticsearchDestinationConfiguration <https://docs.aws.amazon.com/firehose/latest/APIReference/API_ElasticsearchDestinationConfiguration.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .
            :param s3_configuration: The S3 bucket where Kinesis Data Firehose backs up incoming data.
            :param type_name: The Elasticsearch type name that Amazon ES adds to documents when indexing data.
            :param vpc_configuration: The details of the VPC of the Amazon ES destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                elasticsearch_destination_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ElasticsearchDestinationConfigurationProperty(
                    buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ElasticsearchBufferingHintsProperty(
                        interval_in_seconds=123,
                        size_in_mBs=123
                    ),
                    cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                        enabled=False,
                        log_group_name="logGroupName",
                        log_stream_name="logStreamName"
                    ),
                    cluster_endpoint="clusterEndpoint",
                    document_id_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DocumentIdOptionsProperty(
                        default_document_id_format="defaultDocumentIdFormat"
                    ),
                    domain_arn="domainArn",
                    index_name="indexName",
                    index_rotation_period="indexRotationPeriod",
                    processing_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty(
                        enabled=False,
                        processors=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorProperty(
                            parameters=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorParameterProperty(
                                parameter_name="parameterName",
                                parameter_value="parameterValue"
                            )],
                            type="type"
                        )]
                    ),
                    retry_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ElasticsearchRetryOptionsProperty(
                        duration_in_seconds=123
                    ),
                    role_arn="roleArn",
                    s3_backup_mode="s3BackupMode",
                    s3_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty(
                        bucket_arn="bucketArn",
                        buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                            interval_in_seconds=123,
                            size_in_mBs=123
                        ),
                        cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                            enabled=False,
                            log_group_name="logGroupName",
                            log_stream_name="logStreamName"
                        ),
                        compression_format="compressionFormat",
                        encryption_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty(
                            kms_encryption_config=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty(
                                awskms_key_arn="awskmsKeyArn"
                            ),
                            no_encryption_config="noEncryptionConfig"
                        ),
                        error_output_prefix="errorOutputPrefix",
                        prefix="prefix",
                        role_arn="roleArn"
                    ),
                    type_name="typeName",
                    vpc_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.VpcConfigurationProperty(
                        role_arn="roleArn",
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e758896e5c6d2cc811d75e789db6e71a90c4b43e8a37a2666e4de6f0cc56d28)
                check_type(argname="argument buffering_hints", value=buffering_hints, expected_type=type_hints["buffering_hints"])
                check_type(argname="argument cloud_watch_logging_options", value=cloud_watch_logging_options, expected_type=type_hints["cloud_watch_logging_options"])
                check_type(argname="argument cluster_endpoint", value=cluster_endpoint, expected_type=type_hints["cluster_endpoint"])
                check_type(argname="argument document_id_options", value=document_id_options, expected_type=type_hints["document_id_options"])
                check_type(argname="argument domain_arn", value=domain_arn, expected_type=type_hints["domain_arn"])
                check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
                check_type(argname="argument index_rotation_period", value=index_rotation_period, expected_type=type_hints["index_rotation_period"])
                check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
                check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
                check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if buffering_hints is not None:
                self._values["buffering_hints"] = buffering_hints
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if cluster_endpoint is not None:
                self._values["cluster_endpoint"] = cluster_endpoint
            if document_id_options is not None:
                self._values["document_id_options"] = document_id_options
            if domain_arn is not None:
                self._values["domain_arn"] = domain_arn
            if index_name is not None:
                self._values["index_name"] = index_name
            if index_rotation_period is not None:
                self._values["index_rotation_period"] = index_rotation_period
            if processing_configuration is not None:
                self._values["processing_configuration"] = processing_configuration
            if retry_options is not None:
                self._values["retry_options"] = retry_options
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if s3_backup_mode is not None:
                self._values["s3_backup_mode"] = s3_backup_mode
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration
            if type_name is not None:
                self._values["type_name"] = type_name
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def buffering_hints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ElasticsearchBufferingHintsProperty"]]:
            '''Configures how Kinesis Data Firehose buffers incoming data while delivering it to the Amazon ES domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-bufferinghints
            '''
            result = self._values.get("buffering_hints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ElasticsearchBufferingHintsProperty"]], result)

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]]:
            '''The Amazon CloudWatch Logs logging options for the delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-cloudwatchloggingoptions
            '''
            result = self._values.get("cloud_watch_logging_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]], result)

        @builtins.property
        def cluster_endpoint(self) -> typing.Optional[builtins.str]:
            '''The endpoint to use when communicating with the cluster.

            Specify either this ``ClusterEndpoint`` or the ``DomainARN`` field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-clusterendpoint
            '''
            result = self._values.get("cluster_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_id_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DocumentIdOptionsProperty"]]:
            '''Indicates the method for setting up document ID.

            The supported methods are Firehose generated document ID and OpenSearch Service generated document ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-documentidoptions
            '''
            result = self._values.get("document_id_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DocumentIdOptionsProperty"]], result)

        @builtins.property
        def domain_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Amazon ES domain.

            The IAM role must have permissions for ``DescribeElasticsearchDomain`` , ``DescribeElasticsearchDomains`` , and ``DescribeElasticsearchDomainConfig`` after assuming the role specified in *RoleARN* .

            Specify either ``ClusterEndpoint`` or ``DomainARN`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-domainarn
            '''
            result = self._values.get("domain_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def index_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Elasticsearch index to which Kinesis Data Firehose adds data for indexing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-indexname
            '''
            result = self._values.get("index_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def index_rotation_period(self) -> typing.Optional[builtins.str]:
            '''The frequency of Elasticsearch index rotation.

            If you enable index rotation, Kinesis Data Firehose appends a portion of the UTC arrival timestamp to the specified index name, and rotates the appended timestamp accordingly. For more information, see `Index Rotation for the Amazon ES Destination <https://docs.aws.amazon.com/firehose/latest/dev/basic-deliver.html#es-index-rotation>`_ in the *Amazon Kinesis Data Firehose Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-indexrotationperiod
            '''
            result = self._values.get("index_rotation_period")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]]:
            '''The data processing configuration for the Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-processingconfiguration
            '''
            result = self._values.get("processing_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]], result)

        @builtins.property
        def retry_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ElasticsearchRetryOptionsProperty"]]:
            '''The retry behavior when Kinesis Data Firehose is unable to deliver data to Amazon ES.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-retryoptions
            '''
            result = self._values.get("retry_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ElasticsearchRetryOptionsProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role to be assumed by Kinesis Data Firehose for calling the Amazon ES Configuration API and for indexing documents.

            For more information, see `Controlling Access with Amazon Kinesis Data Firehose <https://docs.aws.amazon.com/firehose/latest/dev/controlling-access.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_backup_mode(self) -> typing.Optional[builtins.str]:
            '''The condition under which Kinesis Data Firehose delivers data to Amazon Simple Storage Service (Amazon S3).

            You can send Amazon S3 all documents (all data) or only the documents that Kinesis Data Firehose could not deliver to the Amazon ES destination. For more information and valid values, see the ``S3BackupMode`` content for the `ElasticsearchDestinationConfiguration <https://docs.aws.amazon.com/firehose/latest/APIReference/API_ElasticsearchDestinationConfiguration.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-s3backupmode
            '''
            result = self._values.get("s3_backup_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]]:
            '''The S3 bucket where Kinesis Data Firehose backs up incoming data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]], result)

        @builtins.property
        def type_name(self) -> typing.Optional[builtins.str]:
            '''The Elasticsearch type name that Amazon ES adds to documents when indexing data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-typename
            '''
            result = self._values.get("type_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.VpcConfigurationProperty"]]:
            '''The details of the VPC of the Amazon ES destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.VpcConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticsearchDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.ElasticsearchRetryOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_in_seconds": "durationInSeconds"},
    )
    class ElasticsearchRetryOptionsProperty:
        def __init__(
            self,
            *,
            duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ``ElasticsearchRetryOptions`` property type configures the retry behavior for when Amazon Kinesis Data Firehose (Kinesis Data Firehose) can't deliver data to Amazon Elasticsearch Service (Amazon ES).

            :param duration_in_seconds: After an initial failure to deliver to Amazon ES, the total amount of time during which Kinesis Data Firehose re-attempts delivery (including the first attempt). If Kinesis Data Firehose can't deliver the data within the specified time, it writes the data to the backup S3 bucket. For valid values, see the ``DurationInSeconds`` content for the `ElasticsearchRetryOptions <https://docs.aws.amazon.com/firehose/latest/APIReference/API_ElasticsearchRetryOptions.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchretryoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                elasticsearch_retry_options_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ElasticsearchRetryOptionsProperty(
                    duration_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ecb2ae54fc02aadbb409b34ba7a293998a2255ddc8ae87788aabaad6e6bdd4f1)
                check_type(argname="argument duration_in_seconds", value=duration_in_seconds, expected_type=type_hints["duration_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''After an initial failure to deliver to Amazon ES, the total amount of time during which Kinesis Data Firehose re-attempts delivery (including the first attempt).

            If Kinesis Data Firehose can't deliver the data within the specified time, it writes the data to the backup S3 bucket. For valid values, see the ``DurationInSeconds`` content for the `ElasticsearchRetryOptions <https://docs.aws.amazon.com/firehose/latest/APIReference/API_ElasticsearchRetryOptions.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchretryoptions.html#cfn-kinesisfirehose-deliverystream-elasticsearchretryoptions-durationinseconds
            '''
            result = self._values.get("duration_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticsearchRetryOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_encryption_config": "kmsEncryptionConfig",
            "no_encryption_config": "noEncryptionConfig",
        },
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            kms_encryption_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            no_encryption_config: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``EncryptionConfiguration`` property type specifies the encryption settings that Amazon Kinesis Data Firehose (Kinesis Data Firehose) uses when delivering data to Amazon Simple Storage Service (Amazon S3).

            :param kms_encryption_config: The AWS Key Management Service ( AWS KMS) encryption key that Amazon S3 uses to encrypt your data.
            :param no_encryption_config: Disables encryption. For valid values, see the ``NoEncryptionConfig`` content for the `EncryptionConfiguration <https://docs.aws.amazon.com/firehose/latest/APIReference/API_EncryptionConfiguration.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                encryption_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty(
                    kms_encryption_config=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty(
                        awskms_key_arn="awskmsKeyArn"
                    ),
                    no_encryption_config="noEncryptionConfig"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df3ed42571e6f72c9e4d45b76465b7ae84dd56832e0a18c86742253fe3a51fb6)
                check_type(argname="argument kms_encryption_config", value=kms_encryption_config, expected_type=type_hints["kms_encryption_config"])
                check_type(argname="argument no_encryption_config", value=no_encryption_config, expected_type=type_hints["no_encryption_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_encryption_config is not None:
                self._values["kms_encryption_config"] = kms_encryption_config
            if no_encryption_config is not None:
                self._values["no_encryption_config"] = no_encryption_config

        @builtins.property
        def kms_encryption_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty"]]:
            '''The AWS Key Management Service ( AWS KMS) encryption key that Amazon S3 uses to encrypt your data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-encryptionconfiguration.html#cfn-kinesisfirehose-deliverystream-encryptionconfiguration-kmsencryptionconfig
            '''
            result = self._values.get("kms_encryption_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty"]], result)

        @builtins.property
        def no_encryption_config(self) -> typing.Optional[builtins.str]:
            '''Disables encryption.

            For valid values, see the ``NoEncryptionConfig`` content for the `EncryptionConfiguration <https://docs.aws.amazon.com/firehose/latest/APIReference/API_EncryptionConfiguration.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-encryptionconfiguration.html#cfn-kinesisfirehose-deliverystream-encryptionconfiguration-noencryptionconfig
            '''
            result = self._values.get("no_encryption_config")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.ExtendedS3DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_arn": "bucketArn",
            "buffering_hints": "bufferingHints",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "compression_format": "compressionFormat",
            "custom_time_zone": "customTimeZone",
            "data_format_conversion_configuration": "dataFormatConversionConfiguration",
            "dynamic_partitioning_configuration": "dynamicPartitioningConfiguration",
            "encryption_configuration": "encryptionConfiguration",
            "error_output_prefix": "errorOutputPrefix",
            "file_extension": "fileExtension",
            "prefix": "prefix",
            "processing_configuration": "processingConfiguration",
            "role_arn": "roleArn",
            "s3_backup_configuration": "s3BackupConfiguration",
            "s3_backup_mode": "s3BackupMode",
        },
    )
    class ExtendedS3DestinationConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_arn: typing.Optional[builtins.str] = None,
            buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.BufferingHintsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            compression_format: typing.Optional[builtins.str] = None,
            custom_time_zone: typing.Optional[builtins.str] = None,
            data_format_conversion_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.DataFormatConversionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamic_partitioning_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.DynamicPartitioningConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            error_output_prefix: typing.Optional[builtins.str] = None,
            file_extension: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            s3_backup_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_backup_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ExtendedS3DestinationConfiguration`` property type configures an Amazon S3 destination for an Amazon Kinesis Data Firehose delivery stream.

            :param bucket_arn: The Amazon Resource Name (ARN) of the Amazon S3 bucket. For constraints, see `ExtendedS3DestinationConfiguration <https://docs.aws.amazon.com/firehose/latest/APIReference/API_ExtendedS3DestinationConfiguration.html>`_ in the *Amazon Kinesis Data Firehose API Reference* .
            :param buffering_hints: The buffering option.
            :param cloud_watch_logging_options: The Amazon CloudWatch logging options for your Firehose stream.
            :param compression_format: The compression format. If no value is specified, the default is ``UNCOMPRESSED`` .
            :param custom_time_zone: The time zone you prefer. UTC is the default.
            :param data_format_conversion_configuration: The serializer, deserializer, and schema for converting data from the JSON format to the Parquet or ORC format before writing it to Amazon S3.
            :param dynamic_partitioning_configuration: The configuration of the dynamic partitioning mechanism that creates targeted data sets from the streaming data by partitioning it based on partition keys.
            :param encryption_configuration: The encryption configuration for the Kinesis Data Firehose delivery stream. The default value is ``NoEncryption`` .
            :param error_output_prefix: A prefix that Kinesis Data Firehose evaluates and adds to failed records before writing them to S3. This prefix appears immediately following the bucket name. For information about how to specify this prefix, see `Custom Prefixes for Amazon S3 Objects <https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html>`_ .
            :param file_extension: Specify a file extension. It will override the default file extension
            :param prefix: The ``YYYY/MM/DD/HH`` time format prefix is automatically used for delivered Amazon S3 files. For more information, see `ExtendedS3DestinationConfiguration <https://docs.aws.amazon.com/firehose/latest/APIReference/API_ExtendedS3DestinationConfiguration.html>`_ in the *Amazon Kinesis Data Firehose API Reference* .
            :param processing_configuration: The data processing configuration for the Kinesis Data Firehose delivery stream.
            :param role_arn: The Amazon Resource Name (ARN) of the AWS credentials. For constraints, see `ExtendedS3DestinationConfiguration <https://docs.aws.amazon.com/firehose/latest/APIReference/API_ExtendedS3DestinationConfiguration.html>`_ in the *Amazon Kinesis Data Firehose API Reference* .
            :param s3_backup_configuration: The configuration for backup in Amazon S3.
            :param s3_backup_mode: The Amazon S3 backup mode. After you create a Firehose stream, you can update it to enable Amazon S3 backup if it is disabled. If backup is enabled, you can't update the Firehose stream to disable it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                extended_s3_destination_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ExtendedS3DestinationConfigurationProperty(
                    bucket_arn="bucketArn",
                    buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                        interval_in_seconds=123,
                        size_in_mBs=123
                    ),
                    cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                        enabled=False,
                        log_group_name="logGroupName",
                        log_stream_name="logStreamName"
                    ),
                    compression_format="compressionFormat",
                    custom_time_zone="customTimeZone",
                    data_format_conversion_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DataFormatConversionConfigurationProperty(
                        enabled=False,
                        input_format_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.InputFormatConfigurationProperty(
                            deserializer=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DeserializerProperty(
                                hive_json_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.HiveJsonSerDeProperty(
                                    timestamp_formats=["timestampFormats"]
                                ),
                                open_xJson_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.OpenXJsonSerDeProperty(
                                    case_insensitive=False,
                                    column_to_json_key_mappings={
                                        "column_to_json_key_mappings_key": "columnToJsonKeyMappings"
                                    },
                                    convert_dots_in_json_keys_to_underscores=False
                                )
                            )
                        ),
                        output_format_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.OutputFormatConfigurationProperty(
                            serializer=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SerializerProperty(
                                orc_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.OrcSerDeProperty(
                                    block_size_bytes=123,
                                    bloom_filter_columns=["bloomFilterColumns"],
                                    bloom_filter_false_positive_probability=123,
                                    compression="compression",
                                    dictionary_key_threshold=123,
                                    enable_padding=False,
                                    format_version="formatVersion",
                                    padding_tolerance=123,
                                    row_index_stride=123,
                                    stripe_size_bytes=123
                                ),
                                parquet_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ParquetSerDeProperty(
                                    block_size_bytes=123,
                                    compression="compression",
                                    enable_dictionary_compression=False,
                                    max_padding_bytes=123,
                                    page_size_bytes=123,
                                    writer_version="writerVersion"
                                )
                            )
                        ),
                        schema_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SchemaConfigurationProperty(
                            catalog_id="catalogId",
                            database_name="databaseName",
                            region="region",
                            role_arn="roleArn",
                            table_name="tableName",
                            version_id="versionId"
                        )
                    ),
                    dynamic_partitioning_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DynamicPartitioningConfigurationProperty(
                        enabled=False,
                        retry_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.RetryOptionsProperty(
                            duration_in_seconds=123
                        )
                    ),
                    encryption_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty(
                        kms_encryption_config=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty(
                            awskms_key_arn="awskmsKeyArn"
                        ),
                        no_encryption_config="noEncryptionConfig"
                    ),
                    error_output_prefix="errorOutputPrefix",
                    file_extension="fileExtension",
                    prefix="prefix",
                    processing_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty(
                        enabled=False,
                        processors=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorProperty(
                            parameters=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorParameterProperty(
                                parameter_name="parameterName",
                                parameter_value="parameterValue"
                            )],
                            type="type"
                        )]
                    ),
                    role_arn="roleArn",
                    s3_backup_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty(
                        bucket_arn="bucketArn",
                        buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                            interval_in_seconds=123,
                            size_in_mBs=123
                        ),
                        cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                            enabled=False,
                            log_group_name="logGroupName",
                            log_stream_name="logStreamName"
                        ),
                        compression_format="compressionFormat",
                        encryption_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty(
                            kms_encryption_config=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty(
                                awskms_key_arn="awskmsKeyArn"
                            ),
                            no_encryption_config="noEncryptionConfig"
                        ),
                        error_output_prefix="errorOutputPrefix",
                        prefix="prefix",
                        role_arn="roleArn"
                    ),
                    s3_backup_mode="s3BackupMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__783224085a9beea0c0bf1d18af7f323550d4f27129019a5acbffc4a824b045b8)
                check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
                check_type(argname="argument buffering_hints", value=buffering_hints, expected_type=type_hints["buffering_hints"])
                check_type(argname="argument cloud_watch_logging_options", value=cloud_watch_logging_options, expected_type=type_hints["cloud_watch_logging_options"])
                check_type(argname="argument compression_format", value=compression_format, expected_type=type_hints["compression_format"])
                check_type(argname="argument custom_time_zone", value=custom_time_zone, expected_type=type_hints["custom_time_zone"])
                check_type(argname="argument data_format_conversion_configuration", value=data_format_conversion_configuration, expected_type=type_hints["data_format_conversion_configuration"])
                check_type(argname="argument dynamic_partitioning_configuration", value=dynamic_partitioning_configuration, expected_type=type_hints["dynamic_partitioning_configuration"])
                check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
                check_type(argname="argument error_output_prefix", value=error_output_prefix, expected_type=type_hints["error_output_prefix"])
                check_type(argname="argument file_extension", value=file_extension, expected_type=type_hints["file_extension"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument s3_backup_configuration", value=s3_backup_configuration, expected_type=type_hints["s3_backup_configuration"])
                check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_arn is not None:
                self._values["bucket_arn"] = bucket_arn
            if buffering_hints is not None:
                self._values["buffering_hints"] = buffering_hints
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if compression_format is not None:
                self._values["compression_format"] = compression_format
            if custom_time_zone is not None:
                self._values["custom_time_zone"] = custom_time_zone
            if data_format_conversion_configuration is not None:
                self._values["data_format_conversion_configuration"] = data_format_conversion_configuration
            if dynamic_partitioning_configuration is not None:
                self._values["dynamic_partitioning_configuration"] = dynamic_partitioning_configuration
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if error_output_prefix is not None:
                self._values["error_output_prefix"] = error_output_prefix
            if file_extension is not None:
                self._values["file_extension"] = file_extension
            if prefix is not None:
                self._values["prefix"] = prefix
            if processing_configuration is not None:
                self._values["processing_configuration"] = processing_configuration
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if s3_backup_configuration is not None:
                self._values["s3_backup_configuration"] = s3_backup_configuration
            if s3_backup_mode is not None:
                self._values["s3_backup_mode"] = s3_backup_mode

        @builtins.property
        def bucket_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon S3 bucket.

            For constraints, see `ExtendedS3DestinationConfiguration <https://docs.aws.amazon.com/firehose/latest/APIReference/API_ExtendedS3DestinationConfiguration.html>`_ in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-bucketarn
            '''
            result = self._values.get("bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def buffering_hints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.BufferingHintsProperty"]]:
            '''The buffering option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-bufferinghints
            '''
            result = self._values.get("buffering_hints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.BufferingHintsProperty"]], result)

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]]:
            '''The Amazon CloudWatch logging options for your Firehose stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-cloudwatchloggingoptions
            '''
            result = self._values.get("cloud_watch_logging_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]], result)

        @builtins.property
        def compression_format(self) -> typing.Optional[builtins.str]:
            '''The compression format.

            If no value is specified, the default is ``UNCOMPRESSED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-compressionformat
            '''
            result = self._values.get("compression_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_time_zone(self) -> typing.Optional[builtins.str]:
            '''The time zone you prefer.

            UTC is the default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-customtimezone
            '''
            result = self._values.get("custom_time_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_format_conversion_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DataFormatConversionConfigurationProperty"]]:
            '''The serializer, deserializer, and schema for converting data from the JSON format to the Parquet or ORC format before writing it to Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-dataformatconversionconfiguration
            '''
            result = self._values.get("data_format_conversion_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DataFormatConversionConfigurationProperty"]], result)

        @builtins.property
        def dynamic_partitioning_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DynamicPartitioningConfigurationProperty"]]:
            '''The configuration of the dynamic partitioning mechanism that creates targeted data sets from the streaming data by partitioning it based on partition keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-dynamicpartitioningconfiguration
            '''
            result = self._values.get("dynamic_partitioning_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DynamicPartitioningConfigurationProperty"]], result)

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty"]]:
            '''The encryption configuration for the Kinesis Data Firehose delivery stream.

            The default value is ``NoEncryption`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty"]], result)

        @builtins.property
        def error_output_prefix(self) -> typing.Optional[builtins.str]:
            '''A prefix that Kinesis Data Firehose evaluates and adds to failed records before writing them to S3.

            This prefix appears immediately following the bucket name. For information about how to specify this prefix, see `Custom Prefixes for Amazon S3 Objects <https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-erroroutputprefix
            '''
            result = self._values.get("error_output_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_extension(self) -> typing.Optional[builtins.str]:
            '''Specify a file extension.

            It will override the default file extension

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-fileextension
            '''
            result = self._values.get("file_extension")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The ``YYYY/MM/DD/HH`` time format prefix is automatically used for delivered Amazon S3 files.

            For more information, see `ExtendedS3DestinationConfiguration <https://docs.aws.amazon.com/firehose/latest/APIReference/API_ExtendedS3DestinationConfiguration.html>`_ in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]]:
            '''The data processing configuration for the Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-processingconfiguration
            '''
            result = self._values.get("processing_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS credentials.

            For constraints, see `ExtendedS3DestinationConfiguration <https://docs.aws.amazon.com/firehose/latest/APIReference/API_ExtendedS3DestinationConfiguration.html>`_ in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_backup_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]]:
            '''The configuration for backup in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-s3backupconfiguration
            '''
            result = self._values.get("s3_backup_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]], result)

        @builtins.property
        def s3_backup_mode(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 backup mode.

            After you create a Firehose stream, you can update it to enable Amazon S3 backup if it is disabled. If backup is enabled, you can't update the Firehose stream to disable it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-s3backupmode
            '''
            result = self._values.get("s3_backup_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExtendedS3DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.HiveJsonSerDeProperty",
        jsii_struct_bases=[],
        name_mapping={"timestamp_formats": "timestampFormats"},
    )
    class HiveJsonSerDeProperty:
        def __init__(
            self,
            *,
            timestamp_formats: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The native Hive / HCatalog JsonSerDe.

            Used by Firehose for deserializing data, which means converting it from the JSON format in preparation for serializing it to the Parquet or ORC format. This is one of two deserializers you can choose, depending on which one offers the functionality you need. The other option is the OpenX SerDe.

            :param timestamp_formats: Indicates how you want Firehose to parse the date and timestamps that may be present in your input data JSON. To specify these format strings, follow the pattern syntax of JodaTime's DateTimeFormat format strings. For more information, see `Class DateTimeFormat <https://docs.aws.amazon.com/https://www.joda.org/joda-time/apidocs/org/joda/time/format/DateTimeFormat.html>`_ . You can also use the special value ``millis`` to parse timestamps in epoch milliseconds. If you don't specify a format, Firehose uses ``java.sql.Timestamp::valueOf`` by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-hivejsonserde.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                hive_json_ser_de_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.HiveJsonSerDeProperty(
                    timestamp_formats=["timestampFormats"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__06f96536e5b07af8c6034535dc2d34e07cb2a64a75d72884557760c3bca1cf51)
                check_type(argname="argument timestamp_formats", value=timestamp_formats, expected_type=type_hints["timestamp_formats"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if timestamp_formats is not None:
                self._values["timestamp_formats"] = timestamp_formats

        @builtins.property
        def timestamp_formats(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Indicates how you want Firehose to parse the date and timestamps that may be present in your input data JSON.

            To specify these format strings, follow the pattern syntax of JodaTime's DateTimeFormat format strings. For more information, see `Class DateTimeFormat <https://docs.aws.amazon.com/https://www.joda.org/joda-time/apidocs/org/joda/time/format/DateTimeFormat.html>`_ . You can also use the special value ``millis`` to parse timestamps in epoch milliseconds. If you don't specify a format, Firehose uses ``java.sql.Timestamp::valueOf`` by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-hivejsonserde.html#cfn-kinesisfirehose-deliverystream-hivejsonserde-timestampformats
            '''
            result = self._values.get("timestamp_formats")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HiveJsonSerDeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.HttpEndpointCommonAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_name": "attributeName",
            "attribute_value": "attributeValue",
        },
    )
    class HttpEndpointCommonAttributeProperty:
        def __init__(
            self,
            *,
            attribute_name: typing.Optional[builtins.str] = None,
            attribute_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the metadata that's delivered to the specified HTTP endpoint destination.

            Kinesis Firehose supports any custom HTTP endpoint or HTTP endpoints owned by supported third-party service providers, including Datadog, MongoDB, and New Relic.

            :param attribute_name: The name of the HTTP endpoint common attribute.
            :param attribute_value: The value of the HTTP endpoint common attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointcommonattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                http_endpoint_common_attribute_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.HttpEndpointCommonAttributeProperty(
                    attribute_name="attributeName",
                    attribute_value="attributeValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4edb9d800e8ba6e4158e24c690839eb7e60e776714ef44debb554ac4413f82c)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument attribute_value", value=attribute_value, expected_type=type_hints["attribute_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_name is not None:
                self._values["attribute_name"] = attribute_name
            if attribute_value is not None:
                self._values["attribute_value"] = attribute_value

        @builtins.property
        def attribute_name(self) -> typing.Optional[builtins.str]:
            '''The name of the HTTP endpoint common attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointcommonattribute.html#cfn-kinesisfirehose-deliverystream-httpendpointcommonattribute-attributename
            '''
            result = self._values.get("attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def attribute_value(self) -> typing.Optional[builtins.str]:
            '''The value of the HTTP endpoint common attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointcommonattribute.html#cfn-kinesisfirehose-deliverystream-httpendpointcommonattribute-attributevalue
            '''
            result = self._values.get("attribute_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpEndpointCommonAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.HttpEndpointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"access_key": "accessKey", "name": "name", "url": "url"},
    )
    class HttpEndpointConfigurationProperty:
        def __init__(
            self,
            *,
            access_key: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the configuration of the HTTP endpoint to which Kinesis Firehose delivers data.

            Kinesis Firehose supports any custom HTTP endpoint or HTTP endpoints owned by supported third-party service providers, including Datadog, MongoDB, and New Relic.

            :param access_key: The access key required for Kinesis Firehose to authenticate with the HTTP endpoint selected as the destination.
            :param name: The name of the HTTP endpoint selected as the destination.
            :param url: The URL of the HTTP endpoint selected as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                http_endpoint_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.HttpEndpointConfigurationProperty(
                    access_key="accessKey",
                    name="name",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a27147991fe833129ea69f6d7a7cefc90065b062c44845b4a298e22c26e4c6c)
                check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_key is not None:
                self._values["access_key"] = access_key
            if name is not None:
                self._values["name"] = name
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def access_key(self) -> typing.Optional[builtins.str]:
            '''The access key required for Kinesis Firehose to authenticate with the HTTP endpoint selected as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointconfiguration-accesskey
            '''
            result = self._values.get("access_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the HTTP endpoint selected as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL of the HTTP endpoint selected as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointconfiguration-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpEndpointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.HttpEndpointDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "buffering_hints": "bufferingHints",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "endpoint_configuration": "endpointConfiguration",
            "processing_configuration": "processingConfiguration",
            "request_configuration": "requestConfiguration",
            "retry_options": "retryOptions",
            "role_arn": "roleArn",
            "s3_backup_mode": "s3BackupMode",
            "s3_configuration": "s3Configuration",
            "secrets_manager_configuration": "secretsManagerConfiguration",
        },
    )
    class HttpEndpointDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.BufferingHintsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.HttpEndpointConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            request_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.HttpEndpointRequestConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.RetryOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            s3_backup_mode: typing.Optional[builtins.str] = None,
            s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secrets_manager_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the configuration of the HTTP endpoint destination.

            Kinesis Firehose supports any custom HTTP endpoint or HTTP endpoints owned by supported third-party service providers, including Datadog, MongoDB, and New Relic.

            :param buffering_hints: The buffering options that can be used before data is delivered to the specified destination. Kinesis Data Firehose treats these options as hints, and it might choose to use more optimal values. The SizeInMBs and IntervalInSeconds parameters are optional. However, if you specify a value for one of them, you must also provide a value for the other.
            :param cloud_watch_logging_options: Describes the Amazon CloudWatch logging options for your delivery stream.
            :param endpoint_configuration: The configuration of the HTTP endpoint selected as the destination.
            :param processing_configuration: Describes the data processing configuration.
            :param request_configuration: The configuration of the request sent to the HTTP endpoint specified as the destination.
            :param retry_options: Describes the retry behavior in case Kinesis Data Firehose is unable to deliver data to the specified HTTP endpoint destination, or if it doesn't receive a valid acknowledgment of receipt from the specified HTTP endpoint destination.
            :param role_arn: Kinesis Data Firehose uses this IAM role for all the permissions that the delivery stream needs.
            :param s3_backup_mode: Describes the S3 bucket backup options for the data that Kinesis Data Firehose delivers to the HTTP endpoint destination. You can back up all documents (AllData) or only the documents that Kinesis Data Firehose could not deliver to the specified HTTP endpoint destination (FailedDataOnly).
            :param s3_configuration: Describes the configuration of a destination in Amazon S3.
            :param secrets_manager_configuration: The configuration that defines how you access secrets for HTTP Endpoint destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                http_endpoint_destination_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.HttpEndpointDestinationConfigurationProperty(
                    buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                        interval_in_seconds=123,
                        size_in_mBs=123
                    ),
                    cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                        enabled=False,
                        log_group_name="logGroupName",
                        log_stream_name="logStreamName"
                    ),
                    endpoint_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.HttpEndpointConfigurationProperty(
                        access_key="accessKey",
                        name="name",
                        url="url"
                    ),
                    processing_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty(
                        enabled=False,
                        processors=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorProperty(
                            parameters=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorParameterProperty(
                                parameter_name="parameterName",
                                parameter_value="parameterValue"
                            )],
                            type="type"
                        )]
                    ),
                    request_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.HttpEndpointRequestConfigurationProperty(
                        common_attributes=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.HttpEndpointCommonAttributeProperty(
                            attribute_name="attributeName",
                            attribute_value="attributeValue"
                        )],
                        content_encoding="contentEncoding"
                    ),
                    retry_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.RetryOptionsProperty(
                        duration_in_seconds=123
                    ),
                    role_arn="roleArn",
                    s3_backup_mode="s3BackupMode",
                    s3_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty(
                        bucket_arn="bucketArn",
                        buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                            interval_in_seconds=123,
                            size_in_mBs=123
                        ),
                        cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                            enabled=False,
                            log_group_name="logGroupName",
                            log_stream_name="logStreamName"
                        ),
                        compression_format="compressionFormat",
                        encryption_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty(
                            kms_encryption_config=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty(
                                awskms_key_arn="awskmsKeyArn"
                            ),
                            no_encryption_config="noEncryptionConfig"
                        ),
                        error_output_prefix="errorOutputPrefix",
                        prefix="prefix",
                        role_arn="roleArn"
                    ),
                    secrets_manager_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty(
                        enabled=False,
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__408127f0c8f8f8991159f30f915de3bd00746a74983ffb0a2aa1cc3f9e7370dc)
                check_type(argname="argument buffering_hints", value=buffering_hints, expected_type=type_hints["buffering_hints"])
                check_type(argname="argument cloud_watch_logging_options", value=cloud_watch_logging_options, expected_type=type_hints["cloud_watch_logging_options"])
                check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
                check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
                check_type(argname="argument request_configuration", value=request_configuration, expected_type=type_hints["request_configuration"])
                check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
                check_type(argname="argument secrets_manager_configuration", value=secrets_manager_configuration, expected_type=type_hints["secrets_manager_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if buffering_hints is not None:
                self._values["buffering_hints"] = buffering_hints
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if endpoint_configuration is not None:
                self._values["endpoint_configuration"] = endpoint_configuration
            if processing_configuration is not None:
                self._values["processing_configuration"] = processing_configuration
            if request_configuration is not None:
                self._values["request_configuration"] = request_configuration
            if retry_options is not None:
                self._values["retry_options"] = retry_options
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if s3_backup_mode is not None:
                self._values["s3_backup_mode"] = s3_backup_mode
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration
            if secrets_manager_configuration is not None:
                self._values["secrets_manager_configuration"] = secrets_manager_configuration

        @builtins.property
        def buffering_hints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.BufferingHintsProperty"]]:
            '''The buffering options that can be used before data is delivered to the specified destination.

            Kinesis Data Firehose treats these options as hints, and it might choose to use more optimal values. The SizeInMBs and IntervalInSeconds parameters are optional. However, if you specify a value for one of them, you must also provide a value for the other.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-bufferinghints
            '''
            result = self._values.get("buffering_hints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.BufferingHintsProperty"]], result)

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]]:
            '''Describes the Amazon CloudWatch logging options for your delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-cloudwatchloggingoptions
            '''
            result = self._values.get("cloud_watch_logging_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]], result)

        @builtins.property
        def endpoint_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.HttpEndpointConfigurationProperty"]]:
            '''The configuration of the HTTP endpoint selected as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-endpointconfiguration
            '''
            result = self._values.get("endpoint_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.HttpEndpointConfigurationProperty"]], result)

        @builtins.property
        def processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]]:
            '''Describes the data processing configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-processingconfiguration
            '''
            result = self._values.get("processing_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]], result)

        @builtins.property
        def request_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.HttpEndpointRequestConfigurationProperty"]]:
            '''The configuration of the request sent to the HTTP endpoint specified as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-requestconfiguration
            '''
            result = self._values.get("request_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.HttpEndpointRequestConfigurationProperty"]], result)

        @builtins.property
        def retry_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.RetryOptionsProperty"]]:
            '''Describes the retry behavior in case Kinesis Data Firehose is unable to deliver data to the specified HTTP endpoint destination, or if it doesn't receive a valid acknowledgment of receipt from the specified HTTP endpoint destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-retryoptions
            '''
            result = self._values.get("retry_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.RetryOptionsProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''Kinesis Data Firehose uses this IAM role for all the permissions that the delivery stream needs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_backup_mode(self) -> typing.Optional[builtins.str]:
            '''Describes the S3 bucket backup options for the data that Kinesis Data Firehose delivers to the HTTP endpoint destination.

            You can back up all documents (AllData) or only the documents that Kinesis Data Firehose could not deliver to the specified HTTP endpoint destination (FailedDataOnly).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-s3backupmode
            '''
            result = self._values.get("s3_backup_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]]:
            '''Describes the configuration of a destination in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]], result)

        @builtins.property
        def secrets_manager_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty"]]:
            '''The configuration that defines how you access secrets for HTTP Endpoint destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-secretsmanagerconfiguration
            '''
            result = self._values.get("secrets_manager_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpEndpointDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.HttpEndpointRequestConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "common_attributes": "commonAttributes",
            "content_encoding": "contentEncoding",
        },
    )
    class HttpEndpointRequestConfigurationProperty:
        def __init__(
            self,
            *,
            common_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.HttpEndpointCommonAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            content_encoding: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration of the HTTP endpoint request.

            Kinesis Firehose supports any custom HTTP endpoint or HTTP endpoints owned by supported third-party service providers, including Datadog, MongoDB, and New Relic.

            :param common_attributes: Describes the metadata sent to the HTTP endpoint destination.
            :param content_encoding: Kinesis Data Firehose uses the content encoding to compress the body of a request before sending the request to the destination. For more information, see Content-Encoding in MDN Web Docs, the official Mozilla documentation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointrequestconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                http_endpoint_request_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.HttpEndpointRequestConfigurationProperty(
                    common_attributes=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.HttpEndpointCommonAttributeProperty(
                        attribute_name="attributeName",
                        attribute_value="attributeValue"
                    )],
                    content_encoding="contentEncoding"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f55892b449de511d63fc261df45a89c9ca758f86f38e3116791efec394ea487)
                check_type(argname="argument common_attributes", value=common_attributes, expected_type=type_hints["common_attributes"])
                check_type(argname="argument content_encoding", value=content_encoding, expected_type=type_hints["content_encoding"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if common_attributes is not None:
                self._values["common_attributes"] = common_attributes
            if content_encoding is not None:
                self._values["content_encoding"] = content_encoding

        @builtins.property
        def common_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.HttpEndpointCommonAttributeProperty"]]]]:
            '''Describes the metadata sent to the HTTP endpoint destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointrequestconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointrequestconfiguration-commonattributes
            '''
            result = self._values.get("common_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.HttpEndpointCommonAttributeProperty"]]]], result)

        @builtins.property
        def content_encoding(self) -> typing.Optional[builtins.str]:
            '''Kinesis Data Firehose uses the content encoding to compress the body of a request before sending the request to the destination.

            For more information, see Content-Encoding in MDN Web Docs, the official Mozilla documentation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointrequestconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointrequestconfiguration-contentencoding
            '''
            result = self._values.get("content_encoding")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpEndpointRequestConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.IcebergDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "append_only": "appendOnly",
            "buffering_hints": "bufferingHints",
            "catalog_configuration": "catalogConfiguration",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "destination_table_configuration_list": "destinationTableConfigurationList",
            "processing_configuration": "processingConfiguration",
            "retry_options": "retryOptions",
            "role_arn": "roleArn",
            "s3_backup_mode": "s3BackupMode",
            "s3_configuration": "s3Configuration",
            "schema_evolution_configuration": "schemaEvolutionConfiguration",
            "table_creation_configuration": "tableCreationConfiguration",
        },
    )
    class IcebergDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            append_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.BufferingHintsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            catalog_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.CatalogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            destination_table_configuration_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.DestinationTableConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.RetryOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            s3_backup_mode: typing.Optional[builtins.str] = None,
            s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            schema_evolution_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SchemaEvolutionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_creation_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.TableCreationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the destination configure settings for Apache Iceberg Table.

            :param append_only: Describes whether all incoming data for this delivery stream will be append only (inserts only and not for updates and deletes) for Iceberg delivery. This feature is only applicable for Apache Iceberg Tables. The default value is false. If you set this value to true, Firehose automatically increases the throughput limit of a stream based on the throttling levels of the stream. If you set this parameter to true for a stream with updates and deletes, you will see out of order delivery.
            :param buffering_hints: 
            :param catalog_configuration: Configuration describing where the destination Apache Iceberg Tables are persisted.
            :param cloud_watch_logging_options: 
            :param destination_table_configuration_list: Provides a list of ``DestinationTableConfigurations`` which Firehose uses to deliver data to Apache Iceberg Tables. Firehose will write data with insert if table specific configuration is not provided here.
            :param processing_configuration: 
            :param retry_options: 
            :param role_arn: The Amazon Resource Name (ARN) of the IAM role to be assumed by Firehose for calling Apache Iceberg Tables.
            :param s3_backup_mode: Describes how Firehose will backup records. Currently,S3 backup only supports ``FailedDataOnly`` .
            :param s3_configuration: 
            :param schema_evolution_configuration: The configuration to enable automatic schema evolution. Amazon Data Firehose is in preview release and is subject to change.
            :param table_creation_configuration: The configuration to enable automatic table creation. Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-icebergdestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                iceberg_destination_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.IcebergDestinationConfigurationProperty(
                    append_only=False,
                    buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                        interval_in_seconds=123,
                        size_in_mBs=123
                    ),
                    catalog_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CatalogConfigurationProperty(
                        catalog_arn="catalogArn",
                        warehouse_location="warehouseLocation"
                    ),
                    cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                        enabled=False,
                        log_group_name="logGroupName",
                        log_stream_name="logStreamName"
                    ),
                    destination_table_configuration_list=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DestinationTableConfigurationProperty(
                        destination_database_name="destinationDatabaseName",
                        destination_table_name="destinationTableName",
                        partition_spec=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.PartitionSpecProperty(
                            identity=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.PartitionFieldProperty(
                                source_name="sourceName"
                            )]
                        ),
                        s3_error_output_prefix="s3ErrorOutputPrefix",
                        unique_keys=["uniqueKeys"]
                    )],
                    processing_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty(
                        enabled=False,
                        processors=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorProperty(
                            parameters=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorParameterProperty(
                                parameter_name="parameterName",
                                parameter_value="parameterValue"
                            )],
                            type="type"
                        )]
                    ),
                    retry_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.RetryOptionsProperty(
                        duration_in_seconds=123
                    ),
                    role_arn="roleArn",
                    s3_backup_mode="s3BackupMode",
                    s3_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty(
                        bucket_arn="bucketArn",
                        buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                            interval_in_seconds=123,
                            size_in_mBs=123
                        ),
                        cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                            enabled=False,
                            log_group_name="logGroupName",
                            log_stream_name="logStreamName"
                        ),
                        compression_format="compressionFormat",
                        encryption_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty(
                            kms_encryption_config=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty(
                                awskms_key_arn="awskmsKeyArn"
                            ),
                            no_encryption_config="noEncryptionConfig"
                        ),
                        error_output_prefix="errorOutputPrefix",
                        prefix="prefix",
                        role_arn="roleArn"
                    ),
                    schema_evolution_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SchemaEvolutionConfigurationProperty(
                        enabled=False
                    ),
                    table_creation_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.TableCreationConfigurationProperty(
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6843d5d2d59f1c09726ccf87bca481d0bb15582abb898da8a2a6ff989ed4ef17)
                check_type(argname="argument append_only", value=append_only, expected_type=type_hints["append_only"])
                check_type(argname="argument buffering_hints", value=buffering_hints, expected_type=type_hints["buffering_hints"])
                check_type(argname="argument catalog_configuration", value=catalog_configuration, expected_type=type_hints["catalog_configuration"])
                check_type(argname="argument cloud_watch_logging_options", value=cloud_watch_logging_options, expected_type=type_hints["cloud_watch_logging_options"])
                check_type(argname="argument destination_table_configuration_list", value=destination_table_configuration_list, expected_type=type_hints["destination_table_configuration_list"])
                check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
                check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
                check_type(argname="argument schema_evolution_configuration", value=schema_evolution_configuration, expected_type=type_hints["schema_evolution_configuration"])
                check_type(argname="argument table_creation_configuration", value=table_creation_configuration, expected_type=type_hints["table_creation_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if append_only is not None:
                self._values["append_only"] = append_only
            if buffering_hints is not None:
                self._values["buffering_hints"] = buffering_hints
            if catalog_configuration is not None:
                self._values["catalog_configuration"] = catalog_configuration
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if destination_table_configuration_list is not None:
                self._values["destination_table_configuration_list"] = destination_table_configuration_list
            if processing_configuration is not None:
                self._values["processing_configuration"] = processing_configuration
            if retry_options is not None:
                self._values["retry_options"] = retry_options
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if s3_backup_mode is not None:
                self._values["s3_backup_mode"] = s3_backup_mode
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration
            if schema_evolution_configuration is not None:
                self._values["schema_evolution_configuration"] = schema_evolution_configuration
            if table_creation_configuration is not None:
                self._values["table_creation_configuration"] = table_creation_configuration

        @builtins.property
        def append_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Describes whether all incoming data for this delivery stream will be append only (inserts only and not for updates and deletes) for Iceberg delivery.

            This feature is only applicable for Apache Iceberg Tables.

            The default value is false. If you set this value to true, Firehose automatically increases the throughput limit of a stream based on the throttling levels of the stream. If you set this parameter to true for a stream with updates and deletes, you will see out of order delivery.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-icebergdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-icebergdestinationconfiguration-appendonly
            '''
            result = self._values.get("append_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def buffering_hints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.BufferingHintsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-icebergdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-icebergdestinationconfiguration-bufferinghints
            '''
            result = self._values.get("buffering_hints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.BufferingHintsProperty"]], result)

        @builtins.property
        def catalog_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CatalogConfigurationProperty"]]:
            '''Configuration describing where the destination Apache Iceberg Tables are persisted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-icebergdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-icebergdestinationconfiguration-catalogconfiguration
            '''
            result = self._values.get("catalog_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CatalogConfigurationProperty"]], result)

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-icebergdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-icebergdestinationconfiguration-cloudwatchloggingoptions
            '''
            result = self._values.get("cloud_watch_logging_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]], result)

        @builtins.property
        def destination_table_configuration_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DestinationTableConfigurationProperty"]]]]:
            '''Provides a list of ``DestinationTableConfigurations`` which Firehose uses to deliver data to Apache Iceberg Tables.

            Firehose will write data with insert if table specific configuration is not provided here.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-icebergdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-icebergdestinationconfiguration-destinationtableconfigurationlist
            '''
            result = self._values.get("destination_table_configuration_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DestinationTableConfigurationProperty"]]]], result)

        @builtins.property
        def processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-icebergdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-icebergdestinationconfiguration-processingconfiguration
            '''
            result = self._values.get("processing_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]], result)

        @builtins.property
        def retry_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.RetryOptionsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-icebergdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-icebergdestinationconfiguration-retryoptions
            '''
            result = self._values.get("retry_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.RetryOptionsProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role to be assumed by Firehose for calling Apache Iceberg Tables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-icebergdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-icebergdestinationconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_backup_mode(self) -> typing.Optional[builtins.str]:
            '''Describes how Firehose will backup records.

            Currently,S3 backup only supports ``FailedDataOnly`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-icebergdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-icebergdestinationconfiguration-s3backupmode
            '''
            result = self._values.get("s3_backup_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-icebergdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-icebergdestinationconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]], result)

        @builtins.property
        def schema_evolution_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SchemaEvolutionConfigurationProperty"]]:
            '''The configuration to enable automatic schema evolution.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-icebergdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-icebergdestinationconfiguration-schemaevolutionconfiguration
            '''
            result = self._values.get("schema_evolution_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SchemaEvolutionConfigurationProperty"]], result)

        @builtins.property
        def table_creation_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.TableCreationConfigurationProperty"]]:
            '''The configuration to enable automatic table creation.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-icebergdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-icebergdestinationconfiguration-tablecreationconfiguration
            '''
            result = self._values.get("table_creation_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.TableCreationConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IcebergDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.InputFormatConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"deserializer": "deserializer"},
    )
    class InputFormatConfigurationProperty:
        def __init__(
            self,
            *,
            deserializer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.DeserializerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the deserializer you want to use to convert the format of the input data.

            This parameter is required if ``Enabled`` is set to true.

            :param deserializer: Specifies which deserializer to use. You can choose either the Apache Hive JSON SerDe or the OpenX JSON SerDe. If both are non-null, the server rejects the request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-inputformatconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                input_format_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.InputFormatConfigurationProperty(
                    deserializer=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.DeserializerProperty(
                        hive_json_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.HiveJsonSerDeProperty(
                            timestamp_formats=["timestampFormats"]
                        ),
                        open_xJson_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.OpenXJsonSerDeProperty(
                            case_insensitive=False,
                            column_to_json_key_mappings={
                                "column_to_json_key_mappings_key": "columnToJsonKeyMappings"
                            },
                            convert_dots_in_json_keys_to_underscores=False
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__70afaf6b6d072efcf10368f31131bcecf388ed473d85d80645a62a7340e37b3f)
                check_type(argname="argument deserializer", value=deserializer, expected_type=type_hints["deserializer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if deserializer is not None:
                self._values["deserializer"] = deserializer

        @builtins.property
        def deserializer(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DeserializerProperty"]]:
            '''Specifies which deserializer to use.

            You can choose either the Apache Hive JSON SerDe or the OpenX JSON SerDe. If both are non-null, the server rejects the request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-inputformatconfiguration.html#cfn-kinesisfirehose-deliverystream-inputformatconfiguration-deserializer
            '''
            result = self._values.get("deserializer")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.DeserializerProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputFormatConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"awskms_key_arn": "awskmsKeyArn"},
    )
    class KMSEncryptionConfigProperty:
        def __init__(
            self,
            *,
            awskms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``KMSEncryptionConfig`` property type specifies the AWS Key Management Service ( AWS KMS) encryption key that Amazon Simple Storage Service (Amazon S3) uses to encrypt data delivered by the Amazon Kinesis Data Firehose (Kinesis Data Firehose) stream.

            :param awskms_key_arn: The Amazon Resource Name (ARN) of the AWS KMS encryption key that Amazon S3 uses to encrypt data delivered by the Kinesis Data Firehose stream. The key must belong to the same region as the destination S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kmsencryptionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                k_mSEncryption_config_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty(
                    awskms_key_arn="awskmsKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__48d6d13c432f67e75ef88e8804fd27f83d256e806b85b7d5f3424c0a0586a61a)
                check_type(argname="argument awskms_key_arn", value=awskms_key_arn, expected_type=type_hints["awskms_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if awskms_key_arn is not None:
                self._values["awskms_key_arn"] = awskms_key_arn

        @builtins.property
        def awskms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS KMS encryption key that Amazon S3 uses to encrypt data delivered by the Kinesis Data Firehose stream.

            The key must belong to the same region as the destination S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kmsencryptionconfig.html#cfn-kinesisfirehose-deliverystream-kmsencryptionconfig-awskmskeyarn
            '''
            result = self._values.get("awskms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KMSEncryptionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.KinesisStreamSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kinesis_stream_arn": "kinesisStreamArn", "role_arn": "roleArn"},
    )
    class KinesisStreamSourceConfigurationProperty:
        def __init__(
            self,
            *,
            kinesis_stream_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``KinesisStreamSourceConfiguration`` property type specifies the stream and role Amazon Resource Names (ARNs) for a Kinesis stream used as the source for a delivery stream.

            :param kinesis_stream_arn: The ARN of the source Kinesis data stream.
            :param role_arn: The ARN of the role that provides access to the source Kinesis data stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                kinesis_stream_source_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KinesisStreamSourceConfigurationProperty(
                    kinesis_stream_arn="kinesisStreamArn",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7791b30ef47b2a3c6150ade1147aa40197875cda2ac232cadb2503477611e26e)
                check_type(argname="argument kinesis_stream_arn", value=kinesis_stream_arn, expected_type=type_hints["kinesis_stream_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kinesis_stream_arn is not None:
                self._values["kinesis_stream_arn"] = kinesis_stream_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def kinesis_stream_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the source Kinesis data stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration.html#cfn-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration-kinesisstreamarn
            '''
            result = self._values.get("kinesis_stream_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role that provides access to the source Kinesis data stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration.html#cfn-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.MSKSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_configuration": "authenticationConfiguration",
            "msk_cluster_arn": "mskClusterArn",
            "read_from_timestamp": "readFromTimestamp",
            "topic_name": "topicName",
        },
    )
    class MSKSourceConfigurationProperty:
        def __init__(
            self,
            *,
            authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.AuthenticationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            msk_cluster_arn: typing.Optional[builtins.str] = None,
            read_from_timestamp: typing.Optional[builtins.str] = None,
            topic_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for the Amazon MSK cluster to be used as the source for a delivery stream.

            :param authentication_configuration: The authentication configuration of the Amazon MSK cluster.
            :param msk_cluster_arn: The ARN of the Amazon MSK cluster.
            :param read_from_timestamp: The start date and time in UTC for the offset position within your MSK topic from where Firehose begins to read. By default, this is set to timestamp when Firehose becomes Active. If you want to create a Firehose stream with Earliest start position from SDK or CLI, you need to set the ``ReadFromTimestamp`` parameter to Epoch (1970-01-01T00:00:00Z).
            :param topic_name: The topic name within the Amazon MSK cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-msksourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                m_sKSource_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.MSKSourceConfigurationProperty(
                    authentication_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.AuthenticationConfigurationProperty(
                        connectivity="connectivity",
                        role_arn="roleArn"
                    ),
                    msk_cluster_arn="mskClusterArn",
                    read_from_timestamp="readFromTimestamp",
                    topic_name="topicName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a2d080f038e6b443f45ab5d5fb8923056577f0360a1c8043c6fc08caf3536b8)
                check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
                check_type(argname="argument msk_cluster_arn", value=msk_cluster_arn, expected_type=type_hints["msk_cluster_arn"])
                check_type(argname="argument read_from_timestamp", value=read_from_timestamp, expected_type=type_hints["read_from_timestamp"])
                check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_configuration is not None:
                self._values["authentication_configuration"] = authentication_configuration
            if msk_cluster_arn is not None:
                self._values["msk_cluster_arn"] = msk_cluster_arn
            if read_from_timestamp is not None:
                self._values["read_from_timestamp"] = read_from_timestamp
            if topic_name is not None:
                self._values["topic_name"] = topic_name

        @builtins.property
        def authentication_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.AuthenticationConfigurationProperty"]]:
            '''The authentication configuration of the Amazon MSK cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-msksourceconfiguration.html#cfn-kinesisfirehose-deliverystream-msksourceconfiguration-authenticationconfiguration
            '''
            result = self._values.get("authentication_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.AuthenticationConfigurationProperty"]], result)

        @builtins.property
        def msk_cluster_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Amazon MSK cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-msksourceconfiguration.html#cfn-kinesisfirehose-deliverystream-msksourceconfiguration-mskclusterarn
            '''
            result = self._values.get("msk_cluster_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def read_from_timestamp(self) -> typing.Optional[builtins.str]:
            '''The start date and time in UTC for the offset position within your MSK topic from where Firehose begins to read.

            By default, this is set to timestamp when Firehose becomes Active.

            If you want to create a Firehose stream with Earliest start position from SDK or CLI, you need to set the ``ReadFromTimestamp`` parameter to Epoch (1970-01-01T00:00:00Z).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-msksourceconfiguration.html#cfn-kinesisfirehose-deliverystream-msksourceconfiguration-readfromtimestamp
            '''
            result = self._values.get("read_from_timestamp")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_name(self) -> typing.Optional[builtins.str]:
            '''The topic name within the Amazon MSK cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-msksourceconfiguration.html#cfn-kinesisfirehose-deliverystream-msksourceconfiguration-topicname
            '''
            result = self._values.get("topic_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MSKSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.OpenXJsonSerDeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "case_insensitive": "caseInsensitive",
            "column_to_json_key_mappings": "columnToJsonKeyMappings",
            "convert_dots_in_json_keys_to_underscores": "convertDotsInJsonKeysToUnderscores",
        },
    )
    class OpenXJsonSerDeProperty:
        def __init__(
            self,
            *,
            case_insensitive: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            column_to_json_key_mappings: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            convert_dots_in_json_keys_to_underscores: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The OpenX SerDe.

            Used by Firehose for deserializing data, which means converting it from the JSON format in preparation for serializing it to the Parquet or ORC format. This is one of two deserializers you can choose, depending on which one offers the functionality you need. The other option is the native Hive / HCatalog JsonSerDe.

            :param case_insensitive: When set to ``true`` , which is the default, Firehose converts JSON keys to lowercase before deserializing them.
            :param column_to_json_key_mappings: Maps column names to JSON keys that aren't identical to the column names. This is useful when the JSON contains keys that are Hive keywords. For example, ``timestamp`` is a Hive keyword. If you have a JSON key named ``timestamp`` , set this parameter to ``{"ts": "timestamp"}`` to map this key to a column named ``ts`` .
            :param convert_dots_in_json_keys_to_underscores: When set to ``true`` , specifies that the names of the keys include dots and that you want Firehose to replace them with underscores. This is useful because Apache Hive does not allow dots in column names. For example, if the JSON contains a key whose name is "a.b", you can define the column name to be "a_b" when using this option. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-openxjsonserde.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                open_xJson_ser_de_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.OpenXJsonSerDeProperty(
                    case_insensitive=False,
                    column_to_json_key_mappings={
                        "column_to_json_key_mappings_key": "columnToJsonKeyMappings"
                    },
                    convert_dots_in_json_keys_to_underscores=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1571f01229bc791c71bd13538e53494328aa7f8f504fddaebb2b83f61e3e6111)
                check_type(argname="argument case_insensitive", value=case_insensitive, expected_type=type_hints["case_insensitive"])
                check_type(argname="argument column_to_json_key_mappings", value=column_to_json_key_mappings, expected_type=type_hints["column_to_json_key_mappings"])
                check_type(argname="argument convert_dots_in_json_keys_to_underscores", value=convert_dots_in_json_keys_to_underscores, expected_type=type_hints["convert_dots_in_json_keys_to_underscores"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if case_insensitive is not None:
                self._values["case_insensitive"] = case_insensitive
            if column_to_json_key_mappings is not None:
                self._values["column_to_json_key_mappings"] = column_to_json_key_mappings
            if convert_dots_in_json_keys_to_underscores is not None:
                self._values["convert_dots_in_json_keys_to_underscores"] = convert_dots_in_json_keys_to_underscores

        @builtins.property
        def case_insensitive(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to ``true`` , which is the default, Firehose converts JSON keys to lowercase before deserializing them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-openxjsonserde.html#cfn-kinesisfirehose-deliverystream-openxjsonserde-caseinsensitive
            '''
            result = self._values.get("case_insensitive")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def column_to_json_key_mappings(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Maps column names to JSON keys that aren't identical to the column names.

            This is useful when the JSON contains keys that are Hive keywords. For example, ``timestamp`` is a Hive keyword. If you have a JSON key named ``timestamp`` , set this parameter to ``{"ts": "timestamp"}`` to map this key to a column named ``ts`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-openxjsonserde.html#cfn-kinesisfirehose-deliverystream-openxjsonserde-columntojsonkeymappings
            '''
            result = self._values.get("column_to_json_key_mappings")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def convert_dots_in_json_keys_to_underscores(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to ``true`` , specifies that the names of the keys include dots and that you want Firehose to replace them with underscores.

            This is useful because Apache Hive does not allow dots in column names. For example, if the JSON contains a key whose name is "a.b", you can define the column name to be "a_b" when using this option.

            The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-openxjsonserde.html#cfn-kinesisfirehose-deliverystream-openxjsonserde-convertdotsinjsonkeystounderscores
            '''
            result = self._values.get("convert_dots_in_json_keys_to_underscores")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenXJsonSerDeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.OrcSerDeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "block_size_bytes": "blockSizeBytes",
            "bloom_filter_columns": "bloomFilterColumns",
            "bloom_filter_false_positive_probability": "bloomFilterFalsePositiveProbability",
            "compression": "compression",
            "dictionary_key_threshold": "dictionaryKeyThreshold",
            "enable_padding": "enablePadding",
            "format_version": "formatVersion",
            "padding_tolerance": "paddingTolerance",
            "row_index_stride": "rowIndexStride",
            "stripe_size_bytes": "stripeSizeBytes",
        },
    )
    class OrcSerDeProperty:
        def __init__(
            self,
            *,
            block_size_bytes: typing.Optional[jsii.Number] = None,
            bloom_filter_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
            bloom_filter_false_positive_probability: typing.Optional[jsii.Number] = None,
            compression: typing.Optional[builtins.str] = None,
            dictionary_key_threshold: typing.Optional[jsii.Number] = None,
            enable_padding: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            format_version: typing.Optional[builtins.str] = None,
            padding_tolerance: typing.Optional[jsii.Number] = None,
            row_index_stride: typing.Optional[jsii.Number] = None,
            stripe_size_bytes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A serializer to use for converting data to the ORC format before storing it in Amazon S3.

            For more information, see `Apache ORC <https://docs.aws.amazon.com/https://orc.apache.org/docs/>`_ .

            :param block_size_bytes: The Hadoop Distributed File System (HDFS) block size. This is useful if you intend to copy the data from Amazon S3 to HDFS before querying. The default is 256 MiB and the minimum is 64 MiB. Firehose uses this value for padding calculations.
            :param bloom_filter_columns: The column names for which you want Firehose to create bloom filters. The default is ``null`` .
            :param bloom_filter_false_positive_probability: The Bloom filter false positive probability (FPP). The lower the FPP, the bigger the Bloom filter. The default value is 0.05, the minimum is 0, and the maximum is 1.
            :param compression: The compression code to use over data blocks. The default is ``SNAPPY`` .
            :param dictionary_key_threshold: Represents the fraction of the total number of non-null rows. To turn off dictionary encoding, set this fraction to a number that is less than the number of distinct keys in a dictionary. To always use dictionary encoding, set this threshold to 1.
            :param enable_padding: Set this to ``true`` to indicate that you want stripes to be padded to the HDFS block boundaries. This is useful if you intend to copy the data from Amazon S3 to HDFS before querying. The default is ``false`` .
            :param format_version: The version of the file to write. The possible values are ``V0_11`` and ``V0_12`` . The default is ``V0_12`` .
            :param padding_tolerance: A number between 0 and 1 that defines the tolerance for block padding as a decimal fraction of stripe size. The default value is 0.05, which means 5 percent of stripe size. For the default values of 64 MiB ORC stripes and 256 MiB HDFS blocks, the default block padding tolerance of 5 percent reserves a maximum of 3.2 MiB for padding within the 256 MiB block. In such a case, if the available size within the block is more than 3.2 MiB, a new, smaller stripe is inserted to fit within that space. This ensures that no stripe crosses block boundaries and causes remote reads within a node-local task. Kinesis Data Firehose ignores this parameter when ``EnablePadding`` is ``false`` .
            :param row_index_stride: The number of rows between index entries. The default is 10,000 and the minimum is 1,000.
            :param stripe_size_bytes: The number of bytes in each stripe. The default is 64 MiB and the minimum is 8 MiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                orc_ser_de_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.OrcSerDeProperty(
                    block_size_bytes=123,
                    bloom_filter_columns=["bloomFilterColumns"],
                    bloom_filter_false_positive_probability=123,
                    compression="compression",
                    dictionary_key_threshold=123,
                    enable_padding=False,
                    format_version="formatVersion",
                    padding_tolerance=123,
                    row_index_stride=123,
                    stripe_size_bytes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__502f7aa73c2cedc4007f76d54ade6c7f0d703bdaa58aad2bbf83a3cd76fc45af)
                check_type(argname="argument block_size_bytes", value=block_size_bytes, expected_type=type_hints["block_size_bytes"])
                check_type(argname="argument bloom_filter_columns", value=bloom_filter_columns, expected_type=type_hints["bloom_filter_columns"])
                check_type(argname="argument bloom_filter_false_positive_probability", value=bloom_filter_false_positive_probability, expected_type=type_hints["bloom_filter_false_positive_probability"])
                check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
                check_type(argname="argument dictionary_key_threshold", value=dictionary_key_threshold, expected_type=type_hints["dictionary_key_threshold"])
                check_type(argname="argument enable_padding", value=enable_padding, expected_type=type_hints["enable_padding"])
                check_type(argname="argument format_version", value=format_version, expected_type=type_hints["format_version"])
                check_type(argname="argument padding_tolerance", value=padding_tolerance, expected_type=type_hints["padding_tolerance"])
                check_type(argname="argument row_index_stride", value=row_index_stride, expected_type=type_hints["row_index_stride"])
                check_type(argname="argument stripe_size_bytes", value=stripe_size_bytes, expected_type=type_hints["stripe_size_bytes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if block_size_bytes is not None:
                self._values["block_size_bytes"] = block_size_bytes
            if bloom_filter_columns is not None:
                self._values["bloom_filter_columns"] = bloom_filter_columns
            if bloom_filter_false_positive_probability is not None:
                self._values["bloom_filter_false_positive_probability"] = bloom_filter_false_positive_probability
            if compression is not None:
                self._values["compression"] = compression
            if dictionary_key_threshold is not None:
                self._values["dictionary_key_threshold"] = dictionary_key_threshold
            if enable_padding is not None:
                self._values["enable_padding"] = enable_padding
            if format_version is not None:
                self._values["format_version"] = format_version
            if padding_tolerance is not None:
                self._values["padding_tolerance"] = padding_tolerance
            if row_index_stride is not None:
                self._values["row_index_stride"] = row_index_stride
            if stripe_size_bytes is not None:
                self._values["stripe_size_bytes"] = stripe_size_bytes

        @builtins.property
        def block_size_bytes(self) -> typing.Optional[jsii.Number]:
            '''The Hadoop Distributed File System (HDFS) block size.

            This is useful if you intend to copy the data from Amazon S3 to HDFS before querying. The default is 256 MiB and the minimum is 64 MiB. Firehose uses this value for padding calculations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-blocksizebytes
            '''
            result = self._values.get("block_size_bytes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def bloom_filter_columns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The column names for which you want Firehose to create bloom filters.

            The default is ``null`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-bloomfiltercolumns
            '''
            result = self._values.get("bloom_filter_columns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def bloom_filter_false_positive_probability(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The Bloom filter false positive probability (FPP).

            The lower the FPP, the bigger the Bloom filter. The default value is 0.05, the minimum is 0, and the maximum is 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-bloomfilterfalsepositiveprobability
            '''
            result = self._values.get("bloom_filter_false_positive_probability")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def compression(self) -> typing.Optional[builtins.str]:
            '''The compression code to use over data blocks.

            The default is ``SNAPPY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-compression
            '''
            result = self._values.get("compression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dictionary_key_threshold(self) -> typing.Optional[jsii.Number]:
            '''Represents the fraction of the total number of non-null rows.

            To turn off dictionary encoding, set this fraction to a number that is less than the number of distinct keys in a dictionary. To always use dictionary encoding, set this threshold to 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-dictionarykeythreshold
            '''
            result = self._values.get("dictionary_key_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enable_padding(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this to ``true`` to indicate that you want stripes to be padded to the HDFS block boundaries.

            This is useful if you intend to copy the data from Amazon S3 to HDFS before querying. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-enablepadding
            '''
            result = self._values.get("enable_padding")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def format_version(self) -> typing.Optional[builtins.str]:
            '''The version of the file to write.

            The possible values are ``V0_11`` and ``V0_12`` . The default is ``V0_12`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-formatversion
            '''
            result = self._values.get("format_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def padding_tolerance(self) -> typing.Optional[jsii.Number]:
            '''A number between 0 and 1 that defines the tolerance for block padding as a decimal fraction of stripe size.

            The default value is 0.05, which means 5 percent of stripe size.

            For the default values of 64 MiB ORC stripes and 256 MiB HDFS blocks, the default block padding tolerance of 5 percent reserves a maximum of 3.2 MiB for padding within the 256 MiB block. In such a case, if the available size within the block is more than 3.2 MiB, a new, smaller stripe is inserted to fit within that space. This ensures that no stripe crosses block boundaries and causes remote reads within a node-local task.

            Kinesis Data Firehose ignores this parameter when ``EnablePadding`` is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-paddingtolerance
            '''
            result = self._values.get("padding_tolerance")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def row_index_stride(self) -> typing.Optional[jsii.Number]:
            '''The number of rows between index entries.

            The default is 10,000 and the minimum is 1,000.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-rowindexstride
            '''
            result = self._values.get("row_index_stride")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stripe_size_bytes(self) -> typing.Optional[jsii.Number]:
            '''The number of bytes in each stripe.

            The default is 64 MiB and the minimum is 8 MiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-stripesizebytes
            '''
            result = self._values.get("stripe_size_bytes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrcSerDeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.OutputFormatConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"serializer": "serializer"},
    )
    class OutputFormatConfigurationProperty:
        def __init__(
            self,
            *,
            serializer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SerializerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the serializer that you want Firehose to use to convert the format of your data before it writes it to Amazon S3.

            This parameter is required if ``Enabled`` is set to true.

            :param serializer: Specifies which serializer to use. You can choose either the ORC SerDe or the Parquet SerDe. If both are non-null, the server rejects the request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-outputformatconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                output_format_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.OutputFormatConfigurationProperty(
                    serializer=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SerializerProperty(
                        orc_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.OrcSerDeProperty(
                            block_size_bytes=123,
                            bloom_filter_columns=["bloomFilterColumns"],
                            bloom_filter_false_positive_probability=123,
                            compression="compression",
                            dictionary_key_threshold=123,
                            enable_padding=False,
                            format_version="formatVersion",
                            padding_tolerance=123,
                            row_index_stride=123,
                            stripe_size_bytes=123
                        ),
                        parquet_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ParquetSerDeProperty(
                            block_size_bytes=123,
                            compression="compression",
                            enable_dictionary_compression=False,
                            max_padding_bytes=123,
                            page_size_bytes=123,
                            writer_version="writerVersion"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6dc581c2f5484d33876a12e5059524a2de478e71837b1c1d9041fc2503e7536)
                check_type(argname="argument serializer", value=serializer, expected_type=type_hints["serializer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if serializer is not None:
                self._values["serializer"] = serializer

        @builtins.property
        def serializer(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SerializerProperty"]]:
            '''Specifies which serializer to use.

            You can choose either the ORC SerDe or the Parquet SerDe. If both are non-null, the server rejects the request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-outputformatconfiguration.html#cfn-kinesisfirehose-deliverystream-outputformatconfiguration-serializer
            '''
            result = self._values.get("serializer")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SerializerProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputFormatConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.ParquetSerDeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "block_size_bytes": "blockSizeBytes",
            "compression": "compression",
            "enable_dictionary_compression": "enableDictionaryCompression",
            "max_padding_bytes": "maxPaddingBytes",
            "page_size_bytes": "pageSizeBytes",
            "writer_version": "writerVersion",
        },
    )
    class ParquetSerDeProperty:
        def __init__(
            self,
            *,
            block_size_bytes: typing.Optional[jsii.Number] = None,
            compression: typing.Optional[builtins.str] = None,
            enable_dictionary_compression: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            max_padding_bytes: typing.Optional[jsii.Number] = None,
            page_size_bytes: typing.Optional[jsii.Number] = None,
            writer_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A serializer to use for converting data to the Parquet format before storing it in Amazon S3.

            For more information, see `Apache Parquet <https://docs.aws.amazon.com/https://parquet.apache.org/docs/>`_ .

            :param block_size_bytes: The Hadoop Distributed File System (HDFS) block size. This is useful if you intend to copy the data from Amazon S3 to HDFS before querying. The default is 256 MiB and the minimum is 64 MiB. Firehose uses this value for padding calculations.
            :param compression: The compression code to use over data blocks. The possible values are ``UNCOMPRESSED`` , ``SNAPPY`` , and ``GZIP`` , with the default being ``SNAPPY`` . Use ``SNAPPY`` for higher decompression speed. Use ``GZIP`` if the compression ratio is more important than speed.
            :param enable_dictionary_compression: Indicates whether to enable dictionary compression.
            :param max_padding_bytes: The maximum amount of padding to apply. This is useful if you intend to copy the data from Amazon S3 to HDFS before querying. The default is 0.
            :param page_size_bytes: The Parquet page size. Column chunks are divided into pages. A page is conceptually an indivisible unit (in terms of compression and encoding). The minimum value is 64 KiB and the default is 1 MiB.
            :param writer_version: Indicates the version of row format to output. The possible values are ``V1`` and ``V2`` . The default is ``V1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-parquetserde.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                parquet_ser_de_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ParquetSerDeProperty(
                    block_size_bytes=123,
                    compression="compression",
                    enable_dictionary_compression=False,
                    max_padding_bytes=123,
                    page_size_bytes=123,
                    writer_version="writerVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b55f795b35108fdda51e34317308df87c8866ba7da9ad5cf5619a19faf7806c)
                check_type(argname="argument block_size_bytes", value=block_size_bytes, expected_type=type_hints["block_size_bytes"])
                check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
                check_type(argname="argument enable_dictionary_compression", value=enable_dictionary_compression, expected_type=type_hints["enable_dictionary_compression"])
                check_type(argname="argument max_padding_bytes", value=max_padding_bytes, expected_type=type_hints["max_padding_bytes"])
                check_type(argname="argument page_size_bytes", value=page_size_bytes, expected_type=type_hints["page_size_bytes"])
                check_type(argname="argument writer_version", value=writer_version, expected_type=type_hints["writer_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if block_size_bytes is not None:
                self._values["block_size_bytes"] = block_size_bytes
            if compression is not None:
                self._values["compression"] = compression
            if enable_dictionary_compression is not None:
                self._values["enable_dictionary_compression"] = enable_dictionary_compression
            if max_padding_bytes is not None:
                self._values["max_padding_bytes"] = max_padding_bytes
            if page_size_bytes is not None:
                self._values["page_size_bytes"] = page_size_bytes
            if writer_version is not None:
                self._values["writer_version"] = writer_version

        @builtins.property
        def block_size_bytes(self) -> typing.Optional[jsii.Number]:
            '''The Hadoop Distributed File System (HDFS) block size.

            This is useful if you intend to copy the data from Amazon S3 to HDFS before querying. The default is 256 MiB and the minimum is 64 MiB. Firehose uses this value for padding calculations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-parquetserde.html#cfn-kinesisfirehose-deliverystream-parquetserde-blocksizebytes
            '''
            result = self._values.get("block_size_bytes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def compression(self) -> typing.Optional[builtins.str]:
            '''The compression code to use over data blocks.

            The possible values are ``UNCOMPRESSED`` , ``SNAPPY`` , and ``GZIP`` , with the default being ``SNAPPY`` . Use ``SNAPPY`` for higher decompression speed. Use ``GZIP`` if the compression ratio is more important than speed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-parquetserde.html#cfn-kinesisfirehose-deliverystream-parquetserde-compression
            '''
            result = self._values.get("compression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_dictionary_compression(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to enable dictionary compression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-parquetserde.html#cfn-kinesisfirehose-deliverystream-parquetserde-enabledictionarycompression
            '''
            result = self._values.get("enable_dictionary_compression")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def max_padding_bytes(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of padding to apply.

            This is useful if you intend to copy the data from Amazon S3 to HDFS before querying. The default is 0.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-parquetserde.html#cfn-kinesisfirehose-deliverystream-parquetserde-maxpaddingbytes
            '''
            result = self._values.get("max_padding_bytes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def page_size_bytes(self) -> typing.Optional[jsii.Number]:
            '''The Parquet page size.

            Column chunks are divided into pages. A page is conceptually an indivisible unit (in terms of compression and encoding). The minimum value is 64 KiB and the default is 1 MiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-parquetserde.html#cfn-kinesisfirehose-deliverystream-parquetserde-pagesizebytes
            '''
            result = self._values.get("page_size_bytes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def writer_version(self) -> typing.Optional[builtins.str]:
            '''Indicates the version of row format to output.

            The possible values are ``V1`` and ``V2`` . The default is ``V1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-parquetserde.html#cfn-kinesisfirehose-deliverystream-parquetserde-writerversion
            '''
            result = self._values.get("writer_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParquetSerDeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.PartitionFieldProperty",
        jsii_struct_bases=[],
        name_mapping={"source_name": "sourceName"},
    )
    class PartitionFieldProperty:
        def __init__(
            self,
            *,
            source_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a single field in a ``PartitionSpec`` .

            Amazon Data Firehose is in preview release and is subject to change.

            :param source_name: The column name to be configured in partition spec. Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-partitionfield.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                partition_field_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.PartitionFieldProperty(
                    source_name="sourceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c51e079891a4e8ef39ef34b3c104dc6158a4cdf82c92f7c0a7dbac819ec7c912)
                check_type(argname="argument source_name", value=source_name, expected_type=type_hints["source_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_name is not None:
                self._values["source_name"] = source_name

        @builtins.property
        def source_name(self) -> typing.Optional[builtins.str]:
            '''The column name to be configured in partition spec.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-partitionfield.html#cfn-kinesisfirehose-deliverystream-partitionfield-sourcename
            '''
            result = self._values.get("source_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PartitionFieldProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.PartitionSpecProperty",
        jsii_struct_bases=[],
        name_mapping={"identity": "identity"},
    )
    class PartitionSpecProperty:
        def __init__(
            self,
            *,
            identity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.PartitionFieldProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Represents how to produce partition data for a table.

            Partition data is produced by transforming columns in a table. Each column transform is represented by a named ``PartitionField`` .

            Here is an example of the schema in JSON.

            ``"partitionSpec": { "identity": [ {"sourceName": "column1"}, {"sourceName": "column2"}, {"sourceName": "column3"} ] }``

            Amazon Data Firehose is in preview release and is subject to change.

            :param identity: List of identity `transforms <https://docs.aws.amazon.com/https://iceberg.apache.org/spec/#partition-transforms>`_ that performs an identity transformation. The transform takes the source value, and does not modify it. Result type is the source type. Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-partitionspec.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                partition_spec_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.PartitionSpecProperty(
                    identity=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.PartitionFieldProperty(
                        source_name="sourceName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9db1ab17977ce5681e6b5ad4d15fb5907608bdb88dfec4c6c2667acd935be66b)
                check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if identity is not None:
                self._values["identity"] = identity

        @builtins.property
        def identity(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.PartitionFieldProperty"]]]]:
            '''List of identity `transforms <https://docs.aws.amazon.com/https://iceberg.apache.org/spec/#partition-transforms>`_ that performs an identity transformation. The transform takes the source value, and does not modify it. Result type is the source type.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-partitionspec.html#cfn-kinesisfirehose-deliverystream-partitionspec-identity
            '''
            result = self._values.get("identity")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.PartitionFieldProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PartitionSpecProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "processors": "processors"},
    )
    class ProcessingConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            processors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ProcessorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``ProcessingConfiguration`` property configures data processing for an Amazon Kinesis Data Firehose delivery stream.

            :param enabled: Indicates whether data processing is enabled (true) or disabled (false).
            :param processors: The data processors.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                processing_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty(
                    enabled=False,
                    processors=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorProperty(
                        parameters=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorParameterProperty(
                            parameter_name="parameterName",
                            parameter_value="parameterValue"
                        )],
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed805f8586c149a2b83669105c2270a06f792dc898669dd64305c850bb9d510e)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument processors", value=processors, expected_type=type_hints["processors"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if processors is not None:
                self._values["processors"] = processors

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether data processing is enabled (true) or disabled (false).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processingconfiguration.html#cfn-kinesisfirehose-deliverystream-processingconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def processors(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessorProperty"]]]]:
            '''The data processors.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processingconfiguration.html#cfn-kinesisfirehose-deliverystream-processingconfiguration-processors
            '''
            result = self._values.get("processors")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessorProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProcessingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.ProcessorParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_name": "parameterName",
            "parameter_value": "parameterValue",
        },
    )
    class ProcessorParameterProperty:
        def __init__(
            self,
            *,
            parameter_name: typing.Optional[builtins.str] = None,
            parameter_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ProcessorParameter`` property specifies a processor parameter in a data processor for an Amazon Kinesis Data Firehose delivery stream.

            :param parameter_name: The name of the parameter. Currently the following default values are supported: 3 for ``NumberOfRetries`` and 60 for the ``BufferIntervalInSeconds`` . The ``BufferSizeInMBs`` ranges between 0.2 MB and up to 3MB. The default buffering hint is 1MB for all destinations, except Splunk. For Splunk, the default buffering hint is 256 KB.
            :param parameter_value: The parameter value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processorparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                processor_parameter_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorParameterProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__61df5affdbcf20e7459900a373fddd5801d1b022e822fbcd4a82809947ce8d77)
                check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
                check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameter_name is not None:
                self._values["parameter_name"] = parameter_name
            if parameter_value is not None:
                self._values["parameter_value"] = parameter_value

        @builtins.property
        def parameter_name(self) -> typing.Optional[builtins.str]:
            '''The name of the parameter.

            Currently the following default values are supported: 3 for ``NumberOfRetries`` and 60 for the ``BufferIntervalInSeconds`` . The ``BufferSizeInMBs`` ranges between 0.2 MB and up to 3MB. The default buffering hint is 1MB for all destinations, except Splunk. For Splunk, the default buffering hint is 256 KB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processorparameter.html#cfn-kinesisfirehose-deliverystream-processorparameter-parametername
            '''
            result = self._values.get("parameter_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameter_value(self) -> typing.Optional[builtins.str]:
            '''The parameter value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processorparameter.html#cfn-kinesisfirehose-deliverystream-processorparameter-parametervalue
            '''
            result = self._values.get("parameter_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProcessorParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.ProcessorProperty",
        jsii_struct_bases=[],
        name_mapping={"parameters": "parameters", "type": "type"},
    )
    class ProcessorProperty:
        def __init__(
            self,
            *,
            parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ProcessorParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``Processor`` property specifies a data processor for an Amazon Kinesis Data Firehose delivery stream.

            :param parameters: The processor parameters.
            :param type: The type of processor. Valid values: ``Lambda`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                processor_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorProperty(
                    parameters=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorParameterProperty(
                        parameter_name="parameterName",
                        parameter_value="parameterValue"
                    )],
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3cba94dc162fde6e6229240e7812c4f6ddfcdc0497eeaef2161cb4c2b77c4143)
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameters is not None:
                self._values["parameters"] = parameters
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessorParameterProperty"]]]]:
            '''The processor parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processor.html#cfn-kinesisfirehose-deliverystream-processor-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessorParameterProperty"]]]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of processor.

            Valid values: ``Lambda`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processor.html#cfn-kinesisfirehose-deliverystream-processor-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProcessorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.RedshiftDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "cluster_jdbcurl": "clusterJdbcurl",
            "copy_command": "copyCommand",
            "password": "password",
            "processing_configuration": "processingConfiguration",
            "retry_options": "retryOptions",
            "role_arn": "roleArn",
            "s3_backup_configuration": "s3BackupConfiguration",
            "s3_backup_mode": "s3BackupMode",
            "s3_configuration": "s3Configuration",
            "secrets_manager_configuration": "secretsManagerConfiguration",
            "username": "username",
        },
    )
    class RedshiftDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cluster_jdbcurl: typing.Optional[builtins.str] = None,
            copy_command: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.CopyCommandProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            password: typing.Optional[builtins.str] = None,
            processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.RedshiftRetryOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            s3_backup_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_backup_mode: typing.Optional[builtins.str] = None,
            s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secrets_manager_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``RedshiftDestinationConfiguration`` property type specifies an Amazon Redshift cluster to which Amazon Kinesis Data Firehose (Kinesis Data Firehose) delivers data.

            :param cloud_watch_logging_options: The CloudWatch logging options for your Firehose stream.
            :param cluster_jdbcurl: The connection string that Kinesis Data Firehose uses to connect to the Amazon Redshift cluster.
            :param copy_command: Configures the Amazon Redshift ``COPY`` command that Kinesis Data Firehose uses to load data into the cluster from the Amazon S3 bucket.
            :param password: The password for the Amazon Redshift user that you specified in the ``Username`` property.
            :param processing_configuration: The data processing configuration for the Kinesis Data Firehose delivery stream.
            :param retry_options: The retry behavior in case Firehose is unable to deliver documents to Amazon Redshift. Default value is 3600 (60 minutes).
            :param role_arn: The ARN of the AWS Identity and Access Management (IAM) role that grants Kinesis Data Firehose access to your Amazon S3 bucket and AWS KMS (if you enable data encryption). For more information, see `Grant Kinesis Data Firehose Access to an Amazon Redshift Destination <https://docs.aws.amazon.com/firehose/latest/dev/controlling-access.html#using-iam-rs>`_ in the *Amazon Kinesis Data Firehose Developer Guide* .
            :param s3_backup_configuration: The configuration for backup in Amazon S3.
            :param s3_backup_mode: The Amazon S3 backup mode. After you create a Firehose stream, you can update it to enable Amazon S3 backup if it is disabled. If backup is enabled, you can't update the Firehose stream to disable it.
            :param s3_configuration: The S3 bucket where Kinesis Data Firehose first delivers data. After the data is in the bucket, Kinesis Data Firehose uses the ``COPY`` command to load the data into the Amazon Redshift cluster. For the Amazon S3 bucket's compression format, don't specify ``SNAPPY`` or ``ZIP`` because the Amazon Redshift ``COPY`` command doesn't support them.
            :param secrets_manager_configuration: The configuration that defines how you access secrets for Amazon Redshift.
            :param username: The Amazon Redshift user that has permission to access the Amazon Redshift cluster. This user must have ``INSERT`` privileges for copying data from the Amazon S3 bucket to the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                redshift_destination_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.RedshiftDestinationConfigurationProperty(
                    cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                        enabled=False,
                        log_group_name="logGroupName",
                        log_stream_name="logStreamName"
                    ),
                    cluster_jdbcurl="clusterJdbcurl",
                    copy_command=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CopyCommandProperty(
                        copy_options="copyOptions",
                        data_table_columns="dataTableColumns",
                        data_table_name="dataTableName"
                    ),
                    password="password",
                    processing_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty(
                        enabled=False,
                        processors=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorProperty(
                            parameters=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorParameterProperty(
                                parameter_name="parameterName",
                                parameter_value="parameterValue"
                            )],
                            type="type"
                        )]
                    ),
                    retry_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.RedshiftRetryOptionsProperty(
                        duration_in_seconds=123
                    ),
                    role_arn="roleArn",
                    s3_backup_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty(
                        bucket_arn="bucketArn",
                        buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                            interval_in_seconds=123,
                            size_in_mBs=123
                        ),
                        cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                            enabled=False,
                            log_group_name="logGroupName",
                            log_stream_name="logStreamName"
                        ),
                        compression_format="compressionFormat",
                        encryption_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty(
                            kms_encryption_config=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty(
                                awskms_key_arn="awskmsKeyArn"
                            ),
                            no_encryption_config="noEncryptionConfig"
                        ),
                        error_output_prefix="errorOutputPrefix",
                        prefix="prefix",
                        role_arn="roleArn"
                    ),
                    s3_backup_mode="s3BackupMode",
                    s3_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty(
                        bucket_arn="bucketArn",
                        buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                            interval_in_seconds=123,
                            size_in_mBs=123
                        ),
                        cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                            enabled=False,
                            log_group_name="logGroupName",
                            log_stream_name="logStreamName"
                        ),
                        compression_format="compressionFormat",
                        encryption_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty(
                            kms_encryption_config=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty(
                                awskms_key_arn="awskmsKeyArn"
                            ),
                            no_encryption_config="noEncryptionConfig"
                        ),
                        error_output_prefix="errorOutputPrefix",
                        prefix="prefix",
                        role_arn="roleArn"
                    ),
                    secrets_manager_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty(
                        enabled=False,
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    ),
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6d88e0c93175d5a07a21337809afabb886001f2f68cffcb1ca4389b32270faed)
                check_type(argname="argument cloud_watch_logging_options", value=cloud_watch_logging_options, expected_type=type_hints["cloud_watch_logging_options"])
                check_type(argname="argument cluster_jdbcurl", value=cluster_jdbcurl, expected_type=type_hints["cluster_jdbcurl"])
                check_type(argname="argument copy_command", value=copy_command, expected_type=type_hints["copy_command"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
                check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument s3_backup_configuration", value=s3_backup_configuration, expected_type=type_hints["s3_backup_configuration"])
                check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
                check_type(argname="argument secrets_manager_configuration", value=secrets_manager_configuration, expected_type=type_hints["secrets_manager_configuration"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if cluster_jdbcurl is not None:
                self._values["cluster_jdbcurl"] = cluster_jdbcurl
            if copy_command is not None:
                self._values["copy_command"] = copy_command
            if password is not None:
                self._values["password"] = password
            if processing_configuration is not None:
                self._values["processing_configuration"] = processing_configuration
            if retry_options is not None:
                self._values["retry_options"] = retry_options
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if s3_backup_configuration is not None:
                self._values["s3_backup_configuration"] = s3_backup_configuration
            if s3_backup_mode is not None:
                self._values["s3_backup_mode"] = s3_backup_mode
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration
            if secrets_manager_configuration is not None:
                self._values["secrets_manager_configuration"] = secrets_manager_configuration
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]]:
            '''The CloudWatch logging options for your Firehose stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-cloudwatchloggingoptions
            '''
            result = self._values.get("cloud_watch_logging_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]], result)

        @builtins.property
        def cluster_jdbcurl(self) -> typing.Optional[builtins.str]:
            '''The connection string that Kinesis Data Firehose uses to connect to the Amazon Redshift cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-clusterjdbcurl
            '''
            result = self._values.get("cluster_jdbcurl")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def copy_command(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CopyCommandProperty"]]:
            '''Configures the Amazon Redshift ``COPY`` command that Kinesis Data Firehose uses to load data into the cluster from the Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-copycommand
            '''
            result = self._values.get("copy_command")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CopyCommandProperty"]], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password for the Amazon Redshift user that you specified in the ``Username`` property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]]:
            '''The data processing configuration for the Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-processingconfiguration
            '''
            result = self._values.get("processing_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]], result)

        @builtins.property
        def retry_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.RedshiftRetryOptionsProperty"]]:
            '''The retry behavior in case Firehose is unable to deliver documents to Amazon Redshift.

            Default value is 3600 (60 minutes).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-retryoptions
            '''
            result = self._values.get("retry_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.RedshiftRetryOptionsProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the AWS Identity and Access Management (IAM) role that grants Kinesis Data Firehose access to your Amazon S3 bucket and AWS KMS (if you enable data encryption).

            For more information, see `Grant Kinesis Data Firehose Access to an Amazon Redshift Destination <https://docs.aws.amazon.com/firehose/latest/dev/controlling-access.html#using-iam-rs>`_ in the *Amazon Kinesis Data Firehose Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_backup_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]]:
            '''The configuration for backup in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-s3backupconfiguration
            '''
            result = self._values.get("s3_backup_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]], result)

        @builtins.property
        def s3_backup_mode(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 backup mode.

            After you create a Firehose stream, you can update it to enable Amazon S3 backup if it is disabled. If backup is enabled, you can't update the Firehose stream to disable it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-s3backupmode
            '''
            result = self._values.get("s3_backup_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]]:
            '''The S3 bucket where Kinesis Data Firehose first delivers data.

            After the data is in the bucket, Kinesis Data Firehose uses the ``COPY`` command to load the data into the Amazon Redshift cluster. For the Amazon S3 bucket's compression format, don't specify ``SNAPPY`` or ``ZIP`` because the Amazon Redshift ``COPY`` command doesn't support them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]], result)

        @builtins.property
        def secrets_manager_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty"]]:
            '''The configuration that defines how you access secrets for Amazon Redshift.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-secretsmanagerconfiguration
            '''
            result = self._values.get("secrets_manager_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty"]], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The Amazon Redshift user that has permission to access the Amazon Redshift cluster.

            This user must have ``INSERT`` privileges for copying data from the Amazon S3 bucket to the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.RedshiftRetryOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_in_seconds": "durationInSeconds"},
    )
    class RedshiftRetryOptionsProperty:
        def __init__(
            self,
            *,
            duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configures retry behavior in case Firehose is unable to deliver documents to Amazon Redshift.

            :param duration_in_seconds: The length of time during which Firehose retries delivery after a failure, starting from the initial request and including the first attempt. The default value is 3600 seconds (60 minutes). Firehose does not retry if the value of ``DurationInSeconds`` is 0 (zero) or if the first delivery attempt takes longer than the current value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftretryoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                redshift_retry_options_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.RedshiftRetryOptionsProperty(
                    duration_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2c18c56ad75f163e7f453ee4ce101255e6e6bd40b8f9ddd79a15e2f891259b9)
                check_type(argname="argument duration_in_seconds", value=duration_in_seconds, expected_type=type_hints["duration_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The length of time during which Firehose retries delivery after a failure, starting from the initial request and including the first attempt.

            The default value is 3600 seconds (60 minutes). Firehose does not retry if the value of ``DurationInSeconds`` is 0 (zero) or if the first delivery attempt takes longer than the current value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftretryoptions.html#cfn-kinesisfirehose-deliverystream-redshiftretryoptions-durationinseconds
            '''
            result = self._values.get("duration_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftRetryOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.RetryOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_in_seconds": "durationInSeconds"},
    )
    class RetryOptionsProperty:
        def __init__(
            self,
            *,
            duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the retry behavior in case Kinesis Data Firehose is unable to deliver data to the specified HTTP endpoint destination, or if it doesn't receive a valid acknowledgment of receipt from the specified HTTP endpoint destination.

            Kinesis Firehose supports any custom HTTP endpoint or HTTP endpoints owned by supported third-party service providers, including Datadog, MongoDB, and New Relic.

            :param duration_in_seconds: The total amount of time that Kinesis Data Firehose spends on retries. This duration starts after the initial attempt to send data to the custom destination via HTTPS endpoint fails. It doesn't include the periods during which Kinesis Data Firehose waits for acknowledgment from the specified destination after each attempt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-retryoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                retry_options_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.RetryOptionsProperty(
                    duration_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__971da5b058145004752bfd9c216c83d9295da3978e7099ccb0064062f310db8c)
                check_type(argname="argument duration_in_seconds", value=duration_in_seconds, expected_type=type_hints["duration_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The total amount of time that Kinesis Data Firehose spends on retries.

            This duration starts after the initial attempt to send data to the custom destination via HTTPS endpoint fails. It doesn't include the periods during which Kinesis Data Firehose waits for acknowledgment from the specified destination after each attempt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-retryoptions.html#cfn-kinesisfirehose-deliverystream-retryoptions-durationinseconds
            '''
            result = self._values.get("duration_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetryOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_arn": "bucketArn",
            "buffering_hints": "bufferingHints",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "compression_format": "compressionFormat",
            "encryption_configuration": "encryptionConfiguration",
            "error_output_prefix": "errorOutputPrefix",
            "prefix": "prefix",
            "role_arn": "roleArn",
        },
    )
    class S3DestinationConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_arn: typing.Optional[builtins.str] = None,
            buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.BufferingHintsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            compression_format: typing.Optional[builtins.str] = None,
            encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            error_output_prefix: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``S3DestinationConfiguration`` property type specifies an Amazon Simple Storage Service (Amazon S3) destination to which Amazon Kinesis Data Firehose (Kinesis Data Firehose) delivers data.

            :param bucket_arn: The Amazon Resource Name (ARN) of the Amazon S3 bucket to send data to.
            :param buffering_hints: Configures how Kinesis Data Firehose buffers incoming data while delivering it to the Amazon S3 bucket.
            :param cloud_watch_logging_options: The CloudWatch logging options for your Firehose stream.
            :param compression_format: The type of compression that Kinesis Data Firehose uses to compress the data that it delivers to the Amazon S3 bucket. For valid values, see the ``CompressionFormat`` content for the `S3DestinationConfiguration <https://docs.aws.amazon.com/firehose/latest/APIReference/API_S3DestinationConfiguration.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .
            :param encryption_configuration: Configures Amazon Simple Storage Service (Amazon S3) server-side encryption. Kinesis Data Firehose uses AWS Key Management Service ( AWS KMS) to encrypt the data that it delivers to your Amazon S3 bucket.
            :param error_output_prefix: A prefix that Kinesis Data Firehose evaluates and adds to failed records before writing them to S3. This prefix appears immediately following the bucket name. For information about how to specify this prefix, see `Custom Prefixes for Amazon S3 Objects <https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html>`_ .
            :param prefix: A prefix that Kinesis Data Firehose adds to the files that it delivers to the Amazon S3 bucket. The prefix helps you identify the files that Kinesis Data Firehose delivered.
            :param role_arn: The ARN of an AWS Identity and Access Management (IAM) role that grants Kinesis Data Firehose access to your Amazon S3 bucket and AWS KMS (if you enable data encryption). For more information, see `Grant Kinesis Data Firehose Access to an Amazon S3 Destination <https://docs.aws.amazon.com/firehose/latest/dev/controlling-access.html#using-iam-s3>`_ in the *Amazon Kinesis Data Firehose Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                s3_destination_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty(
                    bucket_arn="bucketArn",
                    buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                        interval_in_seconds=123,
                        size_in_mBs=123
                    ),
                    cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                        enabled=False,
                        log_group_name="logGroupName",
                        log_stream_name="logStreamName"
                    ),
                    compression_format="compressionFormat",
                    encryption_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty(
                        kms_encryption_config=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty(
                            awskms_key_arn="awskmsKeyArn"
                        ),
                        no_encryption_config="noEncryptionConfig"
                    ),
                    error_output_prefix="errorOutputPrefix",
                    prefix="prefix",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__162a83982546ab228dd6e2a8ff7b72be33a25b871e99f2a463ec221b13926058)
                check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
                check_type(argname="argument buffering_hints", value=buffering_hints, expected_type=type_hints["buffering_hints"])
                check_type(argname="argument cloud_watch_logging_options", value=cloud_watch_logging_options, expected_type=type_hints["cloud_watch_logging_options"])
                check_type(argname="argument compression_format", value=compression_format, expected_type=type_hints["compression_format"])
                check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
                check_type(argname="argument error_output_prefix", value=error_output_prefix, expected_type=type_hints["error_output_prefix"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_arn is not None:
                self._values["bucket_arn"] = bucket_arn
            if buffering_hints is not None:
                self._values["buffering_hints"] = buffering_hints
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if compression_format is not None:
                self._values["compression_format"] = compression_format
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if error_output_prefix is not None:
                self._values["error_output_prefix"] = error_output_prefix
            if prefix is not None:
                self._values["prefix"] = prefix
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def bucket_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon S3 bucket to send data to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-bucketarn
            '''
            result = self._values.get("bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def buffering_hints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.BufferingHintsProperty"]]:
            '''Configures how Kinesis Data Firehose buffers incoming data while delivering it to the Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-bufferinghints
            '''
            result = self._values.get("buffering_hints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.BufferingHintsProperty"]], result)

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]]:
            '''The CloudWatch logging options for your Firehose stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-cloudwatchloggingoptions
            '''
            result = self._values.get("cloud_watch_logging_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]], result)

        @builtins.property
        def compression_format(self) -> typing.Optional[builtins.str]:
            '''The type of compression that Kinesis Data Firehose uses to compress the data that it delivers to the Amazon S3 bucket.

            For valid values, see the ``CompressionFormat`` content for the `S3DestinationConfiguration <https://docs.aws.amazon.com/firehose/latest/APIReference/API_S3DestinationConfiguration.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-compressionformat
            '''
            result = self._values.get("compression_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty"]]:
            '''Configures Amazon Simple Storage Service (Amazon S3) server-side encryption.

            Kinesis Data Firehose uses AWS Key Management Service ( AWS KMS) to encrypt the data that it delivers to your Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty"]], result)

        @builtins.property
        def error_output_prefix(self) -> typing.Optional[builtins.str]:
            '''A prefix that Kinesis Data Firehose evaluates and adds to failed records before writing them to S3.

            This prefix appears immediately following the bucket name. For information about how to specify this prefix, see `Custom Prefixes for Amazon S3 Objects <https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-erroroutputprefix
            '''
            result = self._values.get("error_output_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''A prefix that Kinesis Data Firehose adds to the files that it delivers to the Amazon S3 bucket.

            The prefix helps you identify the files that Kinesis Data Firehose delivered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of an AWS Identity and Access Management (IAM) role that grants Kinesis Data Firehose access to your Amazon S3 bucket and AWS KMS (if you enable data encryption).

            For more information, see `Grant Kinesis Data Firehose Access to an Amazon S3 Destination <https://docs.aws.amazon.com/firehose/latest/dev/controlling-access.html#using-iam-s3>`_ in the *Amazon Kinesis Data Firehose Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.SchemaConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "database_name": "databaseName",
            "region": "region",
            "role_arn": "roleArn",
            "table_name": "tableName",
            "version_id": "versionId",
        },
    )
    class SchemaConfigurationProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
            version_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the schema to which you want Firehose to configure your data before it writes it to Amazon S3.

            This parameter is required if ``Enabled`` is set to true.

            :param catalog_id: The ID of the AWS Glue Data Catalog. If you don't supply this, the AWS account ID is used by default.
            :param database_name: Specifies the name of the AWS Glue database that contains the schema for the output data. .. epigraph:: If the ``SchemaConfiguration`` request parameter is used as part of invoking the ``CreateDeliveryStream`` API, then the ``DatabaseName`` property is required and its value must be specified.
            :param region: If you don't specify an AWS Region, the default is the current Region.
            :param role_arn: The role that Firehose can use to access AWS Glue. This role must be in the same account you use for Firehose. Cross-account roles aren't allowed. .. epigraph:: If the ``SchemaConfiguration`` request parameter is used as part of invoking the ``CreateDeliveryStream`` API, then the ``RoleARN`` property is required and its value must be specified.
            :param table_name: Specifies the AWS Glue table that contains the column information that constitutes your data schema. .. epigraph:: If the ``SchemaConfiguration`` request parameter is used as part of invoking the ``CreateDeliveryStream`` API, then the ``TableName`` property is required and its value must be specified.
            :param version_id: Specifies the table version for the output data schema. If you don't specify this version ID, or if you set it to ``LATEST`` , Firehose uses the most recent version. This means that any updates to the table are automatically picked up.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                schema_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SchemaConfigurationProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    region="region",
                    role_arn="roleArn",
                    table_name="tableName",
                    version_id="versionId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9fc21cd148fb795183ec127a12ebdd26c11509a61fd42511664ab9d6353ac12a)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if database_name is not None:
                self._values["database_name"] = database_name
            if region is not None:
                self._values["region"] = region
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if table_name is not None:
                self._values["table_name"] = table_name
            if version_id is not None:
                self._values["version_id"] = version_id

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the AWS Glue Data Catalog.

            If you don't supply this, the AWS account ID is used by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaconfiguration.html#cfn-kinesisfirehose-deliverystream-schemaconfiguration-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''Specifies the name of the AWS Glue database that contains the schema for the output data.

            .. epigraph::

               If the ``SchemaConfiguration`` request parameter is used as part of invoking the ``CreateDeliveryStream`` API, then the ``DatabaseName`` property is required and its value must be specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaconfiguration.html#cfn-kinesisfirehose-deliverystream-schemaconfiguration-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''If you don't specify an AWS Region, the default is the current Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaconfiguration.html#cfn-kinesisfirehose-deliverystream-schemaconfiguration-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The role that Firehose can use to access AWS Glue.

            This role must be in the same account you use for Firehose. Cross-account roles aren't allowed.
            .. epigraph::

               If the ``SchemaConfiguration`` request parameter is used as part of invoking the ``CreateDeliveryStream`` API, then the ``RoleARN`` property is required and its value must be specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaconfiguration.html#cfn-kinesisfirehose-deliverystream-schemaconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''Specifies the AWS Glue table that contains the column information that constitutes your data schema.

            .. epigraph::

               If the ``SchemaConfiguration`` request parameter is used as part of invoking the ``CreateDeliveryStream`` API, then the ``TableName`` property is required and its value must be specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaconfiguration.html#cfn-kinesisfirehose-deliverystream-schemaconfiguration-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version_id(self) -> typing.Optional[builtins.str]:
            '''Specifies the table version for the output data schema.

            If you don't specify this version ID, or if you set it to ``LATEST`` , Firehose uses the most recent version. This means that any updates to the table are automatically picked up.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaconfiguration.html#cfn-kinesisfirehose-deliverystream-schemaconfiguration-versionid
            '''
            result = self._values.get("version_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.SchemaEvolutionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class SchemaEvolutionConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The configuration to enable schema evolution.

            Amazon Data Firehose is in preview release and is subject to change.

            :param enabled: Specify whether you want to enable schema evolution. Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaevolutionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                schema_evolution_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SchemaEvolutionConfigurationProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__722be063ef79b47f7c7a44156c43e4e137e8afb5bd0992a071d183f892955443)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify whether you want to enable schema evolution.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaevolutionconfiguration.html#cfn-kinesisfirehose-deliverystream-schemaevolutionconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaEvolutionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "role_arn": "roleArn",
            "secret_arn": "secretArn",
        },
    )
    class SecretsManagerConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The structure that defines how Firehose accesses the secret.

            :param enabled: Specifies whether you want to use the secrets manager feature. When set as ``True`` the secrets manager configuration overwrites the existing secrets in the destination configuration. When it's set to ``False`` Firehose falls back to the credentials in the destination configuration.
            :param role_arn: Specifies the role that Firehose assumes when calling the Secrets Manager API operation. When you provide the role, it overrides any destination specific role defined in the destination configuration. If you do not provide the then we use the destination specific role. This parameter is required for Splunk.
            :param secret_arn: The ARN of the secret that stores your credentials. It must be in the same region as the Firehose stream and the role. The secret ARN can reside in a different account than the Firehose stream and role as Firehose supports cross-account secret access. This parameter is required when *Enabled* is set to ``True`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-secretsmanagerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                secrets_manager_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty(
                    enabled=False,
                    role_arn="roleArn",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b03ddff3c4d17886193b4fe55d5f0da3129c4d737a8446e85959b3981c099284)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether you want to use the secrets manager feature.

            When set as ``True`` the secrets manager configuration overwrites the existing secrets in the destination configuration. When it's set to ``False`` Firehose falls back to the credentials in the destination configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-secretsmanagerconfiguration.html#cfn-kinesisfirehose-deliverystream-secretsmanagerconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the role that Firehose assumes when calling the Secrets Manager API operation.

            When you provide the role, it overrides any destination specific role defined in the destination configuration. If you do not provide the then we use the destination specific role. This parameter is required for Splunk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-secretsmanagerconfiguration.html#cfn-kinesisfirehose-deliverystream-secretsmanagerconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the secret that stores your credentials.

            It must be in the same region as the Firehose stream and the role. The secret ARN can reside in a different account than the Firehose stream and role as Firehose supports cross-account secret access. This parameter is required when *Enabled* is set to ``True`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-secretsmanagerconfiguration.html#cfn-kinesisfirehose-deliverystream-secretsmanagerconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretsManagerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.SerializerProperty",
        jsii_struct_bases=[],
        name_mapping={"orc_ser_de": "orcSerDe", "parquet_ser_de": "parquetSerDe"},
    )
    class SerializerProperty:
        def __init__(
            self,
            *,
            orc_ser_de: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.OrcSerDeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parquet_ser_de: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ParquetSerDeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The serializer that you want Firehose to use to convert data to the target format before writing it to Amazon S3.

            Firehose supports two types of serializers: the ORC SerDe and the Parquet SerDe.

            :param orc_ser_de: A serializer to use for converting data to the ORC format before storing it in Amazon S3. For more information, see `Apache ORC <https://docs.aws.amazon.com/https://orc.apache.org/docs/>`_ .
            :param parquet_ser_de: A serializer to use for converting data to the Parquet format before storing it in Amazon S3. For more information, see `Apache Parquet <https://docs.aws.amazon.com/https://parquet.apache.org/docs/contribution-guidelines/>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-serializer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                serializer_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SerializerProperty(
                    orc_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.OrcSerDeProperty(
                        block_size_bytes=123,
                        bloom_filter_columns=["bloomFilterColumns"],
                        bloom_filter_false_positive_probability=123,
                        compression="compression",
                        dictionary_key_threshold=123,
                        enable_padding=False,
                        format_version="formatVersion",
                        padding_tolerance=123,
                        row_index_stride=123,
                        stripe_size_bytes=123
                    ),
                    parquet_ser_de=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ParquetSerDeProperty(
                        block_size_bytes=123,
                        compression="compression",
                        enable_dictionary_compression=False,
                        max_padding_bytes=123,
                        page_size_bytes=123,
                        writer_version="writerVersion"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__237799e0d77b8b7822aedebe7aecdecc2def5f249bdcff8f8680cf61838ebafd)
                check_type(argname="argument orc_ser_de", value=orc_ser_de, expected_type=type_hints["orc_ser_de"])
                check_type(argname="argument parquet_ser_de", value=parquet_ser_de, expected_type=type_hints["parquet_ser_de"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if orc_ser_de is not None:
                self._values["orc_ser_de"] = orc_ser_de
            if parquet_ser_de is not None:
                self._values["parquet_ser_de"] = parquet_ser_de

        @builtins.property
        def orc_ser_de(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.OrcSerDeProperty"]]:
            '''A serializer to use for converting data to the ORC format before storing it in Amazon S3.

            For more information, see `Apache ORC <https://docs.aws.amazon.com/https://orc.apache.org/docs/>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-serializer.html#cfn-kinesisfirehose-deliverystream-serializer-orcserde
            '''
            result = self._values.get("orc_ser_de")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.OrcSerDeProperty"]], result)

        @builtins.property
        def parquet_ser_de(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ParquetSerDeProperty"]]:
            '''A serializer to use for converting data to the Parquet format before storing it in Amazon S3.

            For more information, see `Apache Parquet <https://docs.aws.amazon.com/https://parquet.apache.org/docs/contribution-guidelines/>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-serializer.html#cfn-kinesisfirehose-deliverystream-serializer-parquetserde
            '''
            result = self._values.get("parquet_ser_de")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ParquetSerDeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SerializerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.SnowflakeBufferingHintsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "interval_in_seconds": "intervalInSeconds",
            "size_in_m_bs": "sizeInMBs",
        },
    )
    class SnowflakeBufferingHintsProperty:
        def __init__(
            self,
            *,
            interval_in_seconds: typing.Optional[jsii.Number] = None,
            size_in_m_bs: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the buffering to perform before delivering data to the Snowflake destination.

            If you do not specify any value, Firehose uses the default values.

            :param interval_in_seconds: Buffer incoming data for the specified period of time, in seconds, before delivering it to the destination. The default value is 0.
            :param size_in_m_bs: Buffer incoming data to the specified size, in MBs, before delivering it to the destination. The default value is 128.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakebufferinghints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                snowflake_buffering_hints_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SnowflakeBufferingHintsProperty(
                    interval_in_seconds=123,
                    size_in_mBs=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e935d391029a093ae8d3b58f0373cc919f6472c6d12f5fd7f80ec0382a07446d)
                check_type(argname="argument interval_in_seconds", value=interval_in_seconds, expected_type=type_hints["interval_in_seconds"])
                check_type(argname="argument size_in_m_bs", value=size_in_m_bs, expected_type=type_hints["size_in_m_bs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if interval_in_seconds is not None:
                self._values["interval_in_seconds"] = interval_in_seconds
            if size_in_m_bs is not None:
                self._values["size_in_m_bs"] = size_in_m_bs

        @builtins.property
        def interval_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''Buffer incoming data for the specified period of time, in seconds, before delivering it to the destination.

            The default value is 0.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakebufferinghints.html#cfn-kinesisfirehose-deliverystream-snowflakebufferinghints-intervalinseconds
            '''
            result = self._values.get("interval_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def size_in_m_bs(self) -> typing.Optional[jsii.Number]:
            '''Buffer incoming data to the specified size, in MBs, before delivering it to the destination.

            The default value is 128.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakebufferinghints.html#cfn-kinesisfirehose-deliverystream-snowflakebufferinghints-sizeinmbs
            '''
            result = self._values.get("size_in_m_bs")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeBufferingHintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.SnowflakeDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_url": "accountUrl",
            "buffering_hints": "bufferingHints",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "content_column_name": "contentColumnName",
            "database": "database",
            "data_loading_option": "dataLoadingOption",
            "key_passphrase": "keyPassphrase",
            "meta_data_column_name": "metaDataColumnName",
            "private_key": "privateKey",
            "processing_configuration": "processingConfiguration",
            "retry_options": "retryOptions",
            "role_arn": "roleArn",
            "s3_backup_mode": "s3BackupMode",
            "s3_configuration": "s3Configuration",
            "schema": "schema",
            "secrets_manager_configuration": "secretsManagerConfiguration",
            "snowflake_role_configuration": "snowflakeRoleConfiguration",
            "snowflake_vpc_configuration": "snowflakeVpcConfiguration",
            "table": "table",
            "user": "user",
        },
    )
    class SnowflakeDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            account_url: typing.Optional[builtins.str] = None,
            buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SnowflakeBufferingHintsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            content_column_name: typing.Optional[builtins.str] = None,
            database: typing.Optional[builtins.str] = None,
            data_loading_option: typing.Optional[builtins.str] = None,
            key_passphrase: typing.Optional[builtins.str] = None,
            meta_data_column_name: typing.Optional[builtins.str] = None,
            private_key: typing.Optional[builtins.str] = None,
            processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SnowflakeRetryOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            s3_backup_mode: typing.Optional[builtins.str] = None,
            s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            schema: typing.Optional[builtins.str] = None,
            secrets_manager_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            snowflake_role_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SnowflakeRoleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            snowflake_vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SnowflakeVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table: typing.Optional[builtins.str] = None,
            user: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configure Snowflake destination.

            :param account_url: URL for accessing your Snowflake account. This URL must include your `account identifier <https://docs.aws.amazon.com/https://docs.snowflake.com/en/user-guide/admin-account-identifier>`_ . Note that the protocol (https://) and port number are optional.
            :param buffering_hints: Describes the buffering to perform before delivering data to the Snowflake destination. If you do not specify any value, Firehose uses the default values.
            :param cloud_watch_logging_options: 
            :param content_column_name: The name of the record content column.
            :param database: All data in Snowflake is maintained in databases.
            :param data_loading_option: Choose to load JSON keys mapped to table column names or choose to split the JSON payload where content is mapped to a record content column and source metadata is mapped to a record metadata column.
            :param key_passphrase: Passphrase to decrypt the private key when the key is encrypted. For information, see `Using Key Pair Authentication & Key Rotation <https://docs.aws.amazon.com/https://docs.snowflake.com/en/user-guide/data-load-snowpipe-streaming-configuration#using-key-pair-authentication-key-rotation>`_ .
            :param meta_data_column_name: Specify a column name in the table, where the metadata information has to be loaded. When you enable this field, you will see the following column in the snowflake table, which differs based on the source type. For Direct PUT as source ``{ "firehoseDeliveryStreamName" : "streamname", "IngestionTime" : "timestamp" }`` For Kinesis Data Stream as source ``"kinesisStreamName" : "streamname", "kinesisShardId" : "Id", "kinesisPartitionKey" : "key", "kinesisSequenceNumber" : "1234", "subsequenceNumber" : "2334", "IngestionTime" : "timestamp" }``
            :param private_key: The private key used to encrypt your Snowflake client. For information, see `Using Key Pair Authentication & Key Rotation <https://docs.aws.amazon.com/https://docs.snowflake.com/en/user-guide/data-load-snowpipe-streaming-configuration#using-key-pair-authentication-key-rotation>`_ .
            :param processing_configuration: 
            :param retry_options: The time period where Firehose will retry sending data to the chosen HTTP endpoint.
            :param role_arn: The Amazon Resource Name (ARN) of the Snowflake role.
            :param s3_backup_mode: Choose an S3 backup mode.
            :param s3_configuration: 
            :param schema: Each database consists of one or more schemas, which are logical groupings of database objects, such as tables and views.
            :param secrets_manager_configuration: The configuration that defines how you access secrets for Snowflake.
            :param snowflake_role_configuration: Optionally configure a Snowflake role. Otherwise the default user role will be used.
            :param snowflake_vpc_configuration: The VPCE ID for Firehose to privately connect with Snowflake. The ID format is com.amazonaws.vpce.[region].vpce-svc-<[id]>. For more information, see `Amazon PrivateLink & Snowflake <https://docs.aws.amazon.com/https://docs.snowflake.com/en/user-guide/admin-security-privatelink>`_
            :param table: All data in Snowflake is stored in database tables, logically structured as collections of columns and rows.
            :param user: User login name for the Snowflake account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                snowflake_destination_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SnowflakeDestinationConfigurationProperty(
                    account_url="accountUrl",
                    buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SnowflakeBufferingHintsProperty(
                        interval_in_seconds=123,
                        size_in_mBs=123
                    ),
                    cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                        enabled=False,
                        log_group_name="logGroupName",
                        log_stream_name="logStreamName"
                    ),
                    content_column_name="contentColumnName",
                    database="database",
                    data_loading_option="dataLoadingOption",
                    key_passphrase="keyPassphrase",
                    meta_data_column_name="metaDataColumnName",
                    private_key="privateKey",
                    processing_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty(
                        enabled=False,
                        processors=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorProperty(
                            parameters=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorParameterProperty(
                                parameter_name="parameterName",
                                parameter_value="parameterValue"
                            )],
                            type="type"
                        )]
                    ),
                    retry_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SnowflakeRetryOptionsProperty(
                        duration_in_seconds=123
                    ),
                    role_arn="roleArn",
                    s3_backup_mode="s3BackupMode",
                    s3_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty(
                        bucket_arn="bucketArn",
                        buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                            interval_in_seconds=123,
                            size_in_mBs=123
                        ),
                        cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                            enabled=False,
                            log_group_name="logGroupName",
                            log_stream_name="logStreamName"
                        ),
                        compression_format="compressionFormat",
                        encryption_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty(
                            kms_encryption_config=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty(
                                awskms_key_arn="awskmsKeyArn"
                            ),
                            no_encryption_config="noEncryptionConfig"
                        ),
                        error_output_prefix="errorOutputPrefix",
                        prefix="prefix",
                        role_arn="roleArn"
                    ),
                    schema="schema",
                    secrets_manager_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty(
                        enabled=False,
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    ),
                    snowflake_role_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SnowflakeRoleConfigurationProperty(
                        enabled=False,
                        snowflake_role="snowflakeRole"
                    ),
                    snowflake_vpc_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SnowflakeVpcConfigurationProperty(
                        private_link_vpce_id="privateLinkVpceId"
                    ),
                    table="table",
                    user="user"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c8df9b78113b3e3b2c45aac3a7b30427f872d6b9bea8040c378605c7fa150612)
                check_type(argname="argument account_url", value=account_url, expected_type=type_hints["account_url"])
                check_type(argname="argument buffering_hints", value=buffering_hints, expected_type=type_hints["buffering_hints"])
                check_type(argname="argument cloud_watch_logging_options", value=cloud_watch_logging_options, expected_type=type_hints["cloud_watch_logging_options"])
                check_type(argname="argument content_column_name", value=content_column_name, expected_type=type_hints["content_column_name"])
                check_type(argname="argument database", value=database, expected_type=type_hints["database"])
                check_type(argname="argument data_loading_option", value=data_loading_option, expected_type=type_hints["data_loading_option"])
                check_type(argname="argument key_passphrase", value=key_passphrase, expected_type=type_hints["key_passphrase"])
                check_type(argname="argument meta_data_column_name", value=meta_data_column_name, expected_type=type_hints["meta_data_column_name"])
                check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
                check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
                check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
                check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
                check_type(argname="argument secrets_manager_configuration", value=secrets_manager_configuration, expected_type=type_hints["secrets_manager_configuration"])
                check_type(argname="argument snowflake_role_configuration", value=snowflake_role_configuration, expected_type=type_hints["snowflake_role_configuration"])
                check_type(argname="argument snowflake_vpc_configuration", value=snowflake_vpc_configuration, expected_type=type_hints["snowflake_vpc_configuration"])
                check_type(argname="argument table", value=table, expected_type=type_hints["table"])
                check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_url is not None:
                self._values["account_url"] = account_url
            if buffering_hints is not None:
                self._values["buffering_hints"] = buffering_hints
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if content_column_name is not None:
                self._values["content_column_name"] = content_column_name
            if database is not None:
                self._values["database"] = database
            if data_loading_option is not None:
                self._values["data_loading_option"] = data_loading_option
            if key_passphrase is not None:
                self._values["key_passphrase"] = key_passphrase
            if meta_data_column_name is not None:
                self._values["meta_data_column_name"] = meta_data_column_name
            if private_key is not None:
                self._values["private_key"] = private_key
            if processing_configuration is not None:
                self._values["processing_configuration"] = processing_configuration
            if retry_options is not None:
                self._values["retry_options"] = retry_options
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if s3_backup_mode is not None:
                self._values["s3_backup_mode"] = s3_backup_mode
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration
            if schema is not None:
                self._values["schema"] = schema
            if secrets_manager_configuration is not None:
                self._values["secrets_manager_configuration"] = secrets_manager_configuration
            if snowflake_role_configuration is not None:
                self._values["snowflake_role_configuration"] = snowflake_role_configuration
            if snowflake_vpc_configuration is not None:
                self._values["snowflake_vpc_configuration"] = snowflake_vpc_configuration
            if table is not None:
                self._values["table"] = table
            if user is not None:
                self._values["user"] = user

        @builtins.property
        def account_url(self) -> typing.Optional[builtins.str]:
            '''URL for accessing your Snowflake account.

            This URL must include your `account identifier <https://docs.aws.amazon.com/https://docs.snowflake.com/en/user-guide/admin-account-identifier>`_ . Note that the protocol (https://) and port number are optional.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-accounturl
            '''
            result = self._values.get("account_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def buffering_hints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SnowflakeBufferingHintsProperty"]]:
            '''Describes the buffering to perform before delivering data to the Snowflake destination.

            If you do not specify any value, Firehose uses the default values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-bufferinghints
            '''
            result = self._values.get("buffering_hints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SnowflakeBufferingHintsProperty"]], result)

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-cloudwatchloggingoptions
            '''
            result = self._values.get("cloud_watch_logging_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]], result)

        @builtins.property
        def content_column_name(self) -> typing.Optional[builtins.str]:
            '''The name of the record content column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-contentcolumnname
            '''
            result = self._values.get("content_column_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database(self) -> typing.Optional[builtins.str]:
            '''All data in Snowflake is maintained in databases.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-database
            '''
            result = self._values.get("database")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_loading_option(self) -> typing.Optional[builtins.str]:
            '''Choose to load JSON keys mapped to table column names or choose to split the JSON payload where content is mapped to a record content column and source metadata is mapped to a record metadata column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-dataloadingoption
            '''
            result = self._values.get("data_loading_option")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_passphrase(self) -> typing.Optional[builtins.str]:
            '''Passphrase to decrypt the private key when the key is encrypted.

            For information, see `Using Key Pair Authentication & Key Rotation <https://docs.aws.amazon.com/https://docs.snowflake.com/en/user-guide/data-load-snowpipe-streaming-configuration#using-key-pair-authentication-key-rotation>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-keypassphrase
            '''
            result = self._values.get("key_passphrase")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def meta_data_column_name(self) -> typing.Optional[builtins.str]:
            '''Specify a column name in the table, where the metadata information has to be loaded.

            When you enable this field, you will see the following column in the snowflake table, which differs based on the source type.

            For Direct PUT as source

            ``{ "firehoseDeliveryStreamName" : "streamname", "IngestionTime" : "timestamp" }``

            For Kinesis Data Stream as source

            ``"kinesisStreamName" : "streamname", "kinesisShardId" : "Id", "kinesisPartitionKey" : "key", "kinesisSequenceNumber" : "1234", "subsequenceNumber" : "2334", "IngestionTime" : "timestamp" }``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-metadatacolumnname
            '''
            result = self._values.get("meta_data_column_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_key(self) -> typing.Optional[builtins.str]:
            '''The private key used to encrypt your Snowflake client.

            For information, see `Using Key Pair Authentication & Key Rotation <https://docs.aws.amazon.com/https://docs.snowflake.com/en/user-guide/data-load-snowpipe-streaming-configuration#using-key-pair-authentication-key-rotation>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-privatekey
            '''
            result = self._values.get("private_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-processingconfiguration
            '''
            result = self._values.get("processing_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]], result)

        @builtins.property
        def retry_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SnowflakeRetryOptionsProperty"]]:
            '''The time period where Firehose will retry sending data to the chosen HTTP endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-retryoptions
            '''
            result = self._values.get("retry_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SnowflakeRetryOptionsProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Snowflake role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_backup_mode(self) -> typing.Optional[builtins.str]:
            '''Choose an S3 backup mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-s3backupmode
            '''
            result = self._values.get("s3_backup_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]], result)

        @builtins.property
        def schema(self) -> typing.Optional[builtins.str]:
            '''Each database consists of one or more schemas, which are logical groupings of database objects, such as tables and views.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-schema
            '''
            result = self._values.get("schema")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secrets_manager_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty"]]:
            '''The configuration that defines how you access secrets for Snowflake.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-secretsmanagerconfiguration
            '''
            result = self._values.get("secrets_manager_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty"]], result)

        @builtins.property
        def snowflake_role_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SnowflakeRoleConfigurationProperty"]]:
            '''Optionally configure a Snowflake role.

            Otherwise the default user role will be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-snowflakeroleconfiguration
            '''
            result = self._values.get("snowflake_role_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SnowflakeRoleConfigurationProperty"]], result)

        @builtins.property
        def snowflake_vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SnowflakeVpcConfigurationProperty"]]:
            '''The VPCE ID for Firehose to privately connect with Snowflake.

            The ID format is com.amazonaws.vpce.[region].vpce-svc-<[id]>. For more information, see `Amazon PrivateLink & Snowflake <https://docs.aws.amazon.com/https://docs.snowflake.com/en/user-guide/admin-security-privatelink>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-snowflakevpcconfiguration
            '''
            result = self._values.get("snowflake_vpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SnowflakeVpcConfigurationProperty"]], result)

        @builtins.property
        def table(self) -> typing.Optional[builtins.str]:
            '''All data in Snowflake is stored in database tables, logically structured as collections of columns and rows.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-table
            '''
            result = self._values.get("table")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user(self) -> typing.Optional[builtins.str]:
            '''User login name for the Snowflake account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakedestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakedestinationconfiguration-user
            '''
            result = self._values.get("user")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.SnowflakeRetryOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_in_seconds": "durationInSeconds"},
    )
    class SnowflakeRetryOptionsProperty:
        def __init__(
            self,
            *,
            duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specify how long Firehose retries sending data to the New Relic HTTP endpoint.

            After sending data, Firehose first waits for an acknowledgment from the HTTP endpoint. If an error occurs or the acknowledgment doesn’t arrive within the acknowledgment timeout period, Firehose starts the retry duration counter. It keeps retrying until the retry duration expires. After that, Firehose considers it a data delivery failure and backs up the data to your Amazon S3 bucket. Every time that Firehose sends data to the HTTP endpoint (either the initial attempt or a retry), it restarts the acknowledgement timeout counter and waits for an acknowledgement from the HTTP endpoint. Even if the retry duration expires, Firehose still waits for the acknowledgment until it receives it or the acknowledgement timeout period is reached. If the acknowledgment times out, Firehose determines whether there's time left in the retry counter. If there is time left, it retries again and repeats the logic until it receives an acknowledgment or determines that the retry time has expired. If you don't want Firehose to retry sending data, set this value to 0.

            :param duration_in_seconds: the time period where Firehose will retry sending data to the chosen HTTP endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakeretryoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                snowflake_retry_options_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SnowflakeRetryOptionsProperty(
                    duration_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__debdb3dfd51aaf9fccd5332249045df93dd352e5a46879e26aa9f9084f95d312)
                check_type(argname="argument duration_in_seconds", value=duration_in_seconds, expected_type=type_hints["duration_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''the time period where Firehose will retry sending data to the chosen HTTP endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakeretryoptions.html#cfn-kinesisfirehose-deliverystream-snowflakeretryoptions-durationinseconds
            '''
            result = self._values.get("duration_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeRetryOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.SnowflakeRoleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "snowflake_role": "snowflakeRole"},
    )
    class SnowflakeRoleConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            snowflake_role: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Optionally configure a Snowflake role.

            Otherwise the default user role will be used.

            :param enabled: Enable Snowflake role.
            :param snowflake_role: The Snowflake role you wish to configure.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakeroleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                snowflake_role_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SnowflakeRoleConfigurationProperty(
                    enabled=False,
                    snowflake_role="snowflakeRole"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de984f912a786bbaf1c80de41cbccfa94dfee75a90f1e71b7776cbfbd1d9c15c)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument snowflake_role", value=snowflake_role, expected_type=type_hints["snowflake_role"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if snowflake_role is not None:
                self._values["snowflake_role"] = snowflake_role

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enable Snowflake role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakeroleconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakeroleconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def snowflake_role(self) -> typing.Optional[builtins.str]:
            '''The Snowflake role you wish to configure.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakeroleconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakeroleconfiguration-snowflakerole
            '''
            result = self._values.get("snowflake_role")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeRoleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.SnowflakeVpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"private_link_vpce_id": "privateLinkVpceId"},
    )
    class SnowflakeVpcConfigurationProperty:
        def __init__(
            self,
            *,
            private_link_vpce_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configure a Snowflake VPC.

            :param private_link_vpce_id: The VPCE ID for Firehose to privately connect with Snowflake. The ID format is com.amazonaws.vpce.[region].vpce-svc-<[id]>. For more information, see `Amazon PrivateLink & Snowflake <https://docs.aws.amazon.com/https://docs.snowflake.com/en/user-guide/admin-security-privatelink>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakevpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                snowflake_vpc_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SnowflakeVpcConfigurationProperty(
                    private_link_vpce_id="privateLinkVpceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca2b9bb5796c0026804c3aee05faa6cea9da8038b8e796438f9738facfdd29a9)
                check_type(argname="argument private_link_vpce_id", value=private_link_vpce_id, expected_type=type_hints["private_link_vpce_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if private_link_vpce_id is not None:
                self._values["private_link_vpce_id"] = private_link_vpce_id

        @builtins.property
        def private_link_vpce_id(self) -> typing.Optional[builtins.str]:
            '''The VPCE ID for Firehose to privately connect with Snowflake.

            The ID format is com.amazonaws.vpce.[region].vpce-svc-<[id]>. For more information, see `Amazon PrivateLink & Snowflake <https://docs.aws.amazon.com/https://docs.snowflake.com/en/user-guide/admin-security-privatelink>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-snowflakevpcconfiguration.html#cfn-kinesisfirehose-deliverystream-snowflakevpcconfiguration-privatelinkvpceid
            '''
            result = self._values.get("private_link_vpce_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeVpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.SplunkBufferingHintsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "interval_in_seconds": "intervalInSeconds",
            "size_in_m_bs": "sizeInMBs",
        },
    )
    class SplunkBufferingHintsProperty:
        def __init__(
            self,
            *,
            interval_in_seconds: typing.Optional[jsii.Number] = None,
            size_in_m_bs: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The buffering options.

            If no value is specified, the default values for Splunk are used.

            :param interval_in_seconds: Buffer incoming data for the specified period of time, in seconds, before delivering it to the destination. The default value is 60 (1 minute).
            :param size_in_m_bs: Buffer incoming data to the specified size, in MBs, before delivering it to the destination. The default value is 5.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkbufferinghints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                splunk_buffering_hints_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SplunkBufferingHintsProperty(
                    interval_in_seconds=123,
                    size_in_mBs=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__19b780637cbd31c5a7253c27eb28007ca3f451ac85e127ef5cb492756e30944e)
                check_type(argname="argument interval_in_seconds", value=interval_in_seconds, expected_type=type_hints["interval_in_seconds"])
                check_type(argname="argument size_in_m_bs", value=size_in_m_bs, expected_type=type_hints["size_in_m_bs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if interval_in_seconds is not None:
                self._values["interval_in_seconds"] = interval_in_seconds
            if size_in_m_bs is not None:
                self._values["size_in_m_bs"] = size_in_m_bs

        @builtins.property
        def interval_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''Buffer incoming data for the specified period of time, in seconds, before delivering it to the destination.

            The default value is 60 (1 minute).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkbufferinghints.html#cfn-kinesisfirehose-deliverystream-splunkbufferinghints-intervalinseconds
            '''
            result = self._values.get("interval_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def size_in_m_bs(self) -> typing.Optional[jsii.Number]:
            '''Buffer incoming data to the specified size, in MBs, before delivering it to the destination.

            The default value is 5.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkbufferinghints.html#cfn-kinesisfirehose-deliverystream-splunkbufferinghints-sizeinmbs
            '''
            result = self._values.get("size_in_m_bs")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SplunkBufferingHintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.SplunkDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "buffering_hints": "bufferingHints",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "hec_acknowledgment_timeout_in_seconds": "hecAcknowledgmentTimeoutInSeconds",
            "hec_endpoint": "hecEndpoint",
            "hec_endpoint_type": "hecEndpointType",
            "hec_token": "hecToken",
            "processing_configuration": "processingConfiguration",
            "retry_options": "retryOptions",
            "s3_backup_mode": "s3BackupMode",
            "s3_configuration": "s3Configuration",
            "secrets_manager_configuration": "secretsManagerConfiguration",
        },
    )
    class SplunkDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SplunkBufferingHintsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            hec_acknowledgment_timeout_in_seconds: typing.Optional[jsii.Number] = None,
            hec_endpoint: typing.Optional[builtins.str] = None,
            hec_endpoint_type: typing.Optional[builtins.str] = None,
            hec_token: typing.Optional[builtins.str] = None,
            processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SplunkRetryOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_backup_mode: typing.Optional[builtins.str] = None,
            s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secrets_manager_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``SplunkDestinationConfiguration`` property type specifies the configuration of a destination in Splunk for a Kinesis Data Firehose delivery stream.

            :param buffering_hints: The buffering options. If no value is specified, the default values for Splunk are used.
            :param cloud_watch_logging_options: The Amazon CloudWatch logging options for your Firehose stream.
            :param hec_acknowledgment_timeout_in_seconds: The amount of time that Firehose waits to receive an acknowledgment from Splunk after it sends it data. At the end of the timeout period, Firehose either tries to send the data again or considers it an error, based on your retry settings.
            :param hec_endpoint: The HTTP Event Collector (HEC) endpoint to which Firehose sends your data.
            :param hec_endpoint_type: This type can be either ``Raw`` or ``Event`` .
            :param hec_token: This is a GUID that you obtain from your Splunk cluster when you create a new HEC endpoint.
            :param processing_configuration: The data processing configuration.
            :param retry_options: The retry behavior in case Firehose is unable to deliver data to Splunk, or if it doesn't receive an acknowledgment of receipt from Splunk.
            :param s3_backup_mode: Defines how documents should be delivered to Amazon S3. When set to ``FailedEventsOnly`` , Firehose writes any data that could not be indexed to the configured Amazon S3 destination. When set to ``AllEvents`` , Firehose delivers all incoming records to Amazon S3, and also writes failed documents to Amazon S3. The default value is ``FailedEventsOnly`` . You can update this backup mode from ``FailedEventsOnly`` to ``AllEvents`` . You can't update it from ``AllEvents`` to ``FailedEventsOnly`` .
            :param s3_configuration: The configuration for the backup Amazon S3 location.
            :param secrets_manager_configuration: The configuration that defines how you access secrets for Splunk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                splunk_destination_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SplunkDestinationConfigurationProperty(
                    buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SplunkBufferingHintsProperty(
                        interval_in_seconds=123,
                        size_in_mBs=123
                    ),
                    cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                        enabled=False,
                        log_group_name="logGroupName",
                        log_stream_name="logStreamName"
                    ),
                    hec_acknowledgment_timeout_in_seconds=123,
                    hec_endpoint="hecEndpoint",
                    hec_endpoint_type="hecEndpointType",
                    hec_token="hecToken",
                    processing_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty(
                        enabled=False,
                        processors=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorProperty(
                            parameters=[kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.ProcessorParameterProperty(
                                parameter_name="parameterName",
                                parameter_value="parameterValue"
                            )],
                            type="type"
                        )]
                    ),
                    retry_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SplunkRetryOptionsProperty(
                        duration_in_seconds=123
                    ),
                    s3_backup_mode="s3BackupMode",
                    s3_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty(
                        bucket_arn="bucketArn",
                        buffering_hints=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.BufferingHintsProperty(
                            interval_in_seconds=123,
                            size_in_mBs=123
                        ),
                        cloud_watch_logging_options=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty(
                            enabled=False,
                            log_group_name="logGroupName",
                            log_stream_name="logStreamName"
                        ),
                        compression_format="compressionFormat",
                        encryption_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty(
                            kms_encryption_config=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty(
                                awskms_key_arn="awskmsKeyArn"
                            ),
                            no_encryption_config="noEncryptionConfig"
                        ),
                        error_output_prefix="errorOutputPrefix",
                        prefix="prefix",
                        role_arn="roleArn"
                    ),
                    secrets_manager_configuration=kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty(
                        enabled=False,
                        role_arn="roleArn",
                        secret_arn="secretArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72c3e65767c9bb42c2a4788c10c8f05059dc7bcf6558c46180f99f9f15805e4a)
                check_type(argname="argument buffering_hints", value=buffering_hints, expected_type=type_hints["buffering_hints"])
                check_type(argname="argument cloud_watch_logging_options", value=cloud_watch_logging_options, expected_type=type_hints["cloud_watch_logging_options"])
                check_type(argname="argument hec_acknowledgment_timeout_in_seconds", value=hec_acknowledgment_timeout_in_seconds, expected_type=type_hints["hec_acknowledgment_timeout_in_seconds"])
                check_type(argname="argument hec_endpoint", value=hec_endpoint, expected_type=type_hints["hec_endpoint"])
                check_type(argname="argument hec_endpoint_type", value=hec_endpoint_type, expected_type=type_hints["hec_endpoint_type"])
                check_type(argname="argument hec_token", value=hec_token, expected_type=type_hints["hec_token"])
                check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
                check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
                check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
                check_type(argname="argument secrets_manager_configuration", value=secrets_manager_configuration, expected_type=type_hints["secrets_manager_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if buffering_hints is not None:
                self._values["buffering_hints"] = buffering_hints
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if hec_acknowledgment_timeout_in_seconds is not None:
                self._values["hec_acknowledgment_timeout_in_seconds"] = hec_acknowledgment_timeout_in_seconds
            if hec_endpoint is not None:
                self._values["hec_endpoint"] = hec_endpoint
            if hec_endpoint_type is not None:
                self._values["hec_endpoint_type"] = hec_endpoint_type
            if hec_token is not None:
                self._values["hec_token"] = hec_token
            if processing_configuration is not None:
                self._values["processing_configuration"] = processing_configuration
            if retry_options is not None:
                self._values["retry_options"] = retry_options
            if s3_backup_mode is not None:
                self._values["s3_backup_mode"] = s3_backup_mode
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration
            if secrets_manager_configuration is not None:
                self._values["secrets_manager_configuration"] = secrets_manager_configuration

        @builtins.property
        def buffering_hints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SplunkBufferingHintsProperty"]]:
            '''The buffering options.

            If no value is specified, the default values for Splunk are used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-bufferinghints
            '''
            result = self._values.get("buffering_hints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SplunkBufferingHintsProperty"]], result)

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]]:
            '''The Amazon CloudWatch logging options for your Firehose stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-cloudwatchloggingoptions
            '''
            result = self._values.get("cloud_watch_logging_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty"]], result)

        @builtins.property
        def hec_acknowledgment_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The amount of time that Firehose waits to receive an acknowledgment from Splunk after it sends it data.

            At the end of the timeout period, Firehose either tries to send the data again or considers it an error, based on your retry settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-hecacknowledgmenttimeoutinseconds
            '''
            result = self._values.get("hec_acknowledgment_timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def hec_endpoint(self) -> typing.Optional[builtins.str]:
            '''The HTTP Event Collector (HEC) endpoint to which Firehose sends your data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-hecendpoint
            '''
            result = self._values.get("hec_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hec_endpoint_type(self) -> typing.Optional[builtins.str]:
            '''This type can be either ``Raw`` or ``Event`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-hecendpointtype
            '''
            result = self._values.get("hec_endpoint_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hec_token(self) -> typing.Optional[builtins.str]:
            '''This is a GUID that you obtain from your Splunk cluster when you create a new HEC endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-hectoken
            '''
            result = self._values.get("hec_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]]:
            '''The data processing configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-processingconfiguration
            '''
            result = self._values.get("processing_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty"]], result)

        @builtins.property
        def retry_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SplunkRetryOptionsProperty"]]:
            '''The retry behavior in case Firehose is unable to deliver data to Splunk, or if it doesn't receive an acknowledgment of receipt from Splunk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-retryoptions
            '''
            result = self._values.get("retry_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SplunkRetryOptionsProperty"]], result)

        @builtins.property
        def s3_backup_mode(self) -> typing.Optional[builtins.str]:
            '''Defines how documents should be delivered to Amazon S3.

            When set to ``FailedEventsOnly`` , Firehose writes any data that could not be indexed to the configured Amazon S3 destination. When set to ``AllEvents`` , Firehose delivers all incoming records to Amazon S3, and also writes failed documents to Amazon S3. The default value is ``FailedEventsOnly`` .

            You can update this backup mode from ``FailedEventsOnly`` to ``AllEvents`` . You can't update it from ``AllEvents`` to ``FailedEventsOnly`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-s3backupmode
            '''
            result = self._values.get("s3_backup_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]]:
            '''The configuration for the backup Amazon S3 location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty"]], result)

        @builtins.property
        def secrets_manager_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty"]]:
            '''The configuration that defines how you access secrets for Splunk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-secretsmanagerconfiguration
            '''
            result = self._values.get("secrets_manager_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SplunkDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.SplunkRetryOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_in_seconds": "durationInSeconds"},
    )
    class SplunkRetryOptionsProperty:
        def __init__(
            self,
            *,
            duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ``SplunkRetryOptions`` property type specifies retry behavior in case Kinesis Data Firehose is unable to deliver documents to Splunk or if it doesn't receive an acknowledgment from Splunk.

            :param duration_in_seconds: The total amount of time that Firehose spends on retries. This duration starts after the initial attempt to send data to Splunk fails. It doesn't include the periods during which Firehose waits for acknowledgment from Splunk after each attempt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkretryoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                splunk_retry_options_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.SplunkRetryOptionsProperty(
                    duration_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__74de9a01d32e57fd7f60024171b9e240e488ad60446a8b229a3072e0caf7d2f7)
                check_type(argname="argument duration_in_seconds", value=duration_in_seconds, expected_type=type_hints["duration_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The total amount of time that Firehose spends on retries.

            This duration starts after the initial attempt to send data to Splunk fails. It doesn't include the periods during which Firehose waits for acknowledgment from Splunk after each attempt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkretryoptions.html#cfn-kinesisfirehose-deliverystream-splunkretryoptions-durationinseconds
            '''
            result = self._values.get("duration_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SplunkRetryOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.TableCreationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class TableCreationConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The configuration to enable automatic table creation.

            Amazon Data Firehose is in preview release and is subject to change.

            :param enabled: Specify whether you want to enable automatic table creation. Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-tablecreationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                table_creation_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.TableCreationConfigurationProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__85cb2e8fd221edff1555f4e757b7ef36b1e089b120ed6d55ea00b671a65f6411)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify whether you want to enable automatic table creation.

            Amazon Data Firehose is in preview release and is subject to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-tablecreationconfiguration.html#cfn-kinesisfirehose-deliverystream-tablecreationconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableCreationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisfirehose.mixins.CfnDeliveryStreamPropsMixin.VpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "role_arn": "roleArn",
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigurationProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The details of the VPC of the Amazon ES destination.

            :param role_arn: The ARN of the IAM role that you want the delivery stream to use to create endpoints in the destination VPC. You can use your existing Kinesis Data Firehose delivery role or you can specify a new role. In either case, make sure that the role trusts the Kinesis Data Firehose service principal and that it grants the following permissions: - ``ec2:DescribeVpcs`` - ``ec2:DescribeVpcAttribute`` - ``ec2:DescribeSubnets`` - ``ec2:DescribeSecurityGroups`` - ``ec2:DescribeNetworkInterfaces`` - ``ec2:CreateNetworkInterface`` - ``ec2:CreateNetworkInterfacePermission`` - ``ec2:DeleteNetworkInterface`` If you revoke these permissions after you create the delivery stream, Kinesis Data Firehose can't scale out by creating more ENIs when necessary. You might therefore see a degradation in performance.
            :param security_group_ids: The IDs of the security groups that you want Kinesis Data Firehose to use when it creates ENIs in the VPC of the Amazon ES destination. You can use the same security group that the Amazon ES domain uses or different ones. If you specify different security groups here, ensure that they allow outbound HTTPS traffic to the Amazon ES domain's security group. Also ensure that the Amazon ES domain's security group allows HTTPS traffic from the security groups specified here. If you use the same security group for both your delivery stream and the Amazon ES domain, make sure the security group inbound rule allows HTTPS traffic.
            :param subnet_ids: The IDs of the subnets that Kinesis Data Firehose uses to create ENIs in the VPC of the Amazon ES destination. Make sure that the routing tables and inbound and outbound rules allow traffic to flow from the subnets whose IDs are specified here to the subnets that have the destination Amazon ES endpoints. Kinesis Data Firehose creates at least one ENI in each of the subnets that are specified here. Do not delete or modify these ENIs. The number of ENIs that Kinesis Data Firehose creates in the subnets specified here scales up and down automatically based on throughput. To enable Kinesis Data Firehose to scale up the number of ENIs to match throughput, ensure that you have sufficient quota. To help you calculate the quota you need, assume that Kinesis Data Firehose can create up to three ENIs for this delivery stream for each of the subnets specified here.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-vpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisfirehose import mixins as kinesisfirehose_mixins
                
                vpc_configuration_property = kinesisfirehose_mixins.CfnDeliveryStreamPropsMixin.VpcConfigurationProperty(
                    role_arn="roleArn",
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__117d5274c373639b716983c65795e0096e67d4744e770029b04889b7094c4951)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role that you want the delivery stream to use to create endpoints in the destination VPC.

            You can use your existing Kinesis Data Firehose delivery role or you can specify a new role. In either case, make sure that the role trusts the Kinesis Data Firehose service principal and that it grants the following permissions:

            - ``ec2:DescribeVpcs``
            - ``ec2:DescribeVpcAttribute``
            - ``ec2:DescribeSubnets``
            - ``ec2:DescribeSecurityGroups``
            - ``ec2:DescribeNetworkInterfaces``
            - ``ec2:CreateNetworkInterface``
            - ``ec2:CreateNetworkInterfacePermission``
            - ``ec2:DeleteNetworkInterface``

            If you revoke these permissions after you create the delivery stream, Kinesis Data Firehose can't scale out by creating more ENIs when necessary. You might therefore see a degradation in performance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-vpcconfiguration.html#cfn-kinesisfirehose-deliverystream-vpcconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IDs of the security groups that you want Kinesis Data Firehose to use when it creates ENIs in the VPC of the Amazon ES destination.

            You can use the same security group that the Amazon ES domain uses or different ones. If you specify different security groups here, ensure that they allow outbound HTTPS traffic to the Amazon ES domain's security group. Also ensure that the Amazon ES domain's security group allows HTTPS traffic from the security groups specified here. If you use the same security group for both your delivery stream and the Amazon ES domain, make sure the security group inbound rule allows HTTPS traffic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-vpcconfiguration.html#cfn-kinesisfirehose-deliverystream-vpcconfiguration-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IDs of the subnets that Kinesis Data Firehose uses to create ENIs in the VPC of the Amazon ES destination.

            Make sure that the routing tables and inbound and outbound rules allow traffic to flow from the subnets whose IDs are specified here to the subnets that have the destination Amazon ES endpoints. Kinesis Data Firehose creates at least one ENI in each of the subnets that are specified here. Do not delete or modify these ENIs.

            The number of ENIs that Kinesis Data Firehose creates in the subnets specified here scales up and down automatically based on throughput. To enable Kinesis Data Firehose to scale up the number of ENIs to match throughput, ensure that you have sufficient quota. To help you calculate the quota you need, assume that Kinesis Data Firehose can create up to three ENIs for this delivery stream for each of the subnets specified here.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-vpcconfiguration.html#cfn-kinesisfirehose-deliverystream-vpcconfiguration-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnDeliveryStreamMixinProps",
    "CfnDeliveryStreamPropsMixin",
]

publication.publish()

def _typecheckingstub__a8c0d24ea05685a9b99a2ef6fc106d75e6d53124454b910e42658f04d8979294(
    *,
    amazon_open_search_serverless_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    amazonopensearchservice_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.AmazonopensearchserviceDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    database_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.DatabaseSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    delivery_stream_encryption_configuration_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.DeliveryStreamEncryptionConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    delivery_stream_name: typing.Optional[builtins.str] = None,
    delivery_stream_type: typing.Optional[builtins.str] = None,
    direct_put_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.DirectPutSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    elasticsearch_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ElasticsearchDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    extended_s3_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ExtendedS3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http_endpoint_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.HttpEndpointDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iceberg_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.IcebergDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_stream_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.KinesisStreamSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    msk_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.MSKSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    redshift_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.RedshiftDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    snowflake_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SnowflakeDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    splunk_destination_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SplunkDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072742e9c2f67afb5cd43f5cc52a2a4dd22f37af49634ebc1b8ed5a6e520830e(
    props: typing.Union[CfnDeliveryStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b9f940583cf5aac1ecd5a66026c8c04bcff9587ba5ccd52b780e5b673ab6c3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92079f2c941668202bdcb18075579c349b3d6d82b26e21a4f22aef1d7f89203(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__558756424ad3de0a7d8dc47092a36c08349a04f2f4ba97d2b7be735faaa4ae51(
    *,
    interval_in_seconds: typing.Optional[jsii.Number] = None,
    size_in_m_bs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__386908b8d9789dbdfb1c2e7ec419619a60b896ed27520f6082030f29101c88bb(
    *,
    buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessBufferingHintsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    collection_endpoint: typing.Optional[builtins.str] = None,
    index_name: typing.Optional[builtins.str] = None,
    processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.AmazonOpenSearchServerlessRetryOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    s3_backup_mode: typing.Optional[builtins.str] = None,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06d6416eb798b2d42ad0753a77feac835ec40948bad96d1579c78690039ebb7(
    *,
    duration_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9d475873392836595dd9e85cce970f1ca92bc822958718beaccb4968e7dc1d(
    *,
    interval_in_seconds: typing.Optional[jsii.Number] = None,
    size_in_m_bs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7ba29e1bed5a99a7bea24258262e71d8b12c176ca6a269175c595d00649ac3(
    *,
    buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.AmazonopensearchserviceBufferingHintsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cluster_endpoint: typing.Optional[builtins.str] = None,
    document_id_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.DocumentIdOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    domain_arn: typing.Optional[builtins.str] = None,
    index_name: typing.Optional[builtins.str] = None,
    index_rotation_period: typing.Optional[builtins.str] = None,
    processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.AmazonopensearchserviceRetryOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    s3_backup_mode: typing.Optional[builtins.str] = None,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type_name: typing.Optional[builtins.str] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c82e62670e75160b68ab7cbfeec549797c4285d1c2b3e6168e471e9ecf6aa55(
    *,
    duration_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b40b33da2bf525e4e5893f6c761af0b5afff44296dc380fecb52b85e953f5d5e(
    *,
    connectivity: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f663354b24573aee29f12af489e12e95cd1d98e976e4aaa1514904b4e35021dc(
    *,
    interval_in_seconds: typing.Optional[jsii.Number] = None,
    size_in_m_bs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9f7cf40c12ecbff12591f0a1a4f894e641a1712591c0c1f1f56fde8e927f30(
    *,
    catalog_arn: typing.Optional[builtins.str] = None,
    warehouse_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc6dec41148b6f531f60b4316f60bb8a252973a724e78e2c6fbad50986e97a5(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34aa859756ee18037f6d46647870395666701787ba01cbcab05f3774115a2f8(
    *,
    copy_options: typing.Optional[builtins.str] = None,
    data_table_columns: typing.Optional[builtins.str] = None,
    data_table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290dff42a7e66004a43d6d32c49e894292f7f8b13e5fbbfe899a32fa57468b83(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    input_format_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.InputFormatConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    output_format_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.OutputFormatConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schema_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SchemaConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1f82f7b00716b63fcd9bfa364c01a840d424b0ea36511064ef8af4e0f315b8(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec93158e976b5f4ce0d343666f294325c3e2caf58954b8923b5114a7bc51fbd(
    *,
    secrets_manager_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afcad6b2c3e4247aa2069f48fbaf06fec0167181216b3bc1dfabe15f168b978d(
    *,
    columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.DatabaseColumnsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    databases: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.DatabasesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    database_source_authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.DatabaseSourceAuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    database_source_vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.DatabaseSourceVPCConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    digest: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    public_certificate: typing.Optional[builtins.str] = None,
    snapshot_watermark_table: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
    surrogate_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    tables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.DatabaseTablesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8906a2d07384fa31f04a3fff73f920e4e2c557107d2c5ea9616bb9ca5e397958(
    *,
    vpc_endpoint_service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76984fad2f6460a0e5d29bb52d5cab787135dc6d015eb9d9e544601f95543574(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b72b01d120be0197745a951a4bc951e324044f229c292520c6a21b26495eee2c(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efaeb1b8ee044e076d2a5b7b0736db82180b3bac71a8aaa9e98dd834ebce700d(
    *,
    key_arn: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604fb0ece70a83cbe743cb1074f2e1dbfe2e43be5a3f3bab98be63ff99fb35c7(
    *,
    hive_json_ser_de: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.HiveJsonSerDeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    open_x_json_ser_de: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.OpenXJsonSerDeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14427d07417bca7c3409605d1d312907aa3d97f9dd6921658bbc2fa9943bb9f(
    *,
    destination_database_name: typing.Optional[builtins.str] = None,
    destination_table_name: typing.Optional[builtins.str] = None,
    partition_spec: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.PartitionSpecProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_error_output_prefix: typing.Optional[builtins.str] = None,
    unique_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8359d3837050f0bfbac79499997adbd44e39b7302474919b1b41d654b09d651(
    *,
    throughput_hint_in_m_bs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26a659e91deb4e511aaa9d98e27f7c04af731bbd5b6b2cefcc19e79737b4b2c(
    *,
    default_document_id_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da020658709eee245354e7f069f003de29499203033f78755b5a8b912733f2f9(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.RetryOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd326602ce0a3bfa4a28c4673a090a746382a31023093312c23256f32aea3a9(
    *,
    interval_in_seconds: typing.Optional[jsii.Number] = None,
    size_in_m_bs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e758896e5c6d2cc811d75e789db6e71a90c4b43e8a37a2666e4de6f0cc56d28(
    *,
    buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ElasticsearchBufferingHintsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cluster_endpoint: typing.Optional[builtins.str] = None,
    document_id_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.DocumentIdOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    domain_arn: typing.Optional[builtins.str] = None,
    index_name: typing.Optional[builtins.str] = None,
    index_rotation_period: typing.Optional[builtins.str] = None,
    processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ElasticsearchRetryOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    s3_backup_mode: typing.Optional[builtins.str] = None,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type_name: typing.Optional[builtins.str] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb2ae54fc02aadbb409b34ba7a293998a2255ddc8ae87788aabaad6e6bdd4f1(
    *,
    duration_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3ed42571e6f72c9e4d45b76465b7ae84dd56832e0a18c86742253fe3a51fb6(
    *,
    kms_encryption_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.KMSEncryptionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    no_encryption_config: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783224085a9beea0c0bf1d18af7f323550d4f27129019a5acbffc4a824b045b8(
    *,
    bucket_arn: typing.Optional[builtins.str] = None,
    buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.BufferingHintsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    compression_format: typing.Optional[builtins.str] = None,
    custom_time_zone: typing.Optional[builtins.str] = None,
    data_format_conversion_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.DataFormatConversionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamic_partitioning_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.DynamicPartitioningConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    error_output_prefix: typing.Optional[builtins.str] = None,
    file_extension: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    s3_backup_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_backup_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f96536e5b07af8c6034535dc2d34e07cb2a64a75d72884557760c3bca1cf51(
    *,
    timestamp_formats: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4edb9d800e8ba6e4158e24c690839eb7e60e776714ef44debb554ac4413f82c(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
    attribute_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a27147991fe833129ea69f6d7a7cefc90065b062c44845b4a298e22c26e4c6c(
    *,
    access_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408127f0c8f8f8991159f30f915de3bd00746a74983ffb0a2aa1cc3f9e7370dc(
    *,
    buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.BufferingHintsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.HttpEndpointConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    request_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.HttpEndpointRequestConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.RetryOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    s3_backup_mode: typing.Optional[builtins.str] = None,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secrets_manager_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f55892b449de511d63fc261df45a89c9ca758f86f38e3116791efec394ea487(
    *,
    common_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.HttpEndpointCommonAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    content_encoding: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6843d5d2d59f1c09726ccf87bca481d0bb15582abb898da8a2a6ff989ed4ef17(
    *,
    append_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.BufferingHintsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    catalog_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.CatalogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    destination_table_configuration_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.DestinationTableConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.RetryOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    s3_backup_mode: typing.Optional[builtins.str] = None,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schema_evolution_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SchemaEvolutionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_creation_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.TableCreationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70afaf6b6d072efcf10368f31131bcecf388ed473d85d80645a62a7340e37b3f(
    *,
    deserializer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.DeserializerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d6d13c432f67e75ef88e8804fd27f83d256e806b85b7d5f3424c0a0586a61a(
    *,
    awskms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7791b30ef47b2a3c6150ade1147aa40197875cda2ac232cadb2503477611e26e(
    *,
    kinesis_stream_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2d080f038e6b443f45ab5d5fb8923056577f0360a1c8043c6fc08caf3536b8(
    *,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.AuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    msk_cluster_arn: typing.Optional[builtins.str] = None,
    read_from_timestamp: typing.Optional[builtins.str] = None,
    topic_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1571f01229bc791c71bd13538e53494328aa7f8f504fddaebb2b83f61e3e6111(
    *,
    case_insensitive: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    column_to_json_key_mappings: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    convert_dots_in_json_keys_to_underscores: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502f7aa73c2cedc4007f76d54ade6c7f0d703bdaa58aad2bbf83a3cd76fc45af(
    *,
    block_size_bytes: typing.Optional[jsii.Number] = None,
    bloom_filter_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    bloom_filter_false_positive_probability: typing.Optional[jsii.Number] = None,
    compression: typing.Optional[builtins.str] = None,
    dictionary_key_threshold: typing.Optional[jsii.Number] = None,
    enable_padding: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    format_version: typing.Optional[builtins.str] = None,
    padding_tolerance: typing.Optional[jsii.Number] = None,
    row_index_stride: typing.Optional[jsii.Number] = None,
    stripe_size_bytes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6dc581c2f5484d33876a12e5059524a2de478e71837b1c1d9041fc2503e7536(
    *,
    serializer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SerializerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b55f795b35108fdda51e34317308df87c8866ba7da9ad5cf5619a19faf7806c(
    *,
    block_size_bytes: typing.Optional[jsii.Number] = None,
    compression: typing.Optional[builtins.str] = None,
    enable_dictionary_compression: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_padding_bytes: typing.Optional[jsii.Number] = None,
    page_size_bytes: typing.Optional[jsii.Number] = None,
    writer_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51e079891a4e8ef39ef34b3c104dc6158a4cdf82c92f7c0a7dbac819ec7c912(
    *,
    source_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db1ab17977ce5681e6b5ad4d15fb5907608bdb88dfec4c6c2667acd935be66b(
    *,
    identity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.PartitionFieldProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed805f8586c149a2b83669105c2270a06f792dc898669dd64305c850bb9d510e(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    processors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ProcessorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61df5affdbcf20e7459900a373fddd5801d1b022e822fbcd4a82809947ce8d77(
    *,
    parameter_name: typing.Optional[builtins.str] = None,
    parameter_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cba94dc162fde6e6229240e7812c4f6ddfcdc0497eeaef2161cb4c2b77c4143(
    *,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ProcessorParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d88e0c93175d5a07a21337809afabb886001f2f68cffcb1ca4389b32270faed(
    *,
    cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cluster_jdbcurl: typing.Optional[builtins.str] = None,
    copy_command: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.CopyCommandProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    password: typing.Optional[builtins.str] = None,
    processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.RedshiftRetryOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    s3_backup_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_backup_mode: typing.Optional[builtins.str] = None,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secrets_manager_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c18c56ad75f163e7f453ee4ce101255e6e6bd40b8f9ddd79a15e2f891259b9(
    *,
    duration_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971da5b058145004752bfd9c216c83d9295da3978e7099ccb0064062f310db8c(
    *,
    duration_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162a83982546ab228dd6e2a8ff7b72be33a25b871e99f2a463ec221b13926058(
    *,
    bucket_arn: typing.Optional[builtins.str] = None,
    buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.BufferingHintsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    compression_format: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    error_output_prefix: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc21cd148fb795183ec127a12ebdd26c11509a61fd42511664ab9d6353ac12a(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722be063ef79b47f7c7a44156c43e4e137e8afb5bd0992a071d183f892955443(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03ddff3c4d17886193b4fe55d5f0da3129c4d737a8446e85959b3981c099284(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237799e0d77b8b7822aedebe7aecdecc2def5f249bdcff8f8680cf61838ebafd(
    *,
    orc_ser_de: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.OrcSerDeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parquet_ser_de: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ParquetSerDeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e935d391029a093ae8d3b58f0373cc919f6472c6d12f5fd7f80ec0382a07446d(
    *,
    interval_in_seconds: typing.Optional[jsii.Number] = None,
    size_in_m_bs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8df9b78113b3e3b2c45aac3a7b30427f872d6b9bea8040c378605c7fa150612(
    *,
    account_url: typing.Optional[builtins.str] = None,
    buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SnowflakeBufferingHintsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    content_column_name: typing.Optional[builtins.str] = None,
    database: typing.Optional[builtins.str] = None,
    data_loading_option: typing.Optional[builtins.str] = None,
    key_passphrase: typing.Optional[builtins.str] = None,
    meta_data_column_name: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
    processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SnowflakeRetryOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    s3_backup_mode: typing.Optional[builtins.str] = None,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schema: typing.Optional[builtins.str] = None,
    secrets_manager_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    snowflake_role_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SnowflakeRoleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    snowflake_vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SnowflakeVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table: typing.Optional[builtins.str] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__debdb3dfd51aaf9fccd5332249045df93dd352e5a46879e26aa9f9084f95d312(
    *,
    duration_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de984f912a786bbaf1c80de41cbccfa94dfee75a90f1e71b7776cbfbd1d9c15c(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    snowflake_role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2b9bb5796c0026804c3aee05faa6cea9da8038b8e796438f9738facfdd29a9(
    *,
    private_link_vpce_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b780637cbd31c5a7253c27eb28007ca3f451ac85e127ef5cb492756e30944e(
    *,
    interval_in_seconds: typing.Optional[jsii.Number] = None,
    size_in_m_bs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c3e65767c9bb42c2a4788c10c8f05059dc7bcf6558c46180f99f9f15805e4a(
    *,
    buffering_hints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SplunkBufferingHintsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloud_watch_logging_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.CloudWatchLoggingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hec_acknowledgment_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    hec_endpoint: typing.Optional[builtins.str] = None,
    hec_endpoint_type: typing.Optional[builtins.str] = None,
    hec_token: typing.Optional[builtins.str] = None,
    processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.ProcessingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retry_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SplunkRetryOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_backup_mode: typing.Optional[builtins.str] = None,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secrets_manager_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryStreamPropsMixin.SecretsManagerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74de9a01d32e57fd7f60024171b9e240e488ad60446a8b229a3072e0caf7d2f7(
    *,
    duration_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cb2e8fd221edff1555f4e757b7ef36b1e089b120ed6d55ea00b671a65f6411(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117d5274c373639b716983c65795e0096e67d4744e770029b04889b7094c4951(
    *,
    role_arn: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
