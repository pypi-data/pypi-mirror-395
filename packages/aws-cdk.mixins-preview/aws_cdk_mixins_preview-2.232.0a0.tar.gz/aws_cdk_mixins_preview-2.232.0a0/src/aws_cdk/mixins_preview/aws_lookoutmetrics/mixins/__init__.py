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
    jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAlertMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "alert_description": "alertDescription",
        "alert_name": "alertName",
        "alert_sensitivity_threshold": "alertSensitivityThreshold",
        "anomaly_detector_arn": "anomalyDetectorArn",
    },
)
class CfnAlertMixinProps:
    def __init__(
        self,
        *,
        action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlertPropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        alert_description: typing.Optional[builtins.str] = None,
        alert_name: typing.Optional[builtins.str] = None,
        alert_sensitivity_threshold: typing.Optional[jsii.Number] = None,
        anomaly_detector_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAlertPropsMixin.

        :param action: Action that will be triggered when there is an alert.
        :param alert_description: A description of the alert.
        :param alert_name: The name of the alert.
        :param alert_sensitivity_threshold: An integer from 0 to 100 specifying the alert sensitivity threshold.
        :param anomaly_detector_arn: The ARN of the detector to which the alert is attached.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutmetrics-alert.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
            
            cfn_alert_mixin_props = lookoutmetrics_mixins.CfnAlertMixinProps(
                action=lookoutmetrics_mixins.CfnAlertPropsMixin.ActionProperty(
                    lambda_configuration=lookoutmetrics_mixins.CfnAlertPropsMixin.LambdaConfigurationProperty(
                        lambda_arn="lambdaArn",
                        role_arn="roleArn"
                    ),
                    sns_configuration=lookoutmetrics_mixins.CfnAlertPropsMixin.SNSConfigurationProperty(
                        role_arn="roleArn",
                        sns_topic_arn="snsTopicArn"
                    )
                ),
                alert_description="alertDescription",
                alert_name="alertName",
                alert_sensitivity_threshold=123,
                anomaly_detector_arn="anomalyDetectorArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edbdcffb7fe85456e2f8abe868741c96a8ccd0153b24b763c39a33ad67d012ad)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument alert_description", value=alert_description, expected_type=type_hints["alert_description"])
            check_type(argname="argument alert_name", value=alert_name, expected_type=type_hints["alert_name"])
            check_type(argname="argument alert_sensitivity_threshold", value=alert_sensitivity_threshold, expected_type=type_hints["alert_sensitivity_threshold"])
            check_type(argname="argument anomaly_detector_arn", value=anomaly_detector_arn, expected_type=type_hints["anomaly_detector_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if alert_description is not None:
            self._values["alert_description"] = alert_description
        if alert_name is not None:
            self._values["alert_name"] = alert_name
        if alert_sensitivity_threshold is not None:
            self._values["alert_sensitivity_threshold"] = alert_sensitivity_threshold
        if anomaly_detector_arn is not None:
            self._values["anomaly_detector_arn"] = anomaly_detector_arn

    @builtins.property
    def action(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlertPropsMixin.ActionProperty"]]:
        '''Action that will be triggered when there is an alert.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutmetrics-alert.html#cfn-lookoutmetrics-alert-action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlertPropsMixin.ActionProperty"]], result)

    @builtins.property
    def alert_description(self) -> typing.Optional[builtins.str]:
        '''A description of the alert.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutmetrics-alert.html#cfn-lookoutmetrics-alert-alertdescription
        '''
        result = self._values.get("alert_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alert_name(self) -> typing.Optional[builtins.str]:
        '''The name of the alert.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutmetrics-alert.html#cfn-lookoutmetrics-alert-alertname
        '''
        result = self._values.get("alert_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alert_sensitivity_threshold(self) -> typing.Optional[jsii.Number]:
        '''An integer from 0 to 100 specifying the alert sensitivity threshold.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutmetrics-alert.html#cfn-lookoutmetrics-alert-alertsensitivitythreshold
        '''
        result = self._values.get("alert_sensitivity_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def anomaly_detector_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the detector to which the alert is attached.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutmetrics-alert.html#cfn-lookoutmetrics-alert-anomalydetectorarn
        '''
        result = self._values.get("anomaly_detector_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAlertMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAlertPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAlertPropsMixin",
):
    '''.. epigraph::

   End of support notice: On Oct 9, 2025, AWS will end support for Amazon Lookout for Metrics.

    After Oct 9, 2025, you will no longer be able to access the Amazon Lookout for Metrics console or Amazon Lookout for Metrics resources. For more information, see `Amazon Lookout for Metrics end of support <https://docs.aws.amazon.com//blogs/machine-learning/transitioning-off-amazon-lookout-for-metrics/>`_ .

    The ``AWS::LookoutMetrics::Alert`` type creates an alert for an anomaly detector.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutmetrics-alert.html
    :cloudformationResource: AWS::LookoutMetrics::Alert
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
        
        cfn_alert_props_mixin = lookoutmetrics_mixins.CfnAlertPropsMixin(lookoutmetrics_mixins.CfnAlertMixinProps(
            action=lookoutmetrics_mixins.CfnAlertPropsMixin.ActionProperty(
                lambda_configuration=lookoutmetrics_mixins.CfnAlertPropsMixin.LambdaConfigurationProperty(
                    lambda_arn="lambdaArn",
                    role_arn="roleArn"
                ),
                sns_configuration=lookoutmetrics_mixins.CfnAlertPropsMixin.SNSConfigurationProperty(
                    role_arn="roleArn",
                    sns_topic_arn="snsTopicArn"
                )
            ),
            alert_description="alertDescription",
            alert_name="alertName",
            alert_sensitivity_threshold=123,
            anomaly_detector_arn="anomalyDetectorArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAlertMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::LookoutMetrics::Alert``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8651fb2567d4f12977bccc77f0845b1a357caa04b6a1cd3cfcd83394abcb4f07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b46057b3a8a71576e7a1d3d7f5ee8a4837824c8711d98ea2bf622db737b34b47)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17e7bd8a7a764d69b9a4cfa5cab138807e800e26f13b53686441176bdde73a00)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAlertMixinProps:
        return typing.cast(CfnAlertMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAlertPropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_configuration": "lambdaConfiguration",
            "sns_configuration": "snsConfiguration",
        },
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            lambda_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlertPropsMixin.LambdaConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sns_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlertPropsMixin.SNSConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A configuration that specifies the action to perform when anomalies are detected.

            :param lambda_configuration: A configuration for an AWS Lambda channel.
            :param sns_configuration: A configuration for an Amazon SNS channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-alert-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                action_property = lookoutmetrics_mixins.CfnAlertPropsMixin.ActionProperty(
                    lambda_configuration=lookoutmetrics_mixins.CfnAlertPropsMixin.LambdaConfigurationProperty(
                        lambda_arn="lambdaArn",
                        role_arn="roleArn"
                    ),
                    sns_configuration=lookoutmetrics_mixins.CfnAlertPropsMixin.SNSConfigurationProperty(
                        role_arn="roleArn",
                        sns_topic_arn="snsTopicArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17d6dce2bb5a9b5c9fb56d143b6eb61df22a9b61103b9bdb7c6497434a1225ee)
                check_type(argname="argument lambda_configuration", value=lambda_configuration, expected_type=type_hints["lambda_configuration"])
                check_type(argname="argument sns_configuration", value=sns_configuration, expected_type=type_hints["sns_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_configuration is not None:
                self._values["lambda_configuration"] = lambda_configuration
            if sns_configuration is not None:
                self._values["sns_configuration"] = sns_configuration

        @builtins.property
        def lambda_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlertPropsMixin.LambdaConfigurationProperty"]]:
            '''A configuration for an AWS Lambda channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-alert-action.html#cfn-lookoutmetrics-alert-action-lambdaconfiguration
            '''
            result = self._values.get("lambda_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlertPropsMixin.LambdaConfigurationProperty"]], result)

        @builtins.property
        def sns_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlertPropsMixin.SNSConfigurationProperty"]]:
            '''A configuration for an Amazon SNS channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-alert-action.html#cfn-lookoutmetrics-alert-action-snsconfiguration
            '''
            result = self._values.get("sns_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlertPropsMixin.SNSConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAlertPropsMixin.LambdaConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_arn": "lambdaArn", "role_arn": "roleArn"},
    )
    class LambdaConfigurationProperty:
        def __init__(
            self,
            *,
            lambda_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a Lambda configuration.

            :param lambda_arn: The ARN of the Lambda function.
            :param role_arn: The ARN of an IAM role that has permission to invoke the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-alert-lambdaconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                lambda_configuration_property = lookoutmetrics_mixins.CfnAlertPropsMixin.LambdaConfigurationProperty(
                    lambda_arn="lambdaArn",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1e90f8c711796020c1af0531107b632f2f7311f2b750d420afc94518135b6d29)
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_arn is not None:
                self._values["lambda_arn"] = lambda_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def lambda_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-alert-lambdaconfiguration.html#cfn-lookoutmetrics-alert-lambdaconfiguration-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of an IAM role that has permission to invoke the Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-alert-lambdaconfiguration.html#cfn-lookoutmetrics-alert-lambdaconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAlertPropsMixin.SNSConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn", "sns_topic_arn": "snsTopicArn"},
    )
    class SNSConfigurationProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            sns_topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the SNS topic to which you want to send your alerts and the IAM role that has access to that topic.

            :param role_arn: The ARN of the IAM role that has access to the target SNS topic.
            :param sns_topic_arn: The ARN of the target SNS topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-alert-snsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                s_nSConfiguration_property = lookoutmetrics_mixins.CfnAlertPropsMixin.SNSConfigurationProperty(
                    role_arn="roleArn",
                    sns_topic_arn="snsTopicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__657e5b904dc57ba92a1c341f8b94e67029700bde06348d9a69ccfce4930680a9)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument sns_topic_arn", value=sns_topic_arn, expected_type=type_hints["sns_topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if sns_topic_arn is not None:
                self._values["sns_topic_arn"] = sns_topic_arn

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role that has access to the target SNS topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-alert-snsconfiguration.html#cfn-lookoutmetrics-alert-snsconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sns_topic_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the target SNS topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-alert-snsconfiguration.html#cfn-lookoutmetrics-alert-snsconfiguration-snstopicarn
            '''
            result = self._values.get("sns_topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SNSConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "anomaly_detector_config": "anomalyDetectorConfig",
        "anomaly_detector_description": "anomalyDetectorDescription",
        "anomaly_detector_name": "anomalyDetectorName",
        "kms_key_arn": "kmsKeyArn",
        "metric_set_list": "metricSetList",
    },
)
class CfnAnomalyDetectorMixinProps:
    def __init__(
        self,
        *,
        anomaly_detector_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        anomaly_detector_description: typing.Optional[builtins.str] = None,
        anomaly_detector_name: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        metric_set_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.MetricSetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnAnomalyDetectorPropsMixin.

        :param anomaly_detector_config: Contains information about the configuration of the anomaly detector.
        :param anomaly_detector_description: A description of the detector.
        :param anomaly_detector_name: The name of the detector.
        :param kms_key_arn: The ARN of the KMS key to use to encrypt your data.
        :param metric_set_list: The detector's dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutmetrics-anomalydetector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
            
            cfn_anomaly_detector_mixin_props = lookoutmetrics_mixins.CfnAnomalyDetectorMixinProps(
                anomaly_detector_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigProperty(
                    anomaly_detector_frequency="anomalyDetectorFrequency"
                ),
                anomaly_detector_description="anomalyDetectorDescription",
                anomaly_detector_name="anomalyDetectorName",
                kms_key_arn="kmsKeyArn",
                metric_set_list=[lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.MetricSetProperty(
                    dimension_list=["dimensionList"],
                    metric_list=[lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.MetricProperty(
                        aggregation_function="aggregationFunction",
                        metric_name="metricName",
                        namespace="namespace"
                    )],
                    metric_set_description="metricSetDescription",
                    metric_set_frequency="metricSetFrequency",
                    metric_set_name="metricSetName",
                    metric_source=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.MetricSourceProperty(
                        app_flow_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.AppFlowConfigProperty(
                            flow_name="flowName",
                            role_arn="roleArn"
                        ),
                        cloudwatch_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.CloudwatchConfigProperty(
                            role_arn="roleArn"
                        ),
                        rds_source_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.RDSSourceConfigProperty(
                            database_host="databaseHost",
                            database_name="databaseName",
                            database_port=123,
                            db_instance_identifier="dbInstanceIdentifier",
                            role_arn="roleArn",
                            secret_manager_arn="secretManagerArn",
                            table_name="tableName",
                            vpc_configuration=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty(
                                security_group_id_list=["securityGroupIdList"],
                                subnet_id_list=["subnetIdList"]
                            )
                        ),
                        redshift_source_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.RedshiftSourceConfigProperty(
                            cluster_identifier="clusterIdentifier",
                            database_host="databaseHost",
                            database_name="databaseName",
                            database_port=123,
                            role_arn="roleArn",
                            secret_manager_arn="secretManagerArn",
                            table_name="tableName",
                            vpc_configuration=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty(
                                security_group_id_list=["securityGroupIdList"],
                                subnet_id_list=["subnetIdList"]
                            )
                        ),
                        s3_source_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.S3SourceConfigProperty(
                            file_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.FileFormatDescriptorProperty(
                                csv_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.CsvFormatDescriptorProperty(
                                    charset="charset",
                                    contains_header=False,
                                    delimiter="delimiter",
                                    file_compression="fileCompression",
                                    header_list=["headerList"],
                                    quote_symbol="quoteSymbol"
                                ),
                                json_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.JsonFormatDescriptorProperty(
                                    charset="charset",
                                    file_compression="fileCompression"
                                )
                            ),
                            historical_data_path_list=["historicalDataPathList"],
                            role_arn="roleArn",
                            templated_path_list=["templatedPathList"]
                        )
                    ),
                    offset=123,
                    timestamp_column=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.TimestampColumnProperty(
                        column_format="columnFormat",
                        column_name="columnName"
                    ),
                    timezone="timezone"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d983a98e37150e171c3f6a8fdc8eba05ae44452d404aceba860b76fd99763f9b)
            check_type(argname="argument anomaly_detector_config", value=anomaly_detector_config, expected_type=type_hints["anomaly_detector_config"])
            check_type(argname="argument anomaly_detector_description", value=anomaly_detector_description, expected_type=type_hints["anomaly_detector_description"])
            check_type(argname="argument anomaly_detector_name", value=anomaly_detector_name, expected_type=type_hints["anomaly_detector_name"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument metric_set_list", value=metric_set_list, expected_type=type_hints["metric_set_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if anomaly_detector_config is not None:
            self._values["anomaly_detector_config"] = anomaly_detector_config
        if anomaly_detector_description is not None:
            self._values["anomaly_detector_description"] = anomaly_detector_description
        if anomaly_detector_name is not None:
            self._values["anomaly_detector_name"] = anomaly_detector_name
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if metric_set_list is not None:
            self._values["metric_set_list"] = metric_set_list

    @builtins.property
    def anomaly_detector_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigProperty"]]:
        '''Contains information about the configuration of the anomaly detector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutmetrics-anomalydetector.html#cfn-lookoutmetrics-anomalydetector-anomalydetectorconfig
        '''
        result = self._values.get("anomaly_detector_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigProperty"]], result)

    @builtins.property
    def anomaly_detector_description(self) -> typing.Optional[builtins.str]:
        '''A description of the detector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutmetrics-anomalydetector.html#cfn-lookoutmetrics-anomalydetector-anomalydetectordescription
        '''
        result = self._values.get("anomaly_detector_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def anomaly_detector_name(self) -> typing.Optional[builtins.str]:
        '''The name of the detector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutmetrics-anomalydetector.html#cfn-lookoutmetrics-anomalydetector-anomalydetectorname
        '''
        result = self._values.get("anomaly_detector_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the KMS key to use to encrypt your data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutmetrics-anomalydetector.html#cfn-lookoutmetrics-anomalydetector-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_set_list(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricSetProperty"]]]]:
        '''The detector's dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutmetrics-anomalydetector.html#cfn-lookoutmetrics-anomalydetector-metricsetlist
        '''
        result = self._values.get("metric_set_list")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricSetProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAnomalyDetectorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAnomalyDetectorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin",
):
    '''.. epigraph::

   End of support notice: On Oct 9, 2025, AWS will end support for Amazon Lookout for Metrics.

    After Oct 9, 2025, you will no longer be able to access the Amazon Lookout for Metrics console or Amazon Lookout for Metrics resources. For more information, see `Amazon Lookout for Metrics end of support <https://docs.aws.amazon.com//blogs/machine-learning/transitioning-off-amazon-lookout-for-metrics/>`_ .

    The ``AWS::LookoutMetrics::AnomalyDetector`` type creates an anomaly detector.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lookoutmetrics-anomalydetector.html
    :cloudformationResource: AWS::LookoutMetrics::AnomalyDetector
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
        
        cfn_anomaly_detector_props_mixin = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin(lookoutmetrics_mixins.CfnAnomalyDetectorMixinProps(
            anomaly_detector_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigProperty(
                anomaly_detector_frequency="anomalyDetectorFrequency"
            ),
            anomaly_detector_description="anomalyDetectorDescription",
            anomaly_detector_name="anomalyDetectorName",
            kms_key_arn="kmsKeyArn",
            metric_set_list=[lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.MetricSetProperty(
                dimension_list=["dimensionList"],
                metric_list=[lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.MetricProperty(
                    aggregation_function="aggregationFunction",
                    metric_name="metricName",
                    namespace="namespace"
                )],
                metric_set_description="metricSetDescription",
                metric_set_frequency="metricSetFrequency",
                metric_set_name="metricSetName",
                metric_source=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.MetricSourceProperty(
                    app_flow_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.AppFlowConfigProperty(
                        flow_name="flowName",
                        role_arn="roleArn"
                    ),
                    cloudwatch_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.CloudwatchConfigProperty(
                        role_arn="roleArn"
                    ),
                    rds_source_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.RDSSourceConfigProperty(
                        database_host="databaseHost",
                        database_name="databaseName",
                        database_port=123,
                        db_instance_identifier="dbInstanceIdentifier",
                        role_arn="roleArn",
                        secret_manager_arn="secretManagerArn",
                        table_name="tableName",
                        vpc_configuration=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty(
                            security_group_id_list=["securityGroupIdList"],
                            subnet_id_list=["subnetIdList"]
                        )
                    ),
                    redshift_source_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.RedshiftSourceConfigProperty(
                        cluster_identifier="clusterIdentifier",
                        database_host="databaseHost",
                        database_name="databaseName",
                        database_port=123,
                        role_arn="roleArn",
                        secret_manager_arn="secretManagerArn",
                        table_name="tableName",
                        vpc_configuration=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty(
                            security_group_id_list=["securityGroupIdList"],
                            subnet_id_list=["subnetIdList"]
                        )
                    ),
                    s3_source_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.S3SourceConfigProperty(
                        file_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.FileFormatDescriptorProperty(
                            csv_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.CsvFormatDescriptorProperty(
                                charset="charset",
                                contains_header=False,
                                delimiter="delimiter",
                                file_compression="fileCompression",
                                header_list=["headerList"],
                                quote_symbol="quoteSymbol"
                            ),
                            json_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.JsonFormatDescriptorProperty(
                                charset="charset",
                                file_compression="fileCompression"
                            )
                        ),
                        historical_data_path_list=["historicalDataPathList"],
                        role_arn="roleArn",
                        templated_path_list=["templatedPathList"]
                    )
                ),
                offset=123,
                timestamp_column=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.TimestampColumnProperty(
                    column_format="columnFormat",
                    column_name="columnName"
                ),
                timezone="timezone"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAnomalyDetectorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::LookoutMetrics::AnomalyDetector``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcfa271764f08da770e42422ebc0941b88f557ffdb27b9eaf49e2d6e31f35213)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d6f574ebc990af29991007e185c2c5ba27f557763962da03dce7b8c066faffe)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad28285c20234e0191d64922a82bae5e9bedecb23ef4638bc06d31196477190)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAnomalyDetectorMixinProps:
        return typing.cast(CfnAnomalyDetectorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"anomaly_detector_frequency": "anomalyDetectorFrequency"},
    )
    class AnomalyDetectorConfigProperty:
        def __init__(
            self,
            *,
            anomaly_detector_frequency: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a detector's configuration.

            :param anomaly_detector_frequency: The frequency at which the detector analyzes its source data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-anomalydetectorconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                anomaly_detector_config_property = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigProperty(
                    anomaly_detector_frequency="anomalyDetectorFrequency"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92784fc52036d5f01764761a226286bf326a15c4b8b17518dbce6f74ac844371)
                check_type(argname="argument anomaly_detector_frequency", value=anomaly_detector_frequency, expected_type=type_hints["anomaly_detector_frequency"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if anomaly_detector_frequency is not None:
                self._values["anomaly_detector_frequency"] = anomaly_detector_frequency

        @builtins.property
        def anomaly_detector_frequency(self) -> typing.Optional[builtins.str]:
            '''The frequency at which the detector analyzes its source data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-anomalydetectorconfig.html#cfn-lookoutmetrics-anomalydetector-anomalydetectorconfig-anomalydetectorfrequency
            '''
            result = self._values.get("anomaly_detector_frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnomalyDetectorConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin.AppFlowConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"flow_name": "flowName", "role_arn": "roleArn"},
    )
    class AppFlowConfigProperty:
        def __init__(
            self,
            *,
            flow_name: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details about an Amazon AppFlow flow datasource.

            :param flow_name: name of the flow.
            :param role_arn: An IAM role that gives Amazon Lookout for Metrics permission to access the flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-appflowconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                app_flow_config_property = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.AppFlowConfigProperty(
                    flow_name="flowName",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e6448b22ba72a4436614ef3849c05cb051f7abe6c1a23a10f209248f9a66510)
                check_type(argname="argument flow_name", value=flow_name, expected_type=type_hints["flow_name"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if flow_name is not None:
                self._values["flow_name"] = flow_name
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def flow_name(self) -> typing.Optional[builtins.str]:
            '''name of the flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-appflowconfig.html#cfn-lookoutmetrics-anomalydetector-appflowconfig-flowname
            '''
            result = self._values.get("flow_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''An IAM role that gives Amazon Lookout for Metrics permission to access the flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-appflowconfig.html#cfn-lookoutmetrics-anomalydetector-appflowconfig-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppFlowConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin.CloudwatchConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn"},
    )
    class CloudwatchConfigProperty:
        def __init__(self, *, role_arn: typing.Optional[builtins.str] = None) -> None:
            '''Details about an Amazon CloudWatch datasource.

            :param role_arn: An IAM role that gives Amazon Lookout for Metrics permission to access data in Amazon CloudWatch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-cloudwatchconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                cloudwatch_config_property = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.CloudwatchConfigProperty(
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59e5d72a0db2af5889423d074e7569749ddf99aa15050a6dc7e83c32bd2cd773)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''An IAM role that gives Amazon Lookout for Metrics permission to access data in Amazon CloudWatch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-cloudwatchconfig.html#cfn-lookoutmetrics-anomalydetector-cloudwatchconfig-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudwatchConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin.CsvFormatDescriptorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "charset": "charset",
            "contains_header": "containsHeader",
            "delimiter": "delimiter",
            "file_compression": "fileCompression",
            "header_list": "headerList",
            "quote_symbol": "quoteSymbol",
        },
    )
    class CsvFormatDescriptorProperty:
        def __init__(
            self,
            *,
            charset: typing.Optional[builtins.str] = None,
            contains_header: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            delimiter: typing.Optional[builtins.str] = None,
            file_compression: typing.Optional[builtins.str] = None,
            header_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            quote_symbol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about how a source CSV data file should be analyzed.

            :param charset: The character set in which the source CSV file is written.
            :param contains_header: Whether or not the source CSV file contains a header.
            :param delimiter: The character used to delimit the source CSV file.
            :param file_compression: The level of compression of the source CSV file.
            :param header_list: A list of the source CSV file's headers, if any.
            :param quote_symbol: The character used as a quote character.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-csvformatdescriptor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                csv_format_descriptor_property = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.CsvFormatDescriptorProperty(
                    charset="charset",
                    contains_header=False,
                    delimiter="delimiter",
                    file_compression="fileCompression",
                    header_list=["headerList"],
                    quote_symbol="quoteSymbol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6781179588be616a33d0c894d22b9ba20c333dac0ce2e2a7cb7f5f3748d7f1bb)
                check_type(argname="argument charset", value=charset, expected_type=type_hints["charset"])
                check_type(argname="argument contains_header", value=contains_header, expected_type=type_hints["contains_header"])
                check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
                check_type(argname="argument file_compression", value=file_compression, expected_type=type_hints["file_compression"])
                check_type(argname="argument header_list", value=header_list, expected_type=type_hints["header_list"])
                check_type(argname="argument quote_symbol", value=quote_symbol, expected_type=type_hints["quote_symbol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if charset is not None:
                self._values["charset"] = charset
            if contains_header is not None:
                self._values["contains_header"] = contains_header
            if delimiter is not None:
                self._values["delimiter"] = delimiter
            if file_compression is not None:
                self._values["file_compression"] = file_compression
            if header_list is not None:
                self._values["header_list"] = header_list
            if quote_symbol is not None:
                self._values["quote_symbol"] = quote_symbol

        @builtins.property
        def charset(self) -> typing.Optional[builtins.str]:
            '''The character set in which the source CSV file is written.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-csvformatdescriptor.html#cfn-lookoutmetrics-anomalydetector-csvformatdescriptor-charset
            '''
            result = self._values.get("charset")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def contains_header(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether or not the source CSV file contains a header.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-csvformatdescriptor.html#cfn-lookoutmetrics-anomalydetector-csvformatdescriptor-containsheader
            '''
            result = self._values.get("contains_header")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def delimiter(self) -> typing.Optional[builtins.str]:
            '''The character used to delimit the source CSV file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-csvformatdescriptor.html#cfn-lookoutmetrics-anomalydetector-csvformatdescriptor-delimiter
            '''
            result = self._values.get("delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_compression(self) -> typing.Optional[builtins.str]:
            '''The level of compression of the source CSV file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-csvformatdescriptor.html#cfn-lookoutmetrics-anomalydetector-csvformatdescriptor-filecompression
            '''
            result = self._values.get("file_compression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def header_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of the source CSV file's headers, if any.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-csvformatdescriptor.html#cfn-lookoutmetrics-anomalydetector-csvformatdescriptor-headerlist
            '''
            result = self._values.get("header_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def quote_symbol(self) -> typing.Optional[builtins.str]:
            '''The character used as a quote character.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-csvformatdescriptor.html#cfn-lookoutmetrics-anomalydetector-csvformatdescriptor-quotesymbol
            '''
            result = self._values.get("quote_symbol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CsvFormatDescriptorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin.FileFormatDescriptorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "csv_format_descriptor": "csvFormatDescriptor",
            "json_format_descriptor": "jsonFormatDescriptor",
        },
    )
    class FileFormatDescriptorProperty:
        def __init__(
            self,
            *,
            csv_format_descriptor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.CsvFormatDescriptorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            json_format_descriptor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.JsonFormatDescriptorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about a source file's formatting.

            :param csv_format_descriptor: Contains information about how a source CSV data file should be analyzed.
            :param json_format_descriptor: Contains information about how a source JSON data file should be analyzed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-fileformatdescriptor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                file_format_descriptor_property = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.FileFormatDescriptorProperty(
                    csv_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.CsvFormatDescriptorProperty(
                        charset="charset",
                        contains_header=False,
                        delimiter="delimiter",
                        file_compression="fileCompression",
                        header_list=["headerList"],
                        quote_symbol="quoteSymbol"
                    ),
                    json_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.JsonFormatDescriptorProperty(
                        charset="charset",
                        file_compression="fileCompression"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d6e3e8375d444883e8bf75256044c75588c4727563384e5f079e465356785d16)
                check_type(argname="argument csv_format_descriptor", value=csv_format_descriptor, expected_type=type_hints["csv_format_descriptor"])
                check_type(argname="argument json_format_descriptor", value=json_format_descriptor, expected_type=type_hints["json_format_descriptor"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if csv_format_descriptor is not None:
                self._values["csv_format_descriptor"] = csv_format_descriptor
            if json_format_descriptor is not None:
                self._values["json_format_descriptor"] = json_format_descriptor

        @builtins.property
        def csv_format_descriptor(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.CsvFormatDescriptorProperty"]]:
            '''Contains information about how a source CSV data file should be analyzed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-fileformatdescriptor.html#cfn-lookoutmetrics-anomalydetector-fileformatdescriptor-csvformatdescriptor
            '''
            result = self._values.get("csv_format_descriptor")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.CsvFormatDescriptorProperty"]], result)

        @builtins.property
        def json_format_descriptor(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.JsonFormatDescriptorProperty"]]:
            '''Contains information about how a source JSON data file should be analyzed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-fileformatdescriptor.html#cfn-lookoutmetrics-anomalydetector-fileformatdescriptor-jsonformatdescriptor
            '''
            result = self._values.get("json_format_descriptor")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.JsonFormatDescriptorProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FileFormatDescriptorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin.JsonFormatDescriptorProperty",
        jsii_struct_bases=[],
        name_mapping={"charset": "charset", "file_compression": "fileCompression"},
    )
    class JsonFormatDescriptorProperty:
        def __init__(
            self,
            *,
            charset: typing.Optional[builtins.str] = None,
            file_compression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about how a source JSON data file should be analyzed.

            :param charset: The character set in which the source JSON file is written.
            :param file_compression: The level of compression of the source CSV file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-jsonformatdescriptor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                json_format_descriptor_property = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.JsonFormatDescriptorProperty(
                    charset="charset",
                    file_compression="fileCompression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__922bbb2ebb96f83cd0b8e623b4546cd9cc92183e5acc6ea93233e4d7c09b2d0c)
                check_type(argname="argument charset", value=charset, expected_type=type_hints["charset"])
                check_type(argname="argument file_compression", value=file_compression, expected_type=type_hints["file_compression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if charset is not None:
                self._values["charset"] = charset
            if file_compression is not None:
                self._values["file_compression"] = file_compression

        @builtins.property
        def charset(self) -> typing.Optional[builtins.str]:
            '''The character set in which the source JSON file is written.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-jsonformatdescriptor.html#cfn-lookoutmetrics-anomalydetector-jsonformatdescriptor-charset
            '''
            result = self._values.get("charset")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_compression(self) -> typing.Optional[builtins.str]:
            '''The level of compression of the source CSV file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-jsonformatdescriptor.html#cfn-lookoutmetrics-anomalydetector-jsonformatdescriptor-filecompression
            '''
            result = self._values.get("file_compression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JsonFormatDescriptorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin.MetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregation_function": "aggregationFunction",
            "metric_name": "metricName",
            "namespace": "namespace",
        },
    )
    class MetricProperty:
        def __init__(
            self,
            *,
            aggregation_function: typing.Optional[builtins.str] = None,
            metric_name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A calculation made by contrasting a measure and a dimension from your source data.

            :param aggregation_function: The function with which the metric is calculated.
            :param metric_name: The name of the metric.
            :param namespace: The namespace for the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                metric_property = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.MetricProperty(
                    aggregation_function="aggregationFunction",
                    metric_name="metricName",
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__078afd278ae74ef78c1803a81bd5398f24af9fb0c95f588e9d74cf29d985756e)
                check_type(argname="argument aggregation_function", value=aggregation_function, expected_type=type_hints["aggregation_function"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aggregation_function is not None:
                self._values["aggregation_function"] = aggregation_function
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def aggregation_function(self) -> typing.Optional[builtins.str]:
            '''The function with which the metric is calculated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metric.html#cfn-lookoutmetrics-anomalydetector-metric-aggregationfunction
            '''
            result = self._values.get("aggregation_function")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metric.html#cfn-lookoutmetrics-anomalydetector-metric-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace for the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metric.html#cfn-lookoutmetrics-anomalydetector-metric-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin.MetricSetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimension_list": "dimensionList",
            "metric_list": "metricList",
            "metric_set_description": "metricSetDescription",
            "metric_set_frequency": "metricSetFrequency",
            "metric_set_name": "metricSetName",
            "metric_source": "metricSource",
            "offset": "offset",
            "timestamp_column": "timestampColumn",
            "timezone": "timezone",
        },
    )
    class MetricSetProperty:
        def __init__(
            self,
            *,
            dimension_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            metric_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.MetricProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metric_set_description: typing.Optional[builtins.str] = None,
            metric_set_frequency: typing.Optional[builtins.str] = None,
            metric_set_name: typing.Optional[builtins.str] = None,
            metric_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.MetricSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            offset: typing.Optional[jsii.Number] = None,
            timestamp_column: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.TimestampColumnProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timezone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a dataset.

            :param dimension_list: A list of the fields you want to treat as dimensions.
            :param metric_list: A list of metrics that the dataset will contain.
            :param metric_set_description: A description of the dataset you are creating.
            :param metric_set_frequency: The frequency with which the source data will be analyzed for anomalies.
            :param metric_set_name: The name of the dataset.
            :param metric_source: Contains information about how the source data should be interpreted.
            :param offset: After an interval ends, the amount of seconds that the detector waits before importing data. Offset is only supported for S3, Redshift, Athena and datasources.
            :param timestamp_column: Contains information about the column used for tracking time in your source data.
            :param timezone: The time zone in which your source data was recorded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                metric_set_property = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.MetricSetProperty(
                    dimension_list=["dimensionList"],
                    metric_list=[lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.MetricProperty(
                        aggregation_function="aggregationFunction",
                        metric_name="metricName",
                        namespace="namespace"
                    )],
                    metric_set_description="metricSetDescription",
                    metric_set_frequency="metricSetFrequency",
                    metric_set_name="metricSetName",
                    metric_source=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.MetricSourceProperty(
                        app_flow_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.AppFlowConfigProperty(
                            flow_name="flowName",
                            role_arn="roleArn"
                        ),
                        cloudwatch_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.CloudwatchConfigProperty(
                            role_arn="roleArn"
                        ),
                        rds_source_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.RDSSourceConfigProperty(
                            database_host="databaseHost",
                            database_name="databaseName",
                            database_port=123,
                            db_instance_identifier="dbInstanceIdentifier",
                            role_arn="roleArn",
                            secret_manager_arn="secretManagerArn",
                            table_name="tableName",
                            vpc_configuration=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty(
                                security_group_id_list=["securityGroupIdList"],
                                subnet_id_list=["subnetIdList"]
                            )
                        ),
                        redshift_source_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.RedshiftSourceConfigProperty(
                            cluster_identifier="clusterIdentifier",
                            database_host="databaseHost",
                            database_name="databaseName",
                            database_port=123,
                            role_arn="roleArn",
                            secret_manager_arn="secretManagerArn",
                            table_name="tableName",
                            vpc_configuration=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty(
                                security_group_id_list=["securityGroupIdList"],
                                subnet_id_list=["subnetIdList"]
                            )
                        ),
                        s3_source_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.S3SourceConfigProperty(
                            file_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.FileFormatDescriptorProperty(
                                csv_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.CsvFormatDescriptorProperty(
                                    charset="charset",
                                    contains_header=False,
                                    delimiter="delimiter",
                                    file_compression="fileCompression",
                                    header_list=["headerList"],
                                    quote_symbol="quoteSymbol"
                                ),
                                json_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.JsonFormatDescriptorProperty(
                                    charset="charset",
                                    file_compression="fileCompression"
                                )
                            ),
                            historical_data_path_list=["historicalDataPathList"],
                            role_arn="roleArn",
                            templated_path_list=["templatedPathList"]
                        )
                    ),
                    offset=123,
                    timestamp_column=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.TimestampColumnProperty(
                        column_format="columnFormat",
                        column_name="columnName"
                    ),
                    timezone="timezone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a93a27c157fc9195f9e8d00778e1a93c5375f42c2902c42149cfe43006ead030)
                check_type(argname="argument dimension_list", value=dimension_list, expected_type=type_hints["dimension_list"])
                check_type(argname="argument metric_list", value=metric_list, expected_type=type_hints["metric_list"])
                check_type(argname="argument metric_set_description", value=metric_set_description, expected_type=type_hints["metric_set_description"])
                check_type(argname="argument metric_set_frequency", value=metric_set_frequency, expected_type=type_hints["metric_set_frequency"])
                check_type(argname="argument metric_set_name", value=metric_set_name, expected_type=type_hints["metric_set_name"])
                check_type(argname="argument metric_source", value=metric_source, expected_type=type_hints["metric_source"])
                check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
                check_type(argname="argument timestamp_column", value=timestamp_column, expected_type=type_hints["timestamp_column"])
                check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_list is not None:
                self._values["dimension_list"] = dimension_list
            if metric_list is not None:
                self._values["metric_list"] = metric_list
            if metric_set_description is not None:
                self._values["metric_set_description"] = metric_set_description
            if metric_set_frequency is not None:
                self._values["metric_set_frequency"] = metric_set_frequency
            if metric_set_name is not None:
                self._values["metric_set_name"] = metric_set_name
            if metric_source is not None:
                self._values["metric_source"] = metric_source
            if offset is not None:
                self._values["offset"] = offset
            if timestamp_column is not None:
                self._values["timestamp_column"] = timestamp_column
            if timezone is not None:
                self._values["timezone"] = timezone

        @builtins.property
        def dimension_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of the fields you want to treat as dimensions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricset.html#cfn-lookoutmetrics-anomalydetector-metricset-dimensionlist
            '''
            result = self._values.get("dimension_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def metric_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricProperty"]]]]:
            '''A list of metrics that the dataset will contain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricset.html#cfn-lookoutmetrics-anomalydetector-metricset-metriclist
            '''
            result = self._values.get("metric_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricProperty"]]]], result)

        @builtins.property
        def metric_set_description(self) -> typing.Optional[builtins.str]:
            '''A description of the dataset you are creating.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricset.html#cfn-lookoutmetrics-anomalydetector-metricset-metricsetdescription
            '''
            result = self._values.get("metric_set_description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_set_frequency(self) -> typing.Optional[builtins.str]:
            '''The frequency with which the source data will be analyzed for anomalies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricset.html#cfn-lookoutmetrics-anomalydetector-metricset-metricsetfrequency
            '''
            result = self._values.get("metric_set_frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_set_name(self) -> typing.Optional[builtins.str]:
            '''The name of the dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricset.html#cfn-lookoutmetrics-anomalydetector-metricset-metricsetname
            '''
            result = self._values.get("metric_set_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricSourceProperty"]]:
            '''Contains information about how the source data should be interpreted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricset.html#cfn-lookoutmetrics-anomalydetector-metricset-metricsource
            '''
            result = self._values.get("metric_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MetricSourceProperty"]], result)

        @builtins.property
        def offset(self) -> typing.Optional[jsii.Number]:
            '''After an interval ends, the amount of seconds that the detector waits before importing data.

            Offset is only supported for S3, Redshift, Athena and datasources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricset.html#cfn-lookoutmetrics-anomalydetector-metricset-offset
            '''
            result = self._values.get("offset")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timestamp_column(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.TimestampColumnProperty"]]:
            '''Contains information about the column used for tracking time in your source data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricset.html#cfn-lookoutmetrics-anomalydetector-metricset-timestampcolumn
            '''
            result = self._values.get("timestamp_column")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.TimestampColumnProperty"]], result)

        @builtins.property
        def timezone(self) -> typing.Optional[builtins.str]:
            '''The time zone in which your source data was recorded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricset.html#cfn-lookoutmetrics-anomalydetector-metricset-timezone
            '''
            result = self._values.get("timezone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin.MetricSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "app_flow_config": "appFlowConfig",
            "cloudwatch_config": "cloudwatchConfig",
            "rds_source_config": "rdsSourceConfig",
            "redshift_source_config": "redshiftSourceConfig",
            "s3_source_config": "s3SourceConfig",
        },
    )
    class MetricSourceProperty:
        def __init__(
            self,
            *,
            app_flow_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.AppFlowConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cloudwatch_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.CloudwatchConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rds_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.RDSSourceConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            redshift_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.RedshiftSourceConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.S3SourceConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about how the source data should be interpreted.

            :param app_flow_config: Details about an AppFlow datasource.
            :param cloudwatch_config: Details about an Amazon CloudWatch monitoring datasource.
            :param rds_source_config: Details about an Amazon Relational Database Service (RDS) datasource.
            :param redshift_source_config: Details about an Amazon Redshift database datasource.
            :param s3_source_config: Contains information about the configuration of the S3 bucket that contains source files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                metric_source_property = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.MetricSourceProperty(
                    app_flow_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.AppFlowConfigProperty(
                        flow_name="flowName",
                        role_arn="roleArn"
                    ),
                    cloudwatch_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.CloudwatchConfigProperty(
                        role_arn="roleArn"
                    ),
                    rds_source_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.RDSSourceConfigProperty(
                        database_host="databaseHost",
                        database_name="databaseName",
                        database_port=123,
                        db_instance_identifier="dbInstanceIdentifier",
                        role_arn="roleArn",
                        secret_manager_arn="secretManagerArn",
                        table_name="tableName",
                        vpc_configuration=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty(
                            security_group_id_list=["securityGroupIdList"],
                            subnet_id_list=["subnetIdList"]
                        )
                    ),
                    redshift_source_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.RedshiftSourceConfigProperty(
                        cluster_identifier="clusterIdentifier",
                        database_host="databaseHost",
                        database_name="databaseName",
                        database_port=123,
                        role_arn="roleArn",
                        secret_manager_arn="secretManagerArn",
                        table_name="tableName",
                        vpc_configuration=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty(
                            security_group_id_list=["securityGroupIdList"],
                            subnet_id_list=["subnetIdList"]
                        )
                    ),
                    s3_source_config=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.S3SourceConfigProperty(
                        file_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.FileFormatDescriptorProperty(
                            csv_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.CsvFormatDescriptorProperty(
                                charset="charset",
                                contains_header=False,
                                delimiter="delimiter",
                                file_compression="fileCompression",
                                header_list=["headerList"],
                                quote_symbol="quoteSymbol"
                            ),
                            json_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.JsonFormatDescriptorProperty(
                                charset="charset",
                                file_compression="fileCompression"
                            )
                        ),
                        historical_data_path_list=["historicalDataPathList"],
                        role_arn="roleArn",
                        templated_path_list=["templatedPathList"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f91866b3a21b411bfde8f004b17752ee888143e42d78fb2793661ee4c14f448)
                check_type(argname="argument app_flow_config", value=app_flow_config, expected_type=type_hints["app_flow_config"])
                check_type(argname="argument cloudwatch_config", value=cloudwatch_config, expected_type=type_hints["cloudwatch_config"])
                check_type(argname="argument rds_source_config", value=rds_source_config, expected_type=type_hints["rds_source_config"])
                check_type(argname="argument redshift_source_config", value=redshift_source_config, expected_type=type_hints["redshift_source_config"])
                check_type(argname="argument s3_source_config", value=s3_source_config, expected_type=type_hints["s3_source_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_flow_config is not None:
                self._values["app_flow_config"] = app_flow_config
            if cloudwatch_config is not None:
                self._values["cloudwatch_config"] = cloudwatch_config
            if rds_source_config is not None:
                self._values["rds_source_config"] = rds_source_config
            if redshift_source_config is not None:
                self._values["redshift_source_config"] = redshift_source_config
            if s3_source_config is not None:
                self._values["s3_source_config"] = s3_source_config

        @builtins.property
        def app_flow_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.AppFlowConfigProperty"]]:
            '''Details about an AppFlow datasource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricsource.html#cfn-lookoutmetrics-anomalydetector-metricsource-appflowconfig
            '''
            result = self._values.get("app_flow_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.AppFlowConfigProperty"]], result)

        @builtins.property
        def cloudwatch_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.CloudwatchConfigProperty"]]:
            '''Details about an Amazon CloudWatch monitoring datasource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricsource.html#cfn-lookoutmetrics-anomalydetector-metricsource-cloudwatchconfig
            '''
            result = self._values.get("cloudwatch_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.CloudwatchConfigProperty"]], result)

        @builtins.property
        def rds_source_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.RDSSourceConfigProperty"]]:
            '''Details about an Amazon Relational Database Service (RDS) datasource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricsource.html#cfn-lookoutmetrics-anomalydetector-metricsource-rdssourceconfig
            '''
            result = self._values.get("rds_source_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.RDSSourceConfigProperty"]], result)

        @builtins.property
        def redshift_source_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.RedshiftSourceConfigProperty"]]:
            '''Details about an Amazon Redshift database datasource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricsource.html#cfn-lookoutmetrics-anomalydetector-metricsource-redshiftsourceconfig
            '''
            result = self._values.get("redshift_source_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.RedshiftSourceConfigProperty"]], result)

        @builtins.property
        def s3_source_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.S3SourceConfigProperty"]]:
            '''Contains information about the configuration of the S3 bucket that contains source files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-metricsource.html#cfn-lookoutmetrics-anomalydetector-metricsource-s3sourceconfig
            '''
            result = self._values.get("s3_source_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.S3SourceConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin.RDSSourceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_host": "databaseHost",
            "database_name": "databaseName",
            "database_port": "databasePort",
            "db_instance_identifier": "dbInstanceIdentifier",
            "role_arn": "roleArn",
            "secret_manager_arn": "secretManagerArn",
            "table_name": "tableName",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class RDSSourceConfigProperty:
        def __init__(
            self,
            *,
            database_host: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            database_port: typing.Optional[jsii.Number] = None,
            db_instance_identifier: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            secret_manager_arn: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
            vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about the Amazon Relational Database Service (RDS) configuration.

            :param database_host: The host name of the database.
            :param database_name: The name of the RDS database.
            :param database_port: The port number where the database can be accessed.
            :param db_instance_identifier: A string identifying the database instance.
            :param role_arn: The Amazon Resource Name (ARN) of the role.
            :param secret_manager_arn: The Amazon Resource Name (ARN) of the AWS Secrets Manager role.
            :param table_name: The name of the table in the database.
            :param vpc_configuration: An object containing information about the Amazon Virtual Private Cloud (VPC) configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-rdssourceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                r_dSSource_config_property = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.RDSSourceConfigProperty(
                    database_host="databaseHost",
                    database_name="databaseName",
                    database_port=123,
                    db_instance_identifier="dbInstanceIdentifier",
                    role_arn="roleArn",
                    secret_manager_arn="secretManagerArn",
                    table_name="tableName",
                    vpc_configuration=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty(
                        security_group_id_list=["securityGroupIdList"],
                        subnet_id_list=["subnetIdList"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1accb65da1c597e97d1a93a9f668148e2e3430fa434c184f368d9779353c6870)
                check_type(argname="argument database_host", value=database_host, expected_type=type_hints["database_host"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument database_port", value=database_port, expected_type=type_hints["database_port"])
                check_type(argname="argument db_instance_identifier", value=db_instance_identifier, expected_type=type_hints["db_instance_identifier"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument secret_manager_arn", value=secret_manager_arn, expected_type=type_hints["secret_manager_arn"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_host is not None:
                self._values["database_host"] = database_host
            if database_name is not None:
                self._values["database_name"] = database_name
            if database_port is not None:
                self._values["database_port"] = database_port
            if db_instance_identifier is not None:
                self._values["db_instance_identifier"] = db_instance_identifier
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if secret_manager_arn is not None:
                self._values["secret_manager_arn"] = secret_manager_arn
            if table_name is not None:
                self._values["table_name"] = table_name
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def database_host(self) -> typing.Optional[builtins.str]:
            '''The host name of the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-rdssourceconfig.html#cfn-lookoutmetrics-anomalydetector-rdssourceconfig-databasehost
            '''
            result = self._values.get("database_host")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the RDS database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-rdssourceconfig.html#cfn-lookoutmetrics-anomalydetector-rdssourceconfig-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_port(self) -> typing.Optional[jsii.Number]:
            '''The port number where the database can be accessed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-rdssourceconfig.html#cfn-lookoutmetrics-anomalydetector-rdssourceconfig-databaseport
            '''
            result = self._values.get("database_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def db_instance_identifier(self) -> typing.Optional[builtins.str]:
            '''A string identifying the database instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-rdssourceconfig.html#cfn-lookoutmetrics-anomalydetector-rdssourceconfig-dbinstanceidentifier
            '''
            result = self._values.get("db_instance_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-rdssourceconfig.html#cfn-lookoutmetrics-anomalydetector-rdssourceconfig-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_manager_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS Secrets Manager role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-rdssourceconfig.html#cfn-lookoutmetrics-anomalydetector-rdssourceconfig-secretmanagerarn
            '''
            result = self._values.get("secret_manager_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the table in the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-rdssourceconfig.html#cfn-lookoutmetrics-anomalydetector-rdssourceconfig-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty"]]:
            '''An object containing information about the Amazon Virtual Private Cloud (VPC) configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-rdssourceconfig.html#cfn-lookoutmetrics-anomalydetector-rdssourceconfig-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RDSSourceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin.RedshiftSourceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cluster_identifier": "clusterIdentifier",
            "database_host": "databaseHost",
            "database_name": "databaseName",
            "database_port": "databasePort",
            "role_arn": "roleArn",
            "secret_manager_arn": "secretManagerArn",
            "table_name": "tableName",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class RedshiftSourceConfigProperty:
        def __init__(
            self,
            *,
            cluster_identifier: typing.Optional[builtins.str] = None,
            database_host: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            database_port: typing.Optional[jsii.Number] = None,
            role_arn: typing.Optional[builtins.str] = None,
            secret_manager_arn: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
            vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides information about the Amazon Redshift database configuration.

            :param cluster_identifier: A string identifying the Redshift cluster.
            :param database_host: The name of the database host.
            :param database_name: The Redshift database name.
            :param database_port: The port number where the database can be accessed.
            :param role_arn: The Amazon Resource Name (ARN) of the role providing access to the database.
            :param secret_manager_arn: The Amazon Resource Name (ARN) of the AWS Secrets Manager role.
            :param table_name: The table name of the Redshift database.
            :param vpc_configuration: Contains information about the Amazon Virtual Private Cloud (VPC) configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-redshiftsourceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                redshift_source_config_property = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.RedshiftSourceConfigProperty(
                    cluster_identifier="clusterIdentifier",
                    database_host="databaseHost",
                    database_name="databaseName",
                    database_port=123,
                    role_arn="roleArn",
                    secret_manager_arn="secretManagerArn",
                    table_name="tableName",
                    vpc_configuration=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty(
                        security_group_id_list=["securityGroupIdList"],
                        subnet_id_list=["subnetIdList"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__437afd5dbb3158bd52a3cb2f774f1be94abb6a8466c527595a344eb151c6d425)
                check_type(argname="argument cluster_identifier", value=cluster_identifier, expected_type=type_hints["cluster_identifier"])
                check_type(argname="argument database_host", value=database_host, expected_type=type_hints["database_host"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument database_port", value=database_port, expected_type=type_hints["database_port"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument secret_manager_arn", value=secret_manager_arn, expected_type=type_hints["secret_manager_arn"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cluster_identifier is not None:
                self._values["cluster_identifier"] = cluster_identifier
            if database_host is not None:
                self._values["database_host"] = database_host
            if database_name is not None:
                self._values["database_name"] = database_name
            if database_port is not None:
                self._values["database_port"] = database_port
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if secret_manager_arn is not None:
                self._values["secret_manager_arn"] = secret_manager_arn
            if table_name is not None:
                self._values["table_name"] = table_name
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def cluster_identifier(self) -> typing.Optional[builtins.str]:
            '''A string identifying the Redshift cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-redshiftsourceconfig.html#cfn-lookoutmetrics-anomalydetector-redshiftsourceconfig-clusteridentifier
            '''
            result = self._values.get("cluster_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_host(self) -> typing.Optional[builtins.str]:
            '''The name of the database host.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-redshiftsourceconfig.html#cfn-lookoutmetrics-anomalydetector-redshiftsourceconfig-databasehost
            '''
            result = self._values.get("database_host")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The Redshift database name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-redshiftsourceconfig.html#cfn-lookoutmetrics-anomalydetector-redshiftsourceconfig-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_port(self) -> typing.Optional[jsii.Number]:
            '''The port number where the database can be accessed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-redshiftsourceconfig.html#cfn-lookoutmetrics-anomalydetector-redshiftsourceconfig-databaseport
            '''
            result = self._values.get("database_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the role providing access to the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-redshiftsourceconfig.html#cfn-lookoutmetrics-anomalydetector-redshiftsourceconfig-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_manager_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS Secrets Manager role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-redshiftsourceconfig.html#cfn-lookoutmetrics-anomalydetector-redshiftsourceconfig-secretmanagerarn
            '''
            result = self._values.get("secret_manager_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The table name of the Redshift database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-redshiftsourceconfig.html#cfn-lookoutmetrics-anomalydetector-redshiftsourceconfig-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty"]]:
            '''Contains information about the Amazon Virtual Private Cloud (VPC) configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-redshiftsourceconfig.html#cfn-lookoutmetrics-anomalydetector-redshiftsourceconfig-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftSourceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin.S3SourceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "file_format_descriptor": "fileFormatDescriptor",
            "historical_data_path_list": "historicalDataPathList",
            "role_arn": "roleArn",
            "templated_path_list": "templatedPathList",
        },
    )
    class S3SourceConfigProperty:
        def __init__(
            self,
            *,
            file_format_descriptor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.FileFormatDescriptorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            historical_data_path_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            templated_path_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Contains information about the configuration of the S3 bucket that contains source files.

            :param file_format_descriptor: Contains information about a source file's formatting.
            :param historical_data_path_list: A list of paths to the historical data files.
            :param role_arn: The ARN of an IAM role that has read and write access permissions to the source S3 bucket.
            :param templated_path_list: A list of templated paths to the source files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-s3sourceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                s3_source_config_property = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.S3SourceConfigProperty(
                    file_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.FileFormatDescriptorProperty(
                        csv_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.CsvFormatDescriptorProperty(
                            charset="charset",
                            contains_header=False,
                            delimiter="delimiter",
                            file_compression="fileCompression",
                            header_list=["headerList"],
                            quote_symbol="quoteSymbol"
                        ),
                        json_format_descriptor=lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.JsonFormatDescriptorProperty(
                            charset="charset",
                            file_compression="fileCompression"
                        )
                    ),
                    historical_data_path_list=["historicalDataPathList"],
                    role_arn="roleArn",
                    templated_path_list=["templatedPathList"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d0dba596b4fc6ecd7abd24fdb56cc16c28c1a0bd9511b0a02678dded2b78921)
                check_type(argname="argument file_format_descriptor", value=file_format_descriptor, expected_type=type_hints["file_format_descriptor"])
                check_type(argname="argument historical_data_path_list", value=historical_data_path_list, expected_type=type_hints["historical_data_path_list"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument templated_path_list", value=templated_path_list, expected_type=type_hints["templated_path_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file_format_descriptor is not None:
                self._values["file_format_descriptor"] = file_format_descriptor
            if historical_data_path_list is not None:
                self._values["historical_data_path_list"] = historical_data_path_list
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if templated_path_list is not None:
                self._values["templated_path_list"] = templated_path_list

        @builtins.property
        def file_format_descriptor(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.FileFormatDescriptorProperty"]]:
            '''Contains information about a source file's formatting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-s3sourceconfig.html#cfn-lookoutmetrics-anomalydetector-s3sourceconfig-fileformatdescriptor
            '''
            result = self._values.get("file_format_descriptor")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.FileFormatDescriptorProperty"]], result)

        @builtins.property
        def historical_data_path_list(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of paths to the historical data files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-s3sourceconfig.html#cfn-lookoutmetrics-anomalydetector-s3sourceconfig-historicaldatapathlist
            '''
            result = self._values.get("historical_data_path_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of an IAM role that has read and write access permissions to the source S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-s3sourceconfig.html#cfn-lookoutmetrics-anomalydetector-s3sourceconfig-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def templated_path_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of templated paths to the source files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-s3sourceconfig.html#cfn-lookoutmetrics-anomalydetector-s3sourceconfig-templatedpathlist
            '''
            result = self._values.get("templated_path_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3SourceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin.TimestampColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"column_format": "columnFormat", "column_name": "columnName"},
    )
    class TimestampColumnProperty:
        def __init__(
            self,
            *,
            column_format: typing.Optional[builtins.str] = None,
            column_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the column used to track time in a source data file.

            :param column_format: The format of the timestamp column.
            :param column_name: The name of the timestamp column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-timestampcolumn.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                timestamp_column_property = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.TimestampColumnProperty(
                    column_format="columnFormat",
                    column_name="columnName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86ac27bb698f7e4dea93f8e9c76ce0184b91add808157495d7eeb8ee35de9e81)
                check_type(argname="argument column_format", value=column_format, expected_type=type_hints["column_format"])
                check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if column_format is not None:
                self._values["column_format"] = column_format
            if column_name is not None:
                self._values["column_name"] = column_name

        @builtins.property
        def column_format(self) -> typing.Optional[builtins.str]:
            '''The format of the timestamp column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-timestampcolumn.html#cfn-lookoutmetrics-anomalydetector-timestampcolumn-columnformat
            '''
            result = self._values.get("column_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def column_name(self) -> typing.Optional[builtins.str]:
            '''The name of the timestamp column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-timestampcolumn.html#cfn-lookoutmetrics-anomalydetector-timestampcolumn-columnname
            '''
            result = self._values.get("column_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimestampColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lookoutmetrics.mixins.CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_id_list": "securityGroupIdList",
            "subnet_id_list": "subnetIdList",
        },
    )
    class VpcConfigurationProperty:
        def __init__(
            self,
            *,
            security_group_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Contains configuration information about the Amazon Virtual Private Cloud (VPC).

            :param security_group_id_list: An array of strings containing the list of security groups.
            :param subnet_id_list: An array of strings containing the Amazon VPC subnet IDs (e.g., ``subnet-0bb1c79de3EXAMPLE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-vpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lookoutmetrics import mixins as lookoutmetrics_mixins
                
                vpc_configuration_property = lookoutmetrics_mixins.CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty(
                    security_group_id_list=["securityGroupIdList"],
                    subnet_id_list=["subnetIdList"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__214d296d244c19e53531eac02f18a23f744bff6c84d5b2b7f29b97163942a805)
                check_type(argname="argument security_group_id_list", value=security_group_id_list, expected_type=type_hints["security_group_id_list"])
                check_type(argname="argument subnet_id_list", value=subnet_id_list, expected_type=type_hints["subnet_id_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_id_list is not None:
                self._values["security_group_id_list"] = security_group_id_list
            if subnet_id_list is not None:
                self._values["subnet_id_list"] = subnet_id_list

        @builtins.property
        def security_group_id_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of strings containing the list of security groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-vpcconfiguration.html#cfn-lookoutmetrics-anomalydetector-vpcconfiguration-securitygroupidlist
            '''
            result = self._values.get("security_group_id_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_id_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of strings containing the Amazon VPC subnet IDs (e.g., ``subnet-0bb1c79de3EXAMPLE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lookoutmetrics-anomalydetector-vpcconfiguration.html#cfn-lookoutmetrics-anomalydetector-vpcconfiguration-subnetidlist
            '''
            result = self._values.get("subnet_id_list")
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
    "CfnAlertMixinProps",
    "CfnAlertPropsMixin",
    "CfnAnomalyDetectorMixinProps",
    "CfnAnomalyDetectorPropsMixin",
]

publication.publish()

def _typecheckingstub__edbdcffb7fe85456e2f8abe868741c96a8ccd0153b24b763c39a33ad67d012ad(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlertPropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    alert_description: typing.Optional[builtins.str] = None,
    alert_name: typing.Optional[builtins.str] = None,
    alert_sensitivity_threshold: typing.Optional[jsii.Number] = None,
    anomaly_detector_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8651fb2567d4f12977bccc77f0845b1a357caa04b6a1cd3cfcd83394abcb4f07(
    props: typing.Union[CfnAlertMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46057b3a8a71576e7a1d3d7f5ee8a4837824c8711d98ea2bf622db737b34b47(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e7bd8a7a764d69b9a4cfa5cab138807e800e26f13b53686441176bdde73a00(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d6dce2bb5a9b5c9fb56d143b6eb61df22a9b61103b9bdb7c6497434a1225ee(
    *,
    lambda_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlertPropsMixin.LambdaConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sns_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlertPropsMixin.SNSConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e90f8c711796020c1af0531107b632f2f7311f2b750d420afc94518135b6d29(
    *,
    lambda_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657e5b904dc57ba92a1c341f8b94e67029700bde06348d9a69ccfce4930680a9(
    *,
    role_arn: typing.Optional[builtins.str] = None,
    sns_topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d983a98e37150e171c3f6a8fdc8eba05ae44452d404aceba860b76fd99763f9b(
    *,
    anomaly_detector_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    anomaly_detector_description: typing.Optional[builtins.str] = None,
    anomaly_detector_name: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    metric_set_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.MetricSetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcfa271764f08da770e42422ebc0941b88f557ffdb27b9eaf49e2d6e31f35213(
    props: typing.Union[CfnAnomalyDetectorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6f574ebc990af29991007e185c2c5ba27f557763962da03dce7b8c066faffe(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad28285c20234e0191d64922a82bae5e9bedecb23ef4638bc06d31196477190(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92784fc52036d5f01764761a226286bf326a15c4b8b17518dbce6f74ac844371(
    *,
    anomaly_detector_frequency: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6448b22ba72a4436614ef3849c05cb051f7abe6c1a23a10f209248f9a66510(
    *,
    flow_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e5d72a0db2af5889423d074e7569749ddf99aa15050a6dc7e83c32bd2cd773(
    *,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6781179588be616a33d0c894d22b9ba20c333dac0ce2e2a7cb7f5f3748d7f1bb(
    *,
    charset: typing.Optional[builtins.str] = None,
    contains_header: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    delimiter: typing.Optional[builtins.str] = None,
    file_compression: typing.Optional[builtins.str] = None,
    header_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    quote_symbol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e3e8375d444883e8bf75256044c75588c4727563384e5f079e465356785d16(
    *,
    csv_format_descriptor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.CsvFormatDescriptorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    json_format_descriptor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.JsonFormatDescriptorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922bbb2ebb96f83cd0b8e623b4546cd9cc92183e5acc6ea93233e4d7c09b2d0c(
    *,
    charset: typing.Optional[builtins.str] = None,
    file_compression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078afd278ae74ef78c1803a81bd5398f24af9fb0c95f588e9d74cf29d985756e(
    *,
    aggregation_function: typing.Optional[builtins.str] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93a27c157fc9195f9e8d00778e1a93c5375f42c2902c42149cfe43006ead030(
    *,
    dimension_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    metric_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.MetricProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_set_description: typing.Optional[builtins.str] = None,
    metric_set_frequency: typing.Optional[builtins.str] = None,
    metric_set_name: typing.Optional[builtins.str] = None,
    metric_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.MetricSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    offset: typing.Optional[jsii.Number] = None,
    timestamp_column: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.TimestampColumnProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f91866b3a21b411bfde8f004b17752ee888143e42d78fb2793661ee4c14f448(
    *,
    app_flow_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.AppFlowConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cloudwatch_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.CloudwatchConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rds_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.RDSSourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    redshift_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.RedshiftSourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.S3SourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1accb65da1c597e97d1a93a9f668148e2e3430fa434c184f368d9779353c6870(
    *,
    database_host: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    database_port: typing.Optional[jsii.Number] = None,
    db_instance_identifier: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    secret_manager_arn: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437afd5dbb3158bd52a3cb2f774f1be94abb6a8466c527595a344eb151c6d425(
    *,
    cluster_identifier: typing.Optional[builtins.str] = None,
    database_host: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    database_port: typing.Optional[jsii.Number] = None,
    role_arn: typing.Optional[builtins.str] = None,
    secret_manager_arn: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0dba596b4fc6ecd7abd24fdb56cc16c28c1a0bd9511b0a02678dded2b78921(
    *,
    file_format_descriptor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.FileFormatDescriptorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    historical_data_path_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    templated_path_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ac27bb698f7e4dea93f8e9c76ce0184b91add808157495d7eeb8ee35de9e81(
    *,
    column_format: typing.Optional[builtins.str] = None,
    column_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214d296d244c19e53531eac02f18a23f744bff6c84d5b2b7f29b97163942a805(
    *,
    security_group_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
