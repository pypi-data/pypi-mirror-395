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
    jsii_type="@aws-cdk/mixins-preview.aws_lookoutequipment.mixins.CfnInferenceSchedulerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_delay_offset_in_minutes": "dataDelayOffsetInMinutes",
        "data_input_configuration": "dataInputConfiguration",
        "data_output_configuration": "dataOutputConfiguration",
        "data_upload_frequency": "dataUploadFrequency",
        "inference_scheduler_name": "inferenceSchedulerName",
        "model_name": "modelName",
        "role_arn": "roleArn",
        "server_side_kms_key_id": "serverSideKmsKeyId",
        "tags": "tags",
    },
)
class CfnInferenceSchedulerMixinProps:
    def __init__(
        self,
        *,
        data_delay_offset_in_minutes: typing.Optional[jsii.Number] = None,
        data_input_configuration: typing.Any = None,
        data_output_configuration: typing.Any = None,
        data_upload_frequency: typing.Optional[builtins.str] = None,
        inference_scheduler_name: typing.Optional[builtins.str] = None,
        model_name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        server_side_kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnInferenceSchedulerPropsMixin.

        :param data_delay_offset_in_minutes: A period of time (in minutes) by which inference on the data is delayed after the data starts. For instance, if an offset delay time of five minutes was selected, inference will not begin on the data until the first data measurement after the five minute mark. For example, if five minutes is selected, the inference scheduler will wake up at the configured frequency with the additional five minute delay time to check the customer S3 bucket. The customer can upload data at the same frequency and they don't need to stop and restart the scheduler when uploading new data.
        :param data_input_configuration: Specifies configuration information for the input data for the inference scheduler, including delimiter, format, and dataset location.
        :param data_output_configuration: Specifies configuration information for the output results for the inference scheduler, including the Amazon S3 location for the output.
        :param data_upload_frequency: How often data is uploaded to the source S3 bucket for the input data. This value is the length of time between data uploads. For instance, if you select 5 minutes, Amazon Lookout for Equipment will upload the real-time data to the source bucket once every 5 minutes. This frequency also determines how often Amazon Lookout for Equipment starts a scheduled inference on your data. In this example, it starts once every 5 minutes.
        :param inference_scheduler_name: The name of the inference scheduler.
        :param model_name: The name of the machine learning model used for the inference scheduler.
        :param role_arn: The Amazon Resource Name (ARN) of a role with permission to access the data source being used for the inference.
        :param server_side_kms_key_id: Provides the identifier of the AWS KMS key used to encrypt inference scheduler data by .
        :param tags: Any tags associated with the inference scheduler. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lookoutequipment import mixins as lookoutequipment_mixins
            
            # data_input_configuration: Any
            # data_output_configuration: Any
            
            cfn_inference_scheduler_mixin_props = lookoutequipment_mixins.CfnInferenceSchedulerMixinProps(
                data_delay_offset_in_minutes=123,
                data_input_configuration=data_input_configuration,
                data_output_configuration=data_output_configuration,
                data_upload_frequency="dataUploadFrequency",
                inference_scheduler_name="inferenceSchedulerName",
                model_name="modelName",
                role_arn="roleArn",
                server_side_kms_key_id="serverSideKmsKeyId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70870c8ff9a03b870e84889f5383cf4b9ccee727c85cc59153c28bb387ba3f44)
            check_type(argname="argument data_delay_offset_in_minutes", value=data_delay_offset_in_minutes, expected_type=type_hints["data_delay_offset_in_minutes"])
            check_type(argname="argument data_input_configuration", value=data_input_configuration, expected_type=type_hints["data_input_configuration"])
            check_type(argname="argument data_output_configuration", value=data_output_configuration, expected_type=type_hints["data_output_configuration"])
            check_type(argname="argument data_upload_frequency", value=data_upload_frequency, expected_type=type_hints["data_upload_frequency"])
            check_type(argname="argument inference_scheduler_name", value=inference_scheduler_name, expected_type=type_hints["inference_scheduler_name"])
            check_type(argname="argument model_name", value=model_name, expected_type=type_hints["model_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument server_side_kms_key_id", value=server_side_kms_key_id, expected_type=type_hints["server_side_kms_key_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_delay_offset_in_minutes is not None:
            self._values["data_delay_offset_in_minutes"] = data_delay_offset_in_minutes
        if data_input_configuration is not None:
            self._values["data_input_configuration"] = data_input_configuration
        if data_output_configuration is not None:
            self._values["data_output_configuration"] = data_output_configuration
        if data_upload_frequency is not None:
            self._values["data_upload_frequency"] = data_upload_frequency
        if inference_scheduler_name is not None:
            self._values["inference_scheduler_name"] = inference_scheduler_name
        if model_name is not None:
            self._values["model_name"] = model_name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if server_side_kms_key_id is not None:
            self._values["server_side_kms_key_id"] = server_side_kms_key_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_delay_offset_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''A period of time (in minutes) by which inference on the data is delayed after the data starts.

        For instance, if an offset delay time of five minutes was selected, inference will not begin on the data until the first data measurement after the five minute mark. For example, if five minutes is selected, the inference scheduler will wake up at the configured frequency with the additional five minute delay time to check the customer S3 bucket. The customer can upload data at the same frequency and they don't need to stop and restart the scheduler when uploading new data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-datadelayoffsetinminutes
        '''
        result = self._values.get("data_delay_offset_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_input_configuration(self) -> typing.Any:
        '''Specifies configuration information for the input data for the inference scheduler, including delimiter, format, and dataset location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-datainputconfiguration
        '''
        result = self._values.get("data_input_configuration")
        return typing.cast(typing.Any, result)

    @builtins.property
    def data_output_configuration(self) -> typing.Any:
        '''Specifies configuration information for the output results for the inference scheduler, including the Amazon S3 location for the output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-dataoutputconfiguration
        '''
        result = self._values.get("data_output_configuration")
        return typing.cast(typing.Any, result)

    @builtins.property
    def data_upload_frequency(self) -> typing.Optional[builtins.str]:
        '''How often data is uploaded to the source S3 bucket for the input data.

        This value is the length of time between data uploads. For instance, if you select 5 minutes, Amazon Lookout for Equipment will upload the real-time data to the source bucket once every 5 minutes. This frequency also determines how often Amazon Lookout for Equipment starts a scheduled inference on your data. In this example, it starts once every 5 minutes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-datauploadfrequency
        '''
        result = self._values.get("data_upload_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inference_scheduler_name(self) -> typing.Optional[builtins.str]:
        '''The name of the inference scheduler.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-inferenceschedulername
        '''
        result = self._values.get("inference_scheduler_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_name(self) -> typing.Optional[builtins.str]:
        '''The name of the machine learning model used for the inference scheduler.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-modelname
        '''
        result = self._values.get("model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of a role with permission to access the data source being used for the inference.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Provides the identifier of the AWS KMS key used to encrypt inference scheduler data by  .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-serversidekmskeyid
        '''
        result = self._values.get("server_side_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Any tags associated with the inference scheduler.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html#cfn-lookoutequipment-inferencescheduler-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInferenceSchedulerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInferenceSchedulerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lookoutequipment.mixins.CfnInferenceSchedulerPropsMixin",
):
    '''Creates a scheduled inference.

    Scheduling an inference is setting up a continuous real-time inference plan to analyze new measurement data. When setting up the schedule, you provide an Amazon S3 bucket location for the input data, assign it a delimiter between separate entries in the data, set an offset delay if desired, and set the frequency of inferencing. You must also provide an Amazon S3 bucket location for the output data.
    .. epigraph::

       Updating some properties below (for example, InferenceSchedulerName and ServerSideKmsKeyId) triggers a resource replacement, which requires a new model. To replace such a property using CloudFormation , but without creating a completely new stack, you must replace ModelName. If you need to replace the property, but want to use the same model, delete the current stack and create a new one with the updated properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutequipment-inferencescheduler.html
    :cloudformationResource: AWS::LookoutEquipment::InferenceScheduler
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lookoutequipment import mixins as lookoutequipment_mixins
        
        # data_input_configuration: Any
        # data_output_configuration: Any
        
        cfn_inference_scheduler_props_mixin = lookoutequipment_mixins.CfnInferenceSchedulerPropsMixin(lookoutequipment_mixins.CfnInferenceSchedulerMixinProps(
            data_delay_offset_in_minutes=123,
            data_input_configuration=data_input_configuration,
            data_output_configuration=data_output_configuration,
            data_upload_frequency="dataUploadFrequency",
            inference_scheduler_name="inferenceSchedulerName",
            model_name="modelName",
            role_arn="roleArn",
            server_side_kms_key_id="serverSideKmsKeyId",
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
        props: typing.Union[CfnInferenceSchedulerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::LookoutEquipment::InferenceScheduler``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91932b2dbcba402fe7fa7061e566c1078cc15859763fe9db91a38108e9f5b854)
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
            type_hints = typing.get_type_hints(_typecheckingstub__983fa3ceeb0ecb567d5eff5c333b9002661ae2a112b98516b85c2e941301eea7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a640441fe07cb9f79bd441d5e729dcdf7ad0f8d1036137d259d218ed3dc377)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInferenceSchedulerMixinProps:
        return typing.cast(CfnInferenceSchedulerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutequipment.mixins.CfnInferenceSchedulerPropsMixin.DataInputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "inference_input_name_configuration": "inferenceInputNameConfiguration",
            "input_time_zone_offset": "inputTimeZoneOffset",
            "s3_input_configuration": "s3InputConfiguration",
        },
    )
    class DataInputConfigurationProperty:
        def __init__(
            self,
            *,
            inference_input_name_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInferenceSchedulerPropsMixin.InputNameConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            input_time_zone_offset: typing.Optional[builtins.str] = None,
            s3_input_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInferenceSchedulerPropsMixin.S3InputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies configuration information for the input data for the inference scheduler, including delimiter, format, and dataset location.

            :param inference_input_name_configuration: Specifies configuration information for the input data for the inference, including timestamp format and delimiter.
            :param input_time_zone_offset: Indicates the difference between your time zone and Greenwich Mean Time (GMT).
            :param s3_input_configuration: Specifies configuration information for the input data for the inference, including input data S3 location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-datainputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutequipment import mixins as lookoutequipment_mixins
                
                data_input_configuration_property = lookoutequipment_mixins.CfnInferenceSchedulerPropsMixin.DataInputConfigurationProperty(
                    inference_input_name_configuration=lookoutequipment_mixins.CfnInferenceSchedulerPropsMixin.InputNameConfigurationProperty(
                        component_timestamp_delimiter="componentTimestampDelimiter",
                        timestamp_format="timestampFormat"
                    ),
                    input_time_zone_offset="inputTimeZoneOffset",
                    s3_input_configuration=lookoutequipment_mixins.CfnInferenceSchedulerPropsMixin.S3InputConfigurationProperty(
                        bucket="bucket",
                        prefix="prefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2eb00d9470e1176458b7b344e7df856e8be1136222befc8593ad6ee72de74d2d)
                check_type(argname="argument inference_input_name_configuration", value=inference_input_name_configuration, expected_type=type_hints["inference_input_name_configuration"])
                check_type(argname="argument input_time_zone_offset", value=input_time_zone_offset, expected_type=type_hints["input_time_zone_offset"])
                check_type(argname="argument s3_input_configuration", value=s3_input_configuration, expected_type=type_hints["s3_input_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if inference_input_name_configuration is not None:
                self._values["inference_input_name_configuration"] = inference_input_name_configuration
            if input_time_zone_offset is not None:
                self._values["input_time_zone_offset"] = input_time_zone_offset
            if s3_input_configuration is not None:
                self._values["s3_input_configuration"] = s3_input_configuration

        @builtins.property
        def inference_input_name_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInferenceSchedulerPropsMixin.InputNameConfigurationProperty"]]:
            '''Specifies configuration information for the input data for the inference, including timestamp format and delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-datainputconfiguration.html#cfn-lookoutequipment-inferencescheduler-datainputconfiguration-inferenceinputnameconfiguration
            '''
            result = self._values.get("inference_input_name_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInferenceSchedulerPropsMixin.InputNameConfigurationProperty"]], result)

        @builtins.property
        def input_time_zone_offset(self) -> typing.Optional[builtins.str]:
            '''Indicates the difference between your time zone and Greenwich Mean Time (GMT).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-datainputconfiguration.html#cfn-lookoutequipment-inferencescheduler-datainputconfiguration-inputtimezoneoffset
            '''
            result = self._values.get("input_time_zone_offset")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_input_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInferenceSchedulerPropsMixin.S3InputConfigurationProperty"]]:
            '''Specifies configuration information for the input data for the inference, including input data S3 location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-datainputconfiguration.html#cfn-lookoutequipment-inferencescheduler-datainputconfiguration-s3inputconfiguration
            '''
            result = self._values.get("s3_input_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInferenceSchedulerPropsMixin.S3InputConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataInputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutequipment.mixins.CfnInferenceSchedulerPropsMixin.DataOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_key_id": "kmsKeyId",
            "s3_output_configuration": "s3OutputConfiguration",
        },
    )
    class DataOutputConfigurationProperty:
        def __init__(
            self,
            *,
            kms_key_id: typing.Optional[builtins.str] = None,
            s3_output_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInferenceSchedulerPropsMixin.S3OutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies configuration information for the output results for the inference scheduler, including the S3 location for the output.

            :param kms_key_id: The ID number for the AWS KMS key used to encrypt the inference output.
            :param s3_output_configuration: Specifies configuration information for the output results from the inference, including output S3 location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-dataoutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutequipment import mixins as lookoutequipment_mixins
                
                data_output_configuration_property = lookoutequipment_mixins.CfnInferenceSchedulerPropsMixin.DataOutputConfigurationProperty(
                    kms_key_id="kmsKeyId",
                    s3_output_configuration=lookoutequipment_mixins.CfnInferenceSchedulerPropsMixin.S3OutputConfigurationProperty(
                        bucket="bucket",
                        prefix="prefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6783136c753eca83205358b9e673589fd2eb02505ac34b7ea14a19ae77280e3a)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument s3_output_configuration", value=s3_output_configuration, expected_type=type_hints["s3_output_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if s3_output_configuration is not None:
                self._values["s3_output_configuration"] = s3_output_configuration

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The ID number for the AWS KMS key used to encrypt the inference output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-dataoutputconfiguration.html#cfn-lookoutequipment-inferencescheduler-dataoutputconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_output_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInferenceSchedulerPropsMixin.S3OutputConfigurationProperty"]]:
            '''Specifies configuration information for the output results from the inference, including output S3 location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-dataoutputconfiguration.html#cfn-lookoutequipment-inferencescheduler-dataoutputconfiguration-s3outputconfiguration
            '''
            result = self._values.get("s3_output_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInferenceSchedulerPropsMixin.S3OutputConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutequipment.mixins.CfnInferenceSchedulerPropsMixin.InputNameConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_timestamp_delimiter": "componentTimestampDelimiter",
            "timestamp_format": "timestampFormat",
        },
    )
    class InputNameConfigurationProperty:
        def __init__(
            self,
            *,
            component_timestamp_delimiter: typing.Optional[builtins.str] = None,
            timestamp_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies configuration information for the input data for the inference, including timestamp format and delimiter.

            :param component_timestamp_delimiter: Indicates the delimiter character used between items in the data.
            :param timestamp_format: The format of the timestamp, whether Epoch time, or standard, with or without hyphens (-).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-inputnameconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutequipment import mixins as lookoutequipment_mixins
                
                input_name_configuration_property = lookoutequipment_mixins.CfnInferenceSchedulerPropsMixin.InputNameConfigurationProperty(
                    component_timestamp_delimiter="componentTimestampDelimiter",
                    timestamp_format="timestampFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__38362d62fb5391c227d522fb5afebb4e1e39977a0c0e726ea140e6ddf0279518)
                check_type(argname="argument component_timestamp_delimiter", value=component_timestamp_delimiter, expected_type=type_hints["component_timestamp_delimiter"])
                check_type(argname="argument timestamp_format", value=timestamp_format, expected_type=type_hints["timestamp_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_timestamp_delimiter is not None:
                self._values["component_timestamp_delimiter"] = component_timestamp_delimiter
            if timestamp_format is not None:
                self._values["timestamp_format"] = timestamp_format

        @builtins.property
        def component_timestamp_delimiter(self) -> typing.Optional[builtins.str]:
            '''Indicates the delimiter character used between items in the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-inputnameconfiguration.html#cfn-lookoutequipment-inferencescheduler-inputnameconfiguration-componenttimestampdelimiter
            '''
            result = self._values.get("component_timestamp_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timestamp_format(self) -> typing.Optional[builtins.str]:
            '''The format of the timestamp, whether Epoch time, or standard, with or without hyphens (-).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-inputnameconfiguration.html#cfn-lookoutequipment-inferencescheduler-inputnameconfiguration-timestampformat
            '''
            result = self._values.get("timestamp_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputNameConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutequipment.mixins.CfnInferenceSchedulerPropsMixin.S3InputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "prefix": "prefix"},
    )
    class S3InputConfigurationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies configuration information for the input data for the inference, including input data S3 location.

            :param bucket: 
            :param prefix: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-s3inputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutequipment import mixins as lookoutequipment_mixins
                
                s3_input_configuration_property = lookoutequipment_mixins.CfnInferenceSchedulerPropsMixin.S3InputConfigurationProperty(
                    bucket="bucket",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1e1e6c8adca1d87c0865b845919be65d996766428f201fe4f78a8f1a5604517)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-s3inputconfiguration.html#cfn-lookoutequipment-inferencescheduler-s3inputconfiguration-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-s3inputconfiguration.html#cfn-lookoutequipment-inferencescheduler-s3inputconfiguration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3InputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutequipment.mixins.CfnInferenceSchedulerPropsMixin.S3OutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "prefix": "prefix"},
    )
    class S3OutputConfigurationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies configuration information for the output results from the inference, including output S3 location.

            :param bucket: 
            :param prefix: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-s3outputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutequipment import mixins as lookoutequipment_mixins
                
                s3_output_configuration_property = lookoutequipment_mixins.CfnInferenceSchedulerPropsMixin.S3OutputConfigurationProperty(
                    bucket="bucket",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d418add92f8eeccb4fe62ba9c7f9e3547a61479e135e85f92eb13ef73e3ffc29)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-s3outputconfiguration.html#cfn-lookoutequipment-inferencescheduler-s3outputconfiguration-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutequipment-inferencescheduler-s3outputconfiguration.html#cfn-lookoutequipment-inferencescheduler-s3outputconfiguration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3OutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnInferenceSchedulerMixinProps",
    "CfnInferenceSchedulerPropsMixin",
]

publication.publish()

def _typecheckingstub__70870c8ff9a03b870e84889f5383cf4b9ccee727c85cc59153c28bb387ba3f44(
    *,
    data_delay_offset_in_minutes: typing.Optional[jsii.Number] = None,
    data_input_configuration: typing.Any = None,
    data_output_configuration: typing.Any = None,
    data_upload_frequency: typing.Optional[builtins.str] = None,
    inference_scheduler_name: typing.Optional[builtins.str] = None,
    model_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    server_side_kms_key_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91932b2dbcba402fe7fa7061e566c1078cc15859763fe9db91a38108e9f5b854(
    props: typing.Union[CfnInferenceSchedulerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__983fa3ceeb0ecb567d5eff5c333b9002661ae2a112b98516b85c2e941301eea7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a640441fe07cb9f79bd441d5e729dcdf7ad0f8d1036137d259d218ed3dc377(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb00d9470e1176458b7b344e7df856e8be1136222befc8593ad6ee72de74d2d(
    *,
    inference_input_name_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInferenceSchedulerPropsMixin.InputNameConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    input_time_zone_offset: typing.Optional[builtins.str] = None,
    s3_input_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInferenceSchedulerPropsMixin.S3InputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6783136c753eca83205358b9e673589fd2eb02505ac34b7ea14a19ae77280e3a(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
    s3_output_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInferenceSchedulerPropsMixin.S3OutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38362d62fb5391c227d522fb5afebb4e1e39977a0c0e726ea140e6ddf0279518(
    *,
    component_timestamp_delimiter: typing.Optional[builtins.str] = None,
    timestamp_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e1e6c8adca1d87c0865b845919be65d996766428f201fe4f78a8f1a5604517(
    *,
    bucket: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d418add92f8eeccb4fe62ba9c7f9e3547a61479e135e85f92eb13ef73e3ffc29(
    *,
    bucket: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
