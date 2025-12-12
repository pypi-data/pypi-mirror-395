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
    jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnExperimentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "metric_goals": "metricGoals",
        "name": "name",
        "online_ab_config": "onlineAbConfig",
        "project": "project",
        "randomization_salt": "randomizationSalt",
        "remove_segment": "removeSegment",
        "running_status": "runningStatus",
        "sampling_rate": "samplingRate",
        "segment": "segment",
        "tags": "tags",
        "treatments": "treatments",
    },
)
class CfnExperimentMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        metric_goals: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentPropsMixin.MetricGoalObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        online_ab_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentPropsMixin.OnlineAbConfigObjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        project: typing.Optional[builtins.str] = None,
        randomization_salt: typing.Optional[builtins.str] = None,
        remove_segment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        running_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentPropsMixin.RunningStatusObjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sampling_rate: typing.Optional[jsii.Number] = None,
        segment: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        treatments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentPropsMixin.TreatmentObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnExperimentPropsMixin.

        :param description: An optional description of the experiment.
        :param metric_goals: An array of structures that defines the metrics used for the experiment, and whether a higher or lower value for each metric is the goal. You can use up to three metrics in an experiment.
        :param name: A name for the new experiment.
        :param online_ab_config: A structure that contains the configuration of which variation to use as the "control" version. The "control" version is used for comparison with other variations. This structure also specifies how much experiment traffic is allocated to each variation.
        :param project: The name or the ARN of the project where this experiment is to be created.
        :param randomization_salt: When Evidently assigns a particular user session to an experiment, it must use a randomization ID to determine which variation the user session is served. This randomization ID is a combination of the entity ID and ``randomizationSalt`` . If you omit ``randomizationSalt`` , Evidently uses the experiment name as the ``randomizationSalt`` .
        :param remove_segment: Set this to ``true`` to remove the segment that is associated with this experiment. You can't use this parameter if the experiment is currently running.
        :param running_status: A structure that you can use to start and stop the experiment.
        :param sampling_rate: The portion of the available audience that you want to allocate to this experiment, in thousandths of a percent. The available audience is the total audience minus the audience that you have allocated to overrides or current launches of this feature. This is represented in thousandths of a percent. For example, specify 10,000 to allocate 10% of the available audience.
        :param segment: Specifies an audience *segment* to use in the experiment. When a segment is used in an experiment, only user sessions that match the segment pattern are used in the experiment. For more information, see `Segment rule pattern syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html#CloudWatch-Evidently-segments-syntax>`_ .
        :param tags: Assigns one or more tags (key-value pairs) to the experiment. Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values. Tags don't have any semantic meaning to AWS and are interpreted strictly as strings of characters. You can associate as many as 50 tags with an experiment. For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ .
        :param treatments: An array of structures that describe the configuration of each feature variation used in the experiment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
            
            cfn_experiment_mixin_props = evidently_mixins.CfnExperimentMixinProps(
                description="description",
                metric_goals=[evidently_mixins.CfnExperimentPropsMixin.MetricGoalObjectProperty(
                    desired_change="desiredChange",
                    entity_id_key="entityIdKey",
                    event_pattern="eventPattern",
                    metric_name="metricName",
                    unit_label="unitLabel",
                    value_key="valueKey"
                )],
                name="name",
                online_ab_config=evidently_mixins.CfnExperimentPropsMixin.OnlineAbConfigObjectProperty(
                    control_treatment_name="controlTreatmentName",
                    treatment_weights=[evidently_mixins.CfnExperimentPropsMixin.TreatmentToWeightProperty(
                        split_weight=123,
                        treatment="treatment"
                    )]
                ),
                project="project",
                randomization_salt="randomizationSalt",
                remove_segment=False,
                running_status=evidently_mixins.CfnExperimentPropsMixin.RunningStatusObjectProperty(
                    analysis_complete_time="analysisCompleteTime",
                    desired_state="desiredState",
                    reason="reason",
                    status="status"
                ),
                sampling_rate=123,
                segment="segment",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                treatments=[evidently_mixins.CfnExperimentPropsMixin.TreatmentObjectProperty(
                    description="description",
                    feature="feature",
                    treatment_name="treatmentName",
                    variation="variation"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeea5cd39a17c48609bbb40a2be4cad2b01b3b71ae5e725de14b5dbb90cb997c)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument metric_goals", value=metric_goals, expected_type=type_hints["metric_goals"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument online_ab_config", value=online_ab_config, expected_type=type_hints["online_ab_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument randomization_salt", value=randomization_salt, expected_type=type_hints["randomization_salt"])
            check_type(argname="argument remove_segment", value=remove_segment, expected_type=type_hints["remove_segment"])
            check_type(argname="argument running_status", value=running_status, expected_type=type_hints["running_status"])
            check_type(argname="argument sampling_rate", value=sampling_rate, expected_type=type_hints["sampling_rate"])
            check_type(argname="argument segment", value=segment, expected_type=type_hints["segment"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument treatments", value=treatments, expected_type=type_hints["treatments"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if metric_goals is not None:
            self._values["metric_goals"] = metric_goals
        if name is not None:
            self._values["name"] = name
        if online_ab_config is not None:
            self._values["online_ab_config"] = online_ab_config
        if project is not None:
            self._values["project"] = project
        if randomization_salt is not None:
            self._values["randomization_salt"] = randomization_salt
        if remove_segment is not None:
            self._values["remove_segment"] = remove_segment
        if running_status is not None:
            self._values["running_status"] = running_status
        if sampling_rate is not None:
            self._values["sampling_rate"] = sampling_rate
        if segment is not None:
            self._values["segment"] = segment
        if tags is not None:
            self._values["tags"] = tags
        if treatments is not None:
            self._values["treatments"] = treatments

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the experiment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_goals(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentPropsMixin.MetricGoalObjectProperty"]]]]:
        '''An array of structures that defines the metrics used for the experiment, and whether a higher or lower value for each metric is the goal.

        You can use up to three metrics in an experiment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-metricgoals
        '''
        result = self._values.get("metric_goals")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentPropsMixin.MetricGoalObjectProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the new experiment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def online_ab_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentPropsMixin.OnlineAbConfigObjectProperty"]]:
        '''A structure that contains the configuration of which variation to use as the "control" version.

        The "control" version is used for comparison with other variations. This structure also specifies how much experiment traffic is allocated to each variation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-onlineabconfig
        '''
        result = self._values.get("online_ab_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentPropsMixin.OnlineAbConfigObjectProperty"]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The name or the ARN of the project where this experiment is to be created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-project
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def randomization_salt(self) -> typing.Optional[builtins.str]:
        '''When Evidently assigns a particular user session to an experiment, it must use a randomization ID to determine which variation the user session is served.

        This randomization ID is a combination of the entity ID and ``randomizationSalt`` . If you omit ``randomizationSalt`` , Evidently uses the experiment name as the ``randomizationSalt`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-randomizationsalt
        '''
        result = self._values.get("randomization_salt")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remove_segment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Set this to ``true`` to remove the segment that is associated with this experiment.

        You can't use this parameter if the experiment is currently running.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-removesegment
        '''
        result = self._values.get("remove_segment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def running_status(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentPropsMixin.RunningStatusObjectProperty"]]:
        '''A structure that you can use to start and stop the experiment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-runningstatus
        '''
        result = self._values.get("running_status")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentPropsMixin.RunningStatusObjectProperty"]], result)

    @builtins.property
    def sampling_rate(self) -> typing.Optional[jsii.Number]:
        '''The portion of the available audience that you want to allocate to this experiment, in thousandths of a percent.

        The available audience is the total audience minus the audience that you have allocated to overrides or current launches of this feature.

        This is represented in thousandths of a percent. For example, specify 10,000 to allocate 10% of the available audience.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-samplingrate
        '''
        result = self._values.get("sampling_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def segment(self) -> typing.Optional[builtins.str]:
        '''Specifies an audience *segment* to use in the experiment.

        When a segment is used in an experiment, only user sessions that match the segment pattern are used in the experiment.

        For more information, see `Segment rule pattern syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html#CloudWatch-Evidently-segments-syntax>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-segment
        '''
        result = self._values.get("segment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Assigns one or more tags (key-value pairs) to the experiment.

        Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values.

        Tags don't have any semantic meaning to AWS and are interpreted strictly as strings of characters.

        You can associate as many as 50 tags with an experiment.

        For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def treatments(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentPropsMixin.TreatmentObjectProperty"]]]]:
        '''An array of structures that describe the configuration of each feature variation used in the experiment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-treatments
        '''
        result = self._values.get("treatments")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentPropsMixin.TreatmentObjectProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnExperimentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnExperimentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnExperimentPropsMixin",
):
    '''Creates or updates an Evidently *experiment* .

    Before you create an experiment, you must create the feature to use for the experiment.

    An experiment helps you make feature design decisions based on evidence and data. An experiment can test as many as five variations at once. Evidently collects experiment data and analyzes it by statistical methods, and provides clear recommendations about which variations perform better.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html
    :cloudformationResource: AWS::Evidently::Experiment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
        
        cfn_experiment_props_mixin = evidently_mixins.CfnExperimentPropsMixin(evidently_mixins.CfnExperimentMixinProps(
            description="description",
            metric_goals=[evidently_mixins.CfnExperimentPropsMixin.MetricGoalObjectProperty(
                desired_change="desiredChange",
                entity_id_key="entityIdKey",
                event_pattern="eventPattern",
                metric_name="metricName",
                unit_label="unitLabel",
                value_key="valueKey"
            )],
            name="name",
            online_ab_config=evidently_mixins.CfnExperimentPropsMixin.OnlineAbConfigObjectProperty(
                control_treatment_name="controlTreatmentName",
                treatment_weights=[evidently_mixins.CfnExperimentPropsMixin.TreatmentToWeightProperty(
                    split_weight=123,
                    treatment="treatment"
                )]
            ),
            project="project",
            randomization_salt="randomizationSalt",
            remove_segment=False,
            running_status=evidently_mixins.CfnExperimentPropsMixin.RunningStatusObjectProperty(
                analysis_complete_time="analysisCompleteTime",
                desired_state="desiredState",
                reason="reason",
                status="status"
            ),
            sampling_rate=123,
            segment="segment",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            treatments=[evidently_mixins.CfnExperimentPropsMixin.TreatmentObjectProperty(
                description="description",
                feature="feature",
                treatment_name="treatmentName",
                variation="variation"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnExperimentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Evidently::Experiment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53619d5d076a0dd939433ffab9772e3f1511e351fa8b963afdbf2c4e5fa393a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__493db987056e54d0d7e80be5e84e7a2c232f6e712119d41e73959ac1fb60dfdc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78a56b005cfa7e292ca41a186560817686521b4527024a4f3d19af0b0f3c04b3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnExperimentMixinProps:
        return typing.cast(CfnExperimentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnExperimentPropsMixin.MetricGoalObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "desired_change": "desiredChange",
            "entity_id_key": "entityIdKey",
            "event_pattern": "eventPattern",
            "metric_name": "metricName",
            "unit_label": "unitLabel",
            "value_key": "valueKey",
        },
    )
    class MetricGoalObjectProperty:
        def __init__(
            self,
            *,
            desired_change: typing.Optional[builtins.str] = None,
            entity_id_key: typing.Optional[builtins.str] = None,
            event_pattern: typing.Optional[builtins.str] = None,
            metric_name: typing.Optional[builtins.str] = None,
            unit_label: typing.Optional[builtins.str] = None,
            value_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use this structure to tell Evidently whether higher or lower values are desired for a metric that is used in an experiment.

            :param desired_change: ``INCREASE`` means that a variation with a higher number for this metric is performing better. ``DECREASE`` means that a variation with a lower number for this metric is performing better.
            :param entity_id_key: The entity, such as a user or session, that does an action that causes a metric value to be recorded. An example is ``userDetails.userID`` .
            :param event_pattern: The EventBridge event pattern that defines how the metric is recorded. For more information about EventBridge event patterns, see `Amazon EventBridge event patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html>`_ .
            :param metric_name: A name for the metric. It can include up to 255 characters.
            :param unit_label: A label for the units that the metric is measuring.
            :param value_key: The JSON path to reference the numerical metric value in the event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-metricgoalobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                metric_goal_object_property = evidently_mixins.CfnExperimentPropsMixin.MetricGoalObjectProperty(
                    desired_change="desiredChange",
                    entity_id_key="entityIdKey",
                    event_pattern="eventPattern",
                    metric_name="metricName",
                    unit_label="unitLabel",
                    value_key="valueKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee2aa50a6aea30c04909bbc072d830294f90a3ae67ab36c0ec099ba60125a30e)
                check_type(argname="argument desired_change", value=desired_change, expected_type=type_hints["desired_change"])
                check_type(argname="argument entity_id_key", value=entity_id_key, expected_type=type_hints["entity_id_key"])
                check_type(argname="argument event_pattern", value=event_pattern, expected_type=type_hints["event_pattern"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument unit_label", value=unit_label, expected_type=type_hints["unit_label"])
                check_type(argname="argument value_key", value=value_key, expected_type=type_hints["value_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if desired_change is not None:
                self._values["desired_change"] = desired_change
            if entity_id_key is not None:
                self._values["entity_id_key"] = entity_id_key
            if event_pattern is not None:
                self._values["event_pattern"] = event_pattern
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if unit_label is not None:
                self._values["unit_label"] = unit_label
            if value_key is not None:
                self._values["value_key"] = value_key

        @builtins.property
        def desired_change(self) -> typing.Optional[builtins.str]:
            '''``INCREASE`` means that a variation with a higher number for this metric is performing better.

            ``DECREASE`` means that a variation with a lower number for this metric is performing better.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-metricgoalobject.html#cfn-evidently-experiment-metricgoalobject-desiredchange
            '''
            result = self._values.get("desired_change")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def entity_id_key(self) -> typing.Optional[builtins.str]:
            '''The entity, such as a user or session, that does an action that causes a metric value to be recorded.

            An example is ``userDetails.userID`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-metricgoalobject.html#cfn-evidently-experiment-metricgoalobject-entityidkey
            '''
            result = self._values.get("entity_id_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event_pattern(self) -> typing.Optional[builtins.str]:
            '''The EventBridge event pattern that defines how the metric is recorded.

            For more information about EventBridge event patterns, see `Amazon EventBridge event patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-metricgoalobject.html#cfn-evidently-experiment-metricgoalobject-eventpattern
            '''
            result = self._values.get("event_pattern")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''A name for the metric.

            It can include up to 255 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-metricgoalobject.html#cfn-evidently-experiment-metricgoalobject-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit_label(self) -> typing.Optional[builtins.str]:
            '''A label for the units that the metric is measuring.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-metricgoalobject.html#cfn-evidently-experiment-metricgoalobject-unitlabel
            '''
            result = self._values.get("unit_label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value_key(self) -> typing.Optional[builtins.str]:
            '''The JSON path to reference the numerical metric value in the event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-metricgoalobject.html#cfn-evidently-experiment-metricgoalobject-valuekey
            '''
            result = self._values.get("value_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricGoalObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnExperimentPropsMixin.OnlineAbConfigObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "control_treatment_name": "controlTreatmentName",
            "treatment_weights": "treatmentWeights",
        },
    )
    class OnlineAbConfigObjectProperty:
        def __init__(
            self,
            *,
            control_treatment_name: typing.Optional[builtins.str] = None,
            treatment_weights: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentPropsMixin.TreatmentToWeightProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A structure that contains the configuration of which variation to use as the "control" version.

            The "control" version is used for comparison with other variations. This structure also specifies how much experiment traffic is allocated to each variation.

            :param control_treatment_name: The name of the variation that is to be the default variation that the other variations are compared to.
            :param treatment_weights: A set of key-value pairs. The keys are treatment names, and the values are the portion of experiment traffic to be assigned to that treatment. Specify the traffic portion in thousandths of a percent, so 20,000 for a variation would allocate 20% of the experiment traffic to that variation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-onlineabconfigobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                online_ab_config_object_property = evidently_mixins.CfnExperimentPropsMixin.OnlineAbConfigObjectProperty(
                    control_treatment_name="controlTreatmentName",
                    treatment_weights=[evidently_mixins.CfnExperimentPropsMixin.TreatmentToWeightProperty(
                        split_weight=123,
                        treatment="treatment"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__555171b2fa358064daa8314cc501aa2efb2ba20bb3cda56f091ed2be17ad13ba)
                check_type(argname="argument control_treatment_name", value=control_treatment_name, expected_type=type_hints["control_treatment_name"])
                check_type(argname="argument treatment_weights", value=treatment_weights, expected_type=type_hints["treatment_weights"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if control_treatment_name is not None:
                self._values["control_treatment_name"] = control_treatment_name
            if treatment_weights is not None:
                self._values["treatment_weights"] = treatment_weights

        @builtins.property
        def control_treatment_name(self) -> typing.Optional[builtins.str]:
            '''The name of the variation that is to be the default variation that the other variations are compared to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-onlineabconfigobject.html#cfn-evidently-experiment-onlineabconfigobject-controltreatmentname
            '''
            result = self._values.get("control_treatment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def treatment_weights(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentPropsMixin.TreatmentToWeightProperty"]]]]:
            '''A set of key-value pairs.

            The keys are treatment names, and the values are the portion of experiment traffic to be assigned to that treatment. Specify the traffic portion in thousandths of a percent, so 20,000 for a variation would allocate 20% of the experiment traffic to that variation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-onlineabconfigobject.html#cfn-evidently-experiment-onlineabconfigobject-treatmentweights
            '''
            result = self._values.get("treatment_weights")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentPropsMixin.TreatmentToWeightProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnlineAbConfigObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnExperimentPropsMixin.RunningStatusObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "analysis_complete_time": "analysisCompleteTime",
            "desired_state": "desiredState",
            "reason": "reason",
            "status": "status",
        },
    )
    class RunningStatusObjectProperty:
        def __init__(
            self,
            *,
            analysis_complete_time: typing.Optional[builtins.str] = None,
            desired_state: typing.Optional[builtins.str] = None,
            reason: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use this structure to start and stop the experiment.

            :param analysis_complete_time: If you are using CloudFormation to start the experiment, use this field to specify when the experiment is to end. The format is as a UNIX timestamp. For more information about this format, see `The Current Epoch Unix Timestamp <https://docs.aws.amazon.com/https://www.unixtimestamp.com/index.php>`_ .
            :param desired_state: If you are using CloudFormation to stop this experiment, specify either ``COMPLETED`` or ``CANCELLED`` here to indicate how to classify this experiment.
            :param reason: If you are using CloudFormation to stop this experiment, this is an optional field that you can use to record why the experiment is being stopped or cancelled.
            :param status: To start the experiment now, specify ``START`` for this parameter. If this experiment is currently running and you want to stop it now, specify ``STOP`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-runningstatusobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                running_status_object_property = evidently_mixins.CfnExperimentPropsMixin.RunningStatusObjectProperty(
                    analysis_complete_time="analysisCompleteTime",
                    desired_state="desiredState",
                    reason="reason",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__16866767c40ed8d6e9698c152aedea43e331d759984b43f892059059389c321f)
                check_type(argname="argument analysis_complete_time", value=analysis_complete_time, expected_type=type_hints["analysis_complete_time"])
                check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
                check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if analysis_complete_time is not None:
                self._values["analysis_complete_time"] = analysis_complete_time
            if desired_state is not None:
                self._values["desired_state"] = desired_state
            if reason is not None:
                self._values["reason"] = reason
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def analysis_complete_time(self) -> typing.Optional[builtins.str]:
            '''If you are using CloudFormation to start the experiment, use this field to specify when the experiment is to end.

            The format is as a UNIX timestamp. For more information about this format, see `The Current Epoch Unix Timestamp <https://docs.aws.amazon.com/https://www.unixtimestamp.com/index.php>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-runningstatusobject.html#cfn-evidently-experiment-runningstatusobject-analysiscompletetime
            '''
            result = self._values.get("analysis_complete_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def desired_state(self) -> typing.Optional[builtins.str]:
            '''If you are using CloudFormation to stop this experiment, specify either ``COMPLETED`` or ``CANCELLED`` here to indicate how to classify this experiment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-runningstatusobject.html#cfn-evidently-experiment-runningstatusobject-desiredstate
            '''
            result = self._values.get("desired_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def reason(self) -> typing.Optional[builtins.str]:
            '''If you are using CloudFormation to stop this experiment, this is an optional field that you can use to record why the experiment is being stopped or cancelled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-runningstatusobject.html#cfn-evidently-experiment-runningstatusobject-reason
            '''
            result = self._values.get("reason")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''To start the experiment now, specify ``START`` for this parameter.

            If this experiment is currently running and you want to stop it now, specify ``STOP`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-runningstatusobject.html#cfn-evidently-experiment-runningstatusobject-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunningStatusObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnExperimentPropsMixin.TreatmentObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "feature": "feature",
            "treatment_name": "treatmentName",
            "variation": "variation",
        },
    )
    class TreatmentObjectProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            feature: typing.Optional[builtins.str] = None,
            treatment_name: typing.Optional[builtins.str] = None,
            variation: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that defines one treatment in an experiment.

            A treatment is a variation of the feature that you are including in the experiment.

            :param description: The description of the treatment.
            :param feature: The name of the feature for this experiment.
            :param treatment_name: A name for this treatment. It can include up to 127 characters.
            :param variation: The name of the variation to use for this treatment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmentobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                treatment_object_property = evidently_mixins.CfnExperimentPropsMixin.TreatmentObjectProperty(
                    description="description",
                    feature="feature",
                    treatment_name="treatmentName",
                    variation="variation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5546a9ea316102b07fb676f351e8a7a8f270850ab64f83063ee8bff9b2138d4b)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument feature", value=feature, expected_type=type_hints["feature"])
                check_type(argname="argument treatment_name", value=treatment_name, expected_type=type_hints["treatment_name"])
                check_type(argname="argument variation", value=variation, expected_type=type_hints["variation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if feature is not None:
                self._values["feature"] = feature
            if treatment_name is not None:
                self._values["treatment_name"] = treatment_name
            if variation is not None:
                self._values["variation"] = variation

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the treatment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmentobject.html#cfn-evidently-experiment-treatmentobject-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def feature(self) -> typing.Optional[builtins.str]:
            '''The name of the feature for this experiment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmentobject.html#cfn-evidently-experiment-treatmentobject-feature
            '''
            result = self._values.get("feature")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def treatment_name(self) -> typing.Optional[builtins.str]:
            '''A name for this treatment.

            It can include up to 127 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmentobject.html#cfn-evidently-experiment-treatmentobject-treatmentname
            '''
            result = self._values.get("treatment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def variation(self) -> typing.Optional[builtins.str]:
            '''The name of the variation to use for this treatment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmentobject.html#cfn-evidently-experiment-treatmentobject-variation
            '''
            result = self._values.get("variation")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TreatmentObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnExperimentPropsMixin.TreatmentToWeightProperty",
        jsii_struct_bases=[],
        name_mapping={"split_weight": "splitWeight", "treatment": "treatment"},
    )
    class TreatmentToWeightProperty:
        def __init__(
            self,
            *,
            split_weight: typing.Optional[jsii.Number] = None,
            treatment: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure defines how much experiment traffic to allocate to one treatment used in the experiment.

            :param split_weight: The portion of experiment traffic to allocate to this treatment. Specify the traffic portion in thousandths of a percent, so 20,000 allocated to a treatment would allocate 20% of the experiment traffic to that treatment.
            :param treatment: The name of the treatment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmenttoweight.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                treatment_to_weight_property = evidently_mixins.CfnExperimentPropsMixin.TreatmentToWeightProperty(
                    split_weight=123,
                    treatment="treatment"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc321f5957c432d96075bc08299084bfd43ff1ec702b456db4d74526feb9e2a9)
                check_type(argname="argument split_weight", value=split_weight, expected_type=type_hints["split_weight"])
                check_type(argname="argument treatment", value=treatment, expected_type=type_hints["treatment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if split_weight is not None:
                self._values["split_weight"] = split_weight
            if treatment is not None:
                self._values["treatment"] = treatment

        @builtins.property
        def split_weight(self) -> typing.Optional[jsii.Number]:
            '''The portion of experiment traffic to allocate to this treatment.

            Specify the traffic portion in thousandths of a percent, so 20,000 allocated to a treatment would allocate 20% of the experiment traffic to that treatment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmenttoweight.html#cfn-evidently-experiment-treatmenttoweight-splitweight
            '''
            result = self._values.get("split_weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def treatment(self) -> typing.Optional[builtins.str]:
            '''The name of the treatment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmenttoweight.html#cfn-evidently-experiment-treatmenttoweight-treatment
            '''
            result = self._values.get("treatment")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TreatmentToWeightProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnFeatureMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_variation": "defaultVariation",
        "description": "description",
        "entity_overrides": "entityOverrides",
        "evaluation_strategy": "evaluationStrategy",
        "name": "name",
        "project": "project",
        "tags": "tags",
        "variations": "variations",
    },
)
class CfnFeatureMixinProps:
    def __init__(
        self,
        *,
        default_variation: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        entity_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFeaturePropsMixin.EntityOverrideProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        evaluation_strategy: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        variations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFeaturePropsMixin.VariationObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnFeaturePropsMixin.

        :param default_variation: The name of the variation to use as the default variation. The default variation is served to users who are not allocated to any ongoing launches or experiments of this feature. This variation must also be listed in the ``Variations`` structure. If you omit ``DefaultVariation`` , the first variation listed in the ``Variations`` structure is used as the default variation.
        :param description: An optional description of the feature.
        :param entity_overrides: Specify users that should always be served a specific variation of a feature. Each user is specified by a key-value pair . For each key, specify a user by entering their user ID, account ID, or some other identifier. For the value, specify the name of the variation that they are to be served.
        :param evaluation_strategy: Specify ``ALL_RULES`` to activate the traffic allocation specified by any ongoing launches or experiments. Specify ``DEFAULT_VARIATION`` to serve the default variation to all users instead.
        :param name: The name for the feature. It can include up to 127 characters.
        :param project: The name or ARN of the project that is to contain the new feature.
        :param tags: Assigns one or more tags (key-value pairs) to the feature. Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values. Tags don't have any semantic meaning to AWS and are interpreted strictly as strings of characters. You can associate as many as 50 tags with a feature. For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ .
        :param variations: An array of structures that contain the configuration of the feature's different variations. Each ``VariationObject`` in the ``Variations`` array for a feature must have the same type of value ( ``BooleanValue`` , ``DoubleValue`` , ``LongValue`` or ``StringValue`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
            
            cfn_feature_mixin_props = evidently_mixins.CfnFeatureMixinProps(
                default_variation="defaultVariation",
                description="description",
                entity_overrides=[evidently_mixins.CfnFeaturePropsMixin.EntityOverrideProperty(
                    entity_id="entityId",
                    variation="variation"
                )],
                evaluation_strategy="evaluationStrategy",
                name="name",
                project="project",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                variations=[evidently_mixins.CfnFeaturePropsMixin.VariationObjectProperty(
                    boolean_value=False,
                    double_value=123,
                    long_value=123,
                    string_value="stringValue",
                    variation_name="variationName"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe8bdeac82e12a3cda682c589c3ee3ef6d50b2338ec1734ecb41c36867fe87c)
            check_type(argname="argument default_variation", value=default_variation, expected_type=type_hints["default_variation"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument entity_overrides", value=entity_overrides, expected_type=type_hints["entity_overrides"])
            check_type(argname="argument evaluation_strategy", value=evaluation_strategy, expected_type=type_hints["evaluation_strategy"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument variations", value=variations, expected_type=type_hints["variations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_variation is not None:
            self._values["default_variation"] = default_variation
        if description is not None:
            self._values["description"] = description
        if entity_overrides is not None:
            self._values["entity_overrides"] = entity_overrides
        if evaluation_strategy is not None:
            self._values["evaluation_strategy"] = evaluation_strategy
        if name is not None:
            self._values["name"] = name
        if project is not None:
            self._values["project"] = project
        if tags is not None:
            self._values["tags"] = tags
        if variations is not None:
            self._values["variations"] = variations

    @builtins.property
    def default_variation(self) -> typing.Optional[builtins.str]:
        '''The name of the variation to use as the default variation.

        The default variation is served to users who are not allocated to any ongoing launches or experiments of this feature.

        This variation must also be listed in the ``Variations`` structure.

        If you omit ``DefaultVariation`` , the first variation listed in the ``Variations`` structure is used as the default variation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-defaultvariation
        '''
        result = self._values.get("default_variation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the feature.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entity_overrides(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFeaturePropsMixin.EntityOverrideProperty"]]]]:
        '''Specify users that should always be served a specific variation of a feature.

        Each user is specified by a key-value pair . For each key, specify a user by entering their user ID, account ID, or some other identifier. For the value, specify the name of the variation that they are to be served.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-entityoverrides
        '''
        result = self._values.get("entity_overrides")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFeaturePropsMixin.EntityOverrideProperty"]]]], result)

    @builtins.property
    def evaluation_strategy(self) -> typing.Optional[builtins.str]:
        '''Specify ``ALL_RULES`` to activate the traffic allocation specified by any ongoing launches or experiments.

        Specify ``DEFAULT_VARIATION`` to serve the default variation to all users instead.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-evaluationstrategy
        '''
        result = self._values.get("evaluation_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the feature.

        It can include up to 127 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The name or ARN of the project that is to contain the new feature.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-project
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Assigns one or more tags (key-value pairs) to the feature.

        Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values.

        Tags don't have any semantic meaning to AWS and are interpreted strictly as strings of characters.

        You can associate as many as 50 tags with a feature.

        For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def variations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFeaturePropsMixin.VariationObjectProperty"]]]]:
        '''An array of structures that contain the configuration of the feature's different variations.

        Each ``VariationObject`` in the ``Variations`` array for a feature must have the same type of value ( ``BooleanValue`` , ``DoubleValue`` , ``LongValue`` or ``StringValue`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-variations
        '''
        result = self._values.get("variations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFeaturePropsMixin.VariationObjectProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFeatureMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFeaturePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnFeaturePropsMixin",
):
    '''Creates or updates an Evidently *feature* that you want to launch or test.

    You can define up to five variations of a feature, and use these variations in your launches and experiments. A feature must be created in a project. For information about creating a project, see `CreateProject <https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/API_CreateProject.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html
    :cloudformationResource: AWS::Evidently::Feature
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
        
        cfn_feature_props_mixin = evidently_mixins.CfnFeaturePropsMixin(evidently_mixins.CfnFeatureMixinProps(
            default_variation="defaultVariation",
            description="description",
            entity_overrides=[evidently_mixins.CfnFeaturePropsMixin.EntityOverrideProperty(
                entity_id="entityId",
                variation="variation"
            )],
            evaluation_strategy="evaluationStrategy",
            name="name",
            project="project",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            variations=[evidently_mixins.CfnFeaturePropsMixin.VariationObjectProperty(
                boolean_value=False,
                double_value=123,
                long_value=123,
                string_value="stringValue",
                variation_name="variationName"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFeatureMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Evidently::Feature``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f65cb2ad2cd23e83cc00070dafb89e03344ef2f57ffab167a3363eed81b65e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0503ad29218178a353e515037c61796ad360fc02302022a559fed9d6e8878c69)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db5127881905503418325062ea7bb20852adb9df47fa3ec6a025a8dea8c395b0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFeatureMixinProps:
        return typing.cast(CfnFeatureMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnFeaturePropsMixin.EntityOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={"entity_id": "entityId", "variation": "variation"},
    )
    class EntityOverrideProperty:
        def __init__(
            self,
            *,
            entity_id: typing.Optional[builtins.str] = None,
            variation: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A set of key-value pairs that specify users who should always be served a specific variation of a feature.

            Each key specifies a user using their user ID, account ID, or some other identifier. The value specifies the name of the variation that the user is to be served.

            :param entity_id: The entity ID to be served the variation specified in ``Variation`` .
            :param variation: The name of the variation to serve to the user session that matches the ``EntityId`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-entityoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                entity_override_property = evidently_mixins.CfnFeaturePropsMixin.EntityOverrideProperty(
                    entity_id="entityId",
                    variation="variation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fab216d35fc6f72e2790203e6ad798238111fcec45b240b915b1213132d3afa4)
                check_type(argname="argument entity_id", value=entity_id, expected_type=type_hints["entity_id"])
                check_type(argname="argument variation", value=variation, expected_type=type_hints["variation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entity_id is not None:
                self._values["entity_id"] = entity_id
            if variation is not None:
                self._values["variation"] = variation

        @builtins.property
        def entity_id(self) -> typing.Optional[builtins.str]:
            '''The entity ID to be served the variation specified in ``Variation`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-entityoverride.html#cfn-evidently-feature-entityoverride-entityid
            '''
            result = self._values.get("entity_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def variation(self) -> typing.Optional[builtins.str]:
            '''The name of the variation to serve to the user session that matches the ``EntityId`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-entityoverride.html#cfn-evidently-feature-entityoverride-variation
            '''
            result = self._values.get("variation")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EntityOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnFeaturePropsMixin.VariationObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_value": "booleanValue",
            "double_value": "doubleValue",
            "long_value": "longValue",
            "string_value": "stringValue",
            "variation_name": "variationName",
        },
    )
    class VariationObjectProperty:
        def __init__(
            self,
            *,
            boolean_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            double_value: typing.Optional[jsii.Number] = None,
            long_value: typing.Optional[jsii.Number] = None,
            string_value: typing.Optional[builtins.str] = None,
            variation_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure contains the name and variation value of one variation of a feature.

            It can contain only one of the following parameters: ``BooleanValue`` , ``DoubleValue`` , ``LongValue`` or ``StringValue`` .

            :param boolean_value: The value assigned to this variation, if the variation type is boolean.
            :param double_value: The value assigned to this variation, if the variation type is a double.
            :param long_value: The value assigned to this variation, if the variation type is a long.
            :param string_value: The value assigned to this variation, if the variation type is a string.
            :param variation_name: A name for the variation. It can include up to 127 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-variationobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                variation_object_property = evidently_mixins.CfnFeaturePropsMixin.VariationObjectProperty(
                    boolean_value=False,
                    double_value=123,
                    long_value=123,
                    string_value="stringValue",
                    variation_name="variationName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b2680a77b60c61119b8a07a8e099dc6c661a2403df24ce0c2ca7d3f143d9786c)
                check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
                check_type(argname="argument double_value", value=double_value, expected_type=type_hints["double_value"])
                check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
                check_type(argname="argument variation_name", value=variation_name, expected_type=type_hints["variation_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_value is not None:
                self._values["boolean_value"] = boolean_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if long_value is not None:
                self._values["long_value"] = long_value
            if string_value is not None:
                self._values["string_value"] = string_value
            if variation_name is not None:
                self._values["variation_name"] = variation_name

        @builtins.property
        def boolean_value(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The value assigned to this variation, if the variation type is boolean.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-variationobject.html#cfn-evidently-feature-variationobject-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def double_value(self) -> typing.Optional[jsii.Number]:
            '''The value assigned to this variation, if the variation type is a double.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-variationobject.html#cfn-evidently-feature-variationobject-doublevalue
            '''
            result = self._values.get("double_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def long_value(self) -> typing.Optional[jsii.Number]:
            '''The value assigned to this variation, if the variation type is a long.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-variationobject.html#cfn-evidently-feature-variationobject-longvalue
            '''
            result = self._values.get("long_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''The value assigned to this variation, if the variation type is a string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-variationobject.html#cfn-evidently-feature-variationobject-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def variation_name(self) -> typing.Optional[builtins.str]:
            '''A name for the variation.

            It can include up to 127 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-variationobject.html#cfn-evidently-feature-variationobject-variationname
            '''
            result = self._values.get("variation_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VariationObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnLaunchMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "execution_status": "executionStatus",
        "groups": "groups",
        "metric_monitors": "metricMonitors",
        "name": "name",
        "project": "project",
        "randomization_salt": "randomizationSalt",
        "scheduled_splits_config": "scheduledSplitsConfig",
        "tags": "tags",
    },
)
class CfnLaunchMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        execution_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchPropsMixin.ExecutionStatusObjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchPropsMixin.LaunchGroupObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        metric_monitors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchPropsMixin.MetricDefinitionObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        randomization_salt: typing.Optional[builtins.str] = None,
        scheduled_splits_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchPropsMixin.StepConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLaunchPropsMixin.

        :param description: An optional description for the launch.
        :param execution_status: A structure that you can use to start and stop the launch.
        :param groups: An array of structures that contains the feature and variations that are to be used for the launch. You can up to five launch groups in a launch.
        :param metric_monitors: An array of structures that define the metrics that will be used to monitor the launch performance. You can have up to three metric monitors in the array.
        :param name: The name for the launch. It can include up to 127 characters.
        :param project: The name or ARN of the project that you want to create the launch in.
        :param randomization_salt: When Evidently assigns a particular user session to a launch, it must use a randomization ID to determine which variation the user session is served. This randomization ID is a combination of the entity ID and ``randomizationSalt`` . If you omit ``randomizationSalt`` , Evidently uses the launch name as the ``randomizationsSalt`` .
        :param scheduled_splits_config: An array of structures that define the traffic allocation percentages among the feature variations during each step of the launch.
        :param tags: Assigns one or more tags (key-value pairs) to the launch. Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values. Tags don't have any semantic meaning to AWS and are interpreted strictly as strings of characters. You can associate as many as 50 tags with a launch. For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
            
            cfn_launch_mixin_props = evidently_mixins.CfnLaunchMixinProps(
                description="description",
                execution_status=evidently_mixins.CfnLaunchPropsMixin.ExecutionStatusObjectProperty(
                    desired_state="desiredState",
                    reason="reason",
                    status="status"
                ),
                groups=[evidently_mixins.CfnLaunchPropsMixin.LaunchGroupObjectProperty(
                    description="description",
                    feature="feature",
                    group_name="groupName",
                    variation="variation"
                )],
                metric_monitors=[evidently_mixins.CfnLaunchPropsMixin.MetricDefinitionObjectProperty(
                    entity_id_key="entityIdKey",
                    event_pattern="eventPattern",
                    metric_name="metricName",
                    unit_label="unitLabel",
                    value_key="valueKey"
                )],
                name="name",
                project="project",
                randomization_salt="randomizationSalt",
                scheduled_splits_config=[evidently_mixins.CfnLaunchPropsMixin.StepConfigProperty(
                    group_weights=[evidently_mixins.CfnLaunchPropsMixin.GroupToWeightProperty(
                        group_name="groupName",
                        split_weight=123
                    )],
                    segment_overrides=[evidently_mixins.CfnLaunchPropsMixin.SegmentOverrideProperty(
                        evaluation_order=123,
                        segment="segment",
                        weights=[evidently_mixins.CfnLaunchPropsMixin.GroupToWeightProperty(
                            group_name="groupName",
                            split_weight=123
                        )]
                    )],
                    start_time="startTime"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3425e3f8f2a603ef934ab4cec7751a142ed5c1319fad4569decdd7743d02d1b7)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_status", value=execution_status, expected_type=type_hints["execution_status"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument metric_monitors", value=metric_monitors, expected_type=type_hints["metric_monitors"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument randomization_salt", value=randomization_salt, expected_type=type_hints["randomization_salt"])
            check_type(argname="argument scheduled_splits_config", value=scheduled_splits_config, expected_type=type_hints["scheduled_splits_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if execution_status is not None:
            self._values["execution_status"] = execution_status
        if groups is not None:
            self._values["groups"] = groups
        if metric_monitors is not None:
            self._values["metric_monitors"] = metric_monitors
        if name is not None:
            self._values["name"] = name
        if project is not None:
            self._values["project"] = project
        if randomization_salt is not None:
            self._values["randomization_salt"] = randomization_salt
        if scheduled_splits_config is not None:
            self._values["scheduled_splits_config"] = scheduled_splits_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for the launch.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_status(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchPropsMixin.ExecutionStatusObjectProperty"]]:
        '''A structure that you can use to start and stop the launch.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-executionstatus
        '''
        result = self._values.get("execution_status")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchPropsMixin.ExecutionStatusObjectProperty"]], result)

    @builtins.property
    def groups(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchPropsMixin.LaunchGroupObjectProperty"]]]]:
        '''An array of structures that contains the feature and variations that are to be used for the launch.

        You can up to five launch groups in a launch.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-groups
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchPropsMixin.LaunchGroupObjectProperty"]]]], result)

    @builtins.property
    def metric_monitors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchPropsMixin.MetricDefinitionObjectProperty"]]]]:
        '''An array of structures that define the metrics that will be used to monitor the launch performance.

        You can have up to three metric monitors in the array.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-metricmonitors
        '''
        result = self._values.get("metric_monitors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchPropsMixin.MetricDefinitionObjectProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the launch.

        It can include up to 127 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The name or ARN of the project that you want to create the launch in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-project
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def randomization_salt(self) -> typing.Optional[builtins.str]:
        '''When Evidently assigns a particular user session to a launch, it must use a randomization ID to determine which variation the user session is served.

        This randomization ID is a combination of the entity ID and ``randomizationSalt`` . If you omit ``randomizationSalt`` , Evidently uses the launch name as the ``randomizationsSalt`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-randomizationsalt
        '''
        result = self._values.get("randomization_salt")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduled_splits_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchPropsMixin.StepConfigProperty"]]]]:
        '''An array of structures that define the traffic allocation percentages among the feature variations during each step of the launch.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-scheduledsplitsconfig
        '''
        result = self._values.get("scheduled_splits_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchPropsMixin.StepConfigProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Assigns one or more tags (key-value pairs) to the launch.

        Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values.

        Tags don't have any semantic meaning to AWS and are interpreted strictly as strings of characters.

        You can associate as many as 50 tags with a launch.

        For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLaunchMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLaunchPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnLaunchPropsMixin",
):
    '''Creates or updates a *launch* of a given feature.

    Before you create a launch, you must create the feature to use for the launch.

    You can use a launch to safely validate new features by serving them to a specified percentage of your users while you roll out the feature. You can monitor the performance of the new feature to help you decide when to ramp up traffic to more users. This helps you reduce risk and identify unintended consequences before you fully launch the feature.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html
    :cloudformationResource: AWS::Evidently::Launch
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
        
        cfn_launch_props_mixin = evidently_mixins.CfnLaunchPropsMixin(evidently_mixins.CfnLaunchMixinProps(
            description="description",
            execution_status=evidently_mixins.CfnLaunchPropsMixin.ExecutionStatusObjectProperty(
                desired_state="desiredState",
                reason="reason",
                status="status"
            ),
            groups=[evidently_mixins.CfnLaunchPropsMixin.LaunchGroupObjectProperty(
                description="description",
                feature="feature",
                group_name="groupName",
                variation="variation"
            )],
            metric_monitors=[evidently_mixins.CfnLaunchPropsMixin.MetricDefinitionObjectProperty(
                entity_id_key="entityIdKey",
                event_pattern="eventPattern",
                metric_name="metricName",
                unit_label="unitLabel",
                value_key="valueKey"
            )],
            name="name",
            project="project",
            randomization_salt="randomizationSalt",
            scheduled_splits_config=[evidently_mixins.CfnLaunchPropsMixin.StepConfigProperty(
                group_weights=[evidently_mixins.CfnLaunchPropsMixin.GroupToWeightProperty(
                    group_name="groupName",
                    split_weight=123
                )],
                segment_overrides=[evidently_mixins.CfnLaunchPropsMixin.SegmentOverrideProperty(
                    evaluation_order=123,
                    segment="segment",
                    weights=[evidently_mixins.CfnLaunchPropsMixin.GroupToWeightProperty(
                        group_name="groupName",
                        split_weight=123
                    )]
                )],
                start_time="startTime"
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
        props: typing.Union[CfnLaunchMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Evidently::Launch``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7a6587472b98b41b7148c59ccd86671436b343722b4b1cfca006c9b501c426)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d550110a07e17a93e6819e40a8067d8bbe4078ab1e8612ed4814b5b1cc8bcb0b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe50ed5d6530dfcc846573eea5efe14f444dea7e78bc292365ce78d721f1cfd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLaunchMixinProps:
        return typing.cast(CfnLaunchMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnLaunchPropsMixin.ExecutionStatusObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "desired_state": "desiredState",
            "reason": "reason",
            "status": "status",
        },
    )
    class ExecutionStatusObjectProperty:
        def __init__(
            self,
            *,
            desired_state: typing.Optional[builtins.str] = None,
            reason: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use this structure to start and stop the launch.

            :param desired_state: If you are using CloudFormation to stop this launch, specify either ``COMPLETED`` or ``CANCELLED`` here to indicate how to classify this experiment. If you omit this parameter, the default of ``COMPLETED`` is used.
            :param reason: If you are using CloudFormation to stop this launch, this is an optional field that you can use to record why the launch is being stopped or cancelled.
            :param status: To start the launch now, specify ``START`` for this parameter. If this launch is currently running and you want to stop it now, specify ``STOP`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-executionstatusobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                execution_status_object_property = evidently_mixins.CfnLaunchPropsMixin.ExecutionStatusObjectProperty(
                    desired_state="desiredState",
                    reason="reason",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be011ccbe466484ee59e90f4a9aa9cc4c101965c3b55f3079029c9303063719a)
                check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
                check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if desired_state is not None:
                self._values["desired_state"] = desired_state
            if reason is not None:
                self._values["reason"] = reason
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def desired_state(self) -> typing.Optional[builtins.str]:
            '''If you are using CloudFormation to stop this launch, specify either ``COMPLETED`` or ``CANCELLED`` here to indicate how to classify this experiment.

            If you omit this parameter, the default of ``COMPLETED`` is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-executionstatusobject.html#cfn-evidently-launch-executionstatusobject-desiredstate
            '''
            result = self._values.get("desired_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def reason(self) -> typing.Optional[builtins.str]:
            '''If you are using CloudFormation to stop this launch, this is an optional field that you can use to record why the launch is being stopped or cancelled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-executionstatusobject.html#cfn-evidently-launch-executionstatusobject-reason
            '''
            result = self._values.get("reason")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''To start the launch now, specify ``START`` for this parameter.

            If this launch is currently running and you want to stop it now, specify ``STOP`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-executionstatusobject.html#cfn-evidently-launch-executionstatusobject-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExecutionStatusObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnLaunchPropsMixin.GroupToWeightProperty",
        jsii_struct_bases=[],
        name_mapping={"group_name": "groupName", "split_weight": "splitWeight"},
    )
    class GroupToWeightProperty:
        def __init__(
            self,
            *,
            group_name: typing.Optional[builtins.str] = None,
            split_weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A structure containing the percentage of launch traffic to allocate to one launch group.

            :param group_name: The name of the launch group. It can include up to 127 characters.
            :param split_weight: The portion of launch traffic to allocate to this launch group. This is represented in thousandths of a percent. For example, specify 20,000 to allocate 20% of the launch audience to this launch group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-grouptoweight.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                group_to_weight_property = evidently_mixins.CfnLaunchPropsMixin.GroupToWeightProperty(
                    group_name="groupName",
                    split_weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ff20812c1e79e8507223c1764df9648dad5d2318960baa7ae3ee868edc9fd15)
                check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
                check_type(argname="argument split_weight", value=split_weight, expected_type=type_hints["split_weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_name is not None:
                self._values["group_name"] = group_name
            if split_weight is not None:
                self._values["split_weight"] = split_weight

        @builtins.property
        def group_name(self) -> typing.Optional[builtins.str]:
            '''The name of the launch group.

            It can include up to 127 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-grouptoweight.html#cfn-evidently-launch-grouptoweight-groupname
            '''
            result = self._values.get("group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def split_weight(self) -> typing.Optional[jsii.Number]:
            '''The portion of launch traffic to allocate to this launch group.

            This is represented in thousandths of a percent. For example, specify 20,000 to allocate 20% of the launch audience to this launch group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-grouptoweight.html#cfn-evidently-launch-grouptoweight-splitweight
            '''
            result = self._values.get("split_weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupToWeightProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnLaunchPropsMixin.LaunchGroupObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "feature": "feature",
            "group_name": "groupName",
            "variation": "variation",
        },
    )
    class LaunchGroupObjectProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            feature: typing.Optional[builtins.str] = None,
            group_name: typing.Optional[builtins.str] = None,
            variation: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that defines one launch group in a launch.

            A launch group is a variation of the feature that you are including in the launch.

            :param description: A description of the launch group.
            :param feature: The feature that this launch is using.
            :param group_name: A name for this launch group. It can include up to 127 characters.
            :param variation: The feature variation to use for this launch group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-launchgroupobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                launch_group_object_property = evidently_mixins.CfnLaunchPropsMixin.LaunchGroupObjectProperty(
                    description="description",
                    feature="feature",
                    group_name="groupName",
                    variation="variation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0404d94219a5e18deb3b16a72212ece68ab1e3b4400aa72e1a63a2ed3c5a4e7c)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument feature", value=feature, expected_type=type_hints["feature"])
                check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
                check_type(argname="argument variation", value=variation, expected_type=type_hints["variation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if feature is not None:
                self._values["feature"] = feature
            if group_name is not None:
                self._values["group_name"] = group_name
            if variation is not None:
                self._values["variation"] = variation

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the launch group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-launchgroupobject.html#cfn-evidently-launch-launchgroupobject-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def feature(self) -> typing.Optional[builtins.str]:
            '''The feature that this launch is using.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-launchgroupobject.html#cfn-evidently-launch-launchgroupobject-feature
            '''
            result = self._values.get("feature")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_name(self) -> typing.Optional[builtins.str]:
            '''A name for this launch group.

            It can include up to 127 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-launchgroupobject.html#cfn-evidently-launch-launchgroupobject-groupname
            '''
            result = self._values.get("group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def variation(self) -> typing.Optional[builtins.str]:
            '''The feature variation to use for this launch group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-launchgroupobject.html#cfn-evidently-launch-launchgroupobject-variation
            '''
            result = self._values.get("variation")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchGroupObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnLaunchPropsMixin.MetricDefinitionObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "entity_id_key": "entityIdKey",
            "event_pattern": "eventPattern",
            "metric_name": "metricName",
            "unit_label": "unitLabel",
            "value_key": "valueKey",
        },
    )
    class MetricDefinitionObjectProperty:
        def __init__(
            self,
            *,
            entity_id_key: typing.Optional[builtins.str] = None,
            event_pattern: typing.Optional[builtins.str] = None,
            metric_name: typing.Optional[builtins.str] = None,
            unit_label: typing.Optional[builtins.str] = None,
            value_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure defines a metric that you want to use to evaluate the variations during a launch or experiment.

            :param entity_id_key: The entity, such as a user or session, that does an action that causes a metric value to be recorded. An example is ``userDetails.userID`` .
            :param event_pattern: The EventBridge event pattern that defines how the metric is recorded. For more information about EventBridge event patterns, see `Amazon EventBridge event patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html>`_ .
            :param metric_name: A name for the metric. It can include up to 255 characters.
            :param unit_label: A label for the units that the metric is measuring.
            :param value_key: The value that is tracked to produce the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-metricdefinitionobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                metric_definition_object_property = evidently_mixins.CfnLaunchPropsMixin.MetricDefinitionObjectProperty(
                    entity_id_key="entityIdKey",
                    event_pattern="eventPattern",
                    metric_name="metricName",
                    unit_label="unitLabel",
                    value_key="valueKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d22793374d53c6f6e2e9bf8f1b4c82b644f3e5305fba1d542eb7091973c245f)
                check_type(argname="argument entity_id_key", value=entity_id_key, expected_type=type_hints["entity_id_key"])
                check_type(argname="argument event_pattern", value=event_pattern, expected_type=type_hints["event_pattern"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument unit_label", value=unit_label, expected_type=type_hints["unit_label"])
                check_type(argname="argument value_key", value=value_key, expected_type=type_hints["value_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entity_id_key is not None:
                self._values["entity_id_key"] = entity_id_key
            if event_pattern is not None:
                self._values["event_pattern"] = event_pattern
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if unit_label is not None:
                self._values["unit_label"] = unit_label
            if value_key is not None:
                self._values["value_key"] = value_key

        @builtins.property
        def entity_id_key(self) -> typing.Optional[builtins.str]:
            '''The entity, such as a user or session, that does an action that causes a metric value to be recorded.

            An example is ``userDetails.userID`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-metricdefinitionobject.html#cfn-evidently-launch-metricdefinitionobject-entityidkey
            '''
            result = self._values.get("entity_id_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event_pattern(self) -> typing.Optional[builtins.str]:
            '''The EventBridge event pattern that defines how the metric is recorded.

            For more information about EventBridge event patterns, see `Amazon EventBridge event patterns <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-metricdefinitionobject.html#cfn-evidently-launch-metricdefinitionobject-eventpattern
            '''
            result = self._values.get("event_pattern")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''A name for the metric.

            It can include up to 255 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-metricdefinitionobject.html#cfn-evidently-launch-metricdefinitionobject-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit_label(self) -> typing.Optional[builtins.str]:
            '''A label for the units that the metric is measuring.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-metricdefinitionobject.html#cfn-evidently-launch-metricdefinitionobject-unitlabel
            '''
            result = self._values.get("unit_label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value_key(self) -> typing.Optional[builtins.str]:
            '''The value that is tracked to produce the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-metricdefinitionobject.html#cfn-evidently-launch-metricdefinitionobject-valuekey
            '''
            result = self._values.get("value_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDefinitionObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnLaunchPropsMixin.SegmentOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={
            "evaluation_order": "evaluationOrder",
            "segment": "segment",
            "weights": "weights",
        },
    )
    class SegmentOverrideProperty:
        def __init__(
            self,
            *,
            evaluation_order: typing.Optional[jsii.Number] = None,
            segment: typing.Optional[builtins.str] = None,
            weights: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchPropsMixin.GroupToWeightProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Use this structure to specify different traffic splits for one or more audience *segments* .

            A segment is a portion of your audience that share one or more characteristics. Examples could be Chrome browser users, users in Europe, or Firefox browser users in Europe who also fit other criteria that your application collects, such as age.

            For more information, see `Use segments to focus your audience <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html>`_ .

            This sructure is an array of up to six segment override objects. Each of these objects specifies a segment that you have already created, and defines the traffic split for that segment.

            :param evaluation_order: A number indicating the order to use to evaluate segment overrides, if there are more than one. Segment overrides with lower numbers are evaluated first.
            :param segment: The ARN of the segment to use for this override.
            :param weights: The traffic allocation percentages among the feature variations to assign to this segment. This is a set of key-value pairs. The keys are variation names. The values represent the amount of traffic to allocate to that variation for this segment. This is expressed in thousandths of a percent, so a weight of 50000 represents 50% of traffic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-segmentoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                segment_override_property = evidently_mixins.CfnLaunchPropsMixin.SegmentOverrideProperty(
                    evaluation_order=123,
                    segment="segment",
                    weights=[evidently_mixins.CfnLaunchPropsMixin.GroupToWeightProperty(
                        group_name="groupName",
                        split_weight=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__392a0898409aa9f2bb506854102ba2362430d3a6bd6d826e839bb5f18575f7e8)
                check_type(argname="argument evaluation_order", value=evaluation_order, expected_type=type_hints["evaluation_order"])
                check_type(argname="argument segment", value=segment, expected_type=type_hints["segment"])
                check_type(argname="argument weights", value=weights, expected_type=type_hints["weights"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if evaluation_order is not None:
                self._values["evaluation_order"] = evaluation_order
            if segment is not None:
                self._values["segment"] = segment
            if weights is not None:
                self._values["weights"] = weights

        @builtins.property
        def evaluation_order(self) -> typing.Optional[jsii.Number]:
            '''A number indicating the order to use to evaluate segment overrides, if there are more than one.

            Segment overrides with lower numbers are evaluated first.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-segmentoverride.html#cfn-evidently-launch-segmentoverride-evaluationorder
            '''
            result = self._values.get("evaluation_order")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment(self) -> typing.Optional[builtins.str]:
            '''The ARN of the segment to use for this override.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-segmentoverride.html#cfn-evidently-launch-segmentoverride-segment
            '''
            result = self._values.get("segment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weights(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchPropsMixin.GroupToWeightProperty"]]]]:
            '''The traffic allocation percentages among the feature variations to assign to this segment.

            This is a set of key-value pairs. The keys are variation names. The values represent the amount of traffic to allocate to that variation for this segment. This is expressed in thousandths of a percent, so a weight of 50000 represents 50% of traffic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-segmentoverride.html#cfn-evidently-launch-segmentoverride-weights
            '''
            result = self._values.get("weights")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchPropsMixin.GroupToWeightProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SegmentOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnLaunchPropsMixin.StepConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "group_weights": "groupWeights",
            "segment_overrides": "segmentOverrides",
            "start_time": "startTime",
        },
    )
    class StepConfigProperty:
        def __init__(
            self,
            *,
            group_weights: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchPropsMixin.GroupToWeightProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            segment_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchPropsMixin.SegmentOverrideProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            start_time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that defines when each step of the launch is to start, and how much launch traffic is to be allocated to each variation during each step.

            :param group_weights: An array of structures that define how much launch traffic to allocate to each launch group during this step of the launch.
            :param segment_overrides: An array of structures that you can use to specify different traffic splits for one or more audience *segments* . A segment is a portion of your audience that share one or more characteristics. Examples could be Chrome browser users, users in Europe, or Firefox browser users in Europe who also fit other criteria that your application collects, such as age. For more information, see `Use segments to focus your audience <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html>`_ .
            :param start_time: The date and time to start this step of the launch. Use UTC format, ``yyyy-MM-ddTHH:mm:ssZ`` . For example, ``2025-11-25T23:59:59Z``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-stepconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                step_config_property = evidently_mixins.CfnLaunchPropsMixin.StepConfigProperty(
                    group_weights=[evidently_mixins.CfnLaunchPropsMixin.GroupToWeightProperty(
                        group_name="groupName",
                        split_weight=123
                    )],
                    segment_overrides=[evidently_mixins.CfnLaunchPropsMixin.SegmentOverrideProperty(
                        evaluation_order=123,
                        segment="segment",
                        weights=[evidently_mixins.CfnLaunchPropsMixin.GroupToWeightProperty(
                            group_name="groupName",
                            split_weight=123
                        )]
                    )],
                    start_time="startTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c7a91b04823ab2ad18e8f342309b926eae96cd859c4b243a426f0a185707c11f)
                check_type(argname="argument group_weights", value=group_weights, expected_type=type_hints["group_weights"])
                check_type(argname="argument segment_overrides", value=segment_overrides, expected_type=type_hints["segment_overrides"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_weights is not None:
                self._values["group_weights"] = group_weights
            if segment_overrides is not None:
                self._values["segment_overrides"] = segment_overrides
            if start_time is not None:
                self._values["start_time"] = start_time

        @builtins.property
        def group_weights(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchPropsMixin.GroupToWeightProperty"]]]]:
            '''An array of structures that define how much launch traffic to allocate to each launch group during this step of the launch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-stepconfig.html#cfn-evidently-launch-stepconfig-groupweights
            '''
            result = self._values.get("group_weights")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchPropsMixin.GroupToWeightProperty"]]]], result)

        @builtins.property
        def segment_overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchPropsMixin.SegmentOverrideProperty"]]]]:
            '''An array of structures that you can use to specify different traffic splits for one or more audience *segments* .

            A segment is a portion of your audience that share one or more characteristics. Examples could be Chrome browser users, users in Europe, or Firefox browser users in Europe who also fit other criteria that your application collects, such as age.

            For more information, see `Use segments to focus your audience <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-stepconfig.html#cfn-evidently-launch-stepconfig-segmentoverrides
            '''
            result = self._values.get("segment_overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchPropsMixin.SegmentOverrideProperty"]]]], result)

        @builtins.property
        def start_time(self) -> typing.Optional[builtins.str]:
            '''The date and time to start this step of the launch.

            Use UTC format, ``yyyy-MM-ddTHH:mm:ssZ`` . For example, ``2025-11-25T23:59:59Z``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-stepconfig.html#cfn-evidently-launch-stepconfig-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StepConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnProjectMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_config_resource": "appConfigResource",
        "data_delivery": "dataDelivery",
        "description": "description",
        "name": "name",
        "tags": "tags",
    },
)
class CfnProjectMixinProps:
    def __init__(
        self,
        *,
        app_config_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.AppConfigResourceObjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        data_delivery: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.DataDeliveryObjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnProjectPropsMixin.

        :param app_config_resource: Use this parameter if the project will use *client-side evaluation powered by AWS AppConfig* . Client-side evaluation allows your application to assign variations to user sessions locally instead of by calling the `EvaluateFeature <https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/API_EvaluateFeature.html>`_ operation. This mitigates the latency and availability risks that come with an API call. For more information, see `Use client-side evaluation - powered by AWS AppConfig . <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-client-side-evaluation.html>`_ This parameter is a structure that contains information about the AWS AppConfig application that will be used as for client-side evaluation. To create a project that uses client-side evaluation, you must have the ``evidently:ExportProjectAsConfiguration`` permission.
        :param data_delivery: A structure that contains information about where Evidently is to store evaluation events for longer term storage, if you choose to do so. If you choose not to store these events, Evidently deletes them after using them to produce metrics and other experiment results that you can view. You can't specify both ``CloudWatchLogs`` and ``S3Destination`` in the same operation.
        :param description: An optional description of the project.
        :param name: The name for the project. It can include up to 127 characters.
        :param tags: Assigns one or more tags (key-value pairs) to the project. Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values. Tags don't have any semantic meaning to AWS and are interpreted strictly as strings of characters. You can associate as many as 50 tags with a project. For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
            
            cfn_project_mixin_props = evidently_mixins.CfnProjectMixinProps(
                app_config_resource=evidently_mixins.CfnProjectPropsMixin.AppConfigResourceObjectProperty(
                    application_id="applicationId",
                    environment_id="environmentId"
                ),
                data_delivery=evidently_mixins.CfnProjectPropsMixin.DataDeliveryObjectProperty(
                    log_group="logGroup",
                    s3=evidently_mixins.CfnProjectPropsMixin.S3DestinationProperty(
                        bucket_name="bucketName",
                        prefix="prefix"
                    )
                ),
                description="description",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a288342cf4105fe36d00d4d58e9f106bb33667c8117f444dbe6c45a82d37c00)
            check_type(argname="argument app_config_resource", value=app_config_resource, expected_type=type_hints["app_config_resource"])
            check_type(argname="argument data_delivery", value=data_delivery, expected_type=type_hints["data_delivery"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_config_resource is not None:
            self._values["app_config_resource"] = app_config_resource
        if data_delivery is not None:
            self._values["data_delivery"] = data_delivery
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_config_resource(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.AppConfigResourceObjectProperty"]]:
        '''Use this parameter if the project will use *client-side evaluation powered by AWS AppConfig* .

        Client-side evaluation allows your application to assign variations to user sessions locally instead of by calling the `EvaluateFeature <https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/API_EvaluateFeature.html>`_ operation. This mitigates the latency and availability risks that come with an API call. For more information, see `Use client-side evaluation - powered by AWS AppConfig . <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-client-side-evaluation.html>`_

        This parameter is a structure that contains information about the AWS AppConfig application that will be used as for client-side evaluation.

        To create a project that uses client-side evaluation, you must have the ``evidently:ExportProjectAsConfiguration`` permission.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html#cfn-evidently-project-appconfigresource
        '''
        result = self._values.get("app_config_resource")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.AppConfigResourceObjectProperty"]], result)

    @builtins.property
    def data_delivery(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.DataDeliveryObjectProperty"]]:
        '''A structure that contains information about where Evidently is to store evaluation events for longer term storage, if you choose to do so.

        If you choose not to store these events, Evidently deletes them after using them to produce metrics and other experiment results that you can view.

        You can't specify both ``CloudWatchLogs`` and ``S3Destination`` in the same operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html#cfn-evidently-project-datadelivery
        '''
        result = self._values.get("data_delivery")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.DataDeliveryObjectProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html#cfn-evidently-project-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the project.

        It can include up to 127 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html#cfn-evidently-project-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Assigns one or more tags (key-value pairs) to the project.

        Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values.

        Tags don't have any semantic meaning to AWS and are interpreted strictly as strings of characters.

        You can associate as many as 50 tags with a project.

        For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html#cfn-evidently-project-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProjectPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnProjectPropsMixin",
):
    '''Creates a project, which is the logical object in Evidently that can contain features, launches, and experiments.

    Use projects to group similar features together.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html
    :cloudformationResource: AWS::Evidently::Project
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
        
        cfn_project_props_mixin = evidently_mixins.CfnProjectPropsMixin(evidently_mixins.CfnProjectMixinProps(
            app_config_resource=evidently_mixins.CfnProjectPropsMixin.AppConfigResourceObjectProperty(
                application_id="applicationId",
                environment_id="environmentId"
            ),
            data_delivery=evidently_mixins.CfnProjectPropsMixin.DataDeliveryObjectProperty(
                log_group="logGroup",
                s3=evidently_mixins.CfnProjectPropsMixin.S3DestinationProperty(
                    bucket_name="bucketName",
                    prefix="prefix"
                )
            ),
            description="description",
            name="name",
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
        props: typing.Union[CfnProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Evidently::Project``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c591f6b267dab20beb69827520e5647923d64f98499b8ecd920a0d6596ab535a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c785d84f0386a507219009e7046a69936701a7c86bf5c0f84ce66ddd35181b1b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd12450e606cd2ae8b6a08923f93136d912a69c577a986c60c13e50451e5090)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProjectMixinProps:
        return typing.cast(CfnProjectMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnProjectPropsMixin.AppConfigResourceObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_id": "applicationId",
            "environment_id": "environmentId",
        },
    )
    class AppConfigResourceObjectProperty:
        def __init__(
            self,
            *,
            application_id: typing.Optional[builtins.str] = None,
            environment_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This is a structure that defines the configuration of how your application integrates with AWS AppConfig to run client-side evaluation.

            :param application_id: The ID of the AWS AppConfig application to use for client-side evaluation.
            :param environment_id: The ID of the AWS AppConfig environment to use for client-side evaluation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-appconfigresourceobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                app_config_resource_object_property = evidently_mixins.CfnProjectPropsMixin.AppConfigResourceObjectProperty(
                    application_id="applicationId",
                    environment_id="environmentId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f05d0062f9edad84f7fd43de9aa738f9bd6f89028ec2d88b8c1b4b5d4ba3e500)
                check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
                check_type(argname="argument environment_id", value=environment_id, expected_type=type_hints["environment_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_id is not None:
                self._values["application_id"] = application_id
            if environment_id is not None:
                self._values["environment_id"] = environment_id

        @builtins.property
        def application_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the AWS AppConfig application to use for client-side evaluation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-appconfigresourceobject.html#cfn-evidently-project-appconfigresourceobject-applicationid
            '''
            result = self._values.get("application_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def environment_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the AWS AppConfig environment to use for client-side evaluation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-appconfigresourceobject.html#cfn-evidently-project-appconfigresourceobject-environmentid
            '''
            result = self._values.get("environment_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppConfigResourceObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnProjectPropsMixin.DataDeliveryObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group": "logGroup", "s3": "s3"},
    )
    class DataDeliveryObjectProperty:
        def __init__(
            self,
            *,
            log_group: typing.Optional[builtins.str] = None,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.S3DestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure that contains information about where Evidently is to store evaluation events for longer term storage.

            :param log_group: If the project stores evaluation events in CloudWatch Logs , this structure stores the log group name.
            :param s3: If the project stores evaluation events in an Amazon S3 bucket, this structure stores the bucket name and bucket prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-datadeliveryobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                data_delivery_object_property = evidently_mixins.CfnProjectPropsMixin.DataDeliveryObjectProperty(
                    log_group="logGroup",
                    s3=evidently_mixins.CfnProjectPropsMixin.S3DestinationProperty(
                        bucket_name="bucketName",
                        prefix="prefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6464ad5e83d14fd01ccc59ec2bff6d6ee937872f40aa559b7a33a34cdacd8214)
                check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group is not None:
                self._values["log_group"] = log_group
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def log_group(self) -> typing.Optional[builtins.str]:
            '''If the project stores evaluation events in CloudWatch Logs , this structure stores the log group name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-datadeliveryobject.html#cfn-evidently-project-datadeliveryobject-loggroup
            '''
            result = self._values.get("log_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.S3DestinationProperty"]]:
            '''If the project stores evaluation events in an Amazon S3 bucket, this structure stores the bucket name and bucket prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-datadeliveryobject.html#cfn-evidently-project-datadeliveryobject-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.S3DestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataDeliveryObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnProjectPropsMixin.S3DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "prefix": "prefix"},
    )
    class S3DestinationProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''If the project stores evaluation events in an Amazon S3 bucket, this structure stores the bucket name and bucket prefix.

            :param bucket_name: The name of the bucket in which Evidently stores evaluation events.
            :param prefix: The bucket prefix in which Evidently stores evaluation events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-s3destination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
                
                s3_destination_property = evidently_mixins.CfnProjectPropsMixin.S3DestinationProperty(
                    bucket_name="bucketName",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1526e57176858a178abced3c41a38a17ad03f1dca494518dc72a857edff09de9)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the bucket in which Evidently stores evaluation events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-s3destination.html#cfn-evidently-project-s3destination-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The bucket prefix in which Evidently stores evaluation events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-s3destination.html#cfn-evidently-project-s3destination-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnSegmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "pattern": "pattern",
        "tags": "tags",
    },
)
class CfnSegmentMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        pattern: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSegmentPropsMixin.

        :param description: An optional description for this segment.
        :param name: A name for the segment.
        :param pattern: The pattern to use for the segment. For more information about pattern syntax, see `Segment rule pattern syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html#CloudWatch-Evidently-segments-syntax>`_ .
        :param tags: Assigns one or more tags (key-value pairs) to the feature. Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values. Tags don't have any semantic meaning to AWS and are interpreted strictly as strings of characters. You can associate as many as 50 tags with a feature. For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-segment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
            
            cfn_segment_mixin_props = evidently_mixins.CfnSegmentMixinProps(
                description="description",
                name="name",
                pattern="pattern",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae644dbb502184b75ab0e461840a2e49097fca36aa8e042cf499a69f47094ab)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if pattern is not None:
            self._values["pattern"] = pattern
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for this segment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-segment.html#cfn-evidently-segment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the segment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-segment.html#cfn-evidently-segment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''The pattern to use for the segment.

        For more information about pattern syntax, see `Segment rule pattern syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html#CloudWatch-Evidently-segments-syntax>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-segment.html#cfn-evidently-segment-pattern
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Assigns one or more tags (key-value pairs) to the feature.

        Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values.

        Tags don't have any semantic meaning to AWS and are interpreted strictly as strings of characters.

        You can associate as many as 50 tags with a feature.

        For more information, see `Tagging AWS resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-segment.html#cfn-evidently-segment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSegmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSegmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_evidently.mixins.CfnSegmentPropsMixin",
):
    '''Creates or updates a *segment* of your audience.

    A segment is a portion of your audience that share one or more characteristics. Examples could be Chrome browser users, users in Europe, or Firefox browser users in Europe who also fit other criteria that your application collects, such as age.

    Using a segment in an experiment limits that experiment to evaluate only the users who match the segment criteria. Using one or more segments in a launch allow you to define different traffic splits for the different audience segments.

    For more information about segment pattern syntax, see `Segment rule pattern syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html#CloudWatch-Evidently-segments-syntax>`_ .

    The pattern that you define for a segment is matched against the value of ``evaluationContext`` , which is passed into Evidently in the `EvaluateFeature <https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/API_EvaluateFeature.html>`_ operation, when Evidently assigns a feature variation to a user.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-segment.html
    :cloudformationResource: AWS::Evidently::Segment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_evidently import mixins as evidently_mixins
        
        cfn_segment_props_mixin = evidently_mixins.CfnSegmentPropsMixin(evidently_mixins.CfnSegmentMixinProps(
            description="description",
            name="name",
            pattern="pattern",
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
        props: typing.Union[CfnSegmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Evidently::Segment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a6b844ec19c12091ec4c0b813bfe8af904b8cff907889260b38432504dd9fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41e873ea357d74dde5052304e414a994f65621f16b07ac6c71de5913f0b6de94)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95995b16a3a7c4bf44ed879e56998d8cbf709d2df15d360674aa257bd25038d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSegmentMixinProps:
        return typing.cast(CfnSegmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnExperimentMixinProps",
    "CfnExperimentPropsMixin",
    "CfnFeatureMixinProps",
    "CfnFeaturePropsMixin",
    "CfnLaunchMixinProps",
    "CfnLaunchPropsMixin",
    "CfnProjectMixinProps",
    "CfnProjectPropsMixin",
    "CfnSegmentMixinProps",
    "CfnSegmentPropsMixin",
]

publication.publish()

def _typecheckingstub__aeea5cd39a17c48609bbb40a2be4cad2b01b3b71ae5e725de14b5dbb90cb997c(
    *,
    description: typing.Optional[builtins.str] = None,
    metric_goals: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentPropsMixin.MetricGoalObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    online_ab_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentPropsMixin.OnlineAbConfigObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    project: typing.Optional[builtins.str] = None,
    randomization_salt: typing.Optional[builtins.str] = None,
    remove_segment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    running_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentPropsMixin.RunningStatusObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sampling_rate: typing.Optional[jsii.Number] = None,
    segment: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    treatments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentPropsMixin.TreatmentObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53619d5d076a0dd939433ffab9772e3f1511e351fa8b963afdbf2c4e5fa393a9(
    props: typing.Union[CfnExperimentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493db987056e54d0d7e80be5e84e7a2c232f6e712119d41e73959ac1fb60dfdc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a56b005cfa7e292ca41a186560817686521b4527024a4f3d19af0b0f3c04b3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2aa50a6aea30c04909bbc072d830294f90a3ae67ab36c0ec099ba60125a30e(
    *,
    desired_change: typing.Optional[builtins.str] = None,
    entity_id_key: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[builtins.str] = None,
    metric_name: typing.Optional[builtins.str] = None,
    unit_label: typing.Optional[builtins.str] = None,
    value_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555171b2fa358064daa8314cc501aa2efb2ba20bb3cda56f091ed2be17ad13ba(
    *,
    control_treatment_name: typing.Optional[builtins.str] = None,
    treatment_weights: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentPropsMixin.TreatmentToWeightProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16866767c40ed8d6e9698c152aedea43e331d759984b43f892059059389c321f(
    *,
    analysis_complete_time: typing.Optional[builtins.str] = None,
    desired_state: typing.Optional[builtins.str] = None,
    reason: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5546a9ea316102b07fb676f351e8a7a8f270850ab64f83063ee8bff9b2138d4b(
    *,
    description: typing.Optional[builtins.str] = None,
    feature: typing.Optional[builtins.str] = None,
    treatment_name: typing.Optional[builtins.str] = None,
    variation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc321f5957c432d96075bc08299084bfd43ff1ec702b456db4d74526feb9e2a9(
    *,
    split_weight: typing.Optional[jsii.Number] = None,
    treatment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe8bdeac82e12a3cda682c589c3ee3ef6d50b2338ec1734ecb41c36867fe87c(
    *,
    default_variation: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    entity_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFeaturePropsMixin.EntityOverrideProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    evaluation_strategy: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    variations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFeaturePropsMixin.VariationObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f65cb2ad2cd23e83cc00070dafb89e03344ef2f57ffab167a3363eed81b65e(
    props: typing.Union[CfnFeatureMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0503ad29218178a353e515037c61796ad360fc02302022a559fed9d6e8878c69(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5127881905503418325062ea7bb20852adb9df47fa3ec6a025a8dea8c395b0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab216d35fc6f72e2790203e6ad798238111fcec45b240b915b1213132d3afa4(
    *,
    entity_id: typing.Optional[builtins.str] = None,
    variation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2680a77b60c61119b8a07a8e099dc6c661a2403df24ce0c2ca7d3f143d9786c(
    *,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    double_value: typing.Optional[jsii.Number] = None,
    long_value: typing.Optional[jsii.Number] = None,
    string_value: typing.Optional[builtins.str] = None,
    variation_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3425e3f8f2a603ef934ab4cec7751a142ed5c1319fad4569decdd7743d02d1b7(
    *,
    description: typing.Optional[builtins.str] = None,
    execution_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchPropsMixin.ExecutionStatusObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchPropsMixin.LaunchGroupObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_monitors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchPropsMixin.MetricDefinitionObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    randomization_salt: typing.Optional[builtins.str] = None,
    scheduled_splits_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchPropsMixin.StepConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7a6587472b98b41b7148c59ccd86671436b343722b4b1cfca006c9b501c426(
    props: typing.Union[CfnLaunchMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d550110a07e17a93e6819e40a8067d8bbe4078ab1e8612ed4814b5b1cc8bcb0b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe50ed5d6530dfcc846573eea5efe14f444dea7e78bc292365ce78d721f1cfd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be011ccbe466484ee59e90f4a9aa9cc4c101965c3b55f3079029c9303063719a(
    *,
    desired_state: typing.Optional[builtins.str] = None,
    reason: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff20812c1e79e8507223c1764df9648dad5d2318960baa7ae3ee868edc9fd15(
    *,
    group_name: typing.Optional[builtins.str] = None,
    split_weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0404d94219a5e18deb3b16a72212ece68ab1e3b4400aa72e1a63a2ed3c5a4e7c(
    *,
    description: typing.Optional[builtins.str] = None,
    feature: typing.Optional[builtins.str] = None,
    group_name: typing.Optional[builtins.str] = None,
    variation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d22793374d53c6f6e2e9bf8f1b4c82b644f3e5305fba1d542eb7091973c245f(
    *,
    entity_id_key: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[builtins.str] = None,
    metric_name: typing.Optional[builtins.str] = None,
    unit_label: typing.Optional[builtins.str] = None,
    value_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392a0898409aa9f2bb506854102ba2362430d3a6bd6d826e839bb5f18575f7e8(
    *,
    evaluation_order: typing.Optional[jsii.Number] = None,
    segment: typing.Optional[builtins.str] = None,
    weights: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchPropsMixin.GroupToWeightProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a91b04823ab2ad18e8f342309b926eae96cd859c4b243a426f0a185707c11f(
    *,
    group_weights: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchPropsMixin.GroupToWeightProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    segment_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchPropsMixin.SegmentOverrideProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a288342cf4105fe36d00d4d58e9f106bb33667c8117f444dbe6c45a82d37c00(
    *,
    app_config_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.AppConfigResourceObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_delivery: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.DataDeliveryObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c591f6b267dab20beb69827520e5647923d64f98499b8ecd920a0d6596ab535a(
    props: typing.Union[CfnProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c785d84f0386a507219009e7046a69936701a7c86bf5c0f84ce66ddd35181b1b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd12450e606cd2ae8b6a08923f93136d912a69c577a986c60c13e50451e5090(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05d0062f9edad84f7fd43de9aa738f9bd6f89028ec2d88b8c1b4b5d4ba3e500(
    *,
    application_id: typing.Optional[builtins.str] = None,
    environment_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6464ad5e83d14fd01ccc59ec2bff6d6ee937872f40aa559b7a33a34cdacd8214(
    *,
    log_group: typing.Optional[builtins.str] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.S3DestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1526e57176858a178abced3c41a38a17ad03f1dca494518dc72a857edff09de9(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae644dbb502184b75ab0e461840a2e49097fca36aa8e042cf499a69f47094ab(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    pattern: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a6b844ec19c12091ec4c0b813bfe8af904b8cff907889260b38432504dd9fe(
    props: typing.Union[CfnSegmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e873ea357d74dde5052304e414a994f65621f16b07ac6c71de5913f0b6de94(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95995b16a3a7c4bf44ed879e56998d8cbf709d2df15d360674aa257bd25038d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
