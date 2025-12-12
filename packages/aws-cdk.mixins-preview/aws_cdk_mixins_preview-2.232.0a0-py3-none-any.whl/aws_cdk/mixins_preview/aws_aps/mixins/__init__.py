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


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnAnomalyDetectorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "configuration": "configuration",
        "evaluation_interval_in_seconds": "evaluationIntervalInSeconds",
        "labels": "labels",
        "missing_data_action": "missingDataAction",
        "tags": "tags",
        "workspace": "workspace",
    },
)
class CfnAnomalyDetectorMixinProps:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        evaluation_interval_in_seconds: typing.Optional[jsii.Number] = None,
        labels: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.LabelProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        missing_data_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.MissingDataActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        workspace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAnomalyDetectorPropsMixin.

        :param alias: The user-friendly name of the anomaly detector.
        :param configuration: The algorithm configuration of the anomaly detector.
        :param evaluation_interval_in_seconds: The frequency, in seconds, at which the anomaly detector evaluates metrics. Default: - 60
        :param labels: The Amazon Managed Service for Prometheus metric labels associated with the anomaly detector.
        :param missing_data_action: The action taken when data is missing during evaluation.
        :param tags: The tags applied to the anomaly detector.
        :param workspace: An Amazon Managed Service for Prometheus workspace is a logical and isolated Prometheus server dedicated to ingesting, storing, and querying your Prometheus-compatible metrics.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-anomalydetector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
            
            cfn_anomaly_detector_mixin_props = aps_mixins.CfnAnomalyDetectorMixinProps(
                alias="alias",
                configuration=aps_mixins.CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigurationProperty(
                    random_cut_forest=aps_mixins.CfnAnomalyDetectorPropsMixin.RandomCutForestConfigurationProperty(
                        ignore_near_expected_from_above=aps_mixins.CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty(
                            amount=123,
                            ratio=123
                        ),
                        ignore_near_expected_from_below=aps_mixins.CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty(
                            amount=123,
                            ratio=123
                        ),
                        query="query",
                        sample_size=123,
                        shingle_size=123
                    )
                ),
                evaluation_interval_in_seconds=123,
                labels=[aps_mixins.CfnAnomalyDetectorPropsMixin.LabelProperty(
                    key="key",
                    value="value"
                )],
                missing_data_action=aps_mixins.CfnAnomalyDetectorPropsMixin.MissingDataActionProperty(
                    mark_as_anomaly=False,
                    skip=False
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                workspace="workspace"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11b7deb590d0ae343e9a176943be50687a901be15d8e1d1e2e02ed523ba122d4)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument evaluation_interval_in_seconds", value=evaluation_interval_in_seconds, expected_type=type_hints["evaluation_interval_in_seconds"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument missing_data_action", value=missing_data_action, expected_type=type_hints["missing_data_action"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if configuration is not None:
            self._values["configuration"] = configuration
        if evaluation_interval_in_seconds is not None:
            self._values["evaluation_interval_in_seconds"] = evaluation_interval_in_seconds
        if labels is not None:
            self._values["labels"] = labels
        if missing_data_action is not None:
            self._values["missing_data_action"] = missing_data_action
        if tags is not None:
            self._values["tags"] = tags
        if workspace is not None:
            self._values["workspace"] = workspace

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''The user-friendly name of the anomaly detector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-anomalydetector.html#cfn-aps-anomalydetector-alias
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigurationProperty"]]:
        '''The algorithm configuration of the anomaly detector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-anomalydetector.html#cfn-aps-anomalydetector-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigurationProperty"]], result)

    @builtins.property
    def evaluation_interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The frequency, in seconds, at which the anomaly detector evaluates metrics.

        :default: - 60

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-anomalydetector.html#cfn-aps-anomalydetector-evaluationintervalinseconds
        '''
        result = self._values.get("evaluation_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.LabelProperty"]]]]:
        '''The Amazon Managed Service for Prometheus metric labels associated with the anomaly detector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-anomalydetector.html#cfn-aps-anomalydetector-labels
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.LabelProperty"]]]], result)

    @builtins.property
    def missing_data_action(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MissingDataActionProperty"]]:
        '''The action taken when data is missing during evaluation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-anomalydetector.html#cfn-aps-anomalydetector-missingdataaction
        '''
        result = self._values.get("missing_data_action")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.MissingDataActionProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags applied to the anomaly detector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-anomalydetector.html#cfn-aps-anomalydetector-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''An Amazon Managed Service for Prometheus workspace is a logical and isolated Prometheus server dedicated to ingesting, storing, and querying your Prometheus-compatible metrics.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-anomalydetector.html#cfn-aps-anomalydetector-workspace
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnAnomalyDetectorPropsMixin",
):
    '''Anomaly detection uses the Random Cut Forest algorithm for time-series analysis.

    The anomaly detector analyzes Amazon Managed Service for Prometheus metrics to identify unusual patterns and behaviors.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-anomalydetector.html
    :cloudformationResource: AWS::APS::AnomalyDetector
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
        
        cfn_anomaly_detector_props_mixin = aps_mixins.CfnAnomalyDetectorPropsMixin(aps_mixins.CfnAnomalyDetectorMixinProps(
            alias="alias",
            configuration=aps_mixins.CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigurationProperty(
                random_cut_forest=aps_mixins.CfnAnomalyDetectorPropsMixin.RandomCutForestConfigurationProperty(
                    ignore_near_expected_from_above=aps_mixins.CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty(
                        amount=123,
                        ratio=123
                    ),
                    ignore_near_expected_from_below=aps_mixins.CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty(
                        amount=123,
                        ratio=123
                    ),
                    query="query",
                    sample_size=123,
                    shingle_size=123
                )
            ),
            evaluation_interval_in_seconds=123,
            labels=[aps_mixins.CfnAnomalyDetectorPropsMixin.LabelProperty(
                key="key",
                value="value"
            )],
            missing_data_action=aps_mixins.CfnAnomalyDetectorPropsMixin.MissingDataActionProperty(
                mark_as_anomaly=False,
                skip=False
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            workspace="workspace"
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
        '''Create a mixin to apply properties to ``AWS::APS::AnomalyDetector``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8702716b1fbae2e56f44e3fe4a2cf2dc228c14a9cccfdcc8d2e3a91363018407)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c609fb70f45c5f6d977800fd16f62b5142e44d54877cfbd941e7ddb2161932e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8d12f484188e9a954ae27858d6d03504d0feb3b6f46eb6ca1ed59a8036adfab)
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
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"random_cut_forest": "randomCutForest"},
    )
    class AnomalyDetectorConfigurationProperty:
        def __init__(
            self,
            *,
            random_cut_forest: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.RandomCutForestConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for the anomaly detection algorithm.

            :param random_cut_forest: The Random Cut Forest algorithm configuration for anomaly detection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-anomalydetectorconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                anomaly_detector_configuration_property = aps_mixins.CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigurationProperty(
                    random_cut_forest=aps_mixins.CfnAnomalyDetectorPropsMixin.RandomCutForestConfigurationProperty(
                        ignore_near_expected_from_above=aps_mixins.CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty(
                            amount=123,
                            ratio=123
                        ),
                        ignore_near_expected_from_below=aps_mixins.CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty(
                            amount=123,
                            ratio=123
                        ),
                        query="query",
                        sample_size=123,
                        shingle_size=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__649f8b0d5f5e6c4e8d2df6107f628ee1ac2e5aa8f1f96f67f2592925681092b9)
                check_type(argname="argument random_cut_forest", value=random_cut_forest, expected_type=type_hints["random_cut_forest"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if random_cut_forest is not None:
                self._values["random_cut_forest"] = random_cut_forest

        @builtins.property
        def random_cut_forest(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.RandomCutForestConfigurationProperty"]]:
            '''The Random Cut Forest algorithm configuration for anomaly detection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-anomalydetectorconfiguration.html#cfn-aps-anomalydetector-anomalydetectorconfiguration-randomcutforest
            '''
            result = self._values.get("random_cut_forest")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.RandomCutForestConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnomalyDetectorConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty",
        jsii_struct_bases=[],
        name_mapping={"amount": "amount", "ratio": "ratio"},
    )
    class IgnoreNearExpectedProperty:
        def __init__(
            self,
            *,
            amount: typing.Optional[jsii.Number] = None,
            ratio: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configuration for threshold settings that determine when values near expected values should be ignored during anomaly detection.

            :param amount: The absolute amount by which values can differ from expected values before being considered anomalous.
            :param ratio: The ratio by which values can differ from expected values before being considered anomalous.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-ignorenearexpected.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                ignore_near_expected_property = aps_mixins.CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty(
                    amount=123,
                    ratio=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__78e9c5307cd938f9c45079e66827c1e78f9b08d8547c56240c731ad86ee6f710)
                check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
                check_type(argname="argument ratio", value=ratio, expected_type=type_hints["ratio"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amount is not None:
                self._values["amount"] = amount
            if ratio is not None:
                self._values["ratio"] = ratio

        @builtins.property
        def amount(self) -> typing.Optional[jsii.Number]:
            '''The absolute amount by which values can differ from expected values before being considered anomalous.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-ignorenearexpected.html#cfn-aps-anomalydetector-ignorenearexpected-amount
            '''
            result = self._values.get("amount")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ratio(self) -> typing.Optional[jsii.Number]:
            '''The ratio by which values can differ from expected values before being considered anomalous.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-ignorenearexpected.html#cfn-aps-anomalydetector-ignorenearexpected-ratio
            '''
            result = self._values.get("ratio")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IgnoreNearExpectedProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnAnomalyDetectorPropsMixin.LabelProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class LabelProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon Managed Service for Prometheus metric labels associated with the anomaly detector.

            :param key: The key of the label.
            :param value: The value for this label.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-label.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                label_property = aps_mixins.CfnAnomalyDetectorPropsMixin.LabelProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__41f4921859927c1c3763bb78ff22b97469b956a89c4c84815bcfa3a372ae4f9e)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key of the label.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-label.html#cfn-aps-anomalydetector-label-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value for this label.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-label.html#cfn-aps-anomalydetector-label-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LabelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnAnomalyDetectorPropsMixin.MissingDataActionProperty",
        jsii_struct_bases=[],
        name_mapping={"mark_as_anomaly": "markAsAnomaly", "skip": "skip"},
    )
    class MissingDataActionProperty:
        def __init__(
            self,
            *,
            mark_as_anomaly: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            skip: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies the action to take when data is missing during anomaly detection evaluation.

            :param mark_as_anomaly: Marks missing data points as anomalies.
            :param skip: Skips evaluation when data is missing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-missingdataaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                missing_data_action_property = aps_mixins.CfnAnomalyDetectorPropsMixin.MissingDataActionProperty(
                    mark_as_anomaly=False,
                    skip=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f971bdd177370c8246d296b500d82f37138513f9a8587753ce4c5eabf435275)
                check_type(argname="argument mark_as_anomaly", value=mark_as_anomaly, expected_type=type_hints["mark_as_anomaly"])
                check_type(argname="argument skip", value=skip, expected_type=type_hints["skip"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mark_as_anomaly is not None:
                self._values["mark_as_anomaly"] = mark_as_anomaly
            if skip is not None:
                self._values["skip"] = skip

        @builtins.property
        def mark_as_anomaly(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Marks missing data points as anomalies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-missingdataaction.html#cfn-aps-anomalydetector-missingdataaction-markasanomaly
            '''
            result = self._values.get("mark_as_anomaly")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def skip(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Skips evaluation when data is missing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-missingdataaction.html#cfn-aps-anomalydetector-missingdataaction-skip
            '''
            result = self._values.get("skip")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MissingDataActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnAnomalyDetectorPropsMixin.RandomCutForestConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ignore_near_expected_from_above": "ignoreNearExpectedFromAbove",
            "ignore_near_expected_from_below": "ignoreNearExpectedFromBelow",
            "query": "query",
            "sample_size": "sampleSize",
            "shingle_size": "shingleSize",
        },
    )
    class RandomCutForestConfigurationProperty:
        def __init__(
            self,
            *,
            ignore_near_expected_from_above: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ignore_near_expected_from_below: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            query: typing.Optional[builtins.str] = None,
            sample_size: typing.Optional[jsii.Number] = None,
            shingle_size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configuration for the Random Cut Forest algorithm used for anomaly detection in time-series data.

            :param ignore_near_expected_from_above: Configuration for ignoring values that are near expected values from above during anomaly detection.
            :param ignore_near_expected_from_below: Configuration for ignoring values that are near expected values from below during anomaly detection.
            :param query: The Prometheus query used to retrieve the time-series data for anomaly detection. .. epigraph:: Random Cut Forest queries must be wrapped by a supported PromQL aggregation operator. For more information, see `Aggregation operators <https://docs.aws.amazon.com/https://prometheus.io/docs/prometheus/latest/querying/operators/#aggregation-operators>`_ on the *Prometheus docs* website. *Supported PromQL aggregation operators* : ``avg`` , ``count`` , ``group`` , ``max`` , ``min`` , ``quantile`` , ``stddev`` , ``stdvar`` , and ``sum`` .
            :param sample_size: The number of data points sampled from the input stream for the Random Cut Forest algorithm. The default number is 256 consecutive data points. Default: - 256
            :param shingle_size: The number of consecutive data points used to create a shingle for the Random Cut Forest algorithm. The default number is 8 consecutive data points. Default: - 8

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-randomcutforestconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                random_cut_forest_configuration_property = aps_mixins.CfnAnomalyDetectorPropsMixin.RandomCutForestConfigurationProperty(
                    ignore_near_expected_from_above=aps_mixins.CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty(
                        amount=123,
                        ratio=123
                    ),
                    ignore_near_expected_from_below=aps_mixins.CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty(
                        amount=123,
                        ratio=123
                    ),
                    query="query",
                    sample_size=123,
                    shingle_size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0205a9e5b8bbd221fa43419cedae36b9f4478601dc5aa727f48c50140f3b3cf0)
                check_type(argname="argument ignore_near_expected_from_above", value=ignore_near_expected_from_above, expected_type=type_hints["ignore_near_expected_from_above"])
                check_type(argname="argument ignore_near_expected_from_below", value=ignore_near_expected_from_below, expected_type=type_hints["ignore_near_expected_from_below"])
                check_type(argname="argument query", value=query, expected_type=type_hints["query"])
                check_type(argname="argument sample_size", value=sample_size, expected_type=type_hints["sample_size"])
                check_type(argname="argument shingle_size", value=shingle_size, expected_type=type_hints["shingle_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ignore_near_expected_from_above is not None:
                self._values["ignore_near_expected_from_above"] = ignore_near_expected_from_above
            if ignore_near_expected_from_below is not None:
                self._values["ignore_near_expected_from_below"] = ignore_near_expected_from_below
            if query is not None:
                self._values["query"] = query
            if sample_size is not None:
                self._values["sample_size"] = sample_size
            if shingle_size is not None:
                self._values["shingle_size"] = shingle_size

        @builtins.property
        def ignore_near_expected_from_above(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty"]]:
            '''Configuration for ignoring values that are near expected values from above during anomaly detection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-randomcutforestconfiguration.html#cfn-aps-anomalydetector-randomcutforestconfiguration-ignorenearexpectedfromabove
            '''
            result = self._values.get("ignore_near_expected_from_above")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty"]], result)

        @builtins.property
        def ignore_near_expected_from_below(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty"]]:
            '''Configuration for ignoring values that are near expected values from below during anomaly detection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-randomcutforestconfiguration.html#cfn-aps-anomalydetector-randomcutforestconfiguration-ignorenearexpectedfrombelow
            '''
            result = self._values.get("ignore_near_expected_from_below")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty"]], result)

        @builtins.property
        def query(self) -> typing.Optional[builtins.str]:
            '''The Prometheus query used to retrieve the time-series data for anomaly detection.

            .. epigraph::

               Random Cut Forest queries must be wrapped by a supported PromQL aggregation operator. For more information, see `Aggregation operators <https://docs.aws.amazon.com/https://prometheus.io/docs/prometheus/latest/querying/operators/#aggregation-operators>`_ on the *Prometheus docs* website.

               *Supported PromQL aggregation operators* : ``avg`` , ``count`` , ``group`` , ``max`` , ``min`` , ``quantile`` , ``stddev`` , ``stdvar`` , and ``sum`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-randomcutforestconfiguration.html#cfn-aps-anomalydetector-randomcutforestconfiguration-query
            '''
            result = self._values.get("query")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sample_size(self) -> typing.Optional[jsii.Number]:
            '''The number of data points sampled from the input stream for the Random Cut Forest algorithm.

            The default number is 256 consecutive data points.

            :default: - 256

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-randomcutforestconfiguration.html#cfn-aps-anomalydetector-randomcutforestconfiguration-samplesize
            '''
            result = self._values.get("sample_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def shingle_size(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive data points used to create a shingle for the Random Cut Forest algorithm.

            The default number is 8 consecutive data points.

            :default: - 8

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-anomalydetector-randomcutforestconfiguration.html#cfn-aps-anomalydetector-randomcutforestconfiguration-shinglesize
            '''
            result = self._values.get("shingle_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RandomCutForestConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnResourcePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy_document": "policyDocument",
        "workspace_arn": "workspaceArn",
    },
)
class CfnResourcePolicyMixinProps:
    def __init__(
        self,
        *,
        policy_document: typing.Optional[builtins.str] = None,
        workspace_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourcePolicyPropsMixin.

        :param policy_document: The JSON to use as the Resource-based Policy.
        :param workspace_arn: An ARN identifying a Workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
            
            cfn_resource_policy_mixin_props = aps_mixins.CfnResourcePolicyMixinProps(
                policy_document="policyDocument",
                workspace_arn="workspaceArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f23ac0d180559c4cb60d36b402ecafef1638c358bb3a483f76f4455719b934)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument workspace_arn", value=workspace_arn, expected_type=type_hints["workspace_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if workspace_arn is not None:
            self._values["workspace_arn"] = workspace_arn

    @builtins.property
    def policy_document(self) -> typing.Optional[builtins.str]:
        '''The JSON to use as the Resource-based Policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-resourcepolicy.html#cfn-aps-resourcepolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_arn(self) -> typing.Optional[builtins.str]:
        '''An ARN identifying a Workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-resourcepolicy.html#cfn-aps-resourcepolicy-workspacearn
        '''
        result = self._values.get("workspace_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourcePolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnResourcePolicyPropsMixin",
):
    '''Use resource-based policies to grant permissions to other AWS accounts or services to access your workspace.

    Only Prometheus-compatible APIs can be used for workspace sharing. You can add non-Prometheus-compatible APIs to the policy, but they will be ignored. For more information, see `Prometheus-compatible APIs <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-APIReference-Prometheus-Compatible-Apis.html>`_ in the *Amazon Managed Service for Prometheus User Guide* .

    If your workspace uses customer-managed AWS  keys for encryption, you must grant the principals in your resource-based policy access to those AWS  keys. You can do this by creating AWS  grants. For more information, see `CreateGrant <https://docs.aws.amazon.com/kms/latest/APIReference/API_CreateGrant.html>`_ in the *AWS  API Reference* and `Encryption at rest <https://docs.aws.amazon.com/prometheus/latest/userguide/encryption-at-rest-Amazon-Service-Prometheus.html>`_ in the *Amazon Managed Service for Prometheus User Guide* .

    For more information about working with IAM , see `Using Amazon Managed Service for Prometheus with IAM <https://docs.aws.amazon.com/prometheus/latest/userguide/security_iam_service-with-iam.html>`_ in the *Amazon Managed Service for Prometheus User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-resourcepolicy.html
    :cloudformationResource: AWS::APS::ResourcePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
        
        cfn_resource_policy_props_mixin = aps_mixins.CfnResourcePolicyPropsMixin(aps_mixins.CfnResourcePolicyMixinProps(
            policy_document="policyDocument",
            workspace_arn="workspaceArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::APS::ResourcePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d03de09189422d30956319e7a5c75449cd96323eba270de5b4383774c1a262d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc5b8e5728359196e764eb70911e6b5b019a13393e6a245329e0c91bae93c7b3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64dd7baed2a03330d2f5b485d7b789045120e08196f52ef76ed9b1dabf48aa1b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourcePolicyMixinProps:
        return typing.cast(CfnResourcePolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnRuleGroupsNamespaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data": "data",
        "name": "name",
        "tags": "tags",
        "workspace": "workspace",
    },
)
class CfnRuleGroupsNamespaceMixinProps:
    def __init__(
        self,
        *,
        data: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        workspace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnRuleGroupsNamespacePropsMixin.

        :param data: The rules file used in the namespace. For more details about the rules file, see `Creating a rules file <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-ruler-rulesfile.html>`_ in the *Amazon Managed Service for Prometheus User Guide* .
        :param name: The name of the rule groups namespace.
        :param tags: The list of tag keys and values that are associated with the rule groups namespace.
        :param workspace: The ID of the workspace to add the rule groups namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
            
            cfn_rule_groups_namespace_mixin_props = aps_mixins.CfnRuleGroupsNamespaceMixinProps(
                data="data",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                workspace="workspace"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e585613b0693194d1c315b107c0229d5a6f74884fe9329c993ebb74bd28274ce)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data is not None:
            self._values["data"] = data
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if workspace is not None:
            self._values["workspace"] = workspace

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''The rules file used in the namespace.

        For more details about the rules file, see `Creating a rules file <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-ruler-rulesfile.html>`_ in the *Amazon Managed Service for Prometheus User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html#cfn-aps-rulegroupsnamespace-data
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the rule groups namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html#cfn-aps-rulegroupsnamespace-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of tag keys and values that are associated with the rule groups namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html#cfn-aps-rulegroupsnamespace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''The ID of the workspace to add the rule groups namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html#cfn-aps-rulegroupsnamespace-workspace
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleGroupsNamespaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRuleGroupsNamespacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnRuleGroupsNamespacePropsMixin",
):
    '''The definition of a rule groups namespace in an Amazon Managed Service for Prometheus workspace.

    A rule groups namespace is associated with exactly one rules file. A workspace can have multiple rule groups namespaces. For more information about rules files, see `Creating a rules file <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-ruler-rulesfile.html>`_ , in the *Amazon Managed Service for Prometheus User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html
    :cloudformationResource: AWS::APS::RuleGroupsNamespace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
        
        cfn_rule_groups_namespace_props_mixin = aps_mixins.CfnRuleGroupsNamespacePropsMixin(aps_mixins.CfnRuleGroupsNamespaceMixinProps(
            data="data",
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            workspace="workspace"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRuleGroupsNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::APS::RuleGroupsNamespace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fdd425a867282b344348d88c22585596191967ed9a83967c038b08acade2f93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__834d94d2eb48ec71a5eaec35e2251dcdd42bae4aef71d6134b027fb3d6494827)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5133bdffcda0cb565097df0f031425472c7b6d1bc0af8a69aa9e6970816ab683)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRuleGroupsNamespaceMixinProps:
        return typing.cast(CfnRuleGroupsNamespaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


class CfnScraperApplicationLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperApplicationLogs",
):
    '''Builder for CfnScraperLogsMixin to generate APPLICATION_LOGS for CfnScraper.

    :cloudformationResource: AWS::APS::Scraper
    :logType: APPLICATION_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
        
        cfn_scraper_application_logs = aps_mixins.CfnScraperApplicationLogs()
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
    ) -> "CfnScraperLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e8bfbf23366cd4d2fcb156d3cfe7d3e49fc05493d06d1eaecbfa2aeafac6eb)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnScraperLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnScraperLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8faaf42ea1989615d04fec0892c111aad366c7c04f43d43485110fcc589a141)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnScraperLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnScraperLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab41c546ea59afb485cd9c68bc33525f52af138111541a35e75e1abbfcf6715)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnScraperLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnScraperLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperLogsMixin",
):
    '''A scraper is a fully-managed agentless collector that discovers and pulls metrics automatically.

    A scraper pulls metrics from Prometheus-compatible sources within an Amazon EKS cluster, and sends them to your Amazon Managed Service for Prometheus workspace. Scrapers are flexible. You can configure the scraper to control what metrics are collected, the frequency of collection, what transformations are applied to the metrics, and more.

    An IAM role will be created for you that Amazon Managed Service for Prometheus uses to access the metrics in your cluster. You must configure this role with a policy that allows it to scrape metrics from your cluster. For more information, see `Configuring your Amazon EKS cluster <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-collector-how-to.html#AMP-collector-eks-setup>`_ in the *Amazon Managed Service for Prometheus User Guide* .

    The ``scrapeConfiguration`` parameter contains the YAML configuration for the scraper.
    .. epigraph::

       For more information about collectors, including what metrics are collected, and how to configure the scraper, see `Using an AWS managed collector <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-collector-how-to.html>`_ in the *Amazon Managed Service for Prometheus User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-scraper.html
    :cloudformationResource: AWS::APS::Scraper
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_scraper_logs_mixin = aps_mixins.CfnScraperLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::APS::Scraper``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a362522cbf61aebf6e4d0035367dee51c0a05859ba6adf683ed1fc458e850ece)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8f32a2f6c46380703f7a914e07a120b36fb3b3f35335f17c9635961a2d38fe3)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ddb2c52ceee4d4571854b1a516d5bb539da875832ae7e25d3a62883d2f1a015)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="APPLICATION_LOGS")
    def APPLICATION_LOGS(cls) -> CfnScraperApplicationLogs:
        return typing.cast(CfnScraperApplicationLogs, jsii.sget(cls, "APPLICATION_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "destination": "destination",
        "role_configuration": "roleConfiguration",
        "scrape_configuration": "scrapeConfiguration",
        "scraper_logging_configuration": "scraperLoggingConfiguration",
        "source": "source",
        "tags": "tags",
    },
)
class CfnScraperMixinProps:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScraperPropsMixin.DestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScraperPropsMixin.RoleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        scrape_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScraperPropsMixin.ScrapeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        scraper_logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScraperPropsMixin.ScraperLoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScraperPropsMixin.SourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnScraperPropsMixin.

        :param alias: An optional user-assigned scraper alias.
        :param destination: The Amazon Managed Service for Prometheus workspace the scraper sends metrics to.
        :param role_configuration: The role configuration in an Amazon Managed Service for Prometheus scraper.
        :param scrape_configuration: The configuration in use by the scraper.
        :param scraper_logging_configuration: The definition of logging configuration in an Amazon Managed Service for Prometheus workspace.
        :param source: The Amazon EKS cluster from which the scraper collects metrics.
        :param tags: (Optional) The list of tag keys and values associated with the scraper.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-scraper.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
            
            cfn_scraper_mixin_props = aps_mixins.CfnScraperMixinProps(
                alias="alias",
                destination=aps_mixins.CfnScraperPropsMixin.DestinationProperty(
                    amp_configuration=aps_mixins.CfnScraperPropsMixin.AmpConfigurationProperty(
                        workspace_arn="workspaceArn"
                    )
                ),
                role_configuration=aps_mixins.CfnScraperPropsMixin.RoleConfigurationProperty(
                    source_role_arn="sourceRoleArn",
                    target_role_arn="targetRoleArn"
                ),
                scrape_configuration=aps_mixins.CfnScraperPropsMixin.ScrapeConfigurationProperty(
                    configuration_blob="configurationBlob"
                ),
                scraper_logging_configuration=aps_mixins.CfnScraperPropsMixin.ScraperLoggingConfigurationProperty(
                    logging_destination=aps_mixins.CfnScraperPropsMixin.ScraperLoggingDestinationProperty(
                        cloud_watch_logs=aps_mixins.CfnScraperPropsMixin.CloudWatchLogDestinationProperty(
                            log_group_arn="logGroupArn"
                        )
                    ),
                    scraper_components=[aps_mixins.CfnScraperPropsMixin.ScraperComponentProperty(
                        config=aps_mixins.CfnScraperPropsMixin.ComponentConfigProperty(
                            options={
                                "options_key": "options"
                            }
                        ),
                        type="type"
                    )]
                ),
                source=aps_mixins.CfnScraperPropsMixin.SourceProperty(
                    eks_configuration=aps_mixins.CfnScraperPropsMixin.EksConfigurationProperty(
                        cluster_arn="clusterArn",
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    ),
                    vpc_configuration=aps_mixins.CfnScraperPropsMixin.VpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4e20e073a2bac812fdeff6efc7a7793c070392ad12a93a52e33826c2ca8162)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument role_configuration", value=role_configuration, expected_type=type_hints["role_configuration"])
            check_type(argname="argument scrape_configuration", value=scrape_configuration, expected_type=type_hints["scrape_configuration"])
            check_type(argname="argument scraper_logging_configuration", value=scraper_logging_configuration, expected_type=type_hints["scraper_logging_configuration"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if destination is not None:
            self._values["destination"] = destination
        if role_configuration is not None:
            self._values["role_configuration"] = role_configuration
        if scrape_configuration is not None:
            self._values["scrape_configuration"] = scrape_configuration
        if scraper_logging_configuration is not None:
            self._values["scraper_logging_configuration"] = scraper_logging_configuration
        if source is not None:
            self._values["source"] = source
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''An optional user-assigned scraper alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-scraper.html#cfn-aps-scraper-alias
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.DestinationProperty"]]:
        '''The Amazon Managed Service for Prometheus workspace the scraper sends metrics to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-scraper.html#cfn-aps-scraper-destination
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.DestinationProperty"]], result)

    @builtins.property
    def role_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.RoleConfigurationProperty"]]:
        '''The role configuration in an Amazon Managed Service for Prometheus scraper.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-scraper.html#cfn-aps-scraper-roleconfiguration
        '''
        result = self._values.get("role_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.RoleConfigurationProperty"]], result)

    @builtins.property
    def scrape_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.ScrapeConfigurationProperty"]]:
        '''The configuration in use by the scraper.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-scraper.html#cfn-aps-scraper-scrapeconfiguration
        '''
        result = self._values.get("scrape_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.ScrapeConfigurationProperty"]], result)

    @builtins.property
    def scraper_logging_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.ScraperLoggingConfigurationProperty"]]:
        '''The definition of logging configuration in an Amazon Managed Service for Prometheus workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-scraper.html#cfn-aps-scraper-scraperloggingconfiguration
        '''
        result = self._values.get("scraper_logging_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.ScraperLoggingConfigurationProperty"]], result)

    @builtins.property
    def source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.SourceProperty"]]:
        '''The Amazon EKS cluster from which the scraper collects metrics.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-scraper.html#cfn-aps-scraper-source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.SourceProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''(Optional) The list of tag keys and values associated with the scraper.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-scraper.html#cfn-aps-scraper-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScraperMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnScraperPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperPropsMixin",
):
    '''A scraper is a fully-managed agentless collector that discovers and pulls metrics automatically.

    A scraper pulls metrics from Prometheus-compatible sources within an Amazon EKS cluster, and sends them to your Amazon Managed Service for Prometheus workspace. Scrapers are flexible. You can configure the scraper to control what metrics are collected, the frequency of collection, what transformations are applied to the metrics, and more.

    An IAM role will be created for you that Amazon Managed Service for Prometheus uses to access the metrics in your cluster. You must configure this role with a policy that allows it to scrape metrics from your cluster. For more information, see `Configuring your Amazon EKS cluster <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-collector-how-to.html#AMP-collector-eks-setup>`_ in the *Amazon Managed Service for Prometheus User Guide* .

    The ``scrapeConfiguration`` parameter contains the YAML configuration for the scraper.
    .. epigraph::

       For more information about collectors, including what metrics are collected, and how to configure the scraper, see `Using an AWS managed collector <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-collector-how-to.html>`_ in the *Amazon Managed Service for Prometheus User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-scraper.html
    :cloudformationResource: AWS::APS::Scraper
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
        
        cfn_scraper_props_mixin = aps_mixins.CfnScraperPropsMixin(aps_mixins.CfnScraperMixinProps(
            alias="alias",
            destination=aps_mixins.CfnScraperPropsMixin.DestinationProperty(
                amp_configuration=aps_mixins.CfnScraperPropsMixin.AmpConfigurationProperty(
                    workspace_arn="workspaceArn"
                )
            ),
            role_configuration=aps_mixins.CfnScraperPropsMixin.RoleConfigurationProperty(
                source_role_arn="sourceRoleArn",
                target_role_arn="targetRoleArn"
            ),
            scrape_configuration=aps_mixins.CfnScraperPropsMixin.ScrapeConfigurationProperty(
                configuration_blob="configurationBlob"
            ),
            scraper_logging_configuration=aps_mixins.CfnScraperPropsMixin.ScraperLoggingConfigurationProperty(
                logging_destination=aps_mixins.CfnScraperPropsMixin.ScraperLoggingDestinationProperty(
                    cloud_watch_logs=aps_mixins.CfnScraperPropsMixin.CloudWatchLogDestinationProperty(
                        log_group_arn="logGroupArn"
                    )
                ),
                scraper_components=[aps_mixins.CfnScraperPropsMixin.ScraperComponentProperty(
                    config=aps_mixins.CfnScraperPropsMixin.ComponentConfigProperty(
                        options={
                            "options_key": "options"
                        }
                    ),
                    type="type"
                )]
            ),
            source=aps_mixins.CfnScraperPropsMixin.SourceProperty(
                eks_configuration=aps_mixins.CfnScraperPropsMixin.EksConfigurationProperty(
                    cluster_arn="clusterArn",
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                ),
                vpc_configuration=aps_mixins.CfnScraperPropsMixin.VpcConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            ),
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
        props: typing.Union[CfnScraperMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::APS::Scraper``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb3d4fe30762978aba2c784fa45942828bf8d53dcc846f64cfbaad8fdccb007c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71dea35a63306df5542dbd13d651949de844b7213692ee5225c68547feabeff2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88056ffeb80f0b9fe5b7790014b5721cd7f49a86ea5b04ee28d4fea3af676083)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnScraperMixinProps:
        return typing.cast(CfnScraperMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperPropsMixin.AmpConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"workspace_arn": "workspaceArn"},
    )
    class AmpConfigurationProperty:
        def __init__(
            self,
            *,
            workspace_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AmpConfiguration`` structure defines the Amazon Managed Service for Prometheus instance a scraper should send metrics to.

            :param workspace_arn: ARN of the Amazon Managed Service for Prometheus workspace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-ampconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                amp_configuration_property = aps_mixins.CfnScraperPropsMixin.AmpConfigurationProperty(
                    workspace_arn="workspaceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc2a92763eedf3214d89defdba8207397d7487532f1345d81e7de1fe31f9ed2f)
                check_type(argname="argument workspace_arn", value=workspace_arn, expected_type=type_hints["workspace_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if workspace_arn is not None:
                self._values["workspace_arn"] = workspace_arn

        @builtins.property
        def workspace_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the Amazon Managed Service for Prometheus workspace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-ampconfiguration.html#cfn-aps-scraper-ampconfiguration-workspacearn
            '''
            result = self._values.get("workspace_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmpConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperPropsMixin.CloudWatchLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_arn": "logGroupArn"},
    )
    class CloudWatchLogDestinationProperty:
        def __init__(
            self,
            *,
            log_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a cloudwatch logs destination for scraper logging.

            :param log_group_arn: ARN of the CloudWatch log group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-cloudwatchlogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                cloud_watch_log_destination_property = aps_mixins.CfnScraperPropsMixin.CloudWatchLogDestinationProperty(
                    log_group_arn="logGroupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d6dc7b6ec3d81a983674f8e21a8f2765d5c225b818d84592727445eb1c456462)
                check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_arn is not None:
                self._values["log_group_arn"] = log_group_arn

        @builtins.property
        def log_group_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the CloudWatch log group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-cloudwatchlogdestination.html#cfn-aps-scraper-cloudwatchlogdestination-loggrouparn
            '''
            result = self._values.get("log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperPropsMixin.ComponentConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"options": "options"},
    )
    class ComponentConfigProperty:
        def __init__(
            self,
            *,
            options: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Configuration settings for a scraper component.

            :param options: Configuration options for the scraper component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-componentconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                component_config_property = aps_mixins.CfnScraperPropsMixin.ComponentConfigProperty(
                    options={
                        "options_key": "options"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c52058ba8767163409c87d7c0b85a950195987a81dc113182b3e7b9bc005454e)
                check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if options is not None:
                self._values["options"] = options

        @builtins.property
        def options(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Configuration options for the scraper component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-componentconfig.html#cfn-aps-scraper-componentconfig-options
            '''
            result = self._values.get("options")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperPropsMixin.DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"amp_configuration": "ampConfiguration"},
    )
    class DestinationProperty:
        def __init__(
            self,
            *,
            amp_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScraperPropsMixin.AmpConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Where to send the metrics from a scraper.

            :param amp_configuration: The Amazon Managed Service for Prometheus workspace to send metrics to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-destination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                destination_property = aps_mixins.CfnScraperPropsMixin.DestinationProperty(
                    amp_configuration=aps_mixins.CfnScraperPropsMixin.AmpConfigurationProperty(
                        workspace_arn="workspaceArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__47e47d525493346a949aad764cbd9bbc61bbc9b0f7579f9bed3a8fc30c831bda)
                check_type(argname="argument amp_configuration", value=amp_configuration, expected_type=type_hints["amp_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amp_configuration is not None:
                self._values["amp_configuration"] = amp_configuration

        @builtins.property
        def amp_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.AmpConfigurationProperty"]]:
            '''The Amazon Managed Service for Prometheus workspace to send metrics to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-destination.html#cfn-aps-scraper-destination-ampconfiguration
            '''
            result = self._values.get("amp_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.AmpConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperPropsMixin.EksConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cluster_arn": "clusterArn",
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class EksConfigurationProperty:
        def __init__(
            self,
            *,
            cluster_arn: typing.Optional[builtins.str] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The ``EksConfiguration`` structure describes the connection to the Amazon EKS cluster from which a scraper collects metrics.

            :param cluster_arn: ARN of the Amazon EKS cluster.
            :param security_group_ids: A list of the security group IDs for the Amazon EKS cluster VPC configuration.
            :param subnet_ids: A list of subnet IDs for the Amazon EKS cluster VPC configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-eksconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                eks_configuration_property = aps_mixins.CfnScraperPropsMixin.EksConfigurationProperty(
                    cluster_arn="clusterArn",
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3fbb20f19cfc4d6c311e40f4b351bd9ba72706b31c2a5b2085de58d23537f755)
                check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cluster_arn is not None:
                self._values["cluster_arn"] = cluster_arn
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def cluster_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the Amazon EKS cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-eksconfiguration.html#cfn-aps-scraper-eksconfiguration-clusterarn
            '''
            result = self._values.get("cluster_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of the security group IDs for the Amazon EKS cluster VPC configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-eksconfiguration.html#cfn-aps-scraper-eksconfiguration-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of subnet IDs for the Amazon EKS cluster VPC configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-eksconfiguration.html#cfn-aps-scraper-eksconfiguration-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperPropsMixin.RoleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source_role_arn": "sourceRoleArn",
            "target_role_arn": "targetRoleArn",
        },
    )
    class RoleConfigurationProperty:
        def __init__(
            self,
            *,
            source_role_arn: typing.Optional[builtins.str] = None,
            target_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The role configuration in an Amazon Managed Service for Prometheus scraper.

            :param source_role_arn: The ARN of the source role.
            :param target_role_arn: The ARN of the target role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-roleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                role_configuration_property = aps_mixins.CfnScraperPropsMixin.RoleConfigurationProperty(
                    source_role_arn="sourceRoleArn",
                    target_role_arn="targetRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__37a8b2533626a7a87f4b1ac709f150c347cc43c02ee1dc039bdc0025fee7360e)
                check_type(argname="argument source_role_arn", value=source_role_arn, expected_type=type_hints["source_role_arn"])
                check_type(argname="argument target_role_arn", value=target_role_arn, expected_type=type_hints["target_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_role_arn is not None:
                self._values["source_role_arn"] = source_role_arn
            if target_role_arn is not None:
                self._values["target_role_arn"] = target_role_arn

        @builtins.property
        def source_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the source role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-roleconfiguration.html#cfn-aps-scraper-roleconfiguration-sourcerolearn
            '''
            result = self._values.get("source_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the target role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-roleconfiguration.html#cfn-aps-scraper-roleconfiguration-targetrolearn
            '''
            result = self._values.get("target_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperPropsMixin.ScrapeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"configuration_blob": "configurationBlob"},
    )
    class ScrapeConfigurationProperty:
        def __init__(
            self,
            *,
            configuration_blob: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A scrape configuration for a scraper, base 64 encoded.

            For more information, see `Scraper configuration <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-collector-how-to.html#AMP-collector-configuration>`_ in the *Amazon Managed Service for Prometheus User Guide* .

            :param configuration_blob: The base 64 encoded scrape configuration file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-scrapeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                scrape_configuration_property = aps_mixins.CfnScraperPropsMixin.ScrapeConfigurationProperty(
                    configuration_blob="configurationBlob"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db7cc3d510fef1b62e3d6b00b8769965c86d3247faa511004534e6a9cac0784b)
                check_type(argname="argument configuration_blob", value=configuration_blob, expected_type=type_hints["configuration_blob"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configuration_blob is not None:
                self._values["configuration_blob"] = configuration_blob

        @builtins.property
        def configuration_blob(self) -> typing.Optional[builtins.str]:
            '''The base 64 encoded scrape configuration file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-scrapeconfiguration.html#cfn-aps-scraper-scrapeconfiguration-configurationblob
            '''
            result = self._values.get("configuration_blob")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScrapeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperPropsMixin.ScraperComponentProperty",
        jsii_struct_bases=[],
        name_mapping={"config": "config", "type": "type"},
    )
    class ScraperComponentProperty:
        def __init__(
            self,
            *,
            config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScraperPropsMixin.ComponentConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A component of a Amazon Managed Service for Prometheus scraper that can be configured for logging.

            :param config: The configuration settings for the scraper component.
            :param type: The type of the scraper component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-scrapercomponent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                scraper_component_property = aps_mixins.CfnScraperPropsMixin.ScraperComponentProperty(
                    config=aps_mixins.CfnScraperPropsMixin.ComponentConfigProperty(
                        options={
                            "options_key": "options"
                        }
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c067c2e0c68ec940309eec4ab2b9a3bcb11f8a64e11def9d4a87da42f51c9f8d)
                check_type(argname="argument config", value=config, expected_type=type_hints["config"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if config is not None:
                self._values["config"] = config
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.ComponentConfigProperty"]]:
            '''The configuration settings for the scraper component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-scrapercomponent.html#cfn-aps-scraper-scrapercomponent-config
            '''
            result = self._values.get("config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.ComponentConfigProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the scraper component.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-scrapercomponent.html#cfn-aps-scraper-scrapercomponent-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScraperComponentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperPropsMixin.ScraperLoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "logging_destination": "loggingDestination",
            "scraper_components": "scraperComponents",
        },
    )
    class ScraperLoggingConfigurationProperty:
        def __init__(
            self,
            *,
            logging_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScraperPropsMixin.ScraperLoggingDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            scraper_components: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScraperPropsMixin.ScraperComponentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configuration for scraper logging.

            :param logging_destination: Destination for scraper logging.
            :param scraper_components: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-scraperloggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                scraper_logging_configuration_property = aps_mixins.CfnScraperPropsMixin.ScraperLoggingConfigurationProperty(
                    logging_destination=aps_mixins.CfnScraperPropsMixin.ScraperLoggingDestinationProperty(
                        cloud_watch_logs=aps_mixins.CfnScraperPropsMixin.CloudWatchLogDestinationProperty(
                            log_group_arn="logGroupArn"
                        )
                    ),
                    scraper_components=[aps_mixins.CfnScraperPropsMixin.ScraperComponentProperty(
                        config=aps_mixins.CfnScraperPropsMixin.ComponentConfigProperty(
                            options={
                                "options_key": "options"
                            }
                        ),
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__40dd826a760d5d825dcbc2f16eadf7fada388016832d17147069bf776c015f99)
                check_type(argname="argument logging_destination", value=logging_destination, expected_type=type_hints["logging_destination"])
                check_type(argname="argument scraper_components", value=scraper_components, expected_type=type_hints["scraper_components"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if logging_destination is not None:
                self._values["logging_destination"] = logging_destination
            if scraper_components is not None:
                self._values["scraper_components"] = scraper_components

        @builtins.property
        def logging_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.ScraperLoggingDestinationProperty"]]:
            '''Destination for scraper logging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-scraperloggingconfiguration.html#cfn-aps-scraper-scraperloggingconfiguration-loggingdestination
            '''
            result = self._values.get("logging_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.ScraperLoggingDestinationProperty"]], result)

        @builtins.property
        def scraper_components(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.ScraperComponentProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-scraperloggingconfiguration.html#cfn-aps-scraper-scraperloggingconfiguration-scrapercomponents
            '''
            result = self._values.get("scraper_components")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.ScraperComponentProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScraperLoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperPropsMixin.ScraperLoggingDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_logs": "cloudWatchLogs"},
    )
    class ScraperLoggingDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScraperPropsMixin.CloudWatchLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The destination where scraper logs are sent.

            :param cloud_watch_logs: The CloudWatch Logs configuration for the scraper logging destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-scraperloggingdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                scraper_logging_destination_property = aps_mixins.CfnScraperPropsMixin.ScraperLoggingDestinationProperty(
                    cloud_watch_logs=aps_mixins.CfnScraperPropsMixin.CloudWatchLogDestinationProperty(
                        log_group_arn="logGroupArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__505f5999414c5ccfb62f316f63887c2d59f223ec7752ec73da6b8997de89d29b)
                check_type(argname="argument cloud_watch_logs", value=cloud_watch_logs, expected_type=type_hints["cloud_watch_logs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs is not None:
                self._values["cloud_watch_logs"] = cloud_watch_logs

        @builtins.property
        def cloud_watch_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.CloudWatchLogDestinationProperty"]]:
            '''The CloudWatch Logs configuration for the scraper logging destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-scraperloggingdestination.html#cfn-aps-scraper-scraperloggingdestination-cloudwatchlogs
            '''
            result = self._values.get("cloud_watch_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.CloudWatchLogDestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScraperLoggingDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperPropsMixin.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "eks_configuration": "eksConfiguration",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            eks_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScraperPropsMixin.EksConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScraperPropsMixin.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The source of collected metrics for a scraper.

            :param eks_configuration: The Amazon EKS cluster from which a scraper collects metrics.
            :param vpc_configuration: Configuration for VPC metrics source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-source.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                source_property = aps_mixins.CfnScraperPropsMixin.SourceProperty(
                    eks_configuration=aps_mixins.CfnScraperPropsMixin.EksConfigurationProperty(
                        cluster_arn="clusterArn",
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    ),
                    vpc_configuration=aps_mixins.CfnScraperPropsMixin.VpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8542c74f93de6ef162db671889d9071262b2b57a0bf9e844586eff6bc6235da4)
                check_type(argname="argument eks_configuration", value=eks_configuration, expected_type=type_hints["eks_configuration"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if eks_configuration is not None:
                self._values["eks_configuration"] = eks_configuration
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def eks_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.EksConfigurationProperty"]]:
            '''The Amazon EKS cluster from which a scraper collects metrics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-source.html#cfn-aps-scraper-source-eksconfiguration
            '''
            result = self._values.get("eks_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.EksConfigurationProperty"]], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.VpcConfigurationProperty"]]:
            '''Configuration for VPC metrics source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-source.html#cfn-aps-scraper-source-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScraperPropsMixin.VpcConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnScraperPropsMixin.VpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigurationProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Configuration for VPC metrics source.

            :param security_group_ids: List of security group IDs.
            :param subnet_ids: List of subnet IDs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-vpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                vpc_configuration_property = aps_mixins.CfnScraperPropsMixin.VpcConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__18be14bfbee6dc5a68ca000c5bd6ab9e8a5292b346bd06219830be82917af731)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of security group IDs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-vpcconfiguration.html#cfn-aps-scraper-vpcconfiguration-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of subnet IDs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-scraper-vpcconfiguration.html#cfn-aps-scraper-vpcconfiguration-subnetids
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


@jsii.implements(_IMixin_11e4b965)
class CfnWorkspaceLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnWorkspaceLogsMixin",
):
    '''An Amazon Managed Service for Prometheus workspace is a logical and isolated Prometheus server dedicated to ingesting, storing, and querying your Prometheus-compatible metrics.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html
    :cloudformationResource: AWS::APS::Workspace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_workspace_logs_mixin = aps_mixins.CfnWorkspaceLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::APS::Workspace``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58584becf326ed4d54c694ac4a270a054b0b92378a11c73cb24b6743302026e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91a7fb4b14375528f681fcd590bbd342ad6a2659aacb1b07191cdc2d6394f190)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__641fc12e6c2b4d158b5761019b8e856047de0a7bca46598a7115063bc8937365)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MANAGED_PROMETHEUS_LOGS")
    def MANAGED_PROMETHEUS_LOGS(cls) -> "CfnWorkspaceManagedPrometheusLogs":
        return typing.cast("CfnWorkspaceManagedPrometheusLogs", jsii.sget(cls, "MANAGED_PROMETHEUS_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


class CfnWorkspaceManagedPrometheusLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnWorkspaceManagedPrometheusLogs",
):
    '''Builder for CfnWorkspaceLogsMixin to generate MANAGED_PROMETHEUS_LOGS for CfnWorkspace.

    :cloudformationResource: AWS::APS::Workspace
    :logType: MANAGED_PROMETHEUS_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
        
        cfn_workspace_managed_prometheus_logs = aps_mixins.CfnWorkspaceManagedPrometheusLogs()
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
    ) -> CfnWorkspaceLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e749916f112bd00409213ec54e0ffa5491a9df279ab5c787916486daea914795)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnWorkspaceLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnWorkspaceLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59f933af36eff231b4f59a680c8b8e7852391cd62d37a7be9ff1a53cd773850)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnWorkspaceLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnWorkspaceLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51034a507649f14c4403b3d0c93d9e64691867c70fee095be1e9b397017ddec)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnWorkspaceLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnWorkspaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "alert_manager_definition": "alertManagerDefinition",
        "alias": "alias",
        "kms_key_arn": "kmsKeyArn",
        "logging_configuration": "loggingConfiguration",
        "query_logging_configuration": "queryLoggingConfiguration",
        "tags": "tags",
        "workspace_configuration": "workspaceConfiguration",
    },
)
class CfnWorkspaceMixinProps:
    def __init__(
        self,
        *,
        alert_manager_definition: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        query_logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.QueryLoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        workspace_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.WorkspaceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnWorkspacePropsMixin.

        :param alert_manager_definition: The alert manager definition, a YAML configuration for the alert manager in your Amazon Managed Service for Prometheus workspace. For details about the alert manager definition, see `Creating an alert manager configuration files <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-alertmanager-config.html>`_ in the *Amazon Managed Service for Prometheus User Guide* . The following example shows part of a CloudFormation YAML file with an embedded alert manager definition (following the ``- |-`` ). ``Workspace: Type: AWS::APS::Workspace .... Properties: .... AlertManagerDefinition: Fn::Sub: - |- alertmanager_config: | templates: - 'default_template' route: receiver: example-sns receivers: - name: example-sns sns_configs: - topic_arn: 'arn:aws:sns:${AWS::Region}:${AWS::AccountId}:${TopicName}' -``
        :param alias: The alias that is assigned to this workspace to help identify it. It does not need to be unique.
        :param kms_key_arn: (optional) The ARN for a customer managed AWS key to use for encrypting data within your workspace. For more information about using your own key in your workspace, see `Encryption at rest <https://docs.aws.amazon.com/prometheus/latest/userguide/encryption-at-rest-Amazon-Service-Prometheus.html>`_ in the *Amazon Managed Service for Prometheus User Guide* .
        :param logging_configuration: Contains information about the logging configuration for the workspace.
        :param query_logging_configuration: The definition of logging configuration in an Amazon Managed Service for Prometheus workspace.
        :param tags: The list of tag keys and values that are associated with the workspace.
        :param workspace_configuration: Use this structure to define label sets and the ingestion limits for time series that match label sets, and to specify the retention period of the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
            
            cfn_workspace_mixin_props = aps_mixins.CfnWorkspaceMixinProps(
                alert_manager_definition="alertManagerDefinition",
                alias="alias",
                kms_key_arn="kmsKeyArn",
                logging_configuration=aps_mixins.CfnWorkspacePropsMixin.LoggingConfigurationProperty(
                    log_group_arn="logGroupArn"
                ),
                query_logging_configuration=aps_mixins.CfnWorkspacePropsMixin.QueryLoggingConfigurationProperty(
                    destinations=[aps_mixins.CfnWorkspacePropsMixin.LoggingDestinationProperty(
                        cloud_watch_logs=aps_mixins.CfnWorkspacePropsMixin.CloudWatchLogDestinationProperty(
                            log_group_arn="logGroupArn"
                        ),
                        filters=aps_mixins.CfnWorkspacePropsMixin.LoggingFilterProperty(
                            qsp_threshold=123
                        )
                    )]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                workspace_configuration=aps_mixins.CfnWorkspacePropsMixin.WorkspaceConfigurationProperty(
                    limits_per_label_sets=[aps_mixins.CfnWorkspacePropsMixin.LimitsPerLabelSetProperty(
                        label_set=[aps_mixins.CfnWorkspacePropsMixin.LabelProperty(
                            name="name",
                            value="value"
                        )],
                        limits=aps_mixins.CfnWorkspacePropsMixin.LimitsPerLabelSetEntryProperty(
                            max_series=123
                        )
                    )],
                    retention_period_in_days=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c30c64b6c80a313e0023822af9c1ae536138a881e1c82532526313af7b948750)
            check_type(argname="argument alert_manager_definition", value=alert_manager_definition, expected_type=type_hints["alert_manager_definition"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument logging_configuration", value=logging_configuration, expected_type=type_hints["logging_configuration"])
            check_type(argname="argument query_logging_configuration", value=query_logging_configuration, expected_type=type_hints["query_logging_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workspace_configuration", value=workspace_configuration, expected_type=type_hints["workspace_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alert_manager_definition is not None:
            self._values["alert_manager_definition"] = alert_manager_definition
        if alias is not None:
            self._values["alias"] = alias
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if query_logging_configuration is not None:
            self._values["query_logging_configuration"] = query_logging_configuration
        if tags is not None:
            self._values["tags"] = tags
        if workspace_configuration is not None:
            self._values["workspace_configuration"] = workspace_configuration

    @builtins.property
    def alert_manager_definition(self) -> typing.Optional[builtins.str]:
        '''The alert manager definition, a YAML configuration for the alert manager in your Amazon Managed Service for Prometheus workspace.

        For details about the alert manager definition, see `Creating an alert manager configuration files <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-alertmanager-config.html>`_ in the *Amazon Managed Service for Prometheus User Guide* .

        The following example shows part of a CloudFormation YAML file with an embedded alert manager definition (following the ``- |-`` ).

        ``Workspace: Type: AWS::APS::Workspace .... Properties: .... AlertManagerDefinition: Fn::Sub: - |- alertmanager_config: | templates: - 'default_template' route: receiver: example-sns receivers: - name: example-sns sns_configs: - topic_arn: 'arn:aws:sns:${AWS::Region}:${AWS::AccountId}:${TopicName}' -``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-alertmanagerdefinition
        '''
        result = self._values.get("alert_manager_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''The alias that is assigned to this workspace to help identify it.

        It does not need to be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-alias
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''(optional) The ARN for a customer managed AWS  key to use for encrypting data within your workspace.

        For more information about using your own key in your workspace, see `Encryption at rest <https://docs.aws.amazon.com/prometheus/latest/userguide/encryption-at-rest-Amazon-Service-Prometheus.html>`_ in the *Amazon Managed Service for Prometheus User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.LoggingConfigurationProperty"]]:
        '''Contains information about the logging configuration for the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-loggingconfiguration
        '''
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.LoggingConfigurationProperty"]], result)

    @builtins.property
    def query_logging_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.QueryLoggingConfigurationProperty"]]:
        '''The definition of logging configuration in an Amazon Managed Service for Prometheus workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-queryloggingconfiguration
        '''
        result = self._values.get("query_logging_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.QueryLoggingConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of tag keys and values that are associated with the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def workspace_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.WorkspaceConfigurationProperty"]]:
        '''Use this structure to define label sets and the ingestion limits for time series that match label sets, and to specify the retention period of the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-workspaceconfiguration
        '''
        result = self._values.get("workspace_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.WorkspaceConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkspaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWorkspacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnWorkspacePropsMixin",
):
    '''An Amazon Managed Service for Prometheus workspace is a logical and isolated Prometheus server dedicated to ingesting, storing, and querying your Prometheus-compatible metrics.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html
    :cloudformationResource: AWS::APS::Workspace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
        
        cfn_workspace_props_mixin = aps_mixins.CfnWorkspacePropsMixin(aps_mixins.CfnWorkspaceMixinProps(
            alert_manager_definition="alertManagerDefinition",
            alias="alias",
            kms_key_arn="kmsKeyArn",
            logging_configuration=aps_mixins.CfnWorkspacePropsMixin.LoggingConfigurationProperty(
                log_group_arn="logGroupArn"
            ),
            query_logging_configuration=aps_mixins.CfnWorkspacePropsMixin.QueryLoggingConfigurationProperty(
                destinations=[aps_mixins.CfnWorkspacePropsMixin.LoggingDestinationProperty(
                    cloud_watch_logs=aps_mixins.CfnWorkspacePropsMixin.CloudWatchLogDestinationProperty(
                        log_group_arn="logGroupArn"
                    ),
                    filters=aps_mixins.CfnWorkspacePropsMixin.LoggingFilterProperty(
                        qsp_threshold=123
                    )
                )]
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            workspace_configuration=aps_mixins.CfnWorkspacePropsMixin.WorkspaceConfigurationProperty(
                limits_per_label_sets=[aps_mixins.CfnWorkspacePropsMixin.LimitsPerLabelSetProperty(
                    label_set=[aps_mixins.CfnWorkspacePropsMixin.LabelProperty(
                        name="name",
                        value="value"
                    )],
                    limits=aps_mixins.CfnWorkspacePropsMixin.LimitsPerLabelSetEntryProperty(
                        max_series=123
                    )
                )],
                retention_period_in_days=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWorkspaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::APS::Workspace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880dcec5919ccaecd4a36d3d6c7021fb716c0fbf812edd43290668029876c21f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06b8c37006de9ea8b5140580a3248fd7792929cacf2b8bc2ef0287602b503972)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__268ba269700ef1b332765625009aad287e24e02d93bec829f2fbd1d3e62562a2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWorkspaceMixinProps:
        return typing.cast(CfnWorkspaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnWorkspacePropsMixin.CloudWatchLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_arn": "logGroupArn"},
    )
    class CloudWatchLogDestinationProperty:
        def __init__(
            self,
            *,
            log_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration details for logging to CloudWatch Logs.

            :param log_group_arn: The ARN of the CloudWatch log group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-cloudwatchlogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                cloud_watch_log_destination_property = aps_mixins.CfnWorkspacePropsMixin.CloudWatchLogDestinationProperty(
                    log_group_arn="logGroupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0892258f8dfcaa3a963cda9c6a7e6a08e5084bbd2d90801e701e6b2eca1c5ca1)
                check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_arn is not None:
                self._values["log_group_arn"] = log_group_arn

        @builtins.property
        def log_group_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the CloudWatch log group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-cloudwatchlogdestination.html#cfn-aps-workspace-cloudwatchlogdestination-loggrouparn
            '''
            result = self._values.get("log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnWorkspacePropsMixin.LabelProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class LabelProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A label is a name:value pair used to add context to ingested metrics.

            This structure defines the name and value for one label that is used in a label set. You can set ingestion limits on time series that match defined label sets, to help prevent a workspace from being overwhelmed with unexpected spikes in time series ingestion.

            :param name: The name for this label.
            :param value: The value for this label.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-label.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                label_property = aps_mixins.CfnWorkspacePropsMixin.LabelProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2be0c20bf1b1cab04f008c9bd42945a89529a1e809cefff1203a30f69d12cd47)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name for this label.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-label.html#cfn-aps-workspace-label-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value for this label.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-label.html#cfn-aps-workspace-label-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LabelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnWorkspacePropsMixin.LimitsPerLabelSetEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"max_series": "maxSeries"},
    )
    class LimitsPerLabelSetEntryProperty:
        def __init__(self, *, max_series: typing.Optional[jsii.Number] = None) -> None:
            '''This structure contains the limits that apply to time series that match one label set.

            :param max_series: The maximum number of active series that can be ingested that match this label set. Setting this to 0 causes no label set limit to be enforced, but it does cause Amazon Managed Service for Prometheus to vend label set metrics to CloudWatch

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-limitsperlabelsetentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                limits_per_label_set_entry_property = aps_mixins.CfnWorkspacePropsMixin.LimitsPerLabelSetEntryProperty(
                    max_series=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5877ad084c5421df21706df0810c1f122ed764a9cb3c2cf796079948b56b8ff)
                check_type(argname="argument max_series", value=max_series, expected_type=type_hints["max_series"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_series is not None:
                self._values["max_series"] = max_series

        @builtins.property
        def max_series(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of active series that can be ingested that match this label set.

            Setting this to 0 causes no label set limit to be enforced, but it does cause Amazon Managed Service for Prometheus to vend label set metrics to CloudWatch

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-limitsperlabelsetentry.html#cfn-aps-workspace-limitsperlabelsetentry-maxseries
            '''
            result = self._values.get("max_series")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LimitsPerLabelSetEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnWorkspacePropsMixin.LimitsPerLabelSetProperty",
        jsii_struct_bases=[],
        name_mapping={"label_set": "labelSet", "limits": "limits"},
    )
    class LimitsPerLabelSetProperty:
        def __init__(
            self,
            *,
            label_set: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.LabelProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.LimitsPerLabelSetEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This defines a label set for the workspace, and defines the ingestion limit for active time series that match that label set.

            Each label name in a label set must be unique.

            :param label_set: This defines one label set that will have an enforced ingestion limit. You can set ingestion limits on time series that match defined label sets, to help prevent a workspace from being overwhelmed with unexpected spikes in time series ingestion. Label values accept all UTF-8 characters with one exception. If the label name is metric name label ``__ *name* __`` , then the *metric* part of the name must conform to the following pattern: ``[a-zA-Z_:][a-zA-Z0-9_:]*``
            :param limits: This structure contains the information about the limits that apply to time series that match this label set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-limitsperlabelset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                limits_per_label_set_property = aps_mixins.CfnWorkspacePropsMixin.LimitsPerLabelSetProperty(
                    label_set=[aps_mixins.CfnWorkspacePropsMixin.LabelProperty(
                        name="name",
                        value="value"
                    )],
                    limits=aps_mixins.CfnWorkspacePropsMixin.LimitsPerLabelSetEntryProperty(
                        max_series=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ec051848c6c7f5c409fe9c04995823a2c508d40510b152b9a046a82f2bb535d)
                check_type(argname="argument label_set", value=label_set, expected_type=type_hints["label_set"])
                check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if label_set is not None:
                self._values["label_set"] = label_set
            if limits is not None:
                self._values["limits"] = limits

        @builtins.property
        def label_set(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.LabelProperty"]]]]:
            '''This defines one label set that will have an enforced ingestion limit.

            You can set ingestion limits on time series that match defined label sets, to help prevent a workspace from being overwhelmed with unexpected spikes in time series ingestion.

            Label values accept all UTF-8 characters with one exception. If the label name is metric name label ``__ *name* __`` , then the *metric* part of the name must conform to the following pattern: ``[a-zA-Z_:][a-zA-Z0-9_:]*``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-limitsperlabelset.html#cfn-aps-workspace-limitsperlabelset-labelset
            '''
            result = self._values.get("label_set")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.LabelProperty"]]]], result)

        @builtins.property
        def limits(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.LimitsPerLabelSetEntryProperty"]]:
            '''This structure contains the information about the limits that apply to time series that match this label set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-limitsperlabelset.html#cfn-aps-workspace-limitsperlabelset-limits
            '''
            result = self._values.get("limits")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.LimitsPerLabelSetEntryProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LimitsPerLabelSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnWorkspacePropsMixin.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_arn": "logGroupArn"},
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            log_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the rules and alerting logging configuration for the workspace.

            .. epigraph::

               These logging configurations are only for rules and alerting logs.

            :param log_group_arn: The ARN of the CloudWatch log group to which the vended log data will be published. This log group must exist prior to calling this operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-loggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                logging_configuration_property = aps_mixins.CfnWorkspacePropsMixin.LoggingConfigurationProperty(
                    log_group_arn="logGroupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fea4f87fea8da8bb57b2d0254858ec4448b17f6d8a35d5cf86762707682bd267)
                check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_arn is not None:
                self._values["log_group_arn"] = log_group_arn

        @builtins.property
        def log_group_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the CloudWatch log group to which the vended log data will be published.

            This log group must exist prior to calling this operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-loggingconfiguration.html#cfn-aps-workspace-loggingconfiguration-loggrouparn
            '''
            result = self._values.get("log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnWorkspacePropsMixin.LoggingDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_logs": "cloudWatchLogs", "filters": "filters"},
    )
    class LoggingDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.CloudWatchLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.LoggingFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The logging destination in an Amazon Managed Service for Prometheus workspace.

            :param cloud_watch_logs: Configuration details for logging to CloudWatch Logs.
            :param filters: Filtering criteria that determine which queries are logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-loggingdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                logging_destination_property = aps_mixins.CfnWorkspacePropsMixin.LoggingDestinationProperty(
                    cloud_watch_logs=aps_mixins.CfnWorkspacePropsMixin.CloudWatchLogDestinationProperty(
                        log_group_arn="logGroupArn"
                    ),
                    filters=aps_mixins.CfnWorkspacePropsMixin.LoggingFilterProperty(
                        qsp_threshold=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2fa33b34b92a550bc8d645d7d8a7a4ae2f985cb7d111be622923a739844678c)
                check_type(argname="argument cloud_watch_logs", value=cloud_watch_logs, expected_type=type_hints["cloud_watch_logs"])
                check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs is not None:
                self._values["cloud_watch_logs"] = cloud_watch_logs
            if filters is not None:
                self._values["filters"] = filters

        @builtins.property
        def cloud_watch_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.CloudWatchLogDestinationProperty"]]:
            '''Configuration details for logging to CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-loggingdestination.html#cfn-aps-workspace-loggingdestination-cloudwatchlogs
            '''
            result = self._values.get("cloud_watch_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.CloudWatchLogDestinationProperty"]], result)

        @builtins.property
        def filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.LoggingFilterProperty"]]:
            '''Filtering criteria that determine which queries are logged.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-loggingdestination.html#cfn-aps-workspace-loggingdestination-filters
            '''
            result = self._values.get("filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.LoggingFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnWorkspacePropsMixin.LoggingFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"qsp_threshold": "qspThreshold"},
    )
    class LoggingFilterProperty:
        def __init__(
            self,
            *,
            qsp_threshold: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Filtering criteria that determine which queries are logged.

            :param qsp_threshold: The Query Samples Processed (QSP) threshold above which queries will be logged. Queries processing more samples than this threshold will be captured in logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-loggingfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                logging_filter_property = aps_mixins.CfnWorkspacePropsMixin.LoggingFilterProperty(
                    qsp_threshold=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff9866769fdb083f4a8fce9e9ca21e36e3b91ee6a02b86b633b418df028ccb32)
                check_type(argname="argument qsp_threshold", value=qsp_threshold, expected_type=type_hints["qsp_threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if qsp_threshold is not None:
                self._values["qsp_threshold"] = qsp_threshold

        @builtins.property
        def qsp_threshold(self) -> typing.Optional[jsii.Number]:
            '''The Query Samples Processed (QSP) threshold above which queries will be logged.

            Queries processing more samples than this threshold will be captured in logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-loggingfilter.html#cfn-aps-workspace-loggingfilter-qspthreshold
            '''
            result = self._values.get("qsp_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnWorkspacePropsMixin.QueryLoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"destinations": "destinations"},
    )
    class QueryLoggingConfigurationProperty:
        def __init__(
            self,
            *,
            destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.LoggingDestinationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The query logging configuration in an Amazon Managed Service for Prometheus workspace.

            :param destinations: Defines a destination and its associated filtering criteria for query logging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-queryloggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                query_logging_configuration_property = aps_mixins.CfnWorkspacePropsMixin.QueryLoggingConfigurationProperty(
                    destinations=[aps_mixins.CfnWorkspacePropsMixin.LoggingDestinationProperty(
                        cloud_watch_logs=aps_mixins.CfnWorkspacePropsMixin.CloudWatchLogDestinationProperty(
                            log_group_arn="logGroupArn"
                        ),
                        filters=aps_mixins.CfnWorkspacePropsMixin.LoggingFilterProperty(
                            qsp_threshold=123
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4bb5723c52a67e1da8b4bbb9a5ccddcbf5557e35dab1cecf8d91ee03f7247ddb)
                check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destinations is not None:
                self._values["destinations"] = destinations

        @builtins.property
        def destinations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.LoggingDestinationProperty"]]]]:
            '''Defines a destination and its associated filtering criteria for query logging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-queryloggingconfiguration.html#cfn-aps-workspace-queryloggingconfiguration-destinations
            '''
            result = self._values.get("destinations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.LoggingDestinationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryLoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aps.mixins.CfnWorkspacePropsMixin.WorkspaceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "limits_per_label_sets": "limitsPerLabelSets",
            "retention_period_in_days": "retentionPeriodInDays",
        },
    )
    class WorkspaceConfigurationProperty:
        def __init__(
            self,
            *,
            limits_per_label_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspacePropsMixin.LimitsPerLabelSetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            retention_period_in_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Use this structure to define label sets and the ingestion limits for time series that match label sets, and to specify the retention period of the workspace.

            :param limits_per_label_sets: This is an array of structures, where each structure defines a label set for the workspace, and defines the ingestion limit for active time series for each of those label sets. Each label name in a label set must be unique.
            :param retention_period_in_days: Specifies how many days that metrics will be retained in the workspace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-workspaceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aps import mixins as aps_mixins
                
                workspace_configuration_property = aps_mixins.CfnWorkspacePropsMixin.WorkspaceConfigurationProperty(
                    limits_per_label_sets=[aps_mixins.CfnWorkspacePropsMixin.LimitsPerLabelSetProperty(
                        label_set=[aps_mixins.CfnWorkspacePropsMixin.LabelProperty(
                            name="name",
                            value="value"
                        )],
                        limits=aps_mixins.CfnWorkspacePropsMixin.LimitsPerLabelSetEntryProperty(
                            max_series=123
                        )
                    )],
                    retention_period_in_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aab1755c1ab3b8cb1ff3fa1c809e902d27552780d7f77201170e39848eeaa15b)
                check_type(argname="argument limits_per_label_sets", value=limits_per_label_sets, expected_type=type_hints["limits_per_label_sets"])
                check_type(argname="argument retention_period_in_days", value=retention_period_in_days, expected_type=type_hints["retention_period_in_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if limits_per_label_sets is not None:
                self._values["limits_per_label_sets"] = limits_per_label_sets
            if retention_period_in_days is not None:
                self._values["retention_period_in_days"] = retention_period_in_days

        @builtins.property
        def limits_per_label_sets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.LimitsPerLabelSetProperty"]]]]:
            '''This is an array of structures, where each structure defines a label set for the workspace, and defines the ingestion limit for active time series for each of those label sets.

            Each label name in a label set must be unique.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-workspaceconfiguration.html#cfn-aps-workspace-workspaceconfiguration-limitsperlabelsets
            '''
            result = self._values.get("limits_per_label_sets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspacePropsMixin.LimitsPerLabelSetProperty"]]]], result)

        @builtins.property
        def retention_period_in_days(self) -> typing.Optional[jsii.Number]:
            '''Specifies how many days that metrics will be retained in the workspace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-workspaceconfiguration.html#cfn-aps-workspace-workspaceconfiguration-retentionperiodindays
            '''
            result = self._values.get("retention_period_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkspaceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAnomalyDetectorMixinProps",
    "CfnAnomalyDetectorPropsMixin",
    "CfnResourcePolicyMixinProps",
    "CfnResourcePolicyPropsMixin",
    "CfnRuleGroupsNamespaceMixinProps",
    "CfnRuleGroupsNamespacePropsMixin",
    "CfnScraperApplicationLogs",
    "CfnScraperLogsMixin",
    "CfnScraperMixinProps",
    "CfnScraperPropsMixin",
    "CfnWorkspaceLogsMixin",
    "CfnWorkspaceManagedPrometheusLogs",
    "CfnWorkspaceMixinProps",
    "CfnWorkspacePropsMixin",
]

publication.publish()

def _typecheckingstub__11b7deb590d0ae343e9a176943be50687a901be15d8e1d1e2e02ed523ba122d4(
    *,
    alias: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.AnomalyDetectorConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    evaluation_interval_in_seconds: typing.Optional[jsii.Number] = None,
    labels: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.LabelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    missing_data_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.MissingDataActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    workspace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8702716b1fbae2e56f44e3fe4a2cf2dc228c14a9cccfdcc8d2e3a91363018407(
    props: typing.Union[CfnAnomalyDetectorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c609fb70f45c5f6d977800fd16f62b5142e44d54877cfbd941e7ddb2161932e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8d12f484188e9a954ae27858d6d03504d0feb3b6f46eb6ca1ed59a8036adfab(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649f8b0d5f5e6c4e8d2df6107f628ee1ac2e5aa8f1f96f67f2592925681092b9(
    *,
    random_cut_forest: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.RandomCutForestConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e9c5307cd938f9c45079e66827c1e78f9b08d8547c56240c731ad86ee6f710(
    *,
    amount: typing.Optional[jsii.Number] = None,
    ratio: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f4921859927c1c3763bb78ff22b97469b956a89c4c84815bcfa3a372ae4f9e(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f971bdd177370c8246d296b500d82f37138513f9a8587753ce4c5eabf435275(
    *,
    mark_as_anomaly: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    skip: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0205a9e5b8bbd221fa43419cedae36b9f4478601dc5aa727f48c50140f3b3cf0(
    *,
    ignore_near_expected_from_above: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ignore_near_expected_from_below: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalyDetectorPropsMixin.IgnoreNearExpectedProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    query: typing.Optional[builtins.str] = None,
    sample_size: typing.Optional[jsii.Number] = None,
    shingle_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f23ac0d180559c4cb60d36b402ecafef1638c358bb3a483f76f4455719b934(
    *,
    policy_document: typing.Optional[builtins.str] = None,
    workspace_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d03de09189422d30956319e7a5c75449cd96323eba270de5b4383774c1a262d(
    props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5b8e5728359196e764eb70911e6b5b019a13393e6a245329e0c91bae93c7b3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64dd7baed2a03330d2f5b485d7b789045120e08196f52ef76ed9b1dabf48aa1b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e585613b0693194d1c315b107c0229d5a6f74884fe9329c993ebb74bd28274ce(
    *,
    data: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    workspace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fdd425a867282b344348d88c22585596191967ed9a83967c038b08acade2f93(
    props: typing.Union[CfnRuleGroupsNamespaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834d94d2eb48ec71a5eaec35e2251dcdd42bae4aef71d6134b027fb3d6494827(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5133bdffcda0cb565097df0f031425472c7b6d1bc0af8a69aa9e6970816ab683(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e8bfbf23366cd4d2fcb156d3cfe7d3e49fc05493d06d1eaecbfa2aeafac6eb(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8faaf42ea1989615d04fec0892c111aad366c7c04f43d43485110fcc589a141(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab41c546ea59afb485cd9c68bc33525f52af138111541a35e75e1abbfcf6715(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a362522cbf61aebf6e4d0035367dee51c0a05859ba6adf683ed1fc458e850ece(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f32a2f6c46380703f7a914e07a120b36fb3b3f35335f17c9635961a2d38fe3(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddb2c52ceee4d4571854b1a516d5bb539da875832ae7e25d3a62883d2f1a015(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4e20e073a2bac812fdeff6efc7a7793c070392ad12a93a52e33826c2ca8162(
    *,
    alias: typing.Optional[builtins.str] = None,
    destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScraperPropsMixin.DestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScraperPropsMixin.RoleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scrape_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScraperPropsMixin.ScrapeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scraper_logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScraperPropsMixin.ScraperLoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScraperPropsMixin.SourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3d4fe30762978aba2c784fa45942828bf8d53dcc846f64cfbaad8fdccb007c(
    props: typing.Union[CfnScraperMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71dea35a63306df5542dbd13d651949de844b7213692ee5225c68547feabeff2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88056ffeb80f0b9fe5b7790014b5721cd7f49a86ea5b04ee28d4fea3af676083(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2a92763eedf3214d89defdba8207397d7487532f1345d81e7de1fe31f9ed2f(
    *,
    workspace_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6dc7b6ec3d81a983674f8e21a8f2765d5c225b818d84592727445eb1c456462(
    *,
    log_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52058ba8767163409c87d7c0b85a950195987a81dc113182b3e7b9bc005454e(
    *,
    options: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e47d525493346a949aad764cbd9bbc61bbc9b0f7579f9bed3a8fc30c831bda(
    *,
    amp_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScraperPropsMixin.AmpConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fbb20f19cfc4d6c311e40f4b351bd9ba72706b31c2a5b2085de58d23537f755(
    *,
    cluster_arn: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a8b2533626a7a87f4b1ac709f150c347cc43c02ee1dc039bdc0025fee7360e(
    *,
    source_role_arn: typing.Optional[builtins.str] = None,
    target_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7cc3d510fef1b62e3d6b00b8769965c86d3247faa511004534e6a9cac0784b(
    *,
    configuration_blob: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c067c2e0c68ec940309eec4ab2b9a3bcb11f8a64e11def9d4a87da42f51c9f8d(
    *,
    config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScraperPropsMixin.ComponentConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40dd826a760d5d825dcbc2f16eadf7fada388016832d17147069bf776c015f99(
    *,
    logging_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScraperPropsMixin.ScraperLoggingDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scraper_components: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScraperPropsMixin.ScraperComponentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505f5999414c5ccfb62f316f63887c2d59f223ec7752ec73da6b8997de89d29b(
    *,
    cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScraperPropsMixin.CloudWatchLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8542c74f93de6ef162db671889d9071262b2b57a0bf9e844586eff6bc6235da4(
    *,
    eks_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScraperPropsMixin.EksConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScraperPropsMixin.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18be14bfbee6dc5a68ca000c5bd6ab9e8a5292b346bd06219830be82917af731(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58584becf326ed4d54c694ac4a270a054b0b92378a11c73cb24b6743302026e(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a7fb4b14375528f681fcd590bbd342ad6a2659aacb1b07191cdc2d6394f190(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641fc12e6c2b4d158b5761019b8e856047de0a7bca46598a7115063bc8937365(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e749916f112bd00409213ec54e0ffa5491a9df279ab5c787916486daea914795(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59f933af36eff231b4f59a680c8b8e7852391cd62d37a7be9ff1a53cd773850(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51034a507649f14c4403b3d0c93d9e64691867c70fee095be1e9b397017ddec(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c30c64b6c80a313e0023822af9c1ae536138a881e1c82532526313af7b948750(
    *,
    alert_manager_definition: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    query_logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.QueryLoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    workspace_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.WorkspaceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880dcec5919ccaecd4a36d3d6c7021fb716c0fbf812edd43290668029876c21f(
    props: typing.Union[CfnWorkspaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b8c37006de9ea8b5140580a3248fd7792929cacf2b8bc2ef0287602b503972(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__268ba269700ef1b332765625009aad287e24e02d93bec829f2fbd1d3e62562a2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0892258f8dfcaa3a963cda9c6a7e6a08e5084bbd2d90801e701e6b2eca1c5ca1(
    *,
    log_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be0c20bf1b1cab04f008c9bd42945a89529a1e809cefff1203a30f69d12cd47(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5877ad084c5421df21706df0810c1f122ed764a9cb3c2cf796079948b56b8ff(
    *,
    max_series: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec051848c6c7f5c409fe9c04995823a2c508d40510b152b9a046a82f2bb535d(
    *,
    label_set: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.LabelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.LimitsPerLabelSetEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea4f87fea8da8bb57b2d0254858ec4448b17f6d8a35d5cf86762707682bd267(
    *,
    log_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2fa33b34b92a550bc8d645d7d8a7a4ae2f985cb7d111be622923a739844678c(
    *,
    cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.CloudWatchLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.LoggingFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9866769fdb083f4a8fce9e9ca21e36e3b91ee6a02b86b633b418df028ccb32(
    *,
    qsp_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb5723c52a67e1da8b4bbb9a5ccddcbf5557e35dab1cecf8d91ee03f7247ddb(
    *,
    destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.LoggingDestinationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab1755c1ab3b8cb1ff3fa1c809e902d27552780d7f77201170e39848eeaa15b(
    *,
    limits_per_label_sets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspacePropsMixin.LimitsPerLabelSetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    retention_period_in_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
