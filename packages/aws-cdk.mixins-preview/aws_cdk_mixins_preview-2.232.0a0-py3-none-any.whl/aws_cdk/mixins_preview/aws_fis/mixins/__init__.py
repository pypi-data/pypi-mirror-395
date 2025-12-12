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
    jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnExperimentTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "description": "description",
        "experiment_options": "experimentOptions",
        "experiment_report_configuration": "experimentReportConfiguration",
        "log_configuration": "logConfiguration",
        "role_arn": "roleArn",
        "stop_conditions": "stopConditions",
        "tags": "tags",
        "targets": "targets",
    },
)
class CfnExperimentTemplateMixinProps:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentTemplatePropsMixin.ExperimentTemplateActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        experiment_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        experiment_report_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentReportConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentTemplatePropsMixin.ExperimentTemplateLogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        stop_conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentTemplatePropsMixin.ExperimentTemplateStopConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnExperimentTemplatePropsMixin.

        :param actions: The actions for the experiment.
        :param description: The description for the experiment template.
        :param experiment_options: The experiment options for an experiment template.
        :param experiment_report_configuration: Describes the report configuration for the experiment template.
        :param log_configuration: The configuration for experiment logging.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role.
        :param stop_conditions: The stop conditions for the experiment.
        :param tags: The tags for the experiment template.
        :param targets: The targets for the experiment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
            
            # cloud_watch_logs_configuration: Any
            # s3_configuration: Any
            
            cfn_experiment_template_mixin_props = fis_mixins.CfnExperimentTemplateMixinProps(
                actions={
                    "actions_key": fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateActionProperty(
                        action_id="actionId",
                        description="description",
                        parameters={
                            "parameters_key": "parameters"
                        },
                        start_after=["startAfter"],
                        targets={
                            "targets_key": "targets"
                        }
                    )
                },
                description="description",
                experiment_options=fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentOptionsProperty(
                    account_targeting="accountTargeting",
                    empty_target_resolution_mode="emptyTargetResolutionMode"
                ),
                experiment_report_configuration=fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentReportConfigurationProperty(
                    data_sources=fis_mixins.CfnExperimentTemplatePropsMixin.DataSourcesProperty(
                        cloud_watch_dashboards=[fis_mixins.CfnExperimentTemplatePropsMixin.CloudWatchDashboardProperty(
                            dashboard_identifier="dashboardIdentifier"
                        )]
                    ),
                    outputs=fis_mixins.CfnExperimentTemplatePropsMixin.OutputsProperty(
                        experiment_report_s3_configuration=fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentReportS3ConfigurationProperty(
                            bucket_name="bucketName",
                            prefix="prefix"
                        )
                    ),
                    post_experiment_duration="postExperimentDuration",
                    pre_experiment_duration="preExperimentDuration"
                ),
                log_configuration=fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateLogConfigurationProperty(
                    cloud_watch_logs_configuration=cloud_watch_logs_configuration,
                    log_schema_version=123,
                    s3_configuration=s3_configuration
                ),
                role_arn="roleArn",
                stop_conditions=[fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateStopConditionProperty(
                    source="source",
                    value="value"
                )],
                tags={
                    "tags_key": "tags"
                },
                targets={
                    "targets_key": fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetProperty(
                        filters=[fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetFilterProperty(
                            path="path",
                            values=["values"]
                        )],
                        parameters={
                            "parameters_key": "parameters"
                        },
                        resource_arns=["resourceArns"],
                        resource_tags={
                            "resource_tags_key": "resourceTags"
                        },
                        resource_type="resourceType",
                        selection_mode="selectionMode"
                    )
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__619b2c3c584e9865cba4d175029788c320c903938bde3c2b5dfc1d8acebe9b48)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument experiment_options", value=experiment_options, expected_type=type_hints["experiment_options"])
            check_type(argname="argument experiment_report_configuration", value=experiment_report_configuration, expected_type=type_hints["experiment_report_configuration"])
            check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stop_conditions", value=stop_conditions, expected_type=type_hints["stop_conditions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if description is not None:
            self._values["description"] = description
        if experiment_options is not None:
            self._values["experiment_options"] = experiment_options
        if experiment_report_configuration is not None:
            self._values["experiment_report_configuration"] = experiment_report_configuration
        if log_configuration is not None:
            self._values["log_configuration"] = log_configuration
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if stop_conditions is not None:
            self._values["stop_conditions"] = stop_conditions
        if tags is not None:
            self._values["tags"] = tags
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentTemplateActionProperty"]]]]:
        '''The actions for the experiment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentTemplateActionProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the experiment template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def experiment_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentOptionsProperty"]]:
        '''The experiment options for an experiment template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-experimentoptions
        '''
        result = self._values.get("experiment_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentOptionsProperty"]], result)

    @builtins.property
    def experiment_report_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentReportConfigurationProperty"]]:
        '''Describes the report configuration for the experiment template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-experimentreportconfiguration
        '''
        result = self._values.get("experiment_report_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentReportConfigurationProperty"]], result)

    @builtins.property
    def log_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentTemplateLogConfigurationProperty"]]:
        '''The configuration for experiment logging.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-logconfiguration
        '''
        result = self._values.get("log_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentTemplateLogConfigurationProperty"]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an IAM role.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stop_conditions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentTemplateStopConditionProperty"]]]]:
        '''The stop conditions for the experiment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-stopconditions
        '''
        result = self._values.get("stop_conditions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentTemplateStopConditionProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags for the experiment template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetProperty"]]]]:
        '''The targets for the experiment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-targets
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnExperimentTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnExperimentTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnExperimentTemplatePropsMixin",
):
    '''Specifies an experiment template.

    An experiment template includes the following components:

    - *Targets* : A target can be a specific resource in your AWS environment, or one or more resources that match criteria that you specify, for example, resources that have specific tags.
    - *Actions* : The actions to carry out on the target. You can specify multiple actions, the duration of each action, and when to start each action during an experiment.
    - *Stop conditions* : If a stop condition is triggered while an experiment is running, the experiment is automatically stopped. You can define a stop condition as a CloudWatch alarm.

    For more information, see `Experiment templates <https://docs.aws.amazon.com/fis/latest/userguide/experiment-templates.html>`_ in the *AWS Fault Injection Service User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html
    :cloudformationResource: AWS::FIS::ExperimentTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
        
        # cloud_watch_logs_configuration: Any
        # s3_configuration: Any
        
        cfn_experiment_template_props_mixin = fis_mixins.CfnExperimentTemplatePropsMixin(fis_mixins.CfnExperimentTemplateMixinProps(
            actions={
                "actions_key": fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateActionProperty(
                    action_id="actionId",
                    description="description",
                    parameters={
                        "parameters_key": "parameters"
                    },
                    start_after=["startAfter"],
                    targets={
                        "targets_key": "targets"
                    }
                )
            },
            description="description",
            experiment_options=fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentOptionsProperty(
                account_targeting="accountTargeting",
                empty_target_resolution_mode="emptyTargetResolutionMode"
            ),
            experiment_report_configuration=fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentReportConfigurationProperty(
                data_sources=fis_mixins.CfnExperimentTemplatePropsMixin.DataSourcesProperty(
                    cloud_watch_dashboards=[fis_mixins.CfnExperimentTemplatePropsMixin.CloudWatchDashboardProperty(
                        dashboard_identifier="dashboardIdentifier"
                    )]
                ),
                outputs=fis_mixins.CfnExperimentTemplatePropsMixin.OutputsProperty(
                    experiment_report_s3_configuration=fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentReportS3ConfigurationProperty(
                        bucket_name="bucketName",
                        prefix="prefix"
                    )
                ),
                post_experiment_duration="postExperimentDuration",
                pre_experiment_duration="preExperimentDuration"
            ),
            log_configuration=fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateLogConfigurationProperty(
                cloud_watch_logs_configuration=cloud_watch_logs_configuration,
                log_schema_version=123,
                s3_configuration=s3_configuration
            ),
            role_arn="roleArn",
            stop_conditions=[fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateStopConditionProperty(
                source="source",
                value="value"
            )],
            tags={
                "tags_key": "tags"
            },
            targets={
                "targets_key": fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetProperty(
                    filters=[fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetFilterProperty(
                        path="path",
                        values=["values"]
                    )],
                    parameters={
                        "parameters_key": "parameters"
                    },
                    resource_arns=["resourceArns"],
                    resource_tags={
                        "resource_tags_key": "resourceTags"
                    },
                    resource_type="resourceType",
                    selection_mode="selectionMode"
                )
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnExperimentTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FIS::ExperimentTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e693b4bffdbf76a948995070560813574083b21fa35e5cc9e211c1c04c3e9262)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc39d2b5238c2d90aa8ce82ed2daaa78377c3bcd5e11cc444ccf01d0248349be)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e905981e6cc3e839f5f17e4ecbe89f4d02cb4e037b2368f01dcafece55d904)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnExperimentTemplateMixinProps:
        return typing.cast(CfnExperimentTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnExperimentTemplatePropsMixin.CloudWatchDashboardProperty",
        jsii_struct_bases=[],
        name_mapping={"dashboard_identifier": "dashboardIdentifier"},
    )
    class CloudWatchDashboardProperty:
        def __init__(
            self,
            *,
            dashboard_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The CloudWatch dashboards to include as data sources in the experiment report.

            :param dashboard_identifier: The Amazon Resource Name (ARN) of the CloudWatch dashboard to include in the experiment report.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-cloudwatchdashboard.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
                
                cloud_watch_dashboard_property = fis_mixins.CfnExperimentTemplatePropsMixin.CloudWatchDashboardProperty(
                    dashboard_identifier="dashboardIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__84b8d7e5ae4c50f5393120d277736bc4a00973c657dd3084605b3b029001d177)
                check_type(argname="argument dashboard_identifier", value=dashboard_identifier, expected_type=type_hints["dashboard_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dashboard_identifier is not None:
                self._values["dashboard_identifier"] = dashboard_identifier

        @builtins.property
        def dashboard_identifier(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the CloudWatch dashboard to include in the experiment report.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-cloudwatchdashboard.html#cfn-fis-experimenttemplate-cloudwatchdashboard-dashboardidentifier
            '''
            result = self._values.get("dashboard_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchDashboardProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnExperimentTemplatePropsMixin.DataSourcesProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_dashboards": "cloudWatchDashboards"},
    )
    class DataSourcesProperty:
        def __init__(
            self,
            *,
            cloud_watch_dashboards: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentTemplatePropsMixin.CloudWatchDashboardProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Describes the data sources for the experiment report.

            :param cloud_watch_dashboards: The CloudWatch dashboards to include as data sources in the experiment report.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-datasources.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
                
                data_sources_property = fis_mixins.CfnExperimentTemplatePropsMixin.DataSourcesProperty(
                    cloud_watch_dashboards=[fis_mixins.CfnExperimentTemplatePropsMixin.CloudWatchDashboardProperty(
                        dashboard_identifier="dashboardIdentifier"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6873b2130eb0eec37215e5757c3ea59060a4fe8ce08343b7d93c85fd911d3cc3)
                check_type(argname="argument cloud_watch_dashboards", value=cloud_watch_dashboards, expected_type=type_hints["cloud_watch_dashboards"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_dashboards is not None:
                self._values["cloud_watch_dashboards"] = cloud_watch_dashboards

        @builtins.property
        def cloud_watch_dashboards(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.CloudWatchDashboardProperty"]]]]:
            '''The CloudWatch dashboards to include as data sources in the experiment report.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-datasources.html#cfn-fis-experimenttemplate-datasources-cloudwatchdashboards
            '''
            result = self._values.get("cloud_watch_dashboards")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.CloudWatchDashboardProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourcesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnExperimentTemplatePropsMixin.ExperimentReportS3ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "prefix": "prefix"},
    )
    class ExperimentReportS3ConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3 destination for the experiment report.

            :param bucket_name: The name of the S3 bucket where the experiment report will be stored.
            :param prefix: The prefix of the S3 bucket where the experiment report will be stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimentreports3configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
                
                experiment_report_s3_configuration_property = fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentReportS3ConfigurationProperty(
                    bucket_name="bucketName",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da593ab252b64178892325ec8175b825bdba1f31cdda3addcbf072d33dd7eb56)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket where the experiment report will be stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimentreports3configuration.html#cfn-fis-experimenttemplate-experimentreports3configuration-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix of the S3 bucket where the experiment report will be stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimentreports3configuration.html#cfn-fis-experimenttemplate-experimentreports3configuration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExperimentReportS3ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_id": "actionId",
            "description": "description",
            "parameters": "parameters",
            "start_after": "startAfter",
            "targets": "targets",
        },
    )
    class ExperimentTemplateActionProperty:
        def __init__(
            self,
            *,
            action_id: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            start_after: typing.Optional[typing.Sequence[builtins.str]] = None,
            targets: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies an action for an experiment template.

            For more information, see `Actions <https://docs.aws.amazon.com/fis/latest/userguide/actions.html>`_ in the *AWS Fault Injection Service User Guide* .

            :param action_id: The ID of the action.
            :param description: A description for the action.
            :param parameters: The parameters for the action.
            :param start_after: The name of the action that must be completed before the current action starts.
            :param targets: The targets for the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
                
                experiment_template_action_property = fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateActionProperty(
                    action_id="actionId",
                    description="description",
                    parameters={
                        "parameters_key": "parameters"
                    },
                    start_after=["startAfter"],
                    targets={
                        "targets_key": "targets"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc9993305a227d1a2897cc8851028d6433e470742cf8004bd062242819092696)
                check_type(argname="argument action_id", value=action_id, expected_type=type_hints["action_id"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument start_after", value=start_after, expected_type=type_hints["start_after"])
                check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_id is not None:
                self._values["action_id"] = action_id
            if description is not None:
                self._values["description"] = description
            if parameters is not None:
                self._values["parameters"] = parameters
            if start_after is not None:
                self._values["start_after"] = start_after
            if targets is not None:
                self._values["targets"] = targets

        @builtins.property
        def action_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateaction.html#cfn-fis-experimenttemplate-experimenttemplateaction-actionid
            '''
            result = self._values.get("action_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description for the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateaction.html#cfn-fis-experimenttemplate-experimenttemplateaction-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The parameters for the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateaction.html#cfn-fis-experimenttemplate-experimenttemplateaction-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def start_after(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The name of the action that must be completed before the current action starts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateaction.html#cfn-fis-experimenttemplate-experimenttemplateaction-startafter
            '''
            result = self._values.get("start_after")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def targets(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The targets for the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateaction.html#cfn-fis-experimenttemplate-experimenttemplateaction-targets
            '''
            result = self._values.get("targets")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExperimentTemplateActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_targeting": "accountTargeting",
            "empty_target_resolution_mode": "emptyTargetResolutionMode",
        },
    )
    class ExperimentTemplateExperimentOptionsProperty:
        def __init__(
            self,
            *,
            account_targeting: typing.Optional[builtins.str] = None,
            empty_target_resolution_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the experiment options for an experiment template.

            :param account_targeting: The account targeting setting for an experiment template.
            :param empty_target_resolution_mode: The empty target resolution mode for an experiment template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateexperimentoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
                
                experiment_template_experiment_options_property = fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentOptionsProperty(
                    account_targeting="accountTargeting",
                    empty_target_resolution_mode="emptyTargetResolutionMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8a0fb96bc20acd96d050be6bd08ba29d5e44ceca0442786b01ecf20b263eacf6)
                check_type(argname="argument account_targeting", value=account_targeting, expected_type=type_hints["account_targeting"])
                check_type(argname="argument empty_target_resolution_mode", value=empty_target_resolution_mode, expected_type=type_hints["empty_target_resolution_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_targeting is not None:
                self._values["account_targeting"] = account_targeting
            if empty_target_resolution_mode is not None:
                self._values["empty_target_resolution_mode"] = empty_target_resolution_mode

        @builtins.property
        def account_targeting(self) -> typing.Optional[builtins.str]:
            '''The account targeting setting for an experiment template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateexperimentoptions.html#cfn-fis-experimenttemplate-experimenttemplateexperimentoptions-accounttargeting
            '''
            result = self._values.get("account_targeting")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def empty_target_resolution_mode(self) -> typing.Optional[builtins.str]:
            '''The empty target resolution mode for an experiment template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateexperimentoptions.html#cfn-fis-experimenttemplate-experimenttemplateexperimentoptions-emptytargetresolutionmode
            '''
            result = self._values.get("empty_target_resolution_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExperimentTemplateExperimentOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentReportConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_sources": "dataSources",
            "outputs": "outputs",
            "post_experiment_duration": "postExperimentDuration",
            "pre_experiment_duration": "preExperimentDuration",
        },
    )
    class ExperimentTemplateExperimentReportConfigurationProperty:
        def __init__(
            self,
            *,
            data_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentTemplatePropsMixin.DataSourcesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            outputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentTemplatePropsMixin.OutputsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            post_experiment_duration: typing.Optional[builtins.str] = None,
            pre_experiment_duration: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the report configuration for the experiment template.

            :param data_sources: The data sources for the experiment report.
            :param outputs: The output destinations of the experiment report.
            :param post_experiment_duration: The duration after the experiment end time for the data sources to include in the report.
            :param pre_experiment_duration: The duration before the experiment start time for the data sources to include in the report.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateexperimentreportconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
                
                experiment_template_experiment_report_configuration_property = fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentReportConfigurationProperty(
                    data_sources=fis_mixins.CfnExperimentTemplatePropsMixin.DataSourcesProperty(
                        cloud_watch_dashboards=[fis_mixins.CfnExperimentTemplatePropsMixin.CloudWatchDashboardProperty(
                            dashboard_identifier="dashboardIdentifier"
                        )]
                    ),
                    outputs=fis_mixins.CfnExperimentTemplatePropsMixin.OutputsProperty(
                        experiment_report_s3_configuration=fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentReportS3ConfigurationProperty(
                            bucket_name="bucketName",
                            prefix="prefix"
                        )
                    ),
                    post_experiment_duration="postExperimentDuration",
                    pre_experiment_duration="preExperimentDuration"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9bbc10c37ae75b1ed698ae203ca3e50efbe51aa785842e5b0a8006da457169dc)
                check_type(argname="argument data_sources", value=data_sources, expected_type=type_hints["data_sources"])
                check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
                check_type(argname="argument post_experiment_duration", value=post_experiment_duration, expected_type=type_hints["post_experiment_duration"])
                check_type(argname="argument pre_experiment_duration", value=pre_experiment_duration, expected_type=type_hints["pre_experiment_duration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_sources is not None:
                self._values["data_sources"] = data_sources
            if outputs is not None:
                self._values["outputs"] = outputs
            if post_experiment_duration is not None:
                self._values["post_experiment_duration"] = post_experiment_duration
            if pre_experiment_duration is not None:
                self._values["pre_experiment_duration"] = pre_experiment_duration

        @builtins.property
        def data_sources(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.DataSourcesProperty"]]:
            '''The data sources for the experiment report.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateexperimentreportconfiguration.html#cfn-fis-experimenttemplate-experimenttemplateexperimentreportconfiguration-datasources
            '''
            result = self._values.get("data_sources")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.DataSourcesProperty"]], result)

        @builtins.property
        def outputs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.OutputsProperty"]]:
            '''The output destinations of the experiment report.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateexperimentreportconfiguration.html#cfn-fis-experimenttemplate-experimenttemplateexperimentreportconfiguration-outputs
            '''
            result = self._values.get("outputs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.OutputsProperty"]], result)

        @builtins.property
        def post_experiment_duration(self) -> typing.Optional[builtins.str]:
            '''The duration after the experiment end time for the data sources to include in the report.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateexperimentreportconfiguration.html#cfn-fis-experimenttemplate-experimenttemplateexperimentreportconfiguration-postexperimentduration
            '''
            result = self._values.get("post_experiment_duration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pre_experiment_duration(self) -> typing.Optional[builtins.str]:
            '''The duration before the experiment start time for the data sources to include in the report.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateexperimentreportconfiguration.html#cfn-fis-experimenttemplate-experimenttemplateexperimentreportconfiguration-preexperimentduration
            '''
            result = self._values.get("pre_experiment_duration")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExperimentTemplateExperimentReportConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateLogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_configuration": "cloudWatchLogsConfiguration",
            "log_schema_version": "logSchemaVersion",
            "s3_configuration": "s3Configuration",
        },
    )
    class ExperimentTemplateLogConfigurationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_configuration: typing.Any = None,
            log_schema_version: typing.Optional[jsii.Number] = None,
            s3_configuration: typing.Any = None,
        ) -> None:
            '''Specifies the configuration for experiment logging.

            For more information, see `Experiment logging <https://docs.aws.amazon.com/fis/latest/userguide/monitoring-logging.html>`_ in the *AWS Fault Injection Service User Guide* .

            :param cloud_watch_logs_configuration: The configuration for experiment logging to CloudWatch Logs .
            :param log_schema_version: The schema version.
            :param s3_configuration: The configuration for experiment logging to Amazon S3 .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatelogconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
                
                # cloud_watch_logs_configuration: Any
                # s3_configuration: Any
                
                experiment_template_log_configuration_property = fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateLogConfigurationProperty(
                    cloud_watch_logs_configuration=cloud_watch_logs_configuration,
                    log_schema_version=123,
                    s3_configuration=s3_configuration
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b4e8d3badbfb15490a78e03b4f03745f6d99b263631bd7eb0bdf526f56473903)
                check_type(argname="argument cloud_watch_logs_configuration", value=cloud_watch_logs_configuration, expected_type=type_hints["cloud_watch_logs_configuration"])
                check_type(argname="argument log_schema_version", value=log_schema_version, expected_type=type_hints["log_schema_version"])
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_configuration is not None:
                self._values["cloud_watch_logs_configuration"] = cloud_watch_logs_configuration
            if log_schema_version is not None:
                self._values["log_schema_version"] = log_schema_version
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration

        @builtins.property
        def cloud_watch_logs_configuration(self) -> typing.Any:
            '''The configuration for experiment logging to CloudWatch Logs .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatelogconfiguration.html#cfn-fis-experimenttemplate-experimenttemplatelogconfiguration-cloudwatchlogsconfiguration
            '''
            result = self._values.get("cloud_watch_logs_configuration")
            return typing.cast(typing.Any, result)

        @builtins.property
        def log_schema_version(self) -> typing.Optional[jsii.Number]:
            '''The schema version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatelogconfiguration.html#cfn-fis-experimenttemplate-experimenttemplatelogconfiguration-logschemaversion
            '''
            result = self._values.get("log_schema_version")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def s3_configuration(self) -> typing.Any:
            '''The configuration for experiment logging to Amazon S3 .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatelogconfiguration.html#cfn-fis-experimenttemplate-experimenttemplatelogconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExperimentTemplateLogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateStopConditionProperty",
        jsii_struct_bases=[],
        name_mapping={"source": "source", "value": "value"},
    )
    class ExperimentTemplateStopConditionProperty:
        def __init__(
            self,
            *,
            source: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a stop condition for an experiment template.

            For more information, see `Stop conditions <https://docs.aws.amazon.com/fis/latest/userguide/stop-conditions.html>`_ in the *AWS Fault Injection Service User Guide* .

            :param source: The source for the stop condition.
            :param value: The Amazon Resource Name (ARN) of the CloudWatch alarm, if applicable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatestopcondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
                
                experiment_template_stop_condition_property = fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateStopConditionProperty(
                    source="source",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc0c7d9d592cf120b1d12901d7026c86fa7bf5701ae4b78e79df6a72d7013832)
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source is not None:
                self._values["source"] = source
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The source for the stop condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatestopcondition.html#cfn-fis-experimenttemplate-experimenttemplatestopcondition-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the CloudWatch alarm, if applicable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatestopcondition.html#cfn-fis-experimenttemplate-experimenttemplatestopcondition-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExperimentTemplateStopConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"path": "path", "values": "values"},
    )
    class ExperimentTemplateTargetFilterProperty:
        def __init__(
            self,
            *,
            path: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies a filter used for the target resource input in an experiment template.

            For more information, see `Resource filters <https://docs.aws.amazon.com/fis/latest/userguide/targets.html#target-filters>`_ in the *AWS Fault Injection Service User Guide* .

            :param path: The attribute path for the filter.
            :param values: The attribute values for the filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetargetfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
                
                experiment_template_target_filter_property = fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetFilterProperty(
                    path="path",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6824f5224585bf2bf4f8be9cc97dc7b704589161a6522df3324824053ab380aa)
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if path is not None:
                self._values["path"] = path
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The attribute path for the filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetargetfilter.html#cfn-fis-experimenttemplate-experimenttemplatetargetfilter-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The attribute values for the filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetargetfilter.html#cfn-fis-experimenttemplate-experimenttemplatetargetfilter-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExperimentTemplateTargetFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "filters": "filters",
            "parameters": "parameters",
            "resource_arns": "resourceArns",
            "resource_tags": "resourceTags",
            "resource_type": "resourceType",
            "selection_mode": "selectionMode",
        },
    )
    class ExperimentTemplateTargetProperty:
        def __init__(
            self,
            *,
            filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            resource_tags: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            resource_type: typing.Optional[builtins.str] = None,
            selection_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a target for an experiment.

            You must specify at least one Amazon Resource Name (ARN) or at least one resource tag. You cannot specify both ARNs and tags.

            For more information, see `Targets <https://docs.aws.amazon.com/fis/latest/userguide/targets.html>`_ in the *AWS Fault Injection Service User Guide* .

            :param filters: The filters to apply to identify target resources using specific attributes.
            :param parameters: The parameters for the resource type.
            :param resource_arns: The Amazon Resource Names (ARNs) of the targets.
            :param resource_tags: The tags for the target resources.
            :param resource_type: The resource type.
            :param selection_mode: Scopes the identified resources to a specific count or percentage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
                
                experiment_template_target_property = fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetProperty(
                    filters=[fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetFilterProperty(
                        path="path",
                        values=["values"]
                    )],
                    parameters={
                        "parameters_key": "parameters"
                    },
                    resource_arns=["resourceArns"],
                    resource_tags={
                        "resource_tags_key": "resourceTags"
                    },
                    resource_type="resourceType",
                    selection_mode="selectionMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c888eaeb73d6da40379dba2c785497ae59be5afed86f35c81e056b17777eaa9)
                check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
                check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
                check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                check_type(argname="argument selection_mode", value=selection_mode, expected_type=type_hints["selection_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filters is not None:
                self._values["filters"] = filters
            if parameters is not None:
                self._values["parameters"] = parameters
            if resource_arns is not None:
                self._values["resource_arns"] = resource_arns
            if resource_tags is not None:
                self._values["resource_tags"] = resource_tags
            if resource_type is not None:
                self._values["resource_type"] = resource_type
            if selection_mode is not None:
                self._values["selection_mode"] = selection_mode

        @builtins.property
        def filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetFilterProperty"]]]]:
            '''The filters to apply to identify target resources using specific attributes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetarget.html#cfn-fis-experimenttemplate-experimenttemplatetarget-filters
            '''
            result = self._values.get("filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetFilterProperty"]]]], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The parameters for the resource type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetarget.html#cfn-fis-experimenttemplate-experimenttemplatetarget-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Amazon Resource Names (ARNs) of the targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetarget.html#cfn-fis-experimenttemplate-experimenttemplatetarget-resourcearns
            '''
            result = self._values.get("resource_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def resource_tags(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The tags for the target resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetarget.html#cfn-fis-experimenttemplate-experimenttemplatetarget-resourcetags
            '''
            result = self._values.get("resource_tags")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def resource_type(self) -> typing.Optional[builtins.str]:
            '''The resource type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetarget.html#cfn-fis-experimenttemplate-experimenttemplatetarget-resourcetype
            '''
            result = self._values.get("resource_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def selection_mode(self) -> typing.Optional[builtins.str]:
            '''Scopes the identified resources to a specific count or percentage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetarget.html#cfn-fis-experimenttemplate-experimenttemplatetarget-selectionmode
            '''
            result = self._values.get("selection_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExperimentTemplateTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnExperimentTemplatePropsMixin.OutputsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "experiment_report_s3_configuration": "experimentReportS3Configuration",
        },
    )
    class OutputsProperty:
        def __init__(
            self,
            *,
            experiment_report_s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExperimentTemplatePropsMixin.ExperimentReportS3ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the output destinations of the experiment report.

            :param experiment_report_s3_configuration: The S3 destination for the experiment report.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-outputs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
                
                outputs_property = fis_mixins.CfnExperimentTemplatePropsMixin.OutputsProperty(
                    experiment_report_s3_configuration=fis_mixins.CfnExperimentTemplatePropsMixin.ExperimentReportS3ConfigurationProperty(
                        bucket_name="bucketName",
                        prefix="prefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d73a34e685c5151ad911c755105267105a919c282b96791e196b8aef81cc97e7)
                check_type(argname="argument experiment_report_s3_configuration", value=experiment_report_s3_configuration, expected_type=type_hints["experiment_report_s3_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if experiment_report_s3_configuration is not None:
                self._values["experiment_report_s3_configuration"] = experiment_report_s3_configuration

        @builtins.property
        def experiment_report_s3_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentReportS3ConfigurationProperty"]]:
            '''The S3 destination for the experiment report.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-outputs.html#cfn-fis-experimenttemplate-outputs-experimentreports3configuration
            '''
            result = self._values.get("experiment_report_s3_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExperimentTemplatePropsMixin.ExperimentReportS3ConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnTargetAccountConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "description": "description",
        "experiment_template_id": "experimentTemplateId",
        "role_arn": "roleArn",
    },
)
class CfnTargetAccountConfigurationMixinProps:
    def __init__(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        experiment_template_id: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTargetAccountConfigurationPropsMixin.

        :param account_id: The AWS account ID of the target account.
        :param description: The description of the target account.
        :param experiment_template_id: The ID of the experiment template.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role for the target account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-targetaccountconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
            
            cfn_target_account_configuration_mixin_props = fis_mixins.CfnTargetAccountConfigurationMixinProps(
                account_id="accountId",
                description="description",
                experiment_template_id="experimentTemplateId",
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ebaa452ba2ac93086bcf4b2bc1c88167b96747c5a1092579f62307b2aa1a85)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument experiment_template_id", value=experiment_template_id, expected_type=type_hints["experiment_template_id"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_id is not None:
            self._values["account_id"] = account_id
        if description is not None:
            self._values["description"] = description
        if experiment_template_id is not None:
            self._values["experiment_template_id"] = experiment_template_id
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of the target account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-targetaccountconfiguration.html#cfn-fis-targetaccountconfiguration-accountid
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the target account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-targetaccountconfiguration.html#cfn-fis-targetaccountconfiguration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def experiment_template_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the experiment template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-targetaccountconfiguration.html#cfn-fis-targetaccountconfiguration-experimenttemplateid
        '''
        result = self._values.get("experiment_template_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an IAM role for the target account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-targetaccountconfiguration.html#cfn-fis-targetaccountconfiguration-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTargetAccountConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTargetAccountConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_fis.mixins.CfnTargetAccountConfigurationPropsMixin",
):
    '''Creates a target account configuration for the experiment template.

    A target account configuration is required when ``accountTargeting`` of ``experimentOptions`` is set to ``multi-account`` . For more information, see `experiment options <https://docs.aws.amazon.com/fis/latest/userguide/experiment-options.html>`_ in the *AWS Fault Injection Service User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-targetaccountconfiguration.html
    :cloudformationResource: AWS::FIS::TargetAccountConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_fis import mixins as fis_mixins
        
        cfn_target_account_configuration_props_mixin = fis_mixins.CfnTargetAccountConfigurationPropsMixin(fis_mixins.CfnTargetAccountConfigurationMixinProps(
            account_id="accountId",
            description="description",
            experiment_template_id="experimentTemplateId",
            role_arn="roleArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTargetAccountConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FIS::TargetAccountConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9d2058a2f072b728b660e177de7f27d11a7adb5b19503fe26da693b428e6f88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a600ff3fdd940793ce58f7f0cec50ee2bfdeece2dd5fde31092f7c924a3c48b1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c68ff0c3dc401125c4825c09fc35c5af10c0ed9b107b888d7ce187ee9d3ce39)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTargetAccountConfigurationMixinProps:
        return typing.cast(CfnTargetAccountConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnExperimentTemplateMixinProps",
    "CfnExperimentTemplatePropsMixin",
    "CfnTargetAccountConfigurationMixinProps",
    "CfnTargetAccountConfigurationPropsMixin",
]

publication.publish()

def _typecheckingstub__619b2c3c584e9865cba4d175029788c320c903938bde3c2b5dfc1d8acebe9b48(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentTemplatePropsMixin.ExperimentTemplateActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    experiment_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    experiment_report_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentTemplatePropsMixin.ExperimentTemplateExperimentReportConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentTemplatePropsMixin.ExperimentTemplateLogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    stop_conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentTemplatePropsMixin.ExperimentTemplateStopConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e693b4bffdbf76a948995070560813574083b21fa35e5cc9e211c1c04c3e9262(
    props: typing.Union[CfnExperimentTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc39d2b5238c2d90aa8ce82ed2daaa78377c3bcd5e11cc444ccf01d0248349be(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e905981e6cc3e839f5f17e4ecbe89f4d02cb4e037b2368f01dcafece55d904(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b8d7e5ae4c50f5393120d277736bc4a00973c657dd3084605b3b029001d177(
    *,
    dashboard_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6873b2130eb0eec37215e5757c3ea59060a4fe8ce08343b7d93c85fd911d3cc3(
    *,
    cloud_watch_dashboards: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentTemplatePropsMixin.CloudWatchDashboardProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da593ab252b64178892325ec8175b825bdba1f31cdda3addcbf072d33dd7eb56(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9993305a227d1a2897cc8851028d6433e470742cf8004bd062242819092696(
    *,
    action_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    start_after: typing.Optional[typing.Sequence[builtins.str]] = None,
    targets: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0fb96bc20acd96d050be6bd08ba29d5e44ceca0442786b01ecf20b263eacf6(
    *,
    account_targeting: typing.Optional[builtins.str] = None,
    empty_target_resolution_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bbc10c37ae75b1ed698ae203ca3e50efbe51aa785842e5b0a8006da457169dc(
    *,
    data_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentTemplatePropsMixin.DataSourcesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentTemplatePropsMixin.OutputsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    post_experiment_duration: typing.Optional[builtins.str] = None,
    pre_experiment_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e8d3badbfb15490a78e03b4f03745f6d99b263631bd7eb0bdf526f56473903(
    *,
    cloud_watch_logs_configuration: typing.Any = None,
    log_schema_version: typing.Optional[jsii.Number] = None,
    s3_configuration: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0c7d9d592cf120b1d12901d7026c86fa7bf5701ae4b78e79df6a72d7013832(
    *,
    source: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6824f5224585bf2bf4f8be9cc97dc7b704589161a6522df3324824053ab380aa(
    *,
    path: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c888eaeb73d6da40379dba2c785497ae59be5afed86f35c81e056b17777eaa9(
    *,
    filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentTemplatePropsMixin.ExperimentTemplateTargetFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_tags: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    selection_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73a34e685c5151ad911c755105267105a919c282b96791e196b8aef81cc97e7(
    *,
    experiment_report_s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExperimentTemplatePropsMixin.ExperimentReportS3ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ebaa452ba2ac93086bcf4b2bc1c88167b96747c5a1092579f62307b2aa1a85(
    *,
    account_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    experiment_template_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d2058a2f072b728b660e177de7f27d11a7adb5b19503fe26da693b428e6f88(
    props: typing.Union[CfnTargetAccountConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a600ff3fdd940793ce58f7f0cec50ee2bfdeece2dd5fde31092f7c924a3c48b1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c68ff0c3dc401125c4825c09fc35c5af10c0ed9b107b888d7ce187ee9d3ce39(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
