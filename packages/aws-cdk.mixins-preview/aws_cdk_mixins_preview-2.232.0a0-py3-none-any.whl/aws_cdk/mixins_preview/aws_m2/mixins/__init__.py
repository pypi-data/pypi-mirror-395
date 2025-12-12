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


class CfnApplicationBatchJobLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnApplicationBatchJobLogs",
):
    '''Builder for CfnApplicationLogsMixin to generate BATCH_JOB_LOGS for CfnApplication.

    :cloudformationResource: AWS::M2::Application
    :logType: BATCH_JOB_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
        
        cfn_application_batch_job_logs = m2_mixins.CfnApplicationBatchJobLogs()
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
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db59956dd75ba2bd9d356d159c349d06319bef39e479cc0e93197d527be3d12)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df1e8372cbf8d3fd2680f54965cacd513ab94e6f6b50445e52449b64a89c40cf)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc4403ba288c0ccc0f384bf7d5678213653422fcc260ede802b7f6d7a6b9409)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toS3", [bucket]))


class CfnApplicationConfigLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnApplicationConfigLogs",
):
    '''Builder for CfnApplicationLogsMixin to generate CONFIG_LOGS for CfnApplication.

    :cloudformationResource: AWS::M2::Application
    :logType: CONFIG_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
        
        cfn_application_config_logs = m2_mixins.CfnApplicationConfigLogs()
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
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8246e9b550b20af071441bcb23503106e45aea8a7c0516c217f927622d4d98c)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d89824f773ab851f951c6ab6845d88a9767213ac2ad2203fa2c5d8e47dbc09c)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2ae302b82eb537b52660aa84bef6ce35dd74fa985a706183f836bfe88fa17b)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toS3", [bucket]))


class CfnApplicationConsoleLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnApplicationConsoleLogs",
):
    '''Builder for CfnApplicationLogsMixin to generate CONSOLE_LOGS for CfnApplication.

    :cloudformationResource: AWS::M2::Application
    :logType: CONSOLE_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
        
        cfn_application_console_logs = m2_mixins.CfnApplicationConsoleLogs()
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
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a84af912955c611caeaa986f808e9701f15f53e31ed251f7dd3296ac7327b56)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6678d24d036d0e9ece2996d6681a3cec6dc817caa00a6ba3c62de1214b05229)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b23233228b15f0a1799a3c1e184b33f60b27382207877f9b9902652b7d889e)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toS3", [bucket]))


class CfnApplicationDatasetImportLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnApplicationDatasetImportLogs",
):
    '''Builder for CfnApplicationLogsMixin to generate DATASET_IMPORT_LOGS for CfnApplication.

    :cloudformationResource: AWS::M2::Application
    :logType: DATASET_IMPORT_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
        
        cfn_application_dataset_import_logs = m2_mixins.CfnApplicationDatasetImportLogs()
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
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6029493e8e170d5c2563cffd163b924be4dfdfe2343873c0164d671a478d9c1f)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6376dc2524b92764c470cedb241776f3afeab6e273703ceebfd0a752bae11216)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnApplicationLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f661466bcb82e67523a4cdac1b98c922d8c7e32e08fd712fcf44bab6f6ad2f92)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnApplicationLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnApplicationLogsMixin",
):
    '''Specifies a new application with given parameters. Requires an existing runtime environment and application definition file.

    For information about application definitions, see the `AWS Mainframe Modernization User Guide <https://docs.aws.amazon.com/m2/latest/userguide/applications-m2-definition.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html
    :cloudformationResource: AWS::M2::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_application_logs_mixin = m2_mixins.CfnApplicationLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::M2::Application``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__044dca81dc8be01a9d835ce8e8ae34312ebfed3ebc79f939001a8c6dab618c5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ead7cb9280e58dd32915d43bbafaf2564e8f3b08976c3018a9ca2ee66ae13048)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7e6f4483f2bc046f2186b5fc553b6fd52c5b9b7fdef90a70fde7ec5d9a4cf3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="BATCH_JOB_LOGS")
    def BATCH_JOB_LOGS(cls) -> CfnApplicationBatchJobLogs:
        return typing.cast(CfnApplicationBatchJobLogs, jsii.sget(cls, "BATCH_JOB_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CONFIG_LOGS")
    def CONFIG_LOGS(cls) -> CfnApplicationConfigLogs:
        return typing.cast(CfnApplicationConfigLogs, jsii.sget(cls, "CONFIG_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CONSOLE_LOGS")
    def CONSOLE_LOGS(cls) -> CfnApplicationConsoleLogs:
        return typing.cast(CfnApplicationConsoleLogs, jsii.sget(cls, "CONSOLE_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DATASET_IMPORT_LOGS")
    def DATASET_IMPORT_LOGS(cls) -> CfnApplicationDatasetImportLogs:
        return typing.cast(CfnApplicationDatasetImportLogs, jsii.sget(cls, "DATASET_IMPORT_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "definition": "definition",
        "description": "description",
        "engine_type": "engineType",
        "kms_key_id": "kmsKeyId",
        "name": "name",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.DefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        engine_type: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param definition: The application definition for a particular application. You can specify either inline JSON or an Amazon S3 bucket location. For information about application definitions, see the `AWS Mainframe Modernization User Guide <https://docs.aws.amazon.com/m2/latest/userguide/applications-m2-definition.html>`_ .
        :param description: The description of the application.
        :param engine_type: The type of the target platform for this application.
        :param kms_key_id: The identifier of a customer managed key.
        :param name: The name of the application.
        :param role_arn: The Amazon Resource Name (ARN) of the role associated with the application.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
            
            cfn_application_mixin_props = m2_mixins.CfnApplicationMixinProps(
                definition=m2_mixins.CfnApplicationPropsMixin.DefinitionProperty(
                    content="content",
                    s3_location="s3Location"
                ),
                description="description",
                engine_type="engineType",
                kms_key_id="kmsKeyId",
                name="name",
                role_arn="roleArn",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02e89e99c428fb0a18071751757f975668bc83e2641faff630894ec662f84dd)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument engine_type", value=engine_type, expected_type=type_hints["engine_type"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if definition is not None:
            self._values["definition"] = definition
        if description is not None:
            self._values["description"] = description
        if engine_type is not None:
            self._values["engine_type"] = engine_type
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def definition(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.DefinitionProperty"]]:
        '''The application definition for a particular application. You can specify either inline JSON or an Amazon S3 bucket location.

        For information about application definitions, see the `AWS Mainframe Modernization User Guide <https://docs.aws.amazon.com/m2/latest/userguide/applications-m2-definition.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-definition
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.DefinitionProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_type(self) -> typing.Optional[builtins.str]:
        '''The type of the target platform for this application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-enginetype
        '''
        result = self._values.get("engine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of a customer managed key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the role associated with the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnApplicationPropsMixin",
):
    '''Specifies a new application with given parameters. Requires an existing runtime environment and application definition file.

    For information about application definitions, see the `AWS Mainframe Modernization User Guide <https://docs.aws.amazon.com/m2/latest/userguide/applications-m2-definition.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html
    :cloudformationResource: AWS::M2::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
        
        cfn_application_props_mixin = m2_mixins.CfnApplicationPropsMixin(m2_mixins.CfnApplicationMixinProps(
            definition=m2_mixins.CfnApplicationPropsMixin.DefinitionProperty(
                content="content",
                s3_location="s3Location"
            ),
            description="description",
            engine_type="engineType",
            kms_key_id="kmsKeyId",
            name="name",
            role_arn="roleArn",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::M2::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0432721b0f6f27257361778403ae6d808ccb78c953829a6ab1a372f04b05e57b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b69521a1b32eeb71f03817093cd1bde5e8636d1729b68a591ccb537372e6ec8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696b2b2dc5826b15f3ed274a7133b99dfe46055b5920800ce18b0736b71ad5f3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationMixinProps:
        return typing.cast(CfnApplicationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnApplicationPropsMixin.DefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"content": "content", "s3_location": "s3Location"},
    )
    class DefinitionProperty:
        def __init__(
            self,
            *,
            content: typing.Optional[builtins.str] = None,
            s3_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The application definition for a particular application.

            You can specify either inline JSON or an Amazon S3 bucket location.

            :param content: The content of the application definition. This is a JSON object that contains the resource configuration/definitions that identify an application.
            :param s3_location: The S3 bucket that contains the application definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-application-definition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
                
                definition_property = m2_mixins.CfnApplicationPropsMixin.DefinitionProperty(
                    content="content",
                    s3_location="s3Location"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d26c60a3035dd2c346d6ec6b7003fde5da9eb277b52c2b9337e28c98e7802bb)
                check_type(argname="argument content", value=content, expected_type=type_hints["content"])
                check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content is not None:
                self._values["content"] = content
            if s3_location is not None:
                self._values["s3_location"] = s3_location

        @builtins.property
        def content(self) -> typing.Optional[builtins.str]:
            '''The content of the application definition.

            This is a JSON object that contains the resource configuration/definitions that identify an application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-application-definition.html#cfn-m2-application-definition-content
            '''
            result = self._values.get("content")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_location(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket that contains the application definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-application-definition.html#cfn-m2-application-definition-s3location
            '''
            result = self._values.get("s3_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnDeploymentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "application_version": "applicationVersion",
        "environment_id": "environmentId",
    },
)
class CfnDeploymentMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        application_version: typing.Optional[jsii.Number] = None,
        environment_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDeploymentPropsMixin.

        :param application_id: The unique identifier of the application.
        :param application_version: The version of the application.
        :param environment_id: The unique identifier of the runtime environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-deployment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
            
            cfn_deployment_mixin_props = m2_mixins.CfnDeploymentMixinProps(
                application_id="applicationId",
                application_version=123,
                environment_id="environmentId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0897535eaedd80c6981ef44cbb4166fb66717ea36b7d9a0d119fb3a24c70ce)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument application_version", value=application_version, expected_type=type_hints["application_version"])
            check_type(argname="argument environment_id", value=environment_id, expected_type=type_hints["environment_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if application_version is not None:
            self._values["application_version"] = application_version
        if environment_id is not None:
            self._values["environment_id"] = environment_id

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-deployment.html#cfn-m2-deployment-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_version(self) -> typing.Optional[jsii.Number]:
        '''The version of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-deployment.html#cfn-m2-deployment-applicationversion
        '''
        result = self._values.get("application_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the runtime environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-deployment.html#cfn-m2-deployment-environmentid
        '''
        result = self._values.get("environment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDeploymentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnDeploymentPropsMixin",
):
    '''.. epigraph::

   AWS Mainframe Modernization Service (Managed Runtime Environment experience) will no longer be open to new customers starting on November 7, 2025.

    If you would like to use the service, please sign up prior to November 7, 2025. For capabilities similar to AWS Mainframe Modernization Service (Managed Runtime Environment experience) explore AWS Mainframe Modernization Service (Self-Managed Experience). Existing customers can continue to use the service as normal. For more information, see `AWS Mainframe Modernization availability change <https://docs.aws.amazon.com/m2/latest/userguide/mainframe-modernization-availability-change.html>`_ .

    Creates and starts a deployment to deploy an application into a runtime environment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-deployment.html
    :cloudformationResource: AWS::M2::Deployment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
        
        cfn_deployment_props_mixin = m2_mixins.CfnDeploymentPropsMixin(m2_mixins.CfnDeploymentMixinProps(
            application_id="applicationId",
            application_version=123,
            environment_id="environmentId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDeploymentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::M2::Deployment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7086001e77e342ccc02b1c6f7d10cb745ec033caeac348c909c36c0d7dfdad53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6fd5a48a9fc14e32960abe928bf54384a6ba5f7f3b2e1ece9afd63f722c9f18)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba651d781c6d24650dad8fc804119806485b679cf113b561d8740ec5f2927b80)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDeploymentMixinProps:
        return typing.cast(CfnDeploymentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnEnvironmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "engine_type": "engineType",
        "engine_version": "engineVersion",
        "high_availability_config": "highAvailabilityConfig",
        "instance_type": "instanceType",
        "kms_key_id": "kmsKeyId",
        "name": "name",
        "network_type": "networkType",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "publicly_accessible": "publiclyAccessible",
        "security_group_ids": "securityGroupIds",
        "storage_configurations": "storageConfigurations",
        "subnet_ids": "subnetIds",
        "tags": "tags",
    },
)
class CfnEnvironmentMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        engine_type: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        high_availability_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.HighAvailabilityConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.StorageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnEnvironmentPropsMixin.

        :param description: The description of the runtime environment.
        :param engine_type: The target platform for the runtime environment.
        :param engine_version: The version of the runtime engine.
        :param high_availability_config: .. epigraph:: AWS Mainframe Modernization Service (Managed Runtime Environment experience) will no longer be open to new customers starting on November 7, 2025. If you would like to use the service, please sign up prior to November 7, 2025. For capabilities similar to AWS Mainframe Modernization Service (Managed Runtime Environment experience) explore AWS Mainframe Modernization Service (Self-Managed Experience). Existing customers can continue to use the service as normal. For more information, see `AWS Mainframe Modernization availability change <https://docs.aws.amazon.com/m2/latest/userguide/mainframe-modernization-availability-change.html>`_ . Defines the details of a high availability configuration.
        :param instance_type: The instance type of the runtime environment.
        :param kms_key_id: The identifier of a customer managed key.
        :param name: The name of the runtime environment.
        :param network_type: The network type supported by the runtime environment.
        :param preferred_maintenance_window: Configures the maintenance window that you want for the runtime environment. The maintenance window must have the format ``ddd:hh24:mi-ddd:hh24:mi`` and must be less than 24 hours. The following two examples are valid maintenance windows: ``sun:23:45-mon:00:15`` or ``sat:01:00-sat:03:00`` . If you do not provide a value, a random system-generated value will be assigned.
        :param publicly_accessible: Specifies whether the runtime environment is publicly accessible.
        :param security_group_ids: The list of security groups for the VPC associated with this runtime environment.
        :param storage_configurations: .. epigraph:: AWS Mainframe Modernization Service (Managed Runtime Environment experience) will no longer be open to new customers starting on November 7, 2025. If you would like to use the service, please sign up prior to November 7, 2025. For capabilities similar to AWS Mainframe Modernization Service (Managed Runtime Environment experience) explore AWS Mainframe Modernization Service (Self-Managed Experience). Existing customers can continue to use the service as normal. For more information, see `AWS Mainframe Modernization availability change <https://docs.aws.amazon.com/m2/latest/userguide/mainframe-modernization-availability-change.html>`_ . Defines the storage configuration for a runtime environment.
        :param subnet_ids: The list of subnets associated with the VPC for this runtime environment.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
            
            cfn_environment_mixin_props = m2_mixins.CfnEnvironmentMixinProps(
                description="description",
                engine_type="engineType",
                engine_version="engineVersion",
                high_availability_config=m2_mixins.CfnEnvironmentPropsMixin.HighAvailabilityConfigProperty(
                    desired_capacity=123
                ),
                instance_type="instanceType",
                kms_key_id="kmsKeyId",
                name="name",
                network_type="networkType",
                preferred_maintenance_window="preferredMaintenanceWindow",
                publicly_accessible=False,
                security_group_ids=["securityGroupIds"],
                storage_configurations=[m2_mixins.CfnEnvironmentPropsMixin.StorageConfigurationProperty(
                    efs=m2_mixins.CfnEnvironmentPropsMixin.EfsStorageConfigurationProperty(
                        file_system_id="fileSystemId",
                        mount_point="mountPoint"
                    ),
                    fsx=m2_mixins.CfnEnvironmentPropsMixin.FsxStorageConfigurationProperty(
                        file_system_id="fileSystemId",
                        mount_point="mountPoint"
                    )
                )],
                subnet_ids=["subnetIds"],
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5460b3564b00f1ba29876e1ac061f68b86f1a0f2abfe7f192eb13945146bec)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument engine_type", value=engine_type, expected_type=type_hints["engine_type"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument high_availability_config", value=high_availability_config, expected_type=type_hints["high_availability_config"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument storage_configurations", value=storage_configurations, expected_type=type_hints["storage_configurations"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if engine_type is not None:
            self._values["engine_type"] = engine_type
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if high_availability_config is not None:
            self._values["high_availability_config"] = high_availability_config
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if name is not None:
            self._values["name"] = name
        if network_type is not None:
            self._values["network_type"] = network_type
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if storage_configurations is not None:
            self._values["storage_configurations"] = storage_configurations
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the runtime environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_type(self) -> typing.Optional[builtins.str]:
        '''The target platform for the runtime environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-enginetype
        '''
        result = self._values.get("engine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version of the runtime engine.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def high_availability_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.HighAvailabilityConfigProperty"]]:
        '''.. epigraph::

   AWS Mainframe Modernization Service (Managed Runtime Environment experience) will no longer be open to new customers starting on November 7, 2025.

        If you would like to use the service, please sign up prior to November 7, 2025. For capabilities similar to AWS Mainframe Modernization Service (Managed Runtime Environment experience) explore AWS Mainframe Modernization Service (Self-Managed Experience). Existing customers can continue to use the service as normal. For more information, see `AWS Mainframe Modernization availability change <https://docs.aws.amazon.com/m2/latest/userguide/mainframe-modernization-availability-change.html>`_ .

        Defines the details of a high availability configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-highavailabilityconfig
        '''
        result = self._values.get("high_availability_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.HighAvailabilityConfigProperty"]], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The instance type of the runtime environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-instancetype
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of a customer managed key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the runtime environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''The network type supported by the runtime environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-networktype
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''Configures the maintenance window that you want for the runtime environment.

        The maintenance window must have the format ``ddd:hh24:mi-ddd:hh24:mi`` and must be less than 24 hours. The following two examples are valid maintenance windows: ``sun:23:45-mon:00:15`` or ``sat:01:00-sat:03:00`` .

        If you do not provide a value, a random system-generated value will be assigned.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the runtime environment is publicly accessible.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-publiclyaccessible
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of security groups for the VPC associated with this runtime environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def storage_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.StorageConfigurationProperty"]]]]:
        '''.. epigraph::

   AWS Mainframe Modernization Service (Managed Runtime Environment experience) will no longer be open to new customers starting on November 7, 2025.

        If you would like to use the service, please sign up prior to November 7, 2025. For capabilities similar to AWS Mainframe Modernization Service (Managed Runtime Environment experience) explore AWS Mainframe Modernization Service (Self-Managed Experience). Existing customers can continue to use the service as normal. For more information, see `AWS Mainframe Modernization availability change <https://docs.aws.amazon.com/m2/latest/userguide/mainframe-modernization-availability-change.html>`_ .

        Defines the storage configuration for a runtime environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-storageconfigurations
        '''
        result = self._values.get("storage_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.StorageConfigurationProperty"]]]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of subnets associated with the VPC for this runtime environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEnvironmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnEnvironmentPropsMixin",
):
    '''Specifies a runtime environment for a given runtime engine.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html
    :cloudformationResource: AWS::M2::Environment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
        
        cfn_environment_props_mixin = m2_mixins.CfnEnvironmentPropsMixin(m2_mixins.CfnEnvironmentMixinProps(
            description="description",
            engine_type="engineType",
            engine_version="engineVersion",
            high_availability_config=m2_mixins.CfnEnvironmentPropsMixin.HighAvailabilityConfigProperty(
                desired_capacity=123
            ),
            instance_type="instanceType",
            kms_key_id="kmsKeyId",
            name="name",
            network_type="networkType",
            preferred_maintenance_window="preferredMaintenanceWindow",
            publicly_accessible=False,
            security_group_ids=["securityGroupIds"],
            storage_configurations=[m2_mixins.CfnEnvironmentPropsMixin.StorageConfigurationProperty(
                efs=m2_mixins.CfnEnvironmentPropsMixin.EfsStorageConfigurationProperty(
                    file_system_id="fileSystemId",
                    mount_point="mountPoint"
                ),
                fsx=m2_mixins.CfnEnvironmentPropsMixin.FsxStorageConfigurationProperty(
                    file_system_id="fileSystemId",
                    mount_point="mountPoint"
                )
            )],
            subnet_ids=["subnetIds"],
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::M2::Environment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c6d12245793f4f672b44c8dc8abea52071fcab30c798fb152f7e94f72fdfcd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74311782333dd7b2f226004be60ceb58d68e311214298e8a09033bd7342f56de)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8377a029154b4a330b830f32502b350ad6f0da6dd07e27e5ff80f204d2772307)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEnvironmentMixinProps:
        return typing.cast(CfnEnvironmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnEnvironmentPropsMixin.EfsStorageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"file_system_id": "fileSystemId", "mount_point": "mountPoint"},
    )
    class EfsStorageConfigurationProperty:
        def __init__(
            self,
            *,
            file_system_id: typing.Optional[builtins.str] = None,
            mount_point: typing.Optional[builtins.str] = None,
        ) -> None:
            '''.. epigraph::

   AWS Mainframe Modernization Service (Managed Runtime Environment experience) will no longer be open to new customers starting on November 7, 2025.

            If you would like to use the service, please sign up prior to November 7, 2025. For capabilities similar to AWS Mainframe Modernization Service (Managed Runtime Environment experience) explore AWS Mainframe Modernization Service (Self-Managed Experience). Existing customers can continue to use the service as normal. For more information, see `AWS Mainframe Modernization availability change <https://docs.aws.amazon.com/m2/latest/userguide/mainframe-modernization-availability-change.html>`_ .

            Defines the storage configuration for an Amazon EFS file system.

            :param file_system_id: The file system identifier.
            :param mount_point: The mount point for the file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-efsstorageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
                
                efs_storage_configuration_property = m2_mixins.CfnEnvironmentPropsMixin.EfsStorageConfigurationProperty(
                    file_system_id="fileSystemId",
                    mount_point="mountPoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__341378249da435981ec586acad5909d5cf623651d34e60cd60fa2e83fbe50295)
                check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
                check_type(argname="argument mount_point", value=mount_point, expected_type=type_hints["mount_point"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file_system_id is not None:
                self._values["file_system_id"] = file_system_id
            if mount_point is not None:
                self._values["mount_point"] = mount_point

        @builtins.property
        def file_system_id(self) -> typing.Optional[builtins.str]:
            '''The file system identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-efsstorageconfiguration.html#cfn-m2-environment-efsstorageconfiguration-filesystemid
            '''
            result = self._values.get("file_system_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mount_point(self) -> typing.Optional[builtins.str]:
            '''The mount point for the file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-efsstorageconfiguration.html#cfn-m2-environment-efsstorageconfiguration-mountpoint
            '''
            result = self._values.get("mount_point")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EfsStorageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnEnvironmentPropsMixin.FsxStorageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"file_system_id": "fileSystemId", "mount_point": "mountPoint"},
    )
    class FsxStorageConfigurationProperty:
        def __init__(
            self,
            *,
            file_system_id: typing.Optional[builtins.str] = None,
            mount_point: typing.Optional[builtins.str] = None,
        ) -> None:
            '''.. epigraph::

   AWS Mainframe Modernization Service (Managed Runtime Environment experience) will no longer be open to new customers starting on November 7, 2025.

            If you would like to use the service, please sign up prior to November 7, 2025. For capabilities similar to AWS Mainframe Modernization Service (Managed Runtime Environment experience) explore AWS Mainframe Modernization Service (Self-Managed Experience). Existing customers can continue to use the service as normal. For more information, see `AWS Mainframe Modernization availability change <https://docs.aws.amazon.com/m2/latest/userguide/mainframe-modernization-availability-change.html>`_ .

            Defines the storage configuration for an Amazon FSx file system.

            :param file_system_id: The file system identifier.
            :param mount_point: The mount point for the file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-fsxstorageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
                
                fsx_storage_configuration_property = m2_mixins.CfnEnvironmentPropsMixin.FsxStorageConfigurationProperty(
                    file_system_id="fileSystemId",
                    mount_point="mountPoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__caf6c525eac1d2870f2787f86a157caad861693211fcb9771c490607f79fc4a4)
                check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
                check_type(argname="argument mount_point", value=mount_point, expected_type=type_hints["mount_point"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file_system_id is not None:
                self._values["file_system_id"] = file_system_id
            if mount_point is not None:
                self._values["mount_point"] = mount_point

        @builtins.property
        def file_system_id(self) -> typing.Optional[builtins.str]:
            '''The file system identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-fsxstorageconfiguration.html#cfn-m2-environment-fsxstorageconfiguration-filesystemid
            '''
            result = self._values.get("file_system_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mount_point(self) -> typing.Optional[builtins.str]:
            '''The mount point for the file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-fsxstorageconfiguration.html#cfn-m2-environment-fsxstorageconfiguration-mountpoint
            '''
            result = self._values.get("mount_point")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FsxStorageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnEnvironmentPropsMixin.HighAvailabilityConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"desired_capacity": "desiredCapacity"},
    )
    class HighAvailabilityConfigProperty:
        def __init__(
            self,
            *,
            desired_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''.. epigraph::

   AWS Mainframe Modernization Service (Managed Runtime Environment experience) will no longer be open to new customers starting on November 7, 2025.

            If you would like to use the service, please sign up prior to November 7, 2025. For capabilities similar to AWS Mainframe Modernization Service (Managed Runtime Environment experience) explore AWS Mainframe Modernization Service (Self-Managed Experience). Existing customers can continue to use the service as normal. For more information, see `AWS Mainframe Modernization availability change <https://docs.aws.amazon.com/m2/latest/userguide/mainframe-modernization-availability-change.html>`_ .

            Defines the details of a high availability configuration.

            :param desired_capacity: The number of instances in a high availability configuration. The minimum possible value is 1 and the maximum is 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-highavailabilityconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
                
                high_availability_config_property = m2_mixins.CfnEnvironmentPropsMixin.HighAvailabilityConfigProperty(
                    desired_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__827412625bc2121c7111b896d2a221d0885153f2d90d2bec96c42480a0692578)
                check_type(argname="argument desired_capacity", value=desired_capacity, expected_type=type_hints["desired_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if desired_capacity is not None:
                self._values["desired_capacity"] = desired_capacity

        @builtins.property
        def desired_capacity(self) -> typing.Optional[jsii.Number]:
            '''The number of instances in a high availability configuration.

            The minimum possible value is 1 and the maximum is 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-highavailabilityconfig.html#cfn-m2-environment-highavailabilityconfig-desiredcapacity
            '''
            result = self._values.get("desired_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HighAvailabilityConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_m2.mixins.CfnEnvironmentPropsMixin.StorageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"efs": "efs", "fsx": "fsx"},
    )
    class StorageConfigurationProperty:
        def __init__(
            self,
            *,
            efs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.EfsStorageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            fsx: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.FsxStorageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''.. epigraph::

   AWS Mainframe Modernization Service (Managed Runtime Environment experience) will no longer be open to new customers starting on November 7, 2025.

            If you would like to use the service, please sign up prior to November 7, 2025. For capabilities similar to AWS Mainframe Modernization Service (Managed Runtime Environment experience) explore AWS Mainframe Modernization Service (Self-Managed Experience). Existing customers can continue to use the service as normal. For more information, see `AWS Mainframe Modernization availability change <https://docs.aws.amazon.com/m2/latest/userguide/mainframe-modernization-availability-change.html>`_ .

            Defines the storage configuration for a runtime environment.

            :param efs: Defines the storage configuration for an Amazon EFS file system.
            :param fsx: Defines the storage configuration for an Amazon FSx file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-storageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_m2 import mixins as m2_mixins
                
                storage_configuration_property = m2_mixins.CfnEnvironmentPropsMixin.StorageConfigurationProperty(
                    efs=m2_mixins.CfnEnvironmentPropsMixin.EfsStorageConfigurationProperty(
                        file_system_id="fileSystemId",
                        mount_point="mountPoint"
                    ),
                    fsx=m2_mixins.CfnEnvironmentPropsMixin.FsxStorageConfigurationProperty(
                        file_system_id="fileSystemId",
                        mount_point="mountPoint"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b2d8847e7a1584542c63e9068e0d2d58bc2de378fe4e1153091fbad2c49b2542)
                check_type(argname="argument efs", value=efs, expected_type=type_hints["efs"])
                check_type(argname="argument fsx", value=fsx, expected_type=type_hints["fsx"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if efs is not None:
                self._values["efs"] = efs
            if fsx is not None:
                self._values["fsx"] = fsx

        @builtins.property
        def efs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.EfsStorageConfigurationProperty"]]:
            '''Defines the storage configuration for an Amazon EFS file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-storageconfiguration.html#cfn-m2-environment-storageconfiguration-efs
            '''
            result = self._values.get("efs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.EfsStorageConfigurationProperty"]], result)

        @builtins.property
        def fsx(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.FsxStorageConfigurationProperty"]]:
            '''Defines the storage configuration for an Amazon FSx file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-storageconfiguration.html#cfn-m2-environment-storageconfiguration-fsx
            '''
            result = self._values.get("fsx")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.FsxStorageConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApplicationBatchJobLogs",
    "CfnApplicationConfigLogs",
    "CfnApplicationConsoleLogs",
    "CfnApplicationDatasetImportLogs",
    "CfnApplicationLogsMixin",
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
    "CfnDeploymentMixinProps",
    "CfnDeploymentPropsMixin",
    "CfnEnvironmentMixinProps",
    "CfnEnvironmentPropsMixin",
]

publication.publish()

def _typecheckingstub__5db59956dd75ba2bd9d356d159c349d06319bef39e479cc0e93197d527be3d12(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1e8372cbf8d3fd2680f54965cacd513ab94e6f6b50445e52449b64a89c40cf(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc4403ba288c0ccc0f384bf7d5678213653422fcc260ede802b7f6d7a6b9409(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8246e9b550b20af071441bcb23503106e45aea8a7c0516c217f927622d4d98c(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d89824f773ab851f951c6ab6845d88a9767213ac2ad2203fa2c5d8e47dbc09c(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2ae302b82eb537b52660aa84bef6ce35dd74fa985a706183f836bfe88fa17b(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a84af912955c611caeaa986f808e9701f15f53e31ed251f7dd3296ac7327b56(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6678d24d036d0e9ece2996d6681a3cec6dc817caa00a6ba3c62de1214b05229(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b23233228b15f0a1799a3c1e184b33f60b27382207877f9b9902652b7d889e(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6029493e8e170d5c2563cffd163b924be4dfdfe2343873c0164d671a478d9c1f(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6376dc2524b92764c470cedb241776f3afeab6e273703ceebfd0a752bae11216(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f661466bcb82e67523a4cdac1b98c922d8c7e32e08fd712fcf44bab6f6ad2f92(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044dca81dc8be01a9d835ce8e8ae34312ebfed3ebc79f939001a8c6dab618c5f(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead7cb9280e58dd32915d43bbafaf2564e8f3b08976c3018a9ca2ee66ae13048(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7e6f4483f2bc046f2186b5fc553b6fd52c5b9b7fdef90a70fde7ec5d9a4cf3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02e89e99c428fb0a18071751757f975668bc83e2641faff630894ec662f84dd(
    *,
    definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.DefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    engine_type: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0432721b0f6f27257361778403ae6d808ccb78c953829a6ab1a372f04b05e57b(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b69521a1b32eeb71f03817093cd1bde5e8636d1729b68a591ccb537372e6ec8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696b2b2dc5826b15f3ed274a7133b99dfe46055b5920800ce18b0736b71ad5f3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d26c60a3035dd2c346d6ec6b7003fde5da9eb277b52c2b9337e28c98e7802bb(
    *,
    content: typing.Optional[builtins.str] = None,
    s3_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0897535eaedd80c6981ef44cbb4166fb66717ea36b7d9a0d119fb3a24c70ce(
    *,
    application_id: typing.Optional[builtins.str] = None,
    application_version: typing.Optional[jsii.Number] = None,
    environment_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7086001e77e342ccc02b1c6f7d10cb745ec033caeac348c909c36c0d7dfdad53(
    props: typing.Union[CfnDeploymentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6fd5a48a9fc14e32960abe928bf54384a6ba5f7f3b2e1ece9afd63f722c9f18(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba651d781c6d24650dad8fc804119806485b679cf113b561d8740ec5f2927b80(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5460b3564b00f1ba29876e1ac061f68b86f1a0f2abfe7f192eb13945146bec(
    *,
    description: typing.Optional[builtins.str] = None,
    engine_type: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    high_availability_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.HighAvailabilityConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_type: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.StorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c6d12245793f4f672b44c8dc8abea52071fcab30c798fb152f7e94f72fdfcd(
    props: typing.Union[CfnEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74311782333dd7b2f226004be60ceb58d68e311214298e8a09033bd7342f56de(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8377a029154b4a330b830f32502b350ad6f0da6dd07e27e5ff80f204d2772307(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341378249da435981ec586acad5909d5cf623651d34e60cd60fa2e83fbe50295(
    *,
    file_system_id: typing.Optional[builtins.str] = None,
    mount_point: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf6c525eac1d2870f2787f86a157caad861693211fcb9771c490607f79fc4a4(
    *,
    file_system_id: typing.Optional[builtins.str] = None,
    mount_point: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827412625bc2121c7111b896d2a221d0885153f2d90d2bec96c42480a0692578(
    *,
    desired_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d8847e7a1584542c63e9068e0d2d58bc2de378fe4e1153091fbad2c49b2542(
    *,
    efs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.EfsStorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fsx: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.FsxStorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
